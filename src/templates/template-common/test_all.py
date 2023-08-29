def test_save_config():
    with open("./config.yaml", "r") as f:
        config = OmegaConf.load(f)

    # Add backend to config (similar to setup_config)
    config.backend = None

    with tempfile.TemporaryDirectory() as output_dir:
        output_dir = Path(output_dir)

        save_config(config, output_dir)

        with open(output_dir / "config-lock.yaml", "r") as f:
            test_config = OmegaConf.load(f)

        assert config == test_config
