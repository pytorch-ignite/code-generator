[![Code-Generator](https://badgen.net/badge/Template%20by/Code-Generator/ee4c2c?labelColor=eaa700)](https://github.com/pytorch-ignite/code-generator)

# Text Classification Template

This template is ported from [Transformers Example with PyTorch-Ignite example](https://github.com/pytorch/ignite/tree/master/examples/contrib/transformers).

<details>
<summary>
Table of Contents
</summary>

- [Getting Started](#getting-started)
- [Training](#training)
- [Configurations](#configurations)

</details>

## Getting Started

<details>
<summary>
Detailed Directory List
</summary>

```bash
text_classification
├── README.md
├── config.py
├── dataset.py
├── main.py
├── models.py
├── requirements.txt
├── test_all.py
├── trainers.py
└── utils.py
```

</details>

- Install the dependencies with `pip`:

  ```sh
  pip install -r requirements.txt --progress-bar off -U
  ```

> **💡 TIP**
>
> To quickly adapt to the generated code structure, there are TODOs in the files that are needed to be edited.
> [PyCharm TODO comments](https://www.jetbrains.com/help/pycharm/using-todo.html) or
> [VSCode Todo Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree)
> can help you find them easily.

## Training

{% if not use_distributed_training %}

### Single Node, Single GPU

```bash
python main.py --verbose
```

{% else %}

{% if nnodes < 2 %}

### Single Node, Multiple GPUs

{% if use_distributed_launcher %}

- Using `torch.distributed.launch` (preferred)

  ```bash
  python -m torch.distributed.launch \
    --nproc_per_node={{nproc_per_node}} \
    --use_env main.py \
    --backend="nccl" \
    --verbose
  ```

{% else %}

- Using function spawn inside the code

  ```bash
  python main.py \
    --backend="nccl" \
    --nproc_per_node={{nproc_per_node}} \
    --verbose
  ```

  {% endif %}

{% else %}

### Multiple Nodes, Multiple GPUs

Let's start training on {{nnodes}} nodes with {{nproc_per_node}} gpus each:

- Execute on master node

  ```bash
  python -m torch.distributed.launch \
    --nnodes={{nnodes}} \
    --nproc_per_node={{nproc_per_node}} \
    --node_rank=0 \
    --master_addr={{master_addr}} \
    --master_port={{master_port}} \
    --use_env main.py \
    --backend="nccl" \
    --verbose
  ```

- Execute on worker nodes

  ```bash
  python -m torch.distributed.launch \
    --nnodes={{nnodes}} \
    --nproc_per_node={{nproc_per_node}} \
    --node_rank=<node_rank> \
    --master_addr={{master_addr}} \
    --master_port={{master_port}} \
    --use_env main.py \
    --backend="nccl" \
    --verbose
  ```

  {% endif %}
  {% endif %}

## Configurations

```bash
usage: main.py [-h] [--use_amp] [--resume_from RESUME_FROM] [--seed SEED] [--verbose] [--backend BACKEND]
               [--nproc_per_node NPROC_PER_NODE] [--node_rank NODE_RANK] [--nnodes NNODES]
               [--master_addr MASTER_ADDR] [--master_port MASTER_PORT] [--epoch_length EPOCH_LENGTH]
               [--save_every_iters SAVE_EVERY_ITERS] [--n_saved N_SAVED] [--log_every_iters LOG_EVERY_ITERS]
               [--with_pbars WITH_PBARS] [--with_pbar_on_iters WITH_PBAR_ON_ITERS]
               [--stop_on_nan STOP_ON_NAN] [--clear_cuda_cache CLEAR_CUDA_CACHE]
               [--with_gpu_stats WITH_GPU_STATS] [--patience PATIENCE] [--limit_sec LIMIT_SEC]
               [--output_dir OUTPUT_DIR] [--logger_log_every_iters LOGGER_LOG_EVERY_ITERS]
               [--data_dir DATA_DIR] [--model {bert-base-uncased}] [--model_dir MODEL_DIR]
               [--tokenizer_dir TOKENIZER_DIR] [--num_classes NUM_CLASSES] [--dropout DROPOUT] [--n_fc N_FC]
               [--max_length MAX_LENGTH] [--batch_size BATCH_SIZE] [--weight_decay WEIGHT_DECAY]
               [--num_workers NUM_WORKERS] [--max_epochs MAX_EPOCHS] [--learning_rate LEARNING_RATE]
               [--num_warmup_epochs NUM_WARMUP_EPOCHS] [--validate_every VALIDATE_EVERY]
               [--checkpoint_every CHECKPOINT_EVERY] [--eval_epoch_length EVAL_EPOCH_LENGTH]

optional arguments:
  -h, --help            show this help message and exit
  --use_amp             use torch.cuda.amp for automatic mixed precision. Default: False
  --resume_from RESUME_FROM
                        path to the checkpoint file to resume, can also url starting with https. Default:
                        None
  --seed SEED           seed to use in ignite.utils.manual_seed(). Default: 666
  --verbose             use logging.INFO in ignite.utils.setup_logger. Default: False
  --backend BACKEND     backend to use for distributed training. Default: None
  --nproc_per_node NPROC_PER_NODE
                        number of processes to launch on each node, for GPU training this is recommended to
                        be set to the number of GPUs in your system so that each process can be bound to a
                        single GPU. Default: None
  --node_rank NODE_RANK
                        rank of the node for multi-node distributed training. Default: None
  --nnodes NNODES       number of nodes to use for distributed training. Default: None
  --master_addr MASTER_ADDR
                        master node TCP/IP address for torch native backends. Default: None
  --master_port MASTER_PORT
                        master node port for torch native backends. Default: None
  --epoch_length EPOCH_LENGTH
                        epoch_length of Engine.run(). Default: None
  --save_every_iters SAVE_EVERY_ITERS
                        Saving iteration interval. Default: 1000
  --n_saved N_SAVED     number of best models to store. Default: 2
  --log_every_iters LOG_EVERY_ITERS
                        Argument to log batch loss every log_every_iters iterations. 0 to disable it.
                        Default: 100
  --with_pbars WITH_PBARS
                        show epoch-wise and iteration-wise progress bars. Default: False
  --with_pbar_on_iters WITH_PBAR_ON_ITERS
                        show iteration progress bar or not. Default: True
  --stop_on_nan STOP_ON_NAN
                        stop the training if engine output contains NaN/inf values. Default: True
  --clear_cuda_cache CLEAR_CUDA_CACHE
                        clear cuda cache every end of epoch. Default: True
  --with_gpu_stats WITH_GPU_STATS
                        show gpu information, requires pynvml. Default: False
  --patience PATIENCE   number of events to wait if no improvement and then stop the training. Default: None
  --limit_sec LIMIT_SEC
                        maximum time before training terminates in seconds. Default: None
  --output_dir OUTPUT_DIR
                        directory to save all outputs. Default: ./logs
  --logger_log_every_iters LOGGER_LOG_EVERY_ITERS
                        logging interval for experiment tracking system. Default: 100
  --data_dir DATA_DIR   Dataset cache directory. Default: ./
  --model {bert-base-uncased}
                        Model name (from transformers) to setup model, tokenize and config to train.
                        Default: bert-base-uncased
  --model_dir MODEL_DIR
                        Cache directory to download the pretrained model. Default: ./
  --tokenizer_dir TOKENIZER_DIR
                        Tokenizer cache directory. Default: ./tokenizer
  --num_classes NUM_CLASSES
                        Number of target classes. Default: 1
  --dropout DROPOUT     Dropout probability. Default: 0.3
  --n_fc N_FC           Number of neurons in the last fully connected layer. Default: 768
  --max_length MAX_LENGTH
                        Maximum number of tokens for the inputs to the transformer model. Default: 256
  --batch_size BATCH_SIZE
                        Total batch size. Default: 16
  --weight_decay WEIGHT_DECAY
                        Weight decay. Default: 0.01
  --num_workers NUM_WORKERS
                        Number of workers in the data loader. Default: 2
  --max_epochs MAX_EPOCHS
                        Number of epochs to train the model. Default: 3
  --learning_rate LEARNING_RATE
                        Peak of piecewise linear learning rate scheduler. Default: 5e-05
  --num_warmup_epochs NUM_WARMUP_EPOCHS
                        Number of warm-up epochs before learning rate decay. Default: 0
  --validate_every VALIDATE_EVERY
                        Run model's validation every validate_every epochs. Default: 1
  --checkpoint_every CHECKPOINT_EVERY
                        Store training checkpoint every checkpoint_every iterations. Default: 1000
  --eval_epoch_length EVAL_EPOCH_LENGTH
                        epoch_length of evaluator. Default: None
```
