"""Streamlit app view.
"""
import streamlit as st


class View:
    page_title = "Code Generator"
    page_icon = "https://raw.githubusercontent.com/pytorch/ignite/master/assets/logo/ignite_logomark.svg"
    description = """
<div align='center'>
<img src="https://raw.githubusercontent.com/pytorch/ignite/master/assets/logo/ignite_logomark.svg" width="100" height="100">

# Code Generator

Application to generate your training scripts with [PyTorch-Ignite](https://github.com/pytorch/ignite).
</div>
"""

    def __init__(self):
        st.set_page_config(page_title=self.page_title, page_icon=self.page_icon)
        st.write(self.description, unsafe_allow_html=True)

    def sidebar(self, task_list=None, config=None):
        """Sidebar on the left.
        """
        task_list = task_list or []
        with st.sidebar:
            self.task = st.selectbox("Task", task_list)
            if self.task:
                config = config(self.task)
                self.config = config.get_configs()
            else:
                self.config = {}

    def render_code(self, fname="", code="", fold=False):
        """Main content with the code.
        """
        if fold:
            with st.beta_expander(f"View generated {fname}"):
                st.code(code)
        else:
            st.code(code)
