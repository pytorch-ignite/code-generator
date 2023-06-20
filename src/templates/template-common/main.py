ckpt_handler_train, ckpt_handler_eval = setup_handlers(
    trainer, evaluator, config, to_save_train, to_save_eval
)

#::: if (it.logger) { :::#
if rank == 0:
    exp_logger.close()
#::: } :::#

#::: if (it.save_training || it.save_evaluation) { :::#
# show last checkpoint names
logger.info(
    "Last training checkpoint name - %s",
    ckpt_handler_train.last_checkpoint,
)

logger.info(
    "Last evaluation checkpoint name - %s",
    ckpt_handler_eval.last_checkpoint,
)
#::: } :::#


# main entrypoint
def main():
    config = setup_config()
    #::: if (it.dist === 'spawn') { :::#
    #::: if (it.nproc_per_node && it.nnodes > 1 && it.master_addr && it.master_port) { :::#
    kwargs = {
        "nproc_per_node": config.nproc_per_node,
        "nnodes": config.nnodes,
        "node_rank": config.node_rank,
        "master_addr": config.master_addr,
        "master_port": config.master_port,
    }
    #::: } else if (it.nproc_per_node) { :::#
    kwargs = {"nproc_per_node": config.nproc_per_node}
    #::: } :::#
    with idist.Parallel(config.backend, **kwargs) as p:
        p.run(run, config=config)
    #::: } else { :::#
    with idist.Parallel(config.backend) as p:
        p.run(run, config=config)
    #::: } :::#
