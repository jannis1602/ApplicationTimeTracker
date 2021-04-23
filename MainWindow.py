import tkinter as tk
from tkinter import Label, Button, Frame, Canvas, Scrollbar, Entry, Text, Toplevel
from WindowObject import WindowObject
import database
import pygetwindow as gw
import tkinter.messagebox


# TODO edit-button for name...

class MainWindow(tk.Tk):

    def __init__(self, windowList, updateWindowList, exitProgram):
        self.windowList = windowList
        tk.Tk.__init__(self)
        self.title("ApplicationTimeTracker")
        self.geometry('800x400')
# TODO icon
        self.resizable(False, False)
        self.running = True
        self.updateWindowList = updateWindowList
        self.exitProgram = exitProgram

        # self.subWindows=[] #TODO immer nur ein window pro art

    def createMainWindow(self):
        menu_bar_frame = Frame(
            master=self, height=20, width=640, bg="gray")
        menu_bar_frame.pack(side='top', padx=2,
                            pady=2, fill="x", expand=False)

    # ShowNames-Button
        show_names_button = Button(
            master=menu_bar_frame, text="show all names", command=self.windowNamesWindow)  # TODO: #21 @superxyxy add end methode
        show_names_button.pack(side='left', padx='5', pady='5', expand=False)
    # String-Entry
        self.string_entry = Entry(
            menu_bar_frame, bd=2, width=40, bg="lightgray")
        self.string_entry.pack(side='left', padx='5', pady='5', expand=False)
    # Add-Button
        addfilter_button = Button(
            master=menu_bar_frame, text="Add to Filter", command=self.addStringToFilter)
        addfilter_button.pack(side='left', padx='5', pady='5', expand=False)
    # reload-Button
        reload_button = Button(
            master=menu_bar_frame, text="reload", command=self.reload)
        reload_button.pack(side='left', padx='5', pady='5', expand=False)
    # Exit-Button
        exit_button = Button(
            master=menu_bar_frame, text="EXIT", command=self.exitProgram)  # TODO: #21 @superxyxy add end methode
        exit_button.pack(side='right', padx='5', pady='5', expand=False)
    # Settings-Button
        settings_button = Button(
            master=menu_bar_frame, text="Settings", command=self.action)  # TODO: #21 @superxyxy add end methode
        settings_button.pack(side='right', padx='5', pady='5', expand=False)

        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.createListFrame()
        self.after(1, lambda: self.focus_force())

        # self.mainloop()  # is blocking
        while self.running:
            self.update()
        self.destroy()

    def windowNamesWindow(self):  # TODO change to windowNames_Window + andere
        root = tk.Tk()
        S = Scrollbar(root)
        T = Text(root, height=20, width=80)
        S.pack(side="right", fill="y")
        T.pack(side="left", fill="y")
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        text = ""
        for s in gw.getAllTitles():
            if len(s) >= 1:
                text += s+"\n"
        T.insert(tk.END, text)
        T.config(state=tk.DISABLED)
        root.mainloop()

    def addStringToFilter(self):
        name = self.string_entry.get()
        print(name)
        if len(name) > 1 and self.checkForWindowName(name) == False:
            print("add", name, "to Filter")
            self.windowList.append(WindowObject(name))
            self.string_entry.delete(0, "end")
            self.reload()
            # ---- test ----
            database.add_program_state(name)
            # database.add_program(name)
            self.updateWindowList()

    def checkForWindowName(self, nameString):
        for w in self.windowList:
            if w.windowName.lower() == nameString.lower():
                return True
        return False

    def stopRunning(self):
        print("quit MainWindow...")
        self.running = False

    def show(self):
        self.deiconify()

    def hide(self):
        self.withdraw()
