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
from WindowObject import WindowObject
from tkinter import Tk, Button, Entry, Label, Scrollbar, Listbox, Frame, Canvas


# TODO:
# - Datenbank?
# - Gui
###

global windowList
windowList = []
windowObjList = []
global running
running = True
blacklist = ["NVIDIA GeForce Overlay", "Program Manager",
             "Microsoft Text Input Application"]  # für später
print('#' * 50)
print("Alle aktiven Fenster:")
for s in gw.getAllTitles():
    if len(s) >= 1 and blacklist.count(s) == 0:
        print(s)
print('#' * 50)

global configWindow
global frame_configWindowList
global entry_addString
saveFile = "applicationTimeTracker/time.save"
maxIdleTime = 2*60  # 120 sec -> 2 min


def getIdleTime():  # returns time from last userinput
    return (win32api.GetTickCount() - win32api.GetLastInputInfo()) / 1000.0


def loadList():
    import os.path
    if os.path.exists(saveFile):
        myfile = open(saveFile)
        lines = myfile.readlines()
        for l in lines:
            wobj = WindowObject(l.split('#')[0], int(l.split('#')[1]))
            windowList.append(wobj)
        myfile.close()


def saveList():
    with open(saveFile, "w") as myfile:
        for w in windowList:
            myfile.write("%s\n" % w.getSaveString())
        myfile.close()


def addWindowName(winName):
    if checkForWindowName(winName) == False:
        windowList.append(WindowObject(winName, 0))
    saveList()


def removeWindowName(winName):
    if checkForWindowName(winName) == True:
        for w in windowList:
            if w.windowName == winName:
                windowList.remove(w)
    saveList()


def checkForWindowName(nameString):
    for w in windowList:
        if w.windowName.lower() == nameString.lower():
            return True
    return False


def refresh():
    print("refresh")


def reload():
    for wol in windowObjList:
        for wo in wol:
            wo.destroy()
    loadConfigStringList()


def addToFilter():
    if len(entry_addString.get()) > 1:
        print("add", entry_addString.get(), "to Filter")
        addWindowName(str(entry_addString.get()))
        loadConfigStringList()
        entry_addString.delete(0, "end")


def hideConfigWindow():
    global configWindow
    configWindow.withdraw()


def loadConfigStringList():
    for w in windowList:
        global frame_configWindowList
        windowObjList.append(w.getConfigMenu(frame_configWindowList, 2+windowList.index(w),
                             lambda: remove(w.windowName)))


def remove(wname):
    print("remove...", wname)
    removeWindowName(wname)
    reload()


def showConfigWindow():
    global configWindow
    global frame_configWindowList
    global entry_addString
    configWindow = Tk()
    configWindow.title("ApplicationTimeTracker")
    configWindow.geometry('800x400')
    frame_configWindowList = Frame(configWindow)

# MenuBar
    menuBar = Frame(configWindow)
    button_change = Button(
        menuBar, text="Aktive Anwendungen (NoFunktion)", command=refresh)
    entry_addString = Entry(menuBar, bd=2, width=40)
    button_addString = Button(
        menuBar, text="add to Filter", command=addToFilter)
    button_reload = Button(
        menuBar, text="reload", command=reload)
    button_change.grid(row=0, column=0, padx=2)
    entry_addString.grid(row=0, column=1, padx=2)
    button_addString.grid(row=0, column=2, padx=2)
    button_reload.grid(row=0, column=3, padx=2)

    loadConfigStringList()

    menuBar.grid(row=0, column=0)
    frame_configWindowList.grid(row=1, column=0)

    configWindow.protocol("WM_DELETE_WINDOW", hideConfigWindow)
    configWindow.mainloop()


def end():
    print("EXIT...")
    saveList()
    icon.stop()
    try:
        global configWindow
        configWindow.quit()
    except:
        pass
    global running
    running = False
    quit()


def configWindowThread():
    try:
        configWindow.deiconify()
    except:
        configWindowThread = threading.Thread(target=showConfigWindow)
        configWindowThread.start()


# -----------------load-----------------------
loadList()
# funktion testen
# addWindowName("Email")
# removeWindowName("Email")

# -----------------------sqlite-------------------
# print('*'*100)


# if(database.get_time_by_program_date("email", "2021-04-20") == None):
#     database.add_program("email","2021-04-20",0)
# database.add_time("email","2021-04-20",5)

# database.delete_by_name("email")
# print(database.get_times_by_program("email"))

# if(database.get_time_by_program_date("Opera", "2021-04-20") == None):
#     database.add_program("Opera","2021-04-20",0)
# print(database.get_times_by_program("Opera"))
# print(database.get_times_by_program("VScode"))
# print('*'*100)

# ------------------------------


for w in windowList:
    print(w.getTimeString())
print('*'*50)

# temp: threadList
# for thread in threading.enumerate():
#     print(thread.name)


# MainLoop ------------------------------------------------------------------
def loop():
    icon.visible = True
    lastTime = time.time()
    global running
    while running:
        if time.time()-lastTime > 1:
            if(getIdleTime() < maxIdleTime):
                for w in windowList:
                    if str(win32gui.GetWindowText(win32gui.GetForegroundWindow())).count(w.windowName) == 1:#TODO: #12 alle fenster...
                        w.addSec()
            saveList()
            lastTime += 1

# configWindowThread()

# ----------pystray----------


# image = Image.open("threeLines.png")
width = 16
height = 16
image = Image.new('RGB', (width, height), color=(255, 255, 255))
dc = ImageDraw.Draw(image)
dc.rectangle([(0, height/5), (width, height/5*2)], fill=(120, 120, 120))
dc.rectangle([(0, height/5*3), (width, height/5*4)], fill=(120, 120, 120))
menu = (MenuItem("Show Window", configWindowThread), MenuItem("Exit", end))
icon = pystray.Icon("ApplicationTimeTracker", image,
                    "ApplicationTimeTracker", menu)
# loop
loopThread = threading.Thread(target=loop)
loopThread.start()
# start trayIcon
icon.run()
