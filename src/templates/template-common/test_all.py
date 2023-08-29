def test_save_config():
    with open("./config.yaml", "r") as f:
        config = OmegaConf.load(f)

    config.sub_output_dir = "job-dir"

    save_config(config, "./")

    del config["sub_output_dir"]

    with open("./config-lock.yaml", "r") as f:
        test_config = OmegaConf.load(f)

    assert config == test_config