# TODO close all open windows

    def createListFrame(self):
        self.list_frame = Frame(master=self)
        self.list_frame.pack(side='left', padx=0,
                             pady=0, fill="both", expand=True)

        canvas = Canvas(self.list_frame, bg="gray")
        scroll_y = Scrollbar(self.list_frame, orient="vertical",
                             command=canvas.yview)
        scroll_frame = Frame(canvas, bg="gray")
        void_label = Label(master=scroll_frame,
                           text=" "*255, bg="gray")
        void_label.pack(padx=2, pady=2, side="bottom")

        for e in self.windowList:
            self.createWindowFrame(scroll_frame, windowObject=e)

        canvas.create_window(0, 0, anchor='nw', window=scroll_frame)
        canvas.update_idletasks()
        scroll_frame.update()
        canvas.configure(scrollregion=canvas.bbox('all'),  # scrollregion=canvas.bbox('all') #TODO: #20 scrollregion
                         yscrollcommand=scroll_y.set)
        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')

    def remove(self, windowObject):
        # delete-request
        result = tkinter.messagebox.askquestion(
            "Delete", "Sure?", icon='warning')
        if result == 'yes':
            pass
        else:
            return
        try:  # TODO: verbessern!!!
            self.windowList.remove(windowObject)
        except:
            print("deleted by name")
            for w in self.windowList:
                if w.getWindowName() == windowObject.getWindowName():
                    self.windowList.remove(w)

        self.list_frame.destroy()
        self.createListFrame()
        # ---- test ----
        database.delete_by_name(windowObject.getWindowName())
        self.updateWindowList()

    def reload(self):
        self.list_frame.destroy()
        self.createListFrame()

    def add(self, windowObject):
        self.windowList.append(windowObject)
        self.list_frame.destroy()
        self.createListFrame()

    # TODO WindowObject... # TODO rename methode
    def createWindowFrame(self, master, windowObject):
        # TODO rename temp_frame
        temp_frame = Frame(
            master=master, height=20, width=200, bg="darkgray")
        temp_frame.pack(side='bottom', padx=5,
                        pady=1, fill="x", expand=False)
        name_label = Label(master=temp_frame,
                           text=windowObject.getWindowName(), anchor='w', width=20, bg="gray")
        name_label.pack(padx=2, pady=2, side="left")

        # TODO #23 getfont length of string

        if len(windowObject.getWindowName()) > 12:  # nur wenn string zu lang?
            CreateToolTip(name_label, text=windowObject.getWindowName())

        # TODO multiple lables for better formatting
        time_label = Label(master=temp_frame,
                           text=windowObject.getTimeString(name=False), width=64, bg="gray")
        time_label.pack(padx=2, pady=2, side="left")
        # TODO add/edit filterStrings
        # -> new tkinter with Text(new line = new filterString)

        remove_button = Button(temp_frame, text="remove",
                               bg="darkgray", command=lambda: self.remove(windowObject))
        remove_button.pack(padx=2, pady=2, side="right", fill="x")
    # On/Off button
        onoff_button = Button(temp_frame, text=windowObject.getStateString(),
                              bg="darkgray", command=lambda: self.switchState(onoff_button, windowObject))       # => change state in database
        onoff_button.pack(padx=2, pady=2, side="right", fill="x")
    # statistics-Button
        statistics_button = Button(
            master=temp_frame, text="statistics", bg="darkgray", command=lambda: self.viewStats_Window(windowObject.getWindowName()))
        statistics_button.pack(padx=2, pady=2, side="right", fill="x")

    def switchState(self, button, windowObject):
        if windowObject.state == True:
            button.configure(text="on")
            windowObject.setState(False)
        elif windowObject.state == False:
            button.configure(text="off")
            windowObject.setState(True)
        self.updateWindowList()
        # -> update list in apptt...

    def viewStats_Window(self, programName):
        root = tk.Tk()
        S = Scrollbar(root)
        T = Text(root, height=20, width=80, bg="#4a4a4a")
        S.pack(side="right", fill="y")
        T.pack(side="left", fill="y")
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)

        # ---- stats to text ----
        text = ""
        for d in database.get_times_by_program(programName):
            text += str(d[1])+" - "+self.convertToTimeString(d[2])+"\n"

        # print(database.get_times_by_program(programName))

        T.insert(tk.END, text)
        T.config(state=tk.DISABLED)
        root.mainloop()

    def convertToTimeString(self, time):
        hh = int(time/60/60)
        mm = int(time/60)-60*hh
        ss = int(time)-60*60*hh-60*mm
        timeString = str(str(hh) +
                         " Stunden " + str(mm) + " Minuten " + str(ss) + " Sekunden")
        return timeString

    def editFilterStrings(self):
        root = tk.Tk()
        S = Scrollbar(root)
        T = Text(root, height=20, width=80)
        S.pack(side="right", fill="y")
        T.pack(side="left", fill="y")
        S.config(command=T.yview)
        T.config(yscrollcommand=S.set)
        text = ""
        for s in gw.getAllTitles():
            if len(s) >= 1:
                text += s+"\n"
        T.insert(tk.END, text)
        # T.config(state=tk.DISABLED)
        root.mainloop()

    def action(self):
        print("action")

        # self.label = Label(root, text="GUI")
        # self.label.pack()

        # self.greet_button = Button(root, text="Greet", command=self.greet)
        # self.greet_button.pack()

        # self.close_button = Button(root, text="Close", command=root.quit)
        # self.close_button.pack()

# if __name__ == '__main__': # test
#     windowList = []
#     for i in range(20):
#         windowList.append(WindowObject("test"+str(i)))
    # windowList.append(WindowObject("Opera"))
    # windowList.append(WindowObject("Visual Studio Code"))
    # MainWindow(windowList)


# ----------- ToolTip -----------
# TODO extra file

class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify="left",
                      background="gray", relief="solid", borderwidth=1,
                      font=("roboto", "10", "normal"))
        label.pack(ipadx=1)
        cx = cx

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
