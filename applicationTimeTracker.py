import database
from PIL import Image, ImageDraw
import time
import pystray
import datetime
import win32gui
import win32api
import threading
import pygetwindow as gw
from PIL import Image
from pystray import MenuItem
from tkinter import Tk, Button, Entry, Label, Scrollbar, Listbox, Frame, Canvas
from WindowObject import WindowObject
from MainWindow import MainWindow

# TODO:
# - Datenbank?
# - Gui
###

# test
global mainWindow
global mainWindowThread
##

global windowList
windowList = []
global running
running = True
print('#' * 50)
print("Alle aktiven Fenster:")
for s in gw.getAllTitles():
    if len(s) >= 1:
        print(s)
print('#' * 50)
maxIdleTime = 2*60  # 120 sec -> 2 min

# -------------------
saveListDatabase = []  # savelist for database #for later


def getIdleTime():  # returns time from last userinput
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0


def loadWindowList():
    global windowList
    windowList.clear()
    for s in database.get_all_programs():
        windowList.append(WindowObject(s))


# def loadList():
#     import os.path
#     if os.path.exists(saveFile):
#         myfile = open(saveFile)
#         lines = myfile.readlines()
#         for l in lines:
#             wobj = WindowObject(l.split('#')[0], int(l.split('#')[1]))
#             windowList.append(wobj)
#         myfile.close()


def addWindowName(winName):
    if checkForWindowName(winName) == False:
        windowList.append(WindowObject(winName, 0))
# ----> SAVE


def removeWindowName(winName):
    if checkForWindowName(winName) == True:
        for w in windowList:
            if w.windowName == winName:
                windowList.remove(w)
# ----> SAVE


def checkForWindowName(nameString):
    for w in windowList:
        if w.windowName.lower() == nameString.lower():
            return True
    return False


def refresh():
    print("refresh")


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


def end():  # TODO: rename
    print("EXIT...")
    global running
    running = False
# ----> SAVE -- save save-list to database
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

# ------------------------------

# database.add_program("Visual Studio Code")
# database.add_program("Opera")

# MainLoop --------------------------------------------


def loop():
    icon.visible = True
    lastTime = time.time()
    lastTimeMin = time.time()
    global running
    while running:
        if time.time()-lastTime > 1:
            if getIdleTime() < maxIdleTime:
                for w in windowList:
                    # TODO: #12 alle fenster...
                    if str(win32gui.GetWindowText(win32gui.GetForegroundWindow())).count(w.windowName) >= 1:
                        w.addSec()  # TODO: #13 filter2: nach speicherort???
                        # if saveListDatabase.count(w.windowName) == 1:
                        # print(saveListDatabase.index(w.windowName))
                        # else:
                        #     saveListDatabase.append(w.windowName)

                        # add window with time to save-list
# ----> SAVE
            lastTime += 1
        if time.time()-lastTimeMin > 60:
            print("save minute")
            # save  save-list to database
            # save times to database
            lastTimeMin += 60


# if __name__ == '__main__': # test
print(database.get_all_programs())

for s in database.get_all_programs():
    windowList.append(WindowObject(s))

for w in windowList:
    print(w.getTimeString())
print('*'*50)

# for thread in threading.enumerate():
#     print(thread.name)

# --------------create mainWindow--------------------
# mainWindowThread = threading.Thread(target=createMainWindow)
# mainWindowThread.start()

# ----------pystray----------
# image = Image.open("threeLines.png")
width = 16
height = 16
image = Image.new('RGB', (width, height), color=(255, 255, 255))
dc = ImageDraw.Draw(image)
dc.rectangle([(0, height/5), (width, height/5*2)], fill=(120, 120, 120))
dc.rectangle([(0, height/5*3), (width, height/5*4)], fill=(120, 120, 120))
menu = (MenuItem("Show Window", showMainWindow), MenuItem("Exit", end))
icon = pystray.Icon("ApplicationTimeTracker", image,
                    "ApplicationTimeTracker", menu)

loopThread = threading.Thread(target=loop, name="loop-Thread")
loopThread.start()

icon.run()
