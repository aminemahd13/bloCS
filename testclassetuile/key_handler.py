import keyboard

direction={"up" : ['w','z','up'] , "down" : ['s','down'] , "right" : ['d' , 'right'] , "left" : ['q' , 'a' , 'left'] , "close" : ['esc']}

def up():
    test=False
    for i in direction["up"]:
        test = test or keyboard.is_pressed(i)
    return test

def down():
    test=False
    for i in direction["down"]:
        test = test or keyboard.is_pressed(i)
    return test

def right():
    test=False
    for i in direction["right"]:
        test = test or keyboard.is_pressed(i)
    return test

def left():
    test=False
    for i in direction["left"]:
        test = test or keyboard.is_pressed(i)
    return test

def close():
    test=False
    for i in direction["close"]:
        test = test or keyboard.is_pressed(i)
    return test