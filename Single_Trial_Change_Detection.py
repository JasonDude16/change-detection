from psychopy import visual, core, event, colors
import serial
import random
import Bilateral_Positions

# 'z' key signifies no change, '/' (slash) signifies change


random.seed()  #Setting current time as seed for random number generation

# Setting up screen constants

# This is where you change settings if running on a different monitor.
# First, change the size to dimensions of current monitor in pixels.
# To find out dimensions, right click on desktop and choose "Screen Resolution."
# Then, to calibrate to current monitor, use the Monitor Center.
# Go to Tools > Monitor Center and enter a name for the current monitor.
# After saving there, in the next line of code change monitor='currentMonitorName' (must be in single quotes)

# Make sure fullscr=False. Otherwise intial dialog box will not appear. Program switches to fullscreen after
# information is entered in dialog box.
win = visual.Window(size=[1920, 1080], monitor='labMonitor', fullscr=False, units='pix', allowGUI=False)
mouse = event.Mouse()

# Preference variables

# Previous versions of this task used a 360-degree "color wheel" format
color_values = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan 
    (255, 255, 255),  # White 
    (1, 1, 1), # Black 
    (255, 128, 0)  # Orange
    ]
color_values_used = []  # Checks potential colors against this list so none are repeated
stim_size = 72  # Size in pixels of the sides of the squares.

# Making sure stimuli don't appear too close to edge of screen
x_axis_limit = int(win.size[0]/1.35)/2 - stim_size
y_axis_limit = int(win.size[1]/1.35)/2 - stim_size

fixation = visual.Circle(win, units = 'pix', radius = 6, fillColor = 'black', lineColor = 'black')
# Creating a buffer zone for the fixation point so stimuli will always appear their own length away
# from center point of the screen
fixation_buffer = visual.Circle(win, units='pix', radius = (stim_size), fillColor = None, lineColor = None)

def create_new_stimulus(chosen_pos):
    color = random.choice(color_values)
    while color in color_values_used:
        color = random.choice(color_values)
    color_values_used.append(color)
    
    stim = visual.Rect(win, units = 'pix', width = stim_size, height = stim_size, pos = chosen_pos,
        fillColor = color, lineColor = None, colorSpace = 'rgb255')

    return stim
       
def display_instructions(image_filename):
    instruction_image = visual.SimpleImageStim(win, image=image_filename)
    instruction_image.draw()
    instruction_text = """This task will flash different numbers of colored boxes scattered around the screen. Your job is to remember what color each box was.

First you'll see the dot, and then the boxes will flash very quickly, and then disappear. Next, only one box will appear on the screen.

Your job is to say whether the color of the box is the same, or different. If they were the same, then you would press the 'YES' button. If they were different, you would press the 'NO' button."""
    instruction_text = visual.TextStim(win, text=instruction_text, pos = [0, 300])
    instruction_text.draw()
    win.flip()
    core.wait(1)  # Prevents subject from clicking through instructions by accident
    # Waits for any key to continue
    event.waitKeys()
    fixation.draw()
    win.flip()

def display_end_of_block_screen(block_number):
    block_end_message_text = """You have finished block number """ + str(block_number) + """ of 3.
When you are ready, press any key to continue."""
    block_end_message = visual.TextStim(win, text=block_end_message_text, pos = [0, 100])
    block_end_message.draw()
    win.flip()    
    core.wait(3)  # Prevents subject from clicking through by accident, encourages them to take break
    # Waits for any key to continue
    event.waitKeys()
    fixation.draw()
    win.flip()

def display_end_of_experiment_screen():
    experiment_end_message_text = 'Finished! Please see the experimenter.'
    experiment_end_message = visual.TextStim(win, text=experiment_end_message_text, pos = [0, 100])
    experiment_end_message.draw()
    win.flip()
    core.wait(3)

