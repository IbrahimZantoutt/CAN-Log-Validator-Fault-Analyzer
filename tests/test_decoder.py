import pytest

from can_validator.decoder import load_db,decode_log,decode_entry

@pytest.mark.parametrize("path",[
    "data/data.csv",
    "logs.csv",
    "sample_log.csv"
])
def test_inv_db(path):
    with pytest.raises(FileNotFoundError):
        load_db(path)

