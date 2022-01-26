#::: if (it.use_dist) { :::#
#::: if (it.dist === 'launch') { :::#
#::: if (it.nproc_per_node) { :::#
#::: if (it.nnodes > 1 && it.master_addr && it.master_port) { :::#

### Multi Node, Multi GPU Training (`torch.distributed.launch`) (recommended)

- Execute on master node

```sh
python -m torch.distributed.launch \
  --nproc_per_node #:::= it.nproc_per_node :::# \
  --nnodes #:::= it.nnodes :::# \
  --node_rank 0 \
  --master_addr #:::= it.master_addr :::# \
  --master_port #:::= it.master_port :::# \
  --use_env main.py \
  --backend #:::= it.backend :::#
```

- Execute on worker nodes

```sh
python -m torch.distributed.launch \
  --nproc_per_node #:::= it.nproc_per_node :::# \
  --nnodes #:::= it.nnodes :::# \
  --node_rank <node_rank> \
  --master_addr #:::= it.master_addr :::# \
  --master_port #:::= it.master_port :::# \
  --use_env main.py \
  --backend #:::= it.backend :::#
```

#::: } else { :::#

### Multi GPU Training (`torch.distributed.launch`) (recommended)

```sh
python -m torch.distributed.launch \
  --nproc_per_node #:::= it.nproc_per_node :::# \
  --use_env main.py \
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
