#!/usr/bin/env python
from ankiqt import mw
from ankiqt.ui.main import AnkiQt
from anki.hooks import addHook, wrap
from threading import Timer

pluginName = 'autoReply'

def notify(str):
    print(pluginName + ': ' + str)

# configuration of plugin

secondsUntilReply = 9.0

# automatically press reply button

def pressReplyButton():
    notify('pressing reply button')
    getattr(mw.mainWin, "easeButton%d" % mw.defaultEaseButton()).click()

pressReplyButtonTimer = Timer(secondsUntilReply, pressReplyButton)

def resetTimer():
   notify('resetting timer')
   global pressReplyButtonTimer
   pressReplyButtonTimer.cancel()
   pressReplyButtonTimer = Timer(secondsUntilReply, pressReplyButton)
   pressReplyButtonTimer.start()

def stopTimer():
   notify('stopping timer')
   global pressReplyButtonTimer
   pressReplyButtonTimer.cancel()

def onPreMoveToState(self, state):
    notify('move to state')
    if state in ["showAnswer"]:
        resetTimer() 
    elif state in ["editCurrentFact", "studyScreen"]:
        stopTimer()

addHook('showQuestion', stopTimer)
addHook('deckFinished', stopTimer)
addHook('deckClosed', stopTimer)
addHook('quit', stopTimer)

AnkiQt.moveToState = wrap(AnkiQt.moveToState, onPreMoveToState, pos="before")

# register plugin

mw.registerPlugin('pluginName', 2012030802)

