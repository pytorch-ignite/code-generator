import ignite.distributed as idist
import torch
from datasets import load_dataset
from transformers import AutoTokenizer


class TransformerDataset(torch.utils.data.Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        text = " ".join(text.split())
        inputs = self.tokenizer.encode_plus(
            text,
            None,
            add_special_tokens=True,
            max_length=self.max_length,
            truncation=True,
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


def setup_data(config):
    #::: if (it.use_dist) { :::#
    local_rank = idist.get_local_rank()

    if local_rank > 0:
        idist.barrier()
    #::: } :::#
    dataset_train, dataset_eval = load_dataset("imdb", split=["train", "test"], cache_dir=config.data_path)
    tokenizer = AutoTokenizer.from_pretrained(config.model, cache_dir=config.tokenizer_dir, do_lower_case=True)
    train_texts, train_labels = dataset_train["text"], dataset_train["label"]
    test_texts, test_labels = dataset_eval["text"], dataset_eval["label"]
    dataset_train = TransformerDataset(train_texts, train_labels, tokenizer, config.max_length)
    dataset_eval = TransformerDataset(test_texts, test_labels, tokenizer, config.max_length)
    #::: if (it.use_dist) { :::#
    if local_rank == 0:
        idist.barrier()
    #::: } :::#

    dataloader_train = idist.auto_dataloader(
        dataset_train,
        batch_size=config.train_batch_size,
        num_workers=config.num_workers,
        shuffle=True,
        drop_last=True,
    )
    dataloader_eval = idist.auto_dataloader(
        dataset_eval,
        batch_size=config.eval_batch_size,
        num_workers=config.num_workers,
        shuffle=False,
    )

    return dataloader_train, dataloader_eval
