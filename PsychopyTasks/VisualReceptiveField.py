#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2022.2.5),
    on January 15, 2023, at 17:59
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019)
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195.
        https://doi.org/10.3758/s13428-018-01193-y

"""
import time

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
from screeninfo import get_monitors
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
import random as rnd
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard
import math

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
# Store info about the experiment session
psychopyVersion = '2022.2.5'
expName = 'visual_receptivefield'  # from the Builder filename that created this script
expInfo = {}
# --- Show participant info dialog --
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s' % (expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
cwd = os.getcwd()
cwd = "\\".join(cwd.split('\\')[:-1])
thisExp = data.ExperimentHandler(name=expName, version='',
                                 extraInfo=expInfo, runtimeInfo=None,
                                 originPath=f'{cwd}\\visual_receptivefield.py',
                                 savePickle=True, saveWideText=True,
                                 dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename + '.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# User Codes
monitor = get_monitors()[0]

screen_width = monitor.width
screen_height = monitor.height
shuffle_pos = True

rect_size = 120
number_of_repeats = 1

width_index = [i for i in range(math.ceil(screen_width / rect_size))]
height_index = [i for i in range(math.ceil(screen_height / rect_size))]

rect_pos = []

for w_ind in width_index:
    for h_ind in height_index:
        rect_pos.append((w_ind, h_ind))

rect_pos = rect_pos * number_of_repeats

print(rect_pos)

if shuffle_pos:
    rnd.shuffle(rect_pos)


# --- Setup the Window ---
win = visual.Window(
    size=[screen_width, screen_height], fullscr=True, screen=0,
    winType='pyglet', allowStencil=False,
    monitor='testMonitor', color=[-1, -1, -1], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')
win.mouseVisible = False
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess
# --- Setup input devices ---
ioConfig = {}

# Setup iohub keyboard
ioConfig['Keyboard'] = dict(use_keymap='psychopy')

ioSession = '1'
if 'session' in expInfo:
    ioSession = str(expInfo['session'])
ioServer = io.launchHubServer(window=win, **ioConfig)
eyetracker = None

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard(backend='iohub')

# --- Initialize components for Routine "black_wait" ---
start_black = visual.Rect(
    win=win, name='start_black',
    width=(1, 1)[0], height=(1, 1)[1],
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0, colorSpace='rgb', lineColor='black', fillColor='black',
    opacity=None, depth=0.0, interpolate=True)

# --- Initialize components for Routine "trial" ---
photo_diod_rect = visual.Rect(
    win=win, name='photo_diod_rect', units='pix',
    width=(60, 60)[0], height=(60, 60)[1],
    ori=0.0, pos=(960, -540), anchor='bottom-right',
    lineWidth=1.0, colorSpace='rgb', lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)
black_screen = visual.Rect(
    win=win, name='black_screen',
    width=(1.0, 1.0)[0], height=(1.0, 1.0)[1],
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0, colorSpace='rgb', lineColor=[-1.0000, -1.0000, -1.0000], fillColor=[-1.0000, -1.0000, -1.0000],
    opacity=None, depth=-1.0, interpolate=True)
stimulus = visual.Rect(
    win=win, name='stimulus',
    units='pix',
    width=rect_size, height=rect_size,
    ori=0.0, pos=(0, 0), anchor='center',
    lineWidth=1.0, colorSpace='rgb', lineColor='white', fillColor='white',
    opacity=None, depth=0.0, interpolate=True)

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.Clock()  # to track time remaining of each (possibly non-slip) routine

# --- Prepare to start Routine "black_wait" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
black_waitComponents = [start_black]
for thisComponent in black_waitComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "black_wait" ---
while continueRoutine and routineTimer.getTime() < 20.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *start_black* updates
    if start_black.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        start_black.frameNStart = frameN  # exact frame index
        start_black.tStart = t  # local t and not account for scr refresh
        start_black.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_black, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'start_black.started')
        start_black.setAutoDraw(True)
    if start_black.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > start_black.tStartRefresh + 1.0 - frameTolerance:
            # keep track of stop time/frame for later
            start_black.tStop = t  # not accounting for scr refresh
            start_black.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_black.stopped')
            start_black.setAutoDraw(False)

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in black_waitComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "black_wait" ---
for thisComponent in black_waitComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-1.000000)

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=len(rect_pos), method='random',
                           extraInfo=expInfo, originPath=-1,
                           trialList=[None],
                           seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial:
        exec('{} = thisTrial[paramName]'.format(paramName))

for trial_index, thisTrial in enumerate(trials):

    x = ((rect_pos[trial_index][0] * rect_size) + (screen_width // 2 * -1)) + rect_size // 2
    y = ((rect_pos[trial_index][1] * rect_size) + (screen_height // 2 * -1)) + rect_size // 2

    stimulus.pos = (x, y)

    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            exec('{} = thisTrial[paramName]'.format(paramName))

    # --- Prepare to start Routine "trial" ---
    continueRoutine = True
    routineForceEnded = False
    # update component parameters for each repeat
    # keep track of which components have finished
    trialComponents = [photo_diod_rect, black_screen, stimulus]
    for thisComponent in trialComponents:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1

    # --- Run Routine "trial" ---
    while continueRoutine and routineTimer.getTime() < 0.4:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *photo_diod_rect* updates
        if photo_diod_rect.status == NOT_STARTED and tThisFlip >= 0.000 - frameTolerance:
            # keep track of start time/frame for later
            photo_diod_rect.frameNStart = frameN  # exact frame index
            photo_diod_rect.tStart = t  # local t and not account for scr refresh
            photo_diod_rect.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(photo_diod_rect, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'photo_diod_rect.started')
            photo_diod_rect.setAutoDraw(True)
        if photo_diod_rect.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > photo_diod_rect.tStartRefresh + 0.20 - frameTolerance:
                # keep track of stop time/frame for later
                photo_diod_rect.tStop = t  # not accounting for scr refresh
                photo_diod_rect.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'photo_diod_rect.stopped')
                photo_diod_rect.setAutoDraw(False)

        # *black_screen* updates
        if black_screen.status == NOT_STARTED and tThisFlip >= 0.20 - frameTolerance:
            # keep track of start time/frame for later
            black_screen.frameNStart = frameN  # exact frame index
            black_screen.tStart = t  # local t and not account for scr refresh
            black_screen.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(black_screen, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'black_screen.started')
            black_screen.setAutoDraw(True)
        if black_screen.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > black_screen.tStartRefresh + 0.380 - frameTolerance:
                # keep track of stop time/frame for later
                black_screen.tStop = t  # not accounting for scr refresh
                black_screen.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'black_screen.stopped')
                black_screen.setAutoDraw(False)

        # *stimulus* updates
        if stimulus.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
            # keep track of start time/frame for later
            stimulus.frameNStart = frameN  # exact frame index
            stimulus.tStart = t  # local t and not account for scr refresh
            stimulus.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(stimulus, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'stimulus.started')
            stimulus.setAutoDraw(True)
        if stimulus.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > stimulus.tStartRefresh + 0.20 - frameTolerance:
                # keep track of stop time/frame for later
                stimulus.tStop = t  # not accounting for scr refresh
                stimulus.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'stimulus.stopped')
                stimulus.setAutoDraw(False)

        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # --- Ending Routine "trial" ---
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if routineForceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-0.400000)
    thisExp.nextEntry()

# completed 20.0 repeats of 'trials'


# --- Prepare to start Routine "black_wait" ---
continueRoutine = True
routineForceEnded = False
# update component parameters for each repeat
# keep track of which components have finished
black_waitComponents = [start_black]
for thisComponent in black_waitComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
frameN = -1

# --- Run Routine "black_wait" ---
while continueRoutine and routineTimer.getTime() < 1.0:
    # get current time
    t = routineTimer.getTime()
    tThisFlip = win.getFutureFlipTime(clock=routineTimer)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame

    # *start_black* updates
    if start_black.status == NOT_STARTED and tThisFlip >= 0.0 - frameTolerance:
        # keep track of start time/frame for later
        start_black.frameNStart = frameN  # exact frame index
        start_black.tStart = t  # local t and not account for scr refresh
        start_black.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(start_black, 'tStartRefresh')  # time at next scr refresh
        # add timestamp to datafile
        thisExp.timestampOnFlip(win, 'start_black.started')
        start_black.setAutoDraw(True)
    if start_black.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > start_black.tStartRefresh + 1.0 - frameTolerance:
            # keep track of stop time/frame for later
            start_black.tStop = t  # not accounting for scr refresh
            start_black.frameNStop = frameN  # exact frame index
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_black.stopped')
            start_black.setAutoDraw(False)

    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()

    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineForceEnded = True
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in black_waitComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished

    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# --- Ending Routine "black_wait" ---
for thisComponent in black_waitComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
# using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
if routineForceEnded:
    routineTimer.reset()
else:
    routineTimer.addTime(-1.000000)

# --- End experiment ---
# Flip one final time so any remaining win.callOnFlip()
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename + '.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
if eyetracker:
    eyetracker.setConnectionState(False)
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
