"""Utilities module.
"""
from importlib.machinery import SourceFileLoader


def import_from_file(module_name: str, filepath: str):
    """Imports a module from file.

    Args:
        module_name (str): Assigned to the module's __name__ parameter (does not
            influence how the module is named outside of this function)
        filepath (str): Path to the .py file

    Returns:
        The module
    """
    return SourceFileLoader(module_name, filepath).load_module()
