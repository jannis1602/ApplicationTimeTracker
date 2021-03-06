import tkinter as tk
from tkinter import Label, Button, Frame, Canvas, Scrollbar, Entry, Text, Toplevel
from WindowObject import WindowObject
import database
import settings
import pygetwindow as gw
import tkinter.messagebox
import time

# tkinter.messagebox.showwarning("Warning", "work in progress", icon='warning')


class MainWindow(tk.Tk):

    def __init__(self, windowList, updateWindowList, exitProgram):
        self.windowList = windowList
        tk.Tk.__init__(self)
        self.title("ApplicationTimeTracker")
        pos = settings.load_windowPosition()
        self.geometry('%dx%d+%d+%d' % (800, 400, pos[0], pos[1]))
        # self.geometry('800x400)
# TODO icon
        self.resizable(False, False)
        self.running = True
        self.updateWindowList = updateWindowList
        self.exitProgram = exitProgram

        # self.subWindows = [] # unused
        # init all subwindows:
        self.settings_Window = None
        self.allWindowNames_Window = None
        self.stats_Window = None
        self.edit_Window = None

    def createMainWindow(self):
        menu_bar_frame = Frame(
            master=self, height=20, width=640, bg="gray")
        menu_bar_frame.pack(side='top', padx=2,
                            pady=2, fill="x", expand=False)

    # ShowNames-Button
        show_names_button = Button(
            master=menu_bar_frame, text="show all titles", command=self.showAllWindowTitles)
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
            master=menu_bar_frame, text="EXIT", command=self.exitProgram)
        exit_button.pack(side='right', padx='5', pady='5', expand=False)
    # Settings-Button
        settings_button = Button(
            master=menu_bar_frame, text="Settings", command=self.showSettings)
        settings_button.pack(side='right', padx='5', pady='5', expand=False)

        self.protocol("WM_DELETE_WINDOW", self.hide)
        self.createListFrame()
        self.after(1, lambda: self.focus_force())

        # self.mainloop()  # is blocking
        while self.running:
            self.update()
        self.destroy()

    def showSettings(self):
        try:
            self.settings_Window.lift(self)
# TODO focus ...
        except:
            self.settings_Window = tk.Tk()
            self.settings_Window.title("ApplicationTimeTracker - settings")
            self.settings_Window.geometry('200x200')

            options = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]
            variable = tk.StringVar(self.settings_Window)
            variable.set(settings.load_idleTime())

            labelTest = tk.Label(
                self.settings_Window, text="max seconds of idle-time:", font=('roboto', 10))
            labelTest.pack(side="top")

        # TODO Dropdown-Menu -> change to textbox
            opt = tk.OptionMenu(self.settings_Window, variable, *options)
            opt.config(width=200, font=('roboto', 12))
            opt.pack(side="top")

            def callback(*args):
                print(variable.get())
                settings.set_idleTime(int(variable.get()))
            variable.trace("w", callback)
            # self.settings_Window.protocol("WM_DELETE_WINDOW", command=close)
            self.settings_Window.mainloop()

    # TODO rename names -> titles
    def showAllWindowTitles(self):
        # TODO linewrap!!!
        # TODO lable + add-button in frame -> in scrollbar
        try:
            self.allWindowNames_Window.lift(self)
        except:
            self.allWindowNames_Window = tk.Tk()
            self.allWindowNames_Window.title(
                "ApplicationTimeTracker - all window titles")
            S = Scrollbar(self.allWindowNames_Window)
            T = Text(self.allWindowNames_Window, height=20, width=80,bg="lightgray")
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
            self.allWindowNames_Window.mainloop()

    def addStringToFilter(self):
        name = self.string_entry.get()
        print(name)
        if len(name) > 1 and self.checkForWindowName(name) == False:
            print("add", name, "to Filter")
            database.add_program_state(name)
            self.windowList.append(WindowObject(name))
            self.string_entry.delete(0, "end")
            self.reload()
            # ---- test ----
            # database.add_program(name)
            self.updateWindowList()

    def checkForWindowName(self, nameString):
        for w in self.windowList:
            if w.windowName.lower() == nameString.lower():
                return True
        return False

    def stopRunning(self):
        print("quit MainWindow...")
        settings.set_windowPosition(self.winfo_x(), self.winfo_y())
        self.running = False

    def show(self):
        self.deiconify()

    def hide(self):
        settings.set_windowPosition(self.winfo_x(), self.winfo_y())
        self.withdraw()

    # TODO destroy if window exists...
        # self.settings_Window.destroy()
        # self.allWindowNames_Window.destroy()

