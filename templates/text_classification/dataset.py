import torch
from torch.utils.data import Dataset

import ignite.distributed as idist
from transformers import AutoTokenizer
from datasets import load_dataset


class TransformerDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        text = " ".join(text.split())
        inputs = self.tokenizer.encode_plus(
            text, None, add_special_tokens=True, max_length=self.max_length, truncation=True
        )

        ids = inputs["input_ids"]
        token_type_ids = inputs["token_type_ids"]
        mask = inputs["attention_mask"]
        padding_length = self.max_length - len(ids)

        ids = ids + ([0] * padding_length)
        mask = mask + ([0] * padding_length)
        token_type_ids = token_type_ids + ([0] * padding_length)
        return {
            "input_ids": torch.tensor(ids, dtype=torch.long),
            "attention_mask": torch.tensor(mask, dtype=torch.long),
            "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
            "label": torch.tensor(self.labels[idx], dtype=torch.float),
        }

    def __len__(self):
        return len(self.labels)


def get_tokenizer(tokenizer_name, tokenizer_dir):
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_name, cache_dir=tokenizer_dir, do_lower_case=True)
    return tokenizer


def get_dataset(cache_dir, tokenizer_name, tokenizer_dir, max_length):
    train_dataset, test_dataset = load_dataset("imdb", split=["train", "test"], cache_dir=cache_dir)
    tokenizer = get_tokenizer(tokenizer_name, tokenizer_dir)
    train_texts, train_labels = train_dataset["text"], train_dataset["label"]
    test_texts, test_labels = test_dataset["text"], test_dataset["label"]
    train_dataset = TransformerDataset(train_texts, train_labels, tokenizer, max_length)
    test_dataset = TransformerDataset(test_texts, test_labels, tokenizer, max_length)
    return train_dataset, test_dataset


def get_dataflow(config):
    # - Get train/test datasets
    if idist.get_local_rank() > 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()

    train_dataset, test_dataset = get_dataset(
        config.data_dir, config.model, config.tokenizer_dir, config.max_length
    )

    if idist.get_local_rank() == 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()

    # Setup data loader also adapted to distributed config: nccl, gloo, xla-tpu
    train_loader = idist.auto_dataloader(
        train_dataset,
        batch_size=config.batch_size,
        num_workers=config.num_workers,
        shuffle=True,
        drop_last=True,
        {% if use_distributed_training and not use_distributed_launcher %}
    persistent_workers = True,
        {% endif %}
    )

    test_loader = idist.auto_dataloader(
        test_dataset,
        batch_size=2 * config.batch_size,
        num_workers=config.num_workers,
        shuffle=False,
        {% if use_distributed_training and not use_distributed_launcher %}
    persistent_workers = True,
        {% endif %}
    )
    return train_loader, test_loader
