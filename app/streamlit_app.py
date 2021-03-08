from pathlib import Path

import importlib
import streamlit as st
from jinja2 import Environment, FileSystemLoader

st.set_page_config(
    page_title="Code Generator",
    page_icon="https://raw.githubusercontent.com/pytorch/ignite/master/assets/logo/ignite_logomark.svg",
)

st.write(
    """
<div align='center'>
<img src="https://raw.githubusercontent.com/pytorch/ignite/master/assets/logo/ignite_logomark.svg" width="100" height="100">

# Code Generator

Application to generate your training scripts with [PyTorch-Ignite](https://github.com/pytorch/ignite).
</div>
""",
    unsafe_allow_html=True,
)


def generate(path: Path, fname: str, code: str) -> None:
    """Generate `fname` with content `code` in `path`."""
    (path / fname).write_text(code)


# copied from https://github.com/jrieke/traingenerator/blob/76e637975989d11c549c17694c5603a409e184dd/app/utils.py#L14-L29
def import_from_file(module_name: str, filepath: str):
    """Imports a module from file.

    Args:
        module_name (str): Assigned to the module's __name__ parameter (does not 
            influence how the module is named outside of this function)
        filepath (str): Path to the .py file

    Returns:
        The module
    """
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    task_list = [p.stem for p in Path("./templates").iterdir() if p.is_dir()]
    with st.sidebar:
        task = st.selectbox("Task", task_list)
        config = import_from_file(
            "template_config", f"./templates/{task}/configs.py"
        ).get_configs()
    env = Environment(
        loader=FileSystemLoader("./templates"), trim_blocks=True, lstrip_blocks=True
    )
    path = Path(f"dist/{task}")
    path.mkdir(parents=True, exist_ok=True)
    templates_list = (
        template
        for template in env.list_templates(".jinja")
        if template.startswith(task)
    )

    for fname in templates_list:
        template = env.get_template(fname)
        fname = fname.strip(f"{task}/").strip(".jinja")
        code = template.render(**config)
        generate(path, fname, code)
        with st.beta_expander(f"View generated {fname}"):
            st.code(code)


if __name__ == "__main__":
    main()