# TODO close all open windows

    def createListFrame(self):  # TODO rename
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

    def remove(self, windowObject):  # TODO rename -> delete!!!
        # delete-request
        result = tkinter.messagebox.askquestion(
            "Delete", "all data of " + windowObject.getWindowName() + " will be deleted!", icon='warning')
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
        database.delete_program_state(windowObject.getWindowName())
        database.delete_program_time_by_name(windowObject.getWindowName())
        database.delete_all_program_filter(windowObject.getWindowName())
        self.updateWindowList()

    def reload(self):
        self.list_frame.destroy()
        self.createListFrame()

    def add(self, windowObject):
        self.windowList.append(windowObject)
        self.list_frame.destroy()
        self.createListFrame()

    # TODO WindowObject... # TODO rename methode -> windowObject
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
                           text="passed Time: "+self.convertToTimeString(windowObject.getTimeSec()), width=62, bg="gray")
# TODO  if not 0: -> +"  ---  Background Time: "+self.convertToTimeString(windowObject.getFullTime())
        if windowObject.getBgTimeSec() > 0:
            time_label.config(text="passed Time: "+self.convertToTimeString(windowObject.getTimeSec()) +
                              "  ---  Background Time: "+self.convertToTimeString(windowObject.getBgTimeSec()))

        time_label.pack(padx=2, pady=2, side="left")
    # remove-Button
        remove_button = Button(temp_frame, text="remove",
                               bg="darkgray", command=lambda: self.remove(windowObject))
        remove_button.pack(padx=2, pady=2, side="right", fill="x")
    # state-Button
        state_button = Button(temp_frame, text="off",
                              bg="darkgray", command=lambda: self.switchState(state_button, windowObject))       # => change state in database
        state_button.pack(padx=2, pady=2, side="right", fill="x")
        if windowObject.getState():
            state_button.configure(text="on")

    # statistics-Button
        statistics_button = Button(
            master=temp_frame, text="statistics", bg="darkgray", command=lambda: self.viewStats_Window(windowObject.getWindowName()))
        statistics_button.pack(padx=2, pady=2, side="right", fill="x")
    # edit-Button
        edit_button = Button(
            master=temp_frame, text="edit", bg="darkgray", command=lambda: self.editFilterStrings_Window(windowObject))  # command=lambda: self.edit_Window(windowObject))
        edit_button.pack(padx=2, pady=2, side="right", fill="x")


