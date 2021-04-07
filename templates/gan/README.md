[![Code-Generator](https://badgen.net/badge/Template%20by/Code-Generator/ee4c2c?labelColor=eaa700)](https://github.com/pytorch-ignite/code-generator)

# GAN Template

This template is ported from [PyTorch-Ignite DCGAN example](https://github.com/pytorch/ignite/tree/master/examples/gan).
This template has structured like a python package to imports modules easily.

<details>
<summary>
Table of Contents
</summary>

- [Getting Started](#getting-started)
- [Training](#training)
- [PyTorch Hub](#pytorch-hub)
- [Configurations](#configurations)

</details>

## Getting Started

<details>
<summary>
Detailed Directory List
</summary>

```sh
gan
├── README.md
├── gan
│   ├── __init__.py
│   ├── config.py
│   ├── datasets.py
│   ├── handlers.py
│   ├── main.py
│   ├── models.py
│   ├── trainers.py
│   └── utils.py
├── hubconf.py
├── requirements.txt
├── setup.py
└── tests
    ├── test_datasets.py
    ├── test_handlers.py
    ├── test_models.py
    ├── test_trainers.py
    └── test_utils.py

2 directories, 17 files
```

</details>

- Install the dependencies with `pip` and install the project in `editable` mode:

  ```sh
  pip install -r requirements.txt --progress-bar off -U
  pip install -e .
  ```

> **💡 TIP**
>
> To quickly adapt to the generated code structure, there are TODOs in the files that are needed to be edited.
> [PyCharm TODO comments](https://www.jetbrains.com/help/pycharm/using-todo.html) or
> [VSCode Todo Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree)
> can help you find them easily.

## Training

### Single Node, Single GPU

```sh
python main.py --verbose
```

### Single Node, Multiple GPUs

- Using `torch.distributed.launch` (recommended)

  ```sh
  python -m torch.distributed.launch \
    --nproc_per_node=2 \
    --use_env main.py \
    --backend="nccl" \
    --verbose \
  ```

- Using function spawn inside the code

  ```sh
  python main.py \
    --backend="nccl" \
    --nproc_per_node=2 \
    --verbose \
  ```

### Multiple Nodes, Multiple GPUs

Let's start training on two nodes with 2 gpus each. We assuming that master node can be connected as master, e.g. ping master.

- Execute on master node

  ```sh
  python -m torch.distributed.launch \
    --nnodes=2 \
    --nproc_per_node=2 \
    --node_rank=0 \
    --master_addr=master \
    --master_port=2222 \
    --use_env main.py \
    --backend="nccl" \
    --verbose \
  ```

- Execute on worker node

  ```sh
  python -m torch.distributed.launch \
    --nnodes=2 \
    --nproc_per_node=2 \
    --node_rank=1 \
    --master_addr=master \
    --master_port=2222 \
    --use_env main.py \
    --backend="nccl" \
    --verbose \
  ```

### Colab 8 TPUs

```sh
python main.py --verbose --backend='xla-tpu' --nproc_per_node=8
```

## PyTorch Hub

- Edit `hubconf.py` to use the custom model easily via `torch.hub.load()`.
- Add additional requirements inside `dependencies` list in `hubconf.py`.

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
               [--dataset {cifar10,lsun,imagenet,folder,lfw,fake,mnist}]
               [--data_path DATA_PATH] [--batch_size BATCH_SIZE]
               [--num_workers NUM_WORKERS] [--beta_1 BETA_1] [--lr LR]
               [--max_epochs MAX_EPOCHS] [--z_dim Z_DIM]
               [--g_filters G_FILTERS] [--d_filters D_FILTERS]

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
                        logging interval for experiment tracking system (100)
  --dataset {cifar10,lsun,imagenet,folder,lfw,fake,mnist}
                        dataset to use (cifar10)
  --data_path DATA_PATH
                        datasets path (./)
  --batch_size BATCH_SIZE
                        will be equally divided by number of GPUs if in
                        distributed (4)
  --num_workers NUM_WORKERS
                        num_workers for DataLoader (2)
  --beta_1 BETA_1       beta_1 for Adam optimizer (0.5)
  --lr LR               learning rate used by torch.optim.* (0.001)
  --max_epochs MAX_EPOCHS
                        max_epochs of ignite.Engine.run() for training (2)
  --z_dim Z_DIM         size of the latent z vector (100)
  --g_filters G_FILTERS
                        number of filters in the second-to-last generator
                        deconv layer (64)
  --d_filters D_FILTERS
                        number of filters in first discriminator conv layer
                        (64)
```
