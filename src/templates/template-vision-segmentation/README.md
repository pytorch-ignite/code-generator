[![Code-Generator](https://badgen.net/badge/Template%20by/Code-Generator/ee4c2c?labelColor=eaa700)](https://github.com/pytorch-ignite/code-generator)

# Segmentation Template

This is the segmentation template by Code-Generator using `deeplabv3_resnet101` and `cifar10` dataset from TorchVision and training is powered by PyTorch and PyTorch-Ignite.

## Getting Started

Install the dependencies with `pip`:

```sh
pip install -r requirements.txt --progress-bar off -U
```

### Code structure

#::: if (it.include_test) { :::#

```
|
|- README.md
|
|- main.py : main script to run
|- data.py : helper module with functions to setup input datasets and create dataloaders
|- models.py : helper module with functions to create a model or multiple models
|- trainers.py : helper module with functions to create trainer and evaluator
|- utils.py : module with various helper functions
|- vis.py : helper module for data visualizations
|
|- requirements.txt : dependencies to install with pip
|
|- config.yaml : global configuration YAML file
|
|- test_all.py : test file with few basic sanity checks
```

#::: } else { :::#

```
|
|- README.md
|
|- main.py : main script to run
|- data.py : helper module with functions to setup input datasets and create dataloaders
|- models.py : helper module with functions to create a model or multiple models
|- trainers.py : helper module with functions to create trainer and evaluator
|- utils.py : module with various helper functions
|- vis.py : helper module for data visualizations
|
|- requirements.txt : dependencies to install with pip
|
|- config.yaml : global configuration YAML file
```

#::: } :::#

## Training

#::: if (it.use_dist) { :::#
#::: if (it.dist === 'torchrun') { :::#
#::: if (it.nproc_per_node) { :::#
#::: if (it.nnodes > 1 && it.master_addr && it.master_port) { :::#

### Multi Node, Multi GPU Training (`torchrun`) (recommended)

- Execute on master node

```sh
torchrun \
  --nproc_per_node #:::= it.nproc_per_node :::# \
  --nnodes #:::= it.nnodes :::# \
  --node_rank 0 \
  --master_addr #:::= it.master_addr :::# \
  --master_port #:::= it.master_port :::# \
  main.py \
  --backend #:::= it.backend :::#
```

- Execute on worker nodes

```sh
torchrun \
  --nproc_per_node #:::= it.nproc_per_node :::# \
  --nnodes #:::= it.nnodes :::# \
  --node_rank <node_rank> \
  --master_addr #:::= it.master_addr :::# \
  --master_port #:::= it.master_port :::# \
  main.py \
  --backend #:::= it.backend :::#
```

#::: } else { :::#

### Multi GPU Training (`torchrun`) (recommended)

```sh
torchrun \
  --nproc_per_node #:::= it.nproc_per_node :::# \
  main.py \
  --backend #:::= it.backend :::#
```

#::: } :::#
#::: } :::#
#::: } :::#

#::: if (it.dist === 'spawn') { :::#
#::: if (it.nproc_per_node) { :::#
#::: if (it.nnodes > 1 && it.master_addr && it.master_port) { :::#

### Multi Node, Multi GPU Training (`torch.multiprocessing.spawn`)

- Execute on master node

```sh
python main.py  \
  --nproc_per_node #:::= it.nproc_per_node :::# \
  --nnodes #:::= it.nnodes :::# \
  --node_rank 0 \
  --master_addr #:::= it.master_addr :::# \
  --master_port #:::= it.master_port :::# \
  --backend #:::= it.backend :::#
```

- Execute on worker nodes

```sh
python main.py  \
  --nproc_per_node #:::= it.nproc_per_node :::# \
  --nnodes #:::= it.nnodes :::# \
  --node_rank <node_rank> \
  --master_addr #:::= it.master_addr :::# \
  --master_port #:::= it.master_port :::# \
  --backend #:::= it.backend :::#
```

#::: } else { :::#

### Multi GPU Training (`torch.multiprocessing.spawn`)

```sh
python main.py  \
  --nproc_per_node #:::= it.nproc_per_node :::# \
  --backend #:::= it.backend :::#
```

#::: } :::#
#::: } :::#
#::: } :::#

#::: } else { :::#

### 1 GPU Training

```sh
python main.py
```

#::: } :::#
