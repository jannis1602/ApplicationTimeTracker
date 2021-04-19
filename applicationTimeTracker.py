from PIL import Image, ImageDraw
import sys
import time
import pystray
import threading
import pygetwindow as gw
import win32gui as wingui
from PIL import Image
from pystray import MenuItem
from WindowObject import WindowObject
from tkinter import Tk
from tkinter import Button
from tkinter import Entry
from tkinter import Label
from tkinter import Scrollbar
from tkinter import Listbox
from tkinter import Frame
from tkinter import Canvas


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
# tracking list - strings als Filter
# fensterNamen = ["Visual Studio Code", "Opera", "Discord",
#                 "OneNote"]  # wird eigentlich nicht gebraucht!

# configWindow
global configWindow
global frame_configWindowList
global entry_addString
# configWindow.title("ApplicationTimeTracker")


def loadList():
    import os.path
    if os.path.exists('save.save'):
        myfile = open('save.save')
        lines = myfile.readlines()
        for l in lines:
            wobj = WindowObject(l.split('#')[0], int(l.split('#')[1]))
            windowList.append(wobj)
        myfile.close()


def saveList():
    with open('save.save', "w") as myfile:
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


def closeConfigWindow():
    global configWindow
    configWindow.quit()
    # global configWindow
    # configWindow.destroy()


def loadConfigStringList():
    for w in windowList:
        global frame_configWindowList
        windowObjList.append(w.getConfigMenue(frame_configWindowList, 2+windowList.index(w),
                             lambda: remove(w.windowName))) 


def remove(wname):
    print("remove...", wname)
    removeWindowName(wname)
    reload()


def showConfigWindow():
    print("show window...")
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

    configWindow.protocol("WM_DELETE_WINDOW", closeConfigWindow)
    configWindow.mainloop()


def end():
    print("EXIT...")
    saveList()
    icon.visible = False
    icon.stop()
    configWindow.quit()
    global running
    running = False
    sys.exit()


def configWindowThread():  # nur Temp! -> #TODO change visibility
    configWindowThread = threading.Thread(target=showConfigWindow)
    configWindowThread.start()
    # global configWindow
    # configWindow.focus()  #TODO !!!

# -----------------load-----------------------
loadList()
# funktion testen
# addWindowName("Email")
# removeWindowName("Email")


for window in windowList:
    print(window.windowName, "Vergangene Zeit:",
          int(window.getTime()/60), "Minuten")
print('*'*50)

# ----------------start-------------------

# image = Image.open("threeLines.png")
width = 16
height = 16
image = Image.new('RGB', (width, height), color=(255, 255, 255))
dc = ImageDraw.Draw(image)
dc.rectangle([(0, height/5), (width, height/5*2)], fill=(120, 120, 120))
dc.rectangle([(0, height/5*3), (width, height/5*4)], fill=(120, 120, 120))
menu = (MenuItem("Show Window", configWindowThread), MenuItem("Exit", end))
icon = pystray.Icon("", image, "WindowTimeTracker", menu)


def loop():  # MainLoop ------------------------------------------------------------------
    # addWindowName("testName")
    icon.visible = True
    lastTime = time.time()
    global running
    while running:
        if time.time()-lastTime > 1:
            for w in windowList:
                if str(wingui.GetWindowText(wingui.GetForegroundWindow())).count(w.windowName) == 1:
                    w.addSec()
            saveList()
            lastTime += 1


# configWindowThread()

# configWindowThread = threading.Thread(target=showConfigWindow)
# configWindowThread.start()

loopThread = threading.Thread(target=loop)
loopThread.start()

icon.run()
