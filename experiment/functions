from psychopy import visual, core

def rgb_transform(color, type="rgb255"):
    if type == "rgb255":
        return tuple(c / 127.5 - 1 for c in color)
    if type == "psychopy":
        return tuple((c + 1) / 127.5 for c in color)

def quit_experiment():
    win.close()
    core.quit()

def create_wheel(colors):

    wheel = []

    # Whidth of each pie (end-start)
    start = 0
    end = 15

    # Pies
    for i in range(6):

        # Create the pie
        pie = visual.Pie(win, radius=PIE_RADI, pos=(0, 0), start=i*60 + start, end=i*60 + end, lineColor=colors[i])

        # Set the color (This is though to PsychoPy bug where fillColor parameter does not work)
        pie.setColor(colors[i], 'rgb')

        # Append it to list of pies
        wheel.append(pie)
        
    # Add a circle with background color so it looks like a wheel
    wheel_cover = visual.Circle(win, radius=WHEEL_COVER_RADI, pos=(0, 0), fillColor=BGC)

    # Append it to the list of shapes that create the wheel
    wheel.append(wheel_cover)

    return wheel

def display_shape(shape_list, stat="on"):

    if stat == "on":
        for w in shape_list:
            w.setAutoDraw(True)

    elif stat == "off":
        for w in shape_list:
            w.setAutoDraw(False)
