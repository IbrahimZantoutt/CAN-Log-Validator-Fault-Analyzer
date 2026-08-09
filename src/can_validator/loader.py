import csv
import logging

logger = logging.getLogger(__name__)

def load_log(file_path: str, continueMode=False)-> list[dict]:
    '''
    load_log function: opens a csv file and gets the data as dicts and changes some datatypes and then returns a list with the data

    params: takes in string file_path
    return: returns a list with all the dictionaries for each entry message
    '''
    listAll = []
    try:
        with open(file_path,'r',encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    row["message_id"] = int(row["message_id"])
                    row["timestamp"] = float(row["timestamp"])
                    strT = row["data"]
                    row["data"] = bytes.fromhex(strT)
                    # print(row)
                    listAll.append(row)
                except ValueError:
                    if(continueMode):
                        logger.warning(f"invalid hex characters skipping row: {row}")
                        continue
                    else:
                        raise ValueError(f"invalid hex data in row: {row}")
                        
                    
    except FileNotFoundError:
        raise FileNotFoundError(f"file was not found at {file_path}")
    except PermissionError:
        raise PermissionError(f"permission error in file at {file_path}")
    except UnicodeDecodeError:
        raise ValueError(f"decoder error for file at {file_path}")
    #print(listAll)
    return listAll

load_log("data/sample_log.csv")
#load_log("data/sample_log_invHex.csv",True)