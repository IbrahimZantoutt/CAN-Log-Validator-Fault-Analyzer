import cantools

db = cantools.database.load_file("dbc/vehicle.dbc")

for message in db.messages:
    print(f"Message: {message.name} (ID: {message.frame_id}, DLC: {message.length})")
    for signal in message.signals:
        print(f"  Signal: {signal.name}  start_bit={signal.start}  length={signal.length}  "
              f"factor={signal.scale}  offset={signal.offset}  min={signal.minimum}  max={signal.maximum}")