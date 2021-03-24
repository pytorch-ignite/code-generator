# Image Classification Template by Code-Generator

This template is ported from [PyTorch-Ignite MNIST example](https://github.com/pytorch/ignite/blob/master/examples/mnist/mnist.py).

After downloading the archive, install the requirements with:

```sh
pip install -r requirements.txt -U --progress-bar off
```

The requirements are:

- PyTorch
- Torchvision
- PyTorch-Ignite

After installing the requirements, run the training with:

```sh
python main.py --verbose
```

The following options are available to configure (`python main.py -h`):

```sh
usage: main.py [-h] [--train_batch_size TRAIN_BATCH_SIZE]
               [--data_path DATA_PATH] [--filepath FILEPATH]
               [--num_workers NUM_WORKERS]
               [--train_max_epochs TRAIN_MAX_EPOCHS]
               [--eval_max_epochs EVAL_MAX_EPOCHS]
               [--train_epoch_length TRAIN_EPOCH_LENGTH]
               [--eval_epoch_length EVAL_EPOCH_LENGTH] [--lr LR]
               [--log_train LOG_TRAIN] [--log_eval LOG_EVAL] [--seed SEED]
               [--eval_batch_size EVAL_BATCH_SIZE] [--verbose]
               [--nproc_per_node NPROC_PER_NODE] [--nnodes NNODES]
               [--node_rank NODE_RANK] [--master_addr MASTER_ADDR]
               [--master_port MASTER_PORT] [--model_name MODEL_NAME]
               [--project_name PROJECT_NAME] [--n_saved N_SAVED]
               [--save_every_iters SAVE_EVERY_ITERS]

optional arguments:
  -h, --help            show this help message and exit
  --train_batch_size TRAIN_BATCH_SIZE
                        will be equally divided by number of GPUs if in
                        distributed (4)
  --data_path DATA_PATH
                        datasets path (./)
  --filepath FILEPATH   logging file path (./logs)
  --num_workers NUM_WORKERS
                        num_workers for DataLoader (2)
  --train_max_epochs TRAIN_MAX_EPOCHS
                        max_epochs of ignite.Engine.run() for training (2)
  --eval_max_epochs EVAL_MAX_EPOCHS
                        max_epochs of ignite.Engine.run() for evaluation (2)
  --train_epoch_length TRAIN_EPOCH_LENGTH
                        epoch_length of ignite.Engine.run() for training
                        (None)
  --eval_epoch_length EVAL_EPOCH_LENGTH
                        epoch_length of ignite.Engine.run() for evaluation
                        (None)
  --lr LR               learning rate used by torch.optim.* (0.001)
  --log_train LOG_TRAIN
                        logging interval of training iteration (50)
  --log_eval LOG_EVAL   logging interval of evaluation epoch (1)
  --seed SEED           used in ignite.utils.manual_seed() (666)
  --eval_batch_size EVAL_BATCH_SIZE
                        will be equally divided by number of GPUs if in
                        distributed (4)
  --verbose             use logging.INFO in ignite.utils.setup_logger
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
                        master node port for torch native backends None
  --model_name MODEL_NAME
                        image classification model name (resnet18)
  --project_name PROJECT_NAME
                        project name of experiment tracking system (None)
  --n_saved N_SAVED     number of best models to store (2)
  --save_every_iters SAVE_EVERY_ITERS
                        model saving interval (1000)
```
