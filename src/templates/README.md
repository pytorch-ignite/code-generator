[![Code-Generator](https://badgen.net/badge/Template%20by/Code-Generator/ee4c2c?labelColor=eaa700)](https://github.com/pytorch-ignite/code-generator)

# Template by Code-Generator

## Getting Started

Install the dependencies with `pip`:

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

Run the training with:

{{ @if (it.nproc_per_node) }}
{{ @if (it.nnodes && it.master_addr && it.master_port) }}

```sh
python -m torch.distributed.launch \
  --nproc-per-node {{ it.nproc_per_node }} \
  --nnodes {{ it.nnodes }} \
  --master-addr {{ it.master_addr }} \
  --master-port {{ it.master_port }}
  main.py --backend nccl
```

{{ #else }}

```sh
python -m torch.distributed.launch \
  --nproc-per-node {{ it.nproc_per_node }} \
  main.py --backend nccl
```

{{ /if }}
{{ #else }}

```sh
python main.py
```

{{ /if }}
