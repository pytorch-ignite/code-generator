#::= from_template_common ::#

#::: if (it.save_training || it.save_evaluation || it.patience || it.terminate_on_nan || it.limit_sec) { :::#


def setup_handlers(
    trainer: Engine,
    evaluator: Engine,
    config: Any,
    to_save_train: Optional[dict] = None,
    to_save_eval: Optional[dict] = None,
):
    """Setup Ignite handlers."""

    ckpt_handler_train = ckpt_handler_eval = None
    #::: if (it.save_training || it.save_evaluation) { :::#
    # checkpointing
    saver = DiskSaver(config.output_dir / "checkpoints", require_empty=False)
    #::: if (it.save_training) { :::#
    ckpt_handler_train = Checkpoint(
        to_save_train,
        saver,
        filename_prefix=config.filename_prefix,
        n_saved=config.n_saved,
    )
    trainer.add_event_handler(
        Events.ITERATION_COMPLETED(every=config.save_every_iters),
        ckpt_handler_train,
    )
    #::: } :::#
    #::: if (it.save_evaluation) { :::#
    global_step_transform = None
    if to_save_train.get("trainer", None) is not None:
        global_step_transform = global_step_from_engine(to_save_train["trainer"])
    ckpt_handler_eval = Checkpoint(
        to_save_eval,
        saver,
        filename_prefix="best",
        n_saved=config.n_saved,
        global_step_transform=global_step_transform,
        score_name="eval_accuracy",
        score_function=Checkpoint.get_default_score_fn("Accuracy"),
    )
    evaluator.add_event_handler(Events.EPOCH_COMPLETED(every=1), ckpt_handler_eval)
    #::: } :::#
    #::: } :::#

    #::: if (it.patience) { :::#
    # early stopping
    def score_fn(engine: Engine):
        return engine.state.metrics["Accuracy"]

    es = EarlyStopping(config.patience, score_fn, trainer)
    evaluator.add_event_handler(Events.EPOCH_COMPLETED, es)
    #::: } :::#

    #::: if (it.terminate_on_nan) { :::#
    # terminate on nan
    trainer.add_event_handler(Events.ITERATION_COMPLETED, TerminateOnNan())
    #::: } :::#

    #::: if (it.limit_sec) { :::#
    # time limit
    trainer.add_event_handler(Events.ITERATION_COMPLETED, TimeLimit(config.limit_sec))
    #::: } :::#
    #::: if (it.save_training || it.save_evaluation) { :::#
    return ckpt_handler_train, ckpt_handler_eval
    #::: } :::#


#::: } :::#


def thresholded_output_transform(output):
    y_pred, y = output
    return torch.round(torch.sigmoid(y_pred)), y
