[![Code-Generator](https://badgen.net/badge/Template%20by/Code-Generator/ee4c2c?labelColor=eaa700)](https://github.com/pytorch-ignite/code-generator)

# Reinforcement Learning Template

This is the Reinforcement Learning template by Code-Generator using OpenAI Gym for the environment CarRacing-v2.

## Getting Started

Install the dependencies with `pip`:

```sh
pip install -r requirements.txt --progress-bar off -U
```

### Code structure

```
|
|- README.md
|
|- a2c.py : main script to run
|- a2c_model_env.py : Utility functions for the reinforcement learning template for various tasks
|- utils.py : module with various helper functions
|- requirements.txt : dependencies to install with pip
|
|- config_a2c.yaml : global configuration YAML file
```

## Training

### 1 GPU Training

```sh
python a2c.py config_a2c.yaml
```
