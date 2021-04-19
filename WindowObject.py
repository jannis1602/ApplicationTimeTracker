from tkinter import Label
from tkinter import Button


class WindowObject:
    windowName = 0
    passedTime = 0

    def __init__(self, windowName, startTime):
        self.windowName = windowName
        self.passedTime = startTime


    def load(self):
        print("Loading save file...")

    def getTime(self):
        return self.passedTime

    def addSec(self):
        print(self.windowName, ">>> Vergangene Zeit:",
              self.passedTime, "Sekunden ->", int(self.passedTime/60), "Minuten ->", int(self.passedTime/60/60), "Stunden")
        self.passedTime += 1

    def getSaveString(self):
        return self.windowName+'#'+str(self.passedTime)

    def getConfigMenue(self, configWindow, gridRow, com):
        lableText = Label(configWindow, text=self.windowName)
        lableTime = Label(configWindow, text=str(
            int(self.passedTime/60))+" Minuten  "+str(int(self.passedTime % 60))+" Sekunden")  # TODO UPDATEN!!!
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
