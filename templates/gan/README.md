# GAN Template by Code-Generator

This template is ported from [PyTorch-Ignite DCGAN example](https://github.com/pytorch/ignite/tree/master/examples/gan).

After downloading the archive, install the requirements with:

```sh
pip install -r requirements.txt -U --progress-bar off
```

The requirements are:

- Pandas
- PyTorch
- Matplotlib
- Torchvision
- PyTorch-Ignite

After installing the requirements, run the training with:

```sh
python main.py --verbose
```

The following options are available to configure (`python main.py -h`):

```sh
usage: main.py [-h] [--batch_size BATCH_SIZE] [--data_path DATA_PATH]
               [--filepath FILEPATH] [--num_workers NUM_WORKERS]
               [--max_epochs MAX_EPOCHS] [--epoch_length EPOCH_LENGTH]
               [--lr LR] [--log_train LOG_TRAIN] [--seed SEED] [--verbose]
               [--nproc_per_node NPROC_PER_NODE] [--nnodes NNODES]
               [--node_rank NODE_RANK] [--master_addr MASTER_ADDR]
               [--master_port MASTER_PORT] [--n_saved N_SAVED]
               [--dataset {cifar10,lsun,imagenet,folder,lfw,fake,mnist}]
               [--z_dim Z_DIM] [--alpha ALPHA] [--g_filters G_FILTERS]
               [--d_filters D_FILTERS] [--beta_1 BETA_1] [--saved_G SAVED_G]
               [--saved_D SAVED_D]

optional arguments:
  -h, --help            show this help message and exit
  --batch_size BATCH_SIZE
                        will be equally divided by number of GPUs if in
                        distributed (4)
  --data_path DATA_PATH
                        datasets path (./)
  --filepath FILEPATH   logging file path (./logs)
  --num_workers NUM_WORKERS
                        num_workers for DataLoader (2)
  --max_epochs MAX_EPOCHS
                        max_epochs of ignite.Engine.run() for training (2)
  --epoch_length EPOCH_LENGTH
                        epoch_length of ignite.Engine.run() for training
                        (None)
  --lr LR               learning rate used by torch.optim.* (0.001)
  --log_train LOG_TRAIN
                        logging interval of training iteration (50)
  --seed SEED           used in ignite.utils.manual_seed() (666)
  --verbose             use logging.INFO in ignite.utils.setup_logger
  --nproc_per_node NPROC_PER_NODE
                        number of processes to launch on each node, for GPU
                        training this is recommended to be set to the number
                        of GPUs in your system so that each process can be
                        bound to a single GPU (1)
  --nnodes NNODES       number of nodes to use for distributed training (1)
  --node_rank NODE_RANK
                        rank of the node for multi-node distributed training
                        (None)
  --master_addr MASTER_ADDR
                        master node TCP/IP address for torch native backends
                        (None)
  --master_port MASTER_PORT
                        master node port for torch native backends None
  --n_saved N_SAVED     number of best models to store (2)
  --dataset {cifar10,lsun,imagenet,folder,lfw,fake,mnist}
                        dataset to use (cifar10)
  --z_dim Z_DIM         size of the latent z vector (100)
  --alpha ALPHA         running average decay factor (0.98)
  --g_filters G_FILTERS
                        number of filters in the second-to-last generator
                        deconv layer (64)
  --d_filters D_FILTERS
                        number of filters in first discriminator conv layer
                        (64)
  --beta_1 BETA_1       beta_1 for Adam optimizer (0.5)
  --saved_G SAVED_G     path to saved generator (None)
  --saved_D SAVED_D     path to saved discriminator (None)
```
