[![Code-Generator](https://badgen.net/badge/Template%20by/Code-Generator/ee4c2c?labelColor=eaa700)](https://github.com/pytorch-ignite/code-generator)

# Single Model, Single Optimizer Template

This is a template generated for single model, single optimizer based training.

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

```sh
dist/single
├── README.md
├── config.py
├── datasets.py
├── handlers.py
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

- Edit `datasets.py` for your custom datasets and dataloaders.
- Edit `models.py` for your custom models.
- Extend `config.py` for additional command line arguments.
- Extend `trainers.py` for your custom models' forward pass, backward pass, and evaluation.
- Extend `handlers.py` for your custom handlers. _(**OPTIONAL**)_

## Training

{% if not use_distributed_training %}

### Single Node, Single GPU

```sh
python main.py --verbose
```

{% else %}

{% if nnodes < 2 %}

### Single Node, Multiple GPUs

{% if use_distributed_launcher %}

- Using `torch.distributed.launch` (preferred)

  ```sh
  python -m torch.distributed.launch \
    --nproc_per_node={{nproc_per_node}} \
    --use_env main.py \
    --backend="nccl" \
    --verbose
  ```

{% else %}

- Using function spawn inside the code

  ```sh
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

  ```sh
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

  ```sh
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

```sh
usage: main.py [-h] [--use_amp] [--resume_from RESUME_FROM] [--seed SEED]
               [--verbose] [--backend BACKEND]
               [--nproc_per_node NPROC_PER_NODE] [--nnodes NNODES]
               [--node_rank NODE_RANK] [--master_addr MASTER_ADDR]
               [--master_port MASTER_PORT]
               [--save_every_iters SAVE_EVERY_ITERS] [--n_saved N_SAVED]
               [--log_every_iters LOG_EVERY_ITERS] [--with_pbars WITH_PBARS]
               [--with_pbar_on_iters WITH_PBAR_ON_ITERS]
               [--stop_on_nan STOP_ON_NAN]
               [--clear_cuda_cache CLEAR_CUDA_CACHE]
               [--with_gpu_stats WITH_GPU_STATS] [--patience PATIENCE]
               [--limit_sec LIMIT_SEC] [--output_dir OUTPUT_DIR]
               [--logger_log_every_iters LOGGER_LOG_EVERY_ITERS]

optional arguments:
  -h, --help            show this help message and exit
  --use_amp             use torch.cuda.amp for automatic mixed precision
  --resume_from RESUME_FROM
                        path to the checkpoint file to resume, can also url
                        starting with https (None)
  --seed SEED           seed to use in ignite.utils.manual_seed() (666)
  --verbose             use logging.INFO in ignite.utils.setup_logger
  --backend BACKEND     backend to use for distributed training (None)
  --nproc_per_node NPROC_PER_NODE
                        number of processes to launch on each node, for GPU
                        training this is recommended to be set to the number
                        of GPUs in your system so that each process can be
                        bound to a single GPU (None)
  --nnodes NNODES       number of nodes to use for distributed training (None)
  --node_rank NODE_RANK
                        rank of the node for multi-node distributed training
                        (None)
  --master_addr MASTER_ADDR
                        master node TCP/IP address for torch native backends
                        (None)
  --master_port MASTER_PORT
                        master node port for torch native backends (None)
  --save_every_iters SAVE_EVERY_ITERS
                        Saving iteration interval (1000)
  --n_saved N_SAVED     number of best models to store (2)
  --log_every_iters LOG_EVERY_ITERS
                        logging interval for iteration progress bar (100)
  --with_pbars WITH_PBARS
                        show epoch-wise and iteration-wise progress bars
                        (True)
  --with_pbar_on_iters WITH_PBAR_ON_ITERS
                        show iteration progress bar or not (True)
  --stop_on_nan STOP_ON_NAN
                        stop the training if engine output contains NaN/inf
                        values (True)
  --clear_cuda_cache CLEAR_CUDA_CACHE
                        clear cuda cache every end of epoch (True)
  --with_gpu_stats WITH_GPU_STATS
                        show gpu information, requires pynvml (False)
  --patience PATIENCE   number of events to wait if no improvement and then
                        stop the training (None)
  --limit_sec LIMIT_SEC
                        maximum time before training terminates in seconds
                        (None)
  --output_dir OUTPUT_DIR
                        directory to save all outputs (./logs)
  --logger_log_every_iters LOGGER_LOG_EVERY_ITERS
                        logging interval for experiment tracking system (None)
```
