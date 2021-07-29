import pytest


@pytest.mark.parametrize("file_path", [("../project/base.db")])
def test_file_exist(file_path):
    assert open(file_path)