# TODO save edit to database...
# TODO add one line for each title


    def editFilterStrings_Window(self, windowObject):  # TODO Reset?
        try:
            self.stats_Window.lift(self)
        except:
            self.edit_Window = tk.Tk()
            self.edit_Window.title("ApplicationTimeTracker - editing: " +
                                   windowObject.getWindowName())
            frame = Frame(
                master=self.edit_Window, height=20, width=200, bg="darkgray")
            frame.pack(side='top', pady=1, fill="x", expand=False)
            name_entry = Entry(frame, bd=2, width=40, bg="lightgray")
            name_entry.pack(side='left', padx=5, pady=1, expand=False)
            name_entry.insert(tk.END, windowObject.getWindowName())

            def rename():
                database.rename_program(
                    windowObject.getWindowName(), name_entry.get())
                windowObject.windowName = name_entry.get()
                self.reload()
                text = ""
                for s in windowObject.getFilterStringList():
                    text += s + "\n"
                filter_Text.insert(tk.END, text)

            rename_button = Button(
                master=frame, text="rename filter name", command=rename)
            rename_button.pack(side='left', padx=5, pady=5, expand=False)
            bg_tracking_button = Button(
                master=frame, text="bg-tracking off", command=lambda: self.switch_bg_tracking_State(bg_tracking_button, windowObject))
            if windowObject.getBgTracking():
                bg_tracking_button.configure(text="bg-tracking on")
            bg_tracking_button.pack(side='left', padx=5, pady=5, expand=False)
    # TODO info: what is bg_tracking...
            scroll_y = Scrollbar(self.edit_Window)
            filter_Text = Text(self.edit_Window, height=20,
                               width=80, bg="lightgray")
            scroll_y.pack(side="right", fill="y")
            filter_Text.pack(side="left", fill="y")
            scroll_y.config(command=filter_Text.yview)
            filter_Text.config(yscrollcommand=scroll_y.set)
            text = ""
            for s in windowObject.getFilterStringList():
                text += s + "\n"
            filter_Text.insert(tk.END, text)

            save_button = Button(
                master=frame, text="save Filter", command=lambda: self.updateStringFilter(windowObject, text=filter_Text.get("1.0", "end-1c")))
            save_button.pack(side='left', padx=5, pady=5, expand=False)

            # self.protocol("WM_DELETE_WINDOW", self.hide) # TODO override:quit or save -> save filter to database
            self.edit_Window.mainloop()

    def updateStringFilter(self, windowObject, text):
        filter = []
        for l in text.splitlines():
            if len(l) >= 1:
                filter.append(l)
        print("---->>> new filter:", filter)
        database.delete_all_program_filter(windowObject.getWindowName())
        for s in filter:
            database.add_program_filter(windowObject.getWindowName(), s)

        print(database.get_program_filter(windowObject.getWindowName()))


# TODO delete all old filterStrings in database -> create new ### or: delete if old and create new for new

    def switchState(self, button, windowObject):
        if windowObject.state == True:
            button.configure(text="off")
            windowObject.setState(False)
        elif windowObject.state == False:
            button.configure(text="on")
            windowObject.setState(True)
        time.sleep(2)   # -> bug...
        self.updateWindowList()  # -> update list in apptt...

    def switch_bg_tracking_State(self, button, windowObject):
        if windowObject.getBgTracking() == True:
            button.configure(text="bg-tracking off")
            windowObject.setBgTracking(False)
        elif windowObject.getBgTracking() == False:
            button.configure(text="bg-tracking on")
            windowObject.setBgTracking(True)
        time.sleep(2)   # -> bug...
        self.updateWindowList()  # -> update list in apptt...

    # TODO replace programName by windowObject?
    def viewStats_Window(self, programName):
        try:
            self.stats_Window.lift(self)
        except:
            self.stats_Window = tk.Tk()
            self.stats_Window.title("ApplicationTimeTracker - stats: " +
                                    programName)
            scroll_y = Scrollbar(self.stats_Window)
            stats_Text = Text(self.stats_Window, height=20,
                              width=80, bg="#4a4a4a")
            scroll_y.pack(side="right", fill="y")
            stats_Text.pack(side="left", fill="y")
            scroll_y.config(command=stats_Text.yview)
            stats_Text.config(yscrollcommand=scroll_y.set)

            # ---- stats to text ----
            text = ""
            for d in database.get_all_times_by_program(programName):
                text += str(d[1])+" - "+self.convertToTimeString(d[2])
                text += " -  bg-Time: "+self.convertToTimeString(d[3])
                text += " =>  full-Time: "+self.convertToTimeString(d[2]+d[3])
                text += "\n"

            stats_Text.insert(tk.END, text)
            stats_Text.config(state=tk.DISABLED)
            self.stats_Window.mainloop()

    def convertToTimeString(self, time_sec):
        hh = int(time_sec/60/60)
        mm = int(time_sec/60)-60*hh
        ss = int(time_sec)-60*60*hh-60*mm
        timeString = str(str(hh) + "h " + str(mm) + "m " + str(ss) + "s")
        return timeString

    def action(self):
        print("action")


# ----------- ToolTip -----------
# TODO extra file?

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
