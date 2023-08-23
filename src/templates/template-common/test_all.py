def test_save_config():
    with open("./config.yaml", "r") as f:
        config = OmegaConf.load(f)

    save_config(config, "./")

    with open("./config-lock.yaml", "r") as f:
        test_config = OmegaConf.load(f)

    assert config == test_config
