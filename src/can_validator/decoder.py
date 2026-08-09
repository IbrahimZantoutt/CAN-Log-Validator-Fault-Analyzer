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
    decode_log(db,entries)