import sys
from pprint import pprint

import ignite.distributed as idist

TEMPLATE_NAME = "image_classification"

sys.path.append(f"./templates/{TEMPLATE_NAME}")
sys.path.append("./app")

from codegen import CodeGenerator
from fuzzer import *


def generate_inputs(dist_train=False, seed=0) -> dict:
    set_random_seed(seed)
    inputs = {
        "amp_mode": None,
        "device": idist.device(),
        "data_path": random_path(),
        "filepath": random_path(),
        "train_batch_size": random_int(1, 2),
        "eval_batch_size": random_int(1, 2),
        "num_workers": random_int(0, 2),
        "max_epochs": random_int(1, 5),
        "lr": random_float(0.0, 1.0),
        "log_train": random_int(1, 10),
        "log_eval": random_int(1, 10),
        "seed": random_int(0, 1000),
        "nproc_per_node": None,
        "nnodes": None,
        "node_rank": None,
        "master_addr": None,
        "master_port": None,
    }
    # if dist_train:
    #     inputs.update(
    #         {
    #             "nproc_per_node": random_int(**params.nproc_per_node.test["dist_train"]),
    #             "nnodes": random_int(**params.nnodes.test["dist_train"]),
    #         }
    #     )
    #     if inputs["nnodes"] > 1:
    #         inputs.update(
    #             {
    #                 "node_rank": random_int(**params.node_rank.test["multinode"]),
    #                 "master_addr": params.master_addr.test["multinode"],
    #                 "master_port": params.master_port.test["multinode"],
    #             }
    #         )

    return inputs


def generate_plain_train():
    """Example run."""
    dist_train = False
    target_dir = "./tests/templates/dist"
    seed = 0
    inputs = generate_inputs(dist_train=dist_train, seed=seed)
    print("Seed:", seed)
    print("Use distributed training:", dist_train)
    print("Generated config:")
    pprint(inputs)
    code_gen = CodeGenerator(target_dir=target_dir)
    [*code_gen.render_templates(TEMPLATE_NAME, inputs)]
    print(f"Generated files can be found in {target_dir}/{TEMPLATE_NAME}")
    print(f"To run generated example:\ncd {target_dir}/{TEMPLATE_NAME}\npython main.py --verbose")


if __name__ == "__main__":
    generate_plain_train()
