# main entrypoint
#::: if ((it.argparser == 'fire')) { :::#
def main(config_path, backend=None, **kwargs):
    config_path = Path(config_path)
    assert config_path.exists(), config_path
    config = setup_config(config_path, backend, **kwargs)


#::: } else if ((it.argparser == 'hydra')) { :::#
@hydra.main(version_base=None, config_path=".", config_name="config")
def main(cfg: DictConfig):
    config = setup_config(cfg)


#::: } else { :::#
def main():
    config = setup_config()
    #::: } :::#

    #::: if (it.dist === 'spawn') { :::#
    #::: if (it.nproc_per_node && it.nnodes > 1 && it.master_addr && it.master_port) { :::#
    spawn_kwargs = {
        "nproc_per_node": config.nproc_per_node,
        "nnodes": config.nnodes,
        "node_rank": config.node_rank,
        "master_addr": config.master_addr,
        "master_port": config.master_port,
    }
    #::: } else if (it.nproc_per_node) { :::#
    spawn_kwargs = {"nproc_per_node": config.nproc_per_node}
    #::: } :::#
    with idist.Parallel(config.backend, **spawn_kwargs) as p:
        p.run(run, config=config)
    #::: } else { :::#
    with idist.Parallel(config.backend) as p:
        p.run(run, config=config)
    #::: } :::#


if __name__ == "__main__":
    #::: if ((it.argparser == 'fire')) { :::#
    fire.Fire(main)

    #::: } else if if ((it.argparser == 'hydra')){ :::#
    sys.argv.append("hydra.run.dir=.")
    sys.argv.append("hydra.output_subdir=null")
    sys.argv.append("hydra/job_logging=stdout")
    main()

    #::: } else { :::#
    main()

    #::: } :::#