def run_trial(trial_stim_number, is_changed, block_number, trial_number, port):
    stim_number = trial_stim_number  # This value comes in from a list generated by ExperimentHandler
    
    if block_number != 0:  # No sending codes if block is 0 because that's the practice block
        port.write(int(98).to_bytes(length = 1, byteorder = "little"))  # Sending EEG code just after user clicks to continue to this trial
    fixation_time_period = core.StaticPeriod()
    fixation_time_period.start(1)  # Making sure there's 1 second exactly between now and stim appearing
    
    # Setting up EEG codes for this trial
    stim_appear_block_code = block_number + 200
    stim_appear_trial_code = trial_number + 100
    stim_number_code = 40 + stim_number
    retention_code = 50 + stim_number
    pulse_duration = 0.1  # Time (in seconds) we will pause after sending certain trigger codes so signal goes through

    # Generating list of positions for stimuli
    if stim_number <= 2:
        pos_list = Bilateral_Positions.create_up_to_2_pos(stim_number, x_axis_limit, y_axis_limit)
    elif stim_number >= 5:
        pos_list = Bilateral_Positions.create_up_to_6_pos(stim_number, x_axis_limit, y_axis_limit)

    # Generating stimuli  
    square1 = create_new_stimulus(pos_list[0])
    square1.name = 1  # Creating a name for this stim so we can judge accuracy of choices later

    if stim_number >= 2:
        square2 = create_new_stimulus(pos_list[1])
    if stim_number >= 3:
        square3 = create_new_stimulus(pos_list[2])
    if stim_number >= 4:
        square4 = create_new_stimulus(pos_list[3])
        square5 = create_new_stimulus(pos_list[4])
    if stim_number == 6:
        square6 = create_new_stimulus(pos_list[5])

    color_values_used[:] = []  # Resetting list of color values used for next time

    # Drawing initial screen with stimuli
    fixation.setAutoDraw(True)
    square1.draw()
    if stim_number >= 2:
        square2.draw()
    if stim_number >= 3:
        square3.draw()
    if stim_number >= 4:
        square4.draw()
        square5.draw()
    if stim_number == 6:
        square6.draw()

    fixation_time_period.complete()  # Moving on once fixation period is over

    # Sending EEG codes with block and trial numbers just before stim appear
    if block_number != 0:
        port.write(stim_appear_block_code.to_bytes(length = 1, byteorder = "little"))
        core.wait(pulse_duration)  # Waiting 100ms to make sure previous code is received
        port.write(stim_appear_trial_code.to_bytes(length = 1, byteorder = "little"))
        core.wait(pulse_duration)  # Waiting 100ms to make sure previous code is received
        
    win.flip()  # Displaying fixation and stimuli
    #reaction_time_clock = core.MonotonicClock()  # Starting to measure RT
    if block_number != 0:
        port.write(stim_number_code.to_bytes(length = 1, byteorder = "little"))  # Sending EEG code with number of stim just after stim appear
    core.wait(0.25, hogCPUperiod=0.1) # Holding this screen for 250ms
    win.flip() # Displaying fixation only
    if block_number != 0:
        port.write(retention_code.to_bytes(length = 1, byteorder = "little"))  # Sending EEG code when stim disappear
    core.wait(1, hogCPUperiod=0.2) # Holding this screen for 1s retention period

    # Redrawing Stim 1
    # Color will be same or different depending on value of is_changed
    if not is_changed:
        square1.draw()
        win.flip()
        reaction_time_clock = core.MonotonicClock()  # Starting to measure RT
    else:
        previous_color = square1.fillColor
        new_color = random.choice(color_values)
        while list(new_color) == list(previous_color):
            new_color = random.choice(color_values)
        square1.fillColor = new_color
        square1.draw()
        win.flip()
        reaction_time_clock = core.MonotonicClock()  # Starting to measure RT
    if block_number != 0:
        fixation_trigger = 99
        port.write(int(99).to_bytes(length = 1, byteorder = "little"))  # Sending EEG code just after single stim appears

    # If no answer is made, accuracy and reaction_time values will remain at 0
    # choice_number will be 2
    accuracy = 0
    reaction_time = 0
    choice_number = 2

    # 'z' key signifies no change, '/' (slash) signifies change
    # Participant can also press escape key to exit experiment prematurely
    # Participant has 1500ms to answer before trial moves on
    # To change how much time they have to answer, change value of maxWait in next line
    # Time is in seconds
    key_pressed = event.waitKeys(maxWait=1.5, keyList=['escape', 'z', 'slash'])
    if key_pressed == ['escape']:
            win.close()
            core.quit()
    elif key_pressed == ['z']:
        reaction_time = reaction_time_clock.getTime()
        choice_number = 0
        if is_changed:
            accuracy = 0
        else:
            accuracy = 1
    elif key_pressed == ['slash']:
        reaction_time = reaction_time_clock.getTime()
        choice_number = 1
        if is_changed:
            accuracy = 1
        else:
            accuracy = 0

    choice_code = 10 + choice_number  # Sending code with choice of particpant
    if block_number != 0:
        port.write(choice_code.to_bytes(length = 1, byteorder = "little"))
        core.wait(pulse_duration)
        accuracy_code = 80 + accuracy
        port.write(accuracy_code.to_bytes(length = 1, byteorder = "little"))  # Sending code showing whether choice was correct or incorrect
        core.wait(pulse_duration) #need this delay otherwise the accuracy code is sent at the same time as the fixation code and doesn't show up
    win.flip()  # Displaying fixation only

    return choice_number, accuracy, reaction_time
