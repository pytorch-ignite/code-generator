import shutil
import sys
from pathlib import Path


def generate():
    """Example run."""
    sys.path.append("./app")

    from codegen import CodeGenerator
    from utils import import_from_file

    for p in Path("./templates").iterdir():
        if p.is_dir() and not p.stem.startswith("_"):
            sys.path.append(f"./templates/{p.stem}")
            dist_dir = "./tests/dist"
            configs = import_from_file("template_config", f"./templates/{p.stem}/_sidebar.py").get_configs()
            configs["setup_timer"] = True
            configs["test_all"] = True
            code_gen = CodeGenerator(dist_dir=dist_dir)
            [*code_gen.render_templates(p.stem, configs)]
            code_gen.make_and_write(p.stem, Path(dist_dir))
            shutil.copy(p / "_test_internal.py", f"{dist_dir}/{p.stem}")


def generate_for_dist_launch():
    sys.path.append("./app")

    from codegen import CodeGenerator
    from utils import import_from_file

    for p in Path("./templates").iterdir():
        if p.is_dir() and not p.stem.startswith("_"):
            sys.path.append(f"./templates/{p.stem}")
            dist_dir = "./tests/dist/launch"
            configs = import_from_file("template_config", f"./templates/{p.stem}/_sidebar.py").get_configs()
            configs["use_distributed_training"] = True
            configs["use_distributed_launcher"] = True
            configs["setup_timer"] = True
            configs["test_all"] = True
            configs["nnodes"] = 1
            code_gen = CodeGenerator(dist_dir=dist_dir)
            [*code_gen.render_templates(p.stem, configs)]
            code_gen.make_and_write(p.stem, Path(dist_dir))
            shutil.copy(p / "_test_internal.py", f"{dist_dir}/{p.stem}")


def generate_for_dist_spawn():
    sys.path.append("./app")

    from codegen import CodeGenerator
    from utils import import_from_file

    for p in Path("./templates").iterdir():
        if p.is_dir() and not p.stem.startswith("_"):
            sys.path.append(f"./templates/{p.stem}")
            dist_dir = "./tests/dist/spawn"
            configs = import_from_file("template_config", f"./templates/{p.stem}/_sidebar.py").get_configs()
            configs["use_distributed_training"] = True
            configs["use_distributed_launcher"] = False
            configs["setup_timer"] = True
            configs["test_all"] = True
            configs["nnodes"] = 1
            code_gen = CodeGenerator(dist_dir=dist_dir)
            [*code_gen.render_templates(p.stem, configs)]
            code_gen.make_and_write(p.stem, Path(dist_dir))
            shutil.copy(p / "_test_internal.py", f"{dist_dir}/{p.stem}")


if __name__ == "__main__":
    generate()
    generate_for_dist_launch()
    generate_for_dist_spawn()
