# main entrypoint
#::: if (['python-fire'].includes(it.argparser)) { :::#
def main(config_path, output_path="./runs", render_mode=None, **kwargs):
    config_path = Path(config_path)
    assert config_path.exists(), config_path
    config = setup_config(config_path, **kwargs)
#::: } else { :::#
def main():
    config = setup_config()
#::: } :::#
    #::: if (it.dist === 'spawn') { :::#
    #::: if (it.nproc_per_node && it.nnodes > 1 && it.master_addr && it.master_port) { :::#
    kwargs_backend = {
        "nproc_per_node": config.nproc_per_node,
        "nnodes": config.nnodes,
        "node_rank": config.node_rank,
        "master_addr": config.master_addr,
        "master_port": config.master_port,
    }
    #::: } else if (it.nproc_per_node) { :::#
    kwargs_backend = {"nproc_per_node": config.nproc_per_node}
    #::: } :::#
    with idist.Parallel(config.backend, **kwargs_backend) as p:
        p.run(run, config=config)
    #::: } else { :::#
    with idist.Parallel(config.backend) as p:
        p.run(run, config=config)
    #::: } :::#


if __name__ == "__main__":
    #::: if (['python-fire'].includes(it.argparser)) { :::#
    fire.Fire(main)
    #::: } else { :::#
    main()
    #::: } :::#
