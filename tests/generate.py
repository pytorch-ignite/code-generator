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
            code_gen = CodeGenerator(dist_dir=dist_dir)
            [*code_gen.render_templates(p.stem, configs)]
            code_gen.mk_dist_template_dir(p.stem)
            code_gen.write_files(p.stem)
            print(f"Generated files can be found in {dist_dir}/{p.stem}")


if __name__ == "__main__":
    generate()
