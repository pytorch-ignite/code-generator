# MAKE SURE YOUR DATASETS ARE DOWNLOADING ON LOCAL_RANK 0.

import ignite.distributed as idist


def get_datasets(local_rank, *args, **kwargs):
    if local_rank > 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()

    # CUSTOM DATASETS GO HERE
    train_dataset = ...
    eval_dataset = ...

    if local_rank == 0:
        # Ensure that only rank 0 download the dataset
        idist.barrier()

    return train_dataset, eval_dataset
