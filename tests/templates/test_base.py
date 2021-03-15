import os
import sys
from pprint import pp

sys.path.append("./templates/base")
sys.path.append("./app")

from codegen import CodeGenerator
from config import params
from fuzzer import *


def generate_inputs(params, dist_train=False, seed=0) -> dict:
    set_random_seed(seed)
    inputs = {
        "amp_mode": random_element(params.amp_mode.test),
        "device": random_element(params.device.test),
        "data_path": random_path(**params.data_path.test),
        "filepath": random_path(**params.filepath.test),
        "train_batch_size": random_int(**params.train_batch_size.test),
        "eval_batch_size": random_int(**params.eval_batch_size.test),
        "num_workers": random_int(**params.num_workers.test),
        "max_epochs": random_int(**params.max_epochs.test),
        "lr": random_float(**params.lr.test),
        "log_train": random_int(**params.log_train.test),
        "log_eval": random_int(**params.log_eval.test),
        "seed": random_int(**params.seed.test),
        "nproc_per_node": params.nproc_per_node.test["nondist_train"],
        "nnodes": params.nnodes.test["nondist_train"],
        "node_rank": params.node_rank.test["singlenode"],
        "master_addr": params.master_addr.test["singlenode"],
        "master_port": params.master_port.test["singlenode"],
    }
    if dist_train:
        inputs.update(
            {
                "nproc_per_node": random_int(**params.nproc_per_node.test["dist_train"]),
                "nnodes": random_int(**params.nnodes.test["dist_train"]),
            }
        )
        if inputs["nnodes"] > 1:
            inputs.update(
                {
                    "node_rank": random_int(**params.node_rank.test["multinode"]),
                    "master_addr": params.master_addr.test["multinode"],
                    "master_port": params.master_port.test["multinode"],
                }
            )

    return inputs


def generate_plain_train():
    """Example run.
    """
    dist_train = False
    template_name = "base"
    target_dir = "./tests/templates/dist"
    seed = 0
    inputs = generate_inputs(params, dist_train=dist_train, seed=seed)
    print("Seed:", seed)
    print("Use distributed training:", dist_train)
    print("Generated config:")
    pp(inputs)
    code_gen = CodeGenerator(target_dir=target_dir)
    [*code_gen.render_templates(template_name, inputs)]
    print(f"Generated files can be found in {target_dir}/{template_name}")
    # Launching
    os.chdir(f"{target_dir}/{template_name}")
    sys.path.append(".")
    import main
    main.main()
    # print(f"To run generated example:\ncd {target_dir}/{template_name}\npython main.py")


if __name__ == "__main__":
    generate_plain_train()
