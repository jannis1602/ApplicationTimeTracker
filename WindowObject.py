from tkinter import Label
from tkinter import Button
import database
import datetime


class WindowObject:
    windowName = 0
    state = 1
    passedTime = 0

    def __init__(self, windowName, startTime=0):
        self.windowName = windowName
        self.passedTime = startTime

    def getWindowName(self):
        return self.windowName

    def getTimeSeconds(self):
        return self.passedTime

    def addSec(self):
        self.passedTime += 1
        database.add_time_if_name_exists(
            self.windowName, datetime.datetime.now().date(), 1)
        print(self.getTimeString())

    # def getTime(self):
    #     hh = int(self.passedTime/60/60)
    #     mm = int(self.passedTime/60)-60*hh
    #     ss = int(self.passedTime)-60*60*hh-60*mm
    #     return [hh, mm, ss]

    def getTime(self):
        fulltime = self.getFullTime()
        hh = int(fulltime/60/60)
        mm = int(fulltime/60)-60*hh
        ss = int(fulltime)-60*60*hh-60*mm
        return [hh, mm, ss]

    def getStateString(self):
        if self.state == 1:
            return "on"
        else:
            return "off"

    def setState(self, state):
        if state == True:
            state = 1
        elif state == False:
            state = 0

    def getTimeString(self, name=True):
        timeString = str(self.windowName + " >>> Vergangene Zeit: " + str(self.getTime()[0]) +
                         "h " + str(self.getTime()[1]) + "m " + str(self.getTime()[2]) + "s")
        # timeString = str(self.windowName + " >>> Vergangene Zeit: " + str(self.getTime()[0]) +
        #                  " Stunden " + str(self.getTime()[1]) + " Minuten " + str(self.getTime()[2]) + " Sekunden")
        if name == False:
            timeString = str("Vergangene Zeit: " + str(self.getTime()[0]) +
                             "h " + str(self.getTime()[1]) + "m " + str(self.getTime()[2]) + "s")
        return timeString

    def getSaveString(self):
        return self.windowName+'#'+str(self.passedTime)

    def getFullTime(self):
        return database.get_fulltime_by_program(self.windowName)

    def getConfigMenu(self, configWindow, gridRow, com):
        lableText = Label(configWindow, text=self.windowName)
        lableTime = Label(configWindow, text=self.getTimeString(False))
        button_remove = Button(
            configWindow, text="remove", command=com)
        lableText.grid(row=gridRow, column=0)
        lableTime.grid(row=gridRow, column=1)
        button_remove.grid(row=gridRow, column=2)
        windowObjList = []
        windowObjList.append(lableText)
        windowObjList.append(lableTime)
        windowObjList.append(button_remove)
        return windowObjList
