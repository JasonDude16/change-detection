# ------------------------------------------------------------------------
#  Change detection task.
#
#  Rachel Klein, January 2016

from psychopy import visual, data, core, gui
from random import random
import Single_Trial_Change_Detection
import serial
import os

title = "Change_Detection"
date = data.getDateStr()

# Making the mouse show up at the beginning
Single_Trial_Change_Detection.mouse.setVisible(1)

# Create a data folder to save files to
dataFolder = os.getcwd() + os.sep + 'data' + os.sep
if not os.path.exists(dataFolder): 
    os.makedirs(dataFolder)

# Initial dialog box to collect info on study participant and year
study_info = {'Participant_ID':0}
study_info_dialog = gui.DlgFromDict(dictionary=study_info, title='Change Detection')
if study_info_dialog.OK:
    output_file_name = dataFolder + 'change_detection_' + str(study_info['Participant_ID'])
else:
    core.quit()  # If you click "cancel" instead of "OK", closes program

IDfolder = dataFolder + os.sep + 'ID_' + str(study_info['Participant_ID'])
if not os.path.exists(IDfolder):
    os.makedirs(IDfolder)

dataFileName = IDfolder + os.sep + u'%s_%s_%s' % (study_info['Participant_ID'], title, date)

# Creating structure of whole experiment
exp = data.ExperimentHandler(name='change_detection',
                version='0.1',
                extraInfo={'Participant_ID':study_info['Participant_ID']},
                runtimeInfo=None,
                originPath=None,
                saveWideText=True,
                dataFileName=dataFileName)

# Making fullscreen for performance
Single_Trial_Change_Detection.win.winHandle.minimize()
Single_Trial_Change_Detection.win.fullscr = True
Single_Trial_Change_Detection.mouse.setVisible(0)  # Mouse is invisible during trials
Single_Trial_Change_Detection.win.winHandle.set_mouse_position(0,0)
Single_Trial_Change_Detection.win.winHandle.maximize()
Single_Trial_Change_Detection.win.winHandle.activate()
Single_Trial_Change_Detection.win.flip()

# Setting up serial port
# Make sure the value below is correct for our computers - may be D010 or 037F or 0278
# port = serial.Serial('COM4')

# Loading external file of practice conditions (must be in same directory)
# If you want different numbers of stimuli to appear you will need to change the possiblities in this file
practice_conditions = data.importConditions('cd_practice_conditions.csv')
practice = data.TrialHandler(trialList=practice_conditions, nReps=1,name='practice',
                 method='sequential')
practice.data.addDataType('choice')
practice.data.addDataType('accuracy')
practice.data.addDataType('rt')

exp.addLoop(practice)

# Showing instructions before practice
image_list = ['imgs/instruct.png', 'imgs/fix1.png', 'imgs/stim1.png', 'imgs/fix2.png', 'imgs/resp1.png',
              'imgs/fix3.png', 'imgs/stim2.png', 'imgs/fix4.png', 'imgs/resp2.png']
                            
for image in image_list:
    Single_Trial_Change_Detection.display_instructions(image)
    
Single_Trial_Change_Detection.display_text_instructions(instructions_text = 'Now it\'s time to practice')

# Running practice trials
# block_number is 0 for practice trials currently - starts at 1 for real trials
# (This shows up later in EEG code values.)
block_number = 0
for trial in practice:
    trial_data = Single_Trial_Change_Detection.run_trial(int(trial['number_of_stim']), int(trial['change']), block_number, practice.thisTrialN+1)
    practice.addData('choice', trial_data[0])
    practice.addData('accuracy', trial_data[1]) 
    practice.addData('rt', trial_data[2])
    exp.nextEntry()
    
# Showing instructions after practice
Single_Trial_Change_Detection.fixation.setAutoDraw(False)
Single_Trial_Change_Detection.display_instructions('Instructions_CD.png')
Single_Trial_Change_Detection.fixation.setAutoDraw(True)

# Creating block structure

block_loop=data.TrialHandler(trialList=[], nReps=3,name='block_loop',
                 method='sequential')
exp.addLoop(block_loop)

# Creating trial structure for each block

block_number = 1  # Keep track of what block we're on so we can inform the user
for thisRep in block_loop:
    
    # Loading external file of trial conditions (must be in same directory)
    # If you want different numbers of stimuli to appear you will need to change the possiblities in this file
    trial_conditions = data.importConditions('cd_trial_conditions.csv')
    
    # nReps (below) sets how many repetitions of the list of trial conditions you want per block.
    # Currently 5 repetitions * 3 possible number_of_stim values * 2 for change/no change = 30 trials per block
    trials = data.TrialHandler(trialList=trial_conditions, nReps=5, method='fullRandom', extraInfo={'Participant_ID':0,'year':0})
    trials.data.addDataType('choice')
    trials.data.addDataType('accuracy')
    trials.data.addDataType('rt')

    exp.addLoop(trials)
    
    # Running trials
    for trial in trials:
        trial_data = Single_Trial_Change_Detection.run_trial(int(trial['number_of_stim']), int(trial['change']), block_number, trials.thisN+1)
        trials.addData('choice', trial_data[0])
        trials.addData('accuracy', trial_data[1])
        trials.addData('rt', trial_data[2])
        exp.nextEntry()
    
    if block_number < 3:
        Single_Trial_Change_Detection.display_end_of_block_screen(block_number)
        block_number += 1
    else:
        Single_Trial_Change_Detection.display_end_of_experiment_screen()
       
# Data automatically gets saved by ExperimentHandler when we quit or when all blocks are done 
