import pytest
import cantools

from can_validator.decoder import load_db,decode_log,decode_entry

@pytest.mark.parametrize("path",[
    "data/data.csv",
    "logs.csv",
    "sample_log.csv"
])
def test_inv_db(path):
    with pytest.raises(FileNotFoundError):
        load_db(path)

def test_inv_msg_id():
    db = cantools.database.load_file("dbc/vehicle.dbc")
    with pytest.raises(KeyError):
        decode_entry(db,{'timestamp': 0.0, 'message_id': 233, 'data': b'2\x00\xe6\x00'})

def test_inv_log_skip():
    db = cantools.database.load_file("dbc/vehicle.dbc")
    assert decode_log(db,[{'timestamp': 0.0, 'message_id': 213, 'data': b'2\x00\xe6\x00'}, {'timestamp': 0.02, 'message_id': 213, 'data': b'3\x00\xe6\x00'}, {'timestamp': 0.04, 'message_id': 13, 'data': b'4\x00\xe6\x00'}, {'timestamp': 0.1, 'message_id': 16, 'data': b'\x05\x01\x00\x00\x00'}, {'timestamp':0.15, 'message_id': 78, 'data': b'2\xff\x04\x00'}, {'timestamp': 0.17, 'message_id': 78, 'data': b'2\xff\x04\x00'}, {'timestamp': 0.19, 'message_id': 78, 'data': b'2\xff\x04\x00'}]) == [{'message_id': 213, 'message_name': 'EngineData', 'signals': {'RPM': 50, 'TempE': -40}}, {'message_id': 213, 'message_name': 'EngineData', 'signals': {'RPM': 51, 'TempE': -40}}, {'message_id': 78, 'message_name': 'BatteryStatus', 'signals': {'Percentage': 50, 'Checksum': 255, 'Counter': 4}}, {'message_id': 78, 'message_name': 'BatteryStatus', 'signals': {'Percentage': 50, 'Checksum': 255, 'Counter': 4}}, {'message_id': 78, 'message_name': 'BatteryStatus', 'signals': {'Percentage': 50, 'Checksum': 255, 'Counter': 4}}]

def test_inv_data_length_skip():
    db = cantools.database.load_file("dbc/vehicle.dbc")
    result = decode_log(db, [{'timestamp': 0.1, 'message_id': 213, 'data': b'\x01'}])  # too short
    assert result == []
