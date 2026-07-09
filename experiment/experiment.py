from psychopy import visual, core, monitors, gui, data, event
import numpy as np

# ===============================
# Functions
# ===============================

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

        # Create a pie
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


# ===============================
# Constants
# ===============================

DISPSIZE = (1920, 1080)

BGC = rgb_transform([128, 128, 128])
YELLOW = rgb_transform([150, 150, 50])
PURPLE = rgb_transform([150, 50, 150])

RADI_LEFT = 0.5/2
FIX_RADI = 0.2/2
RADI_RIGHT = 2/2
WHEEL_COVER_RADI = RADI_RIGHT
PIE_RADI = 2.5 + WHEEL_COVER_RADI

REPS_reproduction = 40 / 5

times = [400, 500, 700, 1100, 1900]


# ===============================
# Dialog Box
# ===============================

# Create the dialog box
info = gui.Dlg(title="Time Perception")
info.addField("Subject ID:", required=True)
info.addField("Block:", required=True)
info.addField("Task Type:", choices=["Temporal Reproduction", "Temporal Discrimination"], required=True)

# Display
okdata = info.show()
if not okdata: core.quit()

# Save the data in variables
ID = info.data[0]
block = info.data[1]
task_type = info.data[2]


# ===============================
# Monitor Set-up
# ===============================

# Custom monitor
mon = monitors.Monitor('ReproductionOfTemporalTasks', width=34.5, distance=57)
mon.setSizePix(DISPSIZE)

# Save the monitor
mon.save()

# Create the window
win = visual.Window(size=DISPSIZE, units='deg', fullscr=True, color=BGC, monitor=mon)

# Escape key for ending the experiment
event.globalKeys.add(key='escape', func=quit_experiment)


# ===============================
# Shapes
# ===============================

if task_type == "Temporal Reproduction":

    colors = [YELLOW, YELLOW, PURPLE, PURPLE, PURPLE, YELLOW]
    wheel = create_wheel(colors)

elif task_type == "Temporal Discrimination":

    colors = [YELLOW, PURPLE] * 3
    wheel = create_wheel(colors)

    colors_b = [PURPLE, YELLOW] * 3
    wheel_b = create_wheel(colors_b)

    correct_fb = visual.Circle(win, radius=1.25/2, pos=(0, 0), fillColor='green', lineColor='green')
    incorrect_fb = visual.Circle(win, radius=1.25/2, pos=(0, 0), fillColor='red', lineColor='red')
    
# Create circles (Fixation and two targets)
fixation = visual.Circle(win, radius=FIX_RADI, pos=(0, 0))
left_target = visual.Circle(win, radius=RADI_LEFT, pos=(-10, 0))
right_target = visual.Circle(win, radius=RADI_RIGHT, pos=(10, 0))

# Craete a list of them
circles = [fixation, left_target, right_target]


# ===============================
# Temporal Reproduction Task
# ===============================

if task_type == "Temporal Reproduction":

    # Define the trials and the experiment
    trials = data.TrialHandler(times, nReps=REPS_reproduction, method='random')

    # Define the experiment
    experiment = data.ExperimentHandler(dataFileName=f'E:\{ID}_{task_type}_{block}.csv')
    experiment.addLoop(trials)

    # Start the experiment
    for trial in trials:

        # ------- STEP 1: Fixation, confirmed by space ------- #
        display_shape(circles)
        win.flip()
        event.waitKeys(keyList=["space"])

        # ------- STEP 2: Presenting the wheel for 26.6 ms ------- #

        # Clear fixations
        display_shape(circles, stat="off")

        # Display shapes
        display_shape(wheel)
        display_shape(circles)
        win.flip()

        # Wait and clear the wheel
        core.wait(26.6/1000)
        display_shape(wheel, stat="off")
        win.flip()

        # ------- STEP 3: Wait base on the trial's time interval ------- #
        core.wait(trial/1000)
        
        # ------- STEP 4: Repeat step 2 ------- #
        display_shape(circles, stat="off")
        display_shape(wheel)
        display_shape(circles)
        win.flip()
        core.wait(26.6/1000)
        display_shape(wheel, stat="off")
        win.flip()

        # ------- STEP 5: Count the response time ------- #

        # cronometer
        response_clock = core.Clock()
        response_clock.reset()

        # Press a key to stop the cronometer
        response = event.waitKeys(keyList=["space"], timeStamped=response_clock)

        # Save the time in ms
        response_time = response[0][1] * 1000

        # Clear the screen
        display_shape(circles, stat="off")

        # ------- STEP 6: Show (response - random time) for 0.8 s ------- #

        # Calculate the time diffrnece
        diff = response_time - trial

        # Write and show it
        diff_text = visual.TextStim(win, text=f"{int(diff)}", pos=(0, 0), bold=True, autoDraw=True)
        win.flip()

        # Wait then clear the screen
        core.wait(0.8)
        diff_text.setAutoDraw(False)
        win.flip()

        # ------- STEP 7: Inter-trial interval (1.2s) ------- #

        # Display the circles again
        fixation.setAutoDraw(True)
        win.flip()

        core.wait(1200/1000)
        fixation.setAutoDraw(False)

        # ------- STEP 8: Save the data for each trial ------- #
        trials.addData('stimTime', trial)
        trials.addData('respTime', response_time)
        trials.addData('timeDiff', diff)

        # Save this trial
        experiment.nextEntry()


