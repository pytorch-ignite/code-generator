#::: if (it.dist === 'launch') { :::#
#::: if (it.nproc_per_node) { :::#
#::: if (it.nnodes && it.master_addr && it.master_port) { :::#

### Multi Node, Multi GPU Training (`torch.distributed.launch`)

```sh
python -m torch.distributed.launch \
  --nproc-per-node #:::= nproc_per_node :::# \
  --nnodes #:::= it.nnodes :::# \
  --master-addr #:::= it.master_addr :::# \
  --master-port #:::= it.master_port :::#
  main.py --backend nccl
```

#::: } else { :::#

### Multi GPU Training (`torch.distributed.launch`)

```sh
python -m torch.distributed.launch \
  --nproc-per-node #:::= it.nproc_per_node :::# \
  main.py --backend nccl
```

#::: } :::#
#::: } :::#
#::: } :::#

#::: if (it.dist === 'spawn') { :::#
#::: if (it.nproc_per_node) { :::#
#::: if (it.nnodes && it.master_addr && it.master_port) { :::#

### Multi Node, Multi GPU Training (`torch.multiprocessing.spawn`)

```sh
python main.py  \
  --nproc-per-node #:::= nproc_per_node :::# \
  --nnodes #:::= it.nnodes :::# \
  --master-addr #:::= it.master_addr :::# \
  --master-port #:::= it.master_port :::#
  --backend nccl
```

#::: } else { :::#

### Multi GPU Training (`torch.multiprocessing.spawn`)

```sh
python main.py  \
  --nproc-per-node #:::= it.nproc_per_node :::# \
  --backend nccl
```

#::: } :::#
#::: } :::#
#::: } :::#

#::: if (!it.nproc_per_node) { :::#

### 1 GPU Training

```sh
python main.py
```

#::: } :::#
