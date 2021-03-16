import subprocess
import sys
from pathlib import Path

from hypothesis import given, settings
from hypothesis import strategies as st

sys.path.append("./templates/base")
sys.path.append("./app")

from codegen import CodeGenerator
from fuzzer import *

target_dir = "./tests/templates/dist/"
# target_dir = random_path()


@settings(deadline=None, derandomize=True)
@given(
    st.integers(min_value=1, max_value=2),  # train_batch_size
    st.integers(min_value=1, max_value=2),  # eval_batch_size
    st.integers(min_value=0, max_value=2),  # num_workers
    st.integers(min_value=1, max_value=1),  # max_epochs
    st.floats(min_value=0.0, max_value=1.0),  # lr
    st.integers(min_value=1, max_value=10),  # log_train
    st.integers(min_value=1, max_value=10),  # log_eval
    st.integers(min_value=0, max_value=1000),  # seed
)
def generate_base_cpu(train_batch_size, eval_batch_size, num_workers, max_epochs, lr, log_train, log_eval, seed):
    inputs = {
        "amp_mode": None,
        "device": "cpu",
        "data_path": random_path(),
        "filepath": random_path(),
        "train_batch_size": train_batch_size,
        "eval_batch_size": eval_batch_size,
        "num_workers": num_workers,
        "max_epochs": max_epochs,
        "lr": lr,
        "log_train": log_train,
        "log_eval": log_eval,
        "seed": seed,
        "nproc_per_node": None,
        "nnodes": None,
        "node_rank": None,
        "master_addr": None,
        "master_port": None,
    }
    template_name = "base"
    # pprint(inputs)
    code_gen = CodeGenerator(target_dir=target_dir)
    [*code_gen.render_templates(template_name, inputs)]
    # print(f"Generated files can be found in {target_dir}/{output_path_name}")
    # print(f"To run generated example:\ncd {target_dir}/{output_path_name}\npython main.py")


def test_base_cpu():
    generated_path = Path(target_dir)
    generated_paths = generated_path.rglob("main.py")
    for p in generated_paths:
        subprocess.run(
            ["cd", f"{str(p).replace('main.py', '')}", "&&", "python", "main.py", "--verbose"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )


if __name__ == "__main__":
    generate_base_cpu()
    test_base_cpu()
