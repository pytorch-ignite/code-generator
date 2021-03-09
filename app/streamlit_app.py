import importlib
from pathlib import Path

import streamlit as st
from jinja2 import Environment, FileSystemLoader

from base_config import get_configs

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


def main():
    task_list = [p.stem for p in Path("./templates").iterdir() if p.is_dir()]
    with st.sidebar:
        task = st.selectbox("Task", task_list)
        config = get_configs()
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
