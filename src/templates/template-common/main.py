ckpt_handler_train, ckpt_handler_eval, timer = setup_handlers(
    trainer, evaluator, config, to_save_train, to_save_eval
)

#::: if (it.save_training || it.save_evaluation || it.patience || it.terminate_on_nan || it.timer || it.limit_sec) { :::#
if timer is not None:
    logger.info("Time per batch: %.4f seconds", timer.value())
    timer.reset()
#::: } :::#

#::: if (it.logger) { :::#
if rank == 0:
    from ignite.contrib.handlers.wandb_logger import WandBLogger

    if isinstance(exp_logger, WandBLogger):
        # why handle differently for wandb?
        # See: https://github.com/pytorch/ignite/issues/1894
        exp_logger.finish()
    elif exp_logger:
        exp_logger.close()
#::: } :::#

#::: if (it.save_training || it.save_evaluation || it.patience || it.terminate_on_nan || it.timer || it.limit_sec) { :::#
if ckpt_handler_train is not None:
    logger.info(
        "Last training checkpoint name - %s",
        ckpt_handler_train.last_checkpoint,
    )

if ckpt_handler_eval is not None:
    logger.info(
        "Last evaluation checkpoint name - %s",
        ckpt_handler_eval.last_checkpoint,
    )
#::: } :::#

# main
@hydra.main(config_name="config")
def main(config):
    #::: if (it.dist === 'spawn') { :::#
    #::: if (it.nproc_per_node && it.nnodes && it.master_addr && it.master_port) { :::#
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
