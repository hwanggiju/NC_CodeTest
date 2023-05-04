import keyboard

val = 0

while True:
    event = keyboard.read_event()
    if event.name == "up":
        if event.event_type == "down" :
            val += 1
            print(val)
    elif event.name == "down":
        if event.event_type == "down" :
            val -= 1
            print(val)
    else :
        pass
