[![Code-Generator](https://badgen.net/badge/Template%20by/Code-Generator/ee4c2c?labelColor=eaa700)](https://github.com/pytorch-ignite/code-generator)

# Text Classification Template

This is the text classification template by Code-Generator using `bert-base-uncased` model from HuggingFace Transformers and `imdb` dataset from HuggingFace datasets and training is powered by PyTorch and PyTorch-Ignite.

## Getting Started

Install the dependencies with `pip`:

```sh
pip install -r requirements.txt --progress-bar off -U
```

## Training

#::: if (it.use_dist) { :::#
#::: if (it.dist === 'launch') { :::#
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
  main.py
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
  main.py
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