# ===============================
# Temporal Discrimination Task
# ===============================

elif task_type == "Temporal Discrimination":

    # Percent offsets for ts2 relative to ts1 (paper: ±[6, 12, 24, 48]%)
    percents = [-48, -24, -12, -6, 6, 12, 24, 48]

    # Every combination of ts1 (5 values) x percent (8 values) = 40 trials
    conditions = []
    for ts1 in times:
        for p in percents:
            conditions.append({'ts1': ts1, 'percent': p})

    # Define the trials and the experiment
    trials = data.TrialHandler(conditions, nReps=1, method='random')

    # Define the experiment
    experiment = data.ExperimentHandler(dataFileName=f'E:\{ID}_{task_type}_{block}.csv')
    experiment.addLoop(trials)

    for trial in trials:
    
        # ------- STEP 1: Fixation and confrimation with Space ------- #
        display_shape(circles)
        win.flip()
        event.waitKeys(keyList=["space"])

        # ------- STEP 2: Random delay------- #
        delay = 0.5 + np.random.exponential(0.25)
        core.wait(delay)

        # ------- STEP 3: First flash ------- #
        display_shape(circles, stat="off")
        display_shape(wheel)
        display_shape(circles)
        win.flip()
        core.wait(26.6 / 1000)
        display_shape(wheel, stat="off")
        win.flip()

        # ------- STEP 4: ts1 interval ------- #
        ts1 = trial["ts1"]
        core.wait(ts1 / 1000)

        # ------- STEP 5: Second flash ------- #
        display_shape(circles, stat="off")
        display_shape(wheel_b)
        display_shape(circles)
        win.flip()
        core.wait(26.6 / 1000)
        display_shape(wheel_b, stat="off")
        win.flip()

        # ------- STEP 6: ts2 interval ------- #
        ts2 = ts1 * (1 + trial['percent'] / 100)
        core.wait(ts2 / 1000)

        # ------- STEP 7: Third flash ------- #
        display_shape(circles, stat="off")
        display_shape(wheel)
        display_shape(circles)
        win.flip()
        core.wait(26.6 / 1000)
        display_shape(wheel, stat="off")
        win.flip()

        # ------- STEP 8: Response (right = ts2 longer, left = ts1 longer) ------- #
        response = event.waitKeys(keyList=["left", "right"])
        response_key = response[0]

        # Store correctness
        if ((ts2 > ts1) and (response_key == "right")) or ((ts2 < ts1) and (response_key == "left")):
           is_correct = 1
        else:
            is_correct = 0

        # Store respone interval
        if response_key == "right":
           response_interval = 2
        else:
            response_interval = 1

        # ------- STEP 9: Feedback circle for 0.8 s ------- #
        display_shape(circles, stat="off")
        if correct:
            correct_fb.setAutoDraw(True)
        else:
            incorrect_fb.setAutoDraw(True)
        win.flip()

        core.wait(0.8)

        correct_fb.setAutoDraw(False)
        incorrect_fb.setAutoDraw(False)
        win.flip()

        # ------- STEP 10: Inter-trial interval (1.2 s) ------- #
        fixation.setAutoDraw(True)
        win.flip()
        core.wait(1200 / 1000)
        fixation.setAutoDraw(False)

        # ------- STEP 11: Save the data for each trial ------- #
        trials.addData('ts1', ts1)
        trials.addData('ts2', ts2)
        trials.addData('percent', trial['percent'])
        trials.addData('respInterval', response_interval)
        trials.addData('isCorrect', is_correct)

        # Save this trial
        experiment.nextEntry()


# ===============================
# Finishing the task
# ===============================

# Save the output
experiment.saveAsWideText(experiment.dataFileName)

# Close the experiment
experiment.close()

# Close the window
core.quit()
