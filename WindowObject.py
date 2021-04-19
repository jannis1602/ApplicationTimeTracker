from tkinter import Label
from tkinter import Button


class WindowObject:
    windowName = 0
    passedTime = 0

    def __init__(self, windowName, startTime):
        self.windowName = windowName
        self.passedTime = startTime

    def getTimeSeconds(self):
        return self.passedTime

    def addSec(self):
        self.passedTime += 1
        print(self.getTimeString())
        # print(self.windowName, ">>> Vergangene Zeit:",
        #       self.passedTime, "Sekunden ->", int(self.passedTime/60), "Minuten ->", int(self.passedTime/60/60), "Stunden")

    def getTime(self):
        hh = int(self.passedTime/60/60)
        mm = int(self.passedTime/60)-60*hh
        ss = int(self.passedTime)-60*60*hh-60*mm
        return [hh, mm, ss]

    def getTimeString(self, formart=0):
        # hh = int(self.passedTime/60/60)
        # mm = int(self.passedTime/60)-60*hh
        # ss = int(self.passedTime)-60*60*hh-60*mm

        timeString = str(self.windowName + " >>> Vergangene Zeit: " + str(self.getTime()[0]) +
                         " Stunden " + str(self.getTime()[1]) + " Minuten " + str(self.getTime()[2]) + " Sekunden")
        if formart == 1:
            timeString = str("Vergangene Zeit: " + str(self.getTime()[0]) +
                             " Stunden " + str(self.getTime()[1]) + " Minuten " + str(self.getTime()[2]) + " Sekunden")

        return timeString

    def getSaveString(self):
        return self.windowName+'#'+str(self.passedTime)

    def getConfigMenu(self, configWindow, gridRow, com):
        lableText = Label(configWindow, text=self.windowName)
        lableTime = Label(configWindow, text=self.getTimeString(1))
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
