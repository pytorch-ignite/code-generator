from tempfile import TemporaryDirectory

from torch.utils.data import Dataset

from {{project_name}}.datasets import get_datasets


def test_get_datasets():
    with TemporaryDirectory() as tmp:
        train_ds, eval_ds = get_datasets(tmp)
        assert isinstance(train_ds, Dataset)
        assert isinstance(eval_ds, Dataset)
