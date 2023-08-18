def test_save_config():
    with open("./config.yaml", "r") as f:
        config = yaml.safe_load(f.read())

    save_config(config, "./save-config-test.yaml")

    with open("./", "r") as f:
        test_config = yaml.safe_load(f.read())

    assert config == test_config
