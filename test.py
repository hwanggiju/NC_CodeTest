import keyboard

val = 0

while True:
    event = keyboard.read_event()
    if event.name == "up":
        if event.event_type == "down" :
            val += 1
    elif event.name == "down":
        if event.event_type == "down" :
            val -= 1
    else :
        pass
    
    print(val)