import database
import settings
from PIL import Image, ImageDraw
import time
import pystray
import datetime
import win32gui
import win32api
import threading
import pygetwindow
from PIL import Image
from pystray import MenuItem
from tkinter import Tk, Button, Entry, Label, Scrollbar, Listbox, Frame, Canvas
from WindowObject import WindowObject
from MainWindow import MainWindow

global mainWindow
global windowList
global maxIdleTime  # global?
global running
running = True
maxIdleTime = 2*60 

# TODO change windowName -> programName

# print('#' * 50)
# print("all active windows:")
# for s in pygetwindow.getAllTitles():
#     if len(s) >= 1:
#         print(s)
# print('#' * 50)


def getIdleTime():  # returns the time from last userinput
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0


def loadWindowList():
    global windowList
    windowList = []
    for s in database.get_all_programs():
        windowList.append(WindowObject(s))


def checkForWindowName(nameString):
    for w in windowList:
        if w.windowName.lower() == nameString.lower():
            return True
    return False


def checkListForElement(checkList, element, lower=True):
    for e in checkList:
        if lower and e.lower() == element.lower():
            return True
        elif lower == False and e == element:
            return True
    return False


def addStringToFilter(name):
    if len(name) > 1 and checkListForElement(windowList, name) == False:
        windowList.append(WindowObject(name))


def end():
    print("EXIT...")
    global running
    running = False
    try:
        icon.visible = False
        while icon.visible:
            pass
        icon.stop()
    except:
        pass
    mainWindow.stopRunning()
    quit(0)


def showMainWindow():
    try:
        global mainWindow
        mainWindow.show()
    except:
        createMainWindow()


def createMainWindow():
    global mainWindow
    mainWindow = MainWindow(windowList=windowList,
                            updateWindowList=loadWindowList,
                            exitProgram=end)
    mainWindowThread = threading.Thread(
        target=mainWindow.createMainWindow(), name="mainWindow-Thread", daemon=True)
    mainWindowThread.start()


def getForegroundWindowTitle():
    return str(win32gui.GetWindowText(win32gui.GetForegroundWindow()))


def getBackgroundWindowTitles():
    bgTitles = []
    for s in pygetwindow.getAllTitles():
        if len(s) >= 1 and bgTitles.count(s) == 0:
            bgTitles.append(s)
    return bgTitles


# MainLoop --------------------------------------------


def loop():
    icon.visible = True
    lastTime = time.time()
    global running
    while running:
        if time.time()-lastTime > 1:
            if getIdleTime() < maxIdleTime:
                for w in windowList:        # -> warning if 2 windows have 1 same FilterString 
                    counted = False
                    if w.state:
                        for fs in w.getFilterStringList():
                            # TODO: all windows...
                            # TODO -> contains or equals?
                            if getForegroundWindowTitle().count(fs) >= 1:
                                w.addSec()  # TODO: #13 filter2: program-location???
                                counted = True  
                                break
                        if w.getBgTracking() and counted == False:
                            for fs in w.getFilterStringList():
                                if counted == False:
                                    for bgt in getBackgroundWindowTitles():
                                        if bgt.count(fs) >= 1:  # TODO 1 name & 2 windows -> warning?
                                            w.addSecBgTime()
                                            counted = True  # -> add only one sec per sec per program
            lastTime += 1

# if __name__ == '__main__': # test

# ---- startup ----

maxIdleTime = settings.load_idleTime()
print("max Idle-Time:", maxIdleTime)

loadWindowList()
print('*'*50)
for w in windowList:
    print(w.getTimeString())
print('*'*50)

# for thread in threading.enumerate():
#     print(thread.name)

# Window on startup
mainWindowThread = threading.Thread(target=createMainWindow)
mainWindowThread.start()

print("~"*50)
print("all programs:", database.get_all_programs())
print("active:", database.get_all_active_programs())
print("~"*50)

# for d in database.get_all_programs_from_time():
#     database.add_program_state(d)

# print(database.get_all_active_programs())

# ----------pystray----------
# image = Image.open("threeLines.png")
width = 16
height = 16
image = Image.new('RGB', (width, height), color=(255, 255, 255))
dc = ImageDraw.Draw(image)
dc.rectangle([(0, height/5), (width, height/5*2)], fill=(120, 120, 120))
dc.rectangle([(0, height/5*3), (width, height/5*4)], fill=(120, 120, 120))
menu = (MenuItem("Show Window", showMainWindow), MenuItem("Exit", end))
# add item: stop/start tracking?
icon = pystray.Icon("ApplicationTimeTracker", image,
                    "ApplicationTimeTracker", menu)

loopThread = threading.Thread(target=loop, name="loop-Thread")
loopThread.start()

icon.run()
