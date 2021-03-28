from argparse import ArgumentParser

from single_cg.utils import get_default_parser


# test get_default_parser of utils.py
def test_get_default_parser():
    parser = get_default_parser()
    assert isinstance(parser, ArgumentParser)
    assert not parser.add_help
