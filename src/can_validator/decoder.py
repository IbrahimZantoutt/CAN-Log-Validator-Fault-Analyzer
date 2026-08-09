import cantools
import logging
from can_validator.loader import load_log

logger = logging.getLogger(__name__)

def load_db(path:str):
    try:
        db = cantools.database.load_file(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"dbc file not found at {path}")
    return db

def decode_entry(db:cantools.database.Database, entry:dict)->dict:
    '''
    takes in a single row/entry and returns a dictionary with the message name and the decoded signals
    params: the dbc and the entry to decode
    return: a dictionary with the message name and the decoded signals
    '''
    
    newDict = {}
    try:
        message = db.get_message_by_frame_id(entry["message_id"])
    except KeyError:
             raise KeyError
    
    newDict["message_id"] = entry["message_id"]
    newDict["message_name"] = message.name

    decoded = db.decode_message(entry["message_id"], entry["data"])
    newDict["signals"] = decoded

    # print(newDict)
    return newDict

def decode_log(db:cantools.database.Database, entries:list[dict])->list:
    decodedLogs = []
    for entry in entries:
        try:
            decodedLogs.append(decode_entry(db,entry))
        except KeyError:
            logger.warning(f"No message with the specified message_id: {entry['message_id']}")
        except cantools.database.errors.DecodeError as e:
            logger.warning(f"Failed to decode entry {entry}: {e}")
    #print(decodedLogs)
    return decodedLogs

if __name__ == "__main__":
    db = load_db("dbc/vehicle.dbc")
    entries = load_log("data/sample_log.csv")
    #entries = load_log("data/sample_log_invID.csv")
    decode_log(db,[{'timestamp': 0.0, 'message_id': 213, 'data': b'2\x00\xe6\x00'}, {'timestamp': 0.02, 'message_id': 213, 'data': b'3\x00\xe6\x00'}, {'timestamp': 0.04, 'message_id': 13, 'data': b'4\x00\xe6\x00'}, {'timestamp': 0.1, 'message_id': 16, 'data': b'\x05\x01\x00\x00\x00'}, {'timestamp':0.15, 'message_id': 78, 'data': b'2\xff\x04\x00'}, {'timestamp': 0.17, 'message_id': 78, 'data': b'2\xff\x04\x00'}, {'timestamp': 0.19, 'message_id': 78, 'data': b'2\xff\x04\x00'}])