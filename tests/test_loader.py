import pytest

from can_validator.loader import load_log


@pytest.mark.parametrize("path",[
    ("data/logs.csv"),
    ("sample_log.csv"),
    ("info/sample_log.csv"),
])
def test_file_not_found(path):
    with pytest.raises(FileNotFoundError):
        load_log(path)

def test_invlid_hex():
    with pytest.raises(ValueError):
        load_log("data/sample_log_invHex.csv")

def test_expected_dict():
    assert load_log("data/sample_log.csv") == [{'timestamp': 0.0, 'message_id': 213, 'data': b'2\x00\xe6\x00'}, {'timestamp': 0.02, 'message_id': 213, 'data': b'3\x00\xe6\x00'}, {'timestamp': 0.04, 'message_id': 213, 'data': b'4\x00\xe6\x00'}, {'timestamp': 0.1, 'message_id': 126, 'data': b'\x05\x01\x00\x00\x00'}, {'timestamp':0.15, 'message_id': 78, 'data': b'2\xff\x04\x00'}, {'timestamp': 0.17, 'message_id': 78, 'data': b'2\xff\x04\x00'}, {'timestamp': 0.19, 'message_id': 78, 'data': b'2\xff\x04\x00'}]

def test_return_good_data():
    assert load_log("data/sample_log_invHex.csv",True) == [{'timestamp': 0.0, 'message_id': 213, 'data': b'2\x00\xe6\x00'}, {'timestamp': 0.02, 'message_id': 213, 'data': b'3\x00\xe6\x00'}, {'timestamp': 0.04, 'message_id': 213, 'data': b'4\x00\xe6\x00'}, {'timestamp': 0.1, 'message_id': 126, 'data': b'\x05\x01\x00\x00\x00'}, {'timestamp':0.15, 'message_id': 78, 'data': b'2\xff\x04\x00'}, {'timestamp': 0.17, 'message_id': 78, 'data': b'2\xff\x04\x00'}, {'timestamp': 0.19, 'message_id': 78, 'data': b'2\xff\x04\x00'}]