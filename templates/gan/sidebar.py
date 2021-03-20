import sys

import streamlit as st

sys.path.append('./templates/')

from base.sidebar import get_configs as base_configs


def get_configs() -> dict:
    config = base_configs()
    return config
