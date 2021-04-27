from tkinter import Label
from tkinter import Button
import database
import datetime


class WindowObject:
    windowName = 0
    state = True
    bgTracking = False  # BackgroundTracking
    filterStrings = []
    # passedTime = 0

    def __init__(self, windowName, startTime=0):
        self.windowName = windowName
        self.state = database.get_program_state(self.windowName)
        self.bgTracking = database.get_program_bg_tracking_state(
            self.windowName)
        self.filterStrings = database.get_program_filter(self.windowName)
        # self.passedTime = startTime
        # TODO load from database-program_config
        # load bg tracking from database
        print("================>>>", self.windowName)
        if self.windowName.count("Code") >= 1:
            self.bgTracking == True
            print("---- TRUE! ----")

    def getBgTracking(self):    # TODO only for testing
        return self.bgTracking

    def setBgTracking(self, bg_tracking):    # TODO only for testing
        self.bgTracking = bg_tracking
        database.set_program_bg_tracking_state(self.windowName, bg_tracking)

    def getWindowName(self):
        return self.windowName

    def getFilterStringList(self):
        return self.filterStrings

    # def addToFilterStringList(self, filterString):
    #     if self.filterStrings.count(filterString) == 0:
    #         self.filterStrings.append(filterString)

    # def getTimeSeconds(self):
    #     return self.passedTime

    def addSec(self):
        database.add_time(
            self.windowName, datetime.datetime.now().date(), 1)
        print(self.windowName, "+1 sec")
        # print(self.getTimeString()) # do not use for better performance?

    def addSecBgTime(self):
        database.add_bg_time(
            self.windowName, datetime.datetime.now().date(), 1)
        print(self.windowName, "+1 sec")
        # print("bg-Tracking is work in progress...")
        # print(self.getTimeString()) # TODO -> bgTimeString

    # def getTime(self):
    #     hh = int(self.passedTime/60/60)
    #     mm = int(self.passedTime/60)-60*hh
    #     ss = int(self.passedTime)-60*60*hh-60*mm
    #     return [hh, mm, ss]

    def getTime(self):
        fulltime = self.getTimeSec()
        hh = int(fulltime/60/60)
        mm = int(fulltime/60)-60*hh
        ss = int(fulltime)-60*60*hh-60*mm
        return [hh, mm, ss]

    def getState(self):
        return self.state

    def setState(self, state):
        self.state = state
        database.set_program_state(self.windowName, state)

    def convertToTimeString(self, time_sec):
        hh = int(time_sec/60/60)
        mm = int(time_sec/60)-60*hh
        ss = int(time_sec)-60*60*hh-60*mm
        timeString = str(str(hh) + "h " + str(mm) + "m " + str(ss) + "s")
        return timeString

    def getTimeString(self):  # convert is better
        timeString = str("passed Time: " + str(self.getTime()[0]) +
                         "h " + str(self.getTime()[1]) + "m " + str(self.getTime()[2]) + "s")
        return timeString

    def getTimeSec(self):
        return database.get_time_by_program(self.windowName)

    def getFullTime(self):
        return database.get_time_by_program(self.windowName)+database.get_bg_time_by_program(self.windowName)

    def getConfigMenu(self, configWindow, gridRow, com):
        lableText = Label(configWindow, text=self.windowName)
        lableTime = Label(configWindow, text=self.getTimeString())
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
