import tkinter as tk
from tkinter import Label, Button, Frame, Canvas, Scrollbar, Entry, Text
from WindowObject import WindowObject
import database
import pygetwindow as gw
import tkinter.messagebox


class MainWindow(tk.Tk):

    def __init__(self, windowList, updateWindowList, exitProgram):
        self.windowList = windowList
        tk.Tk.__init__(self)
        self.title("ApplicationTimeTracker")
        self.geometry('800x400')
        self.resizable(False, False)
        self.running = True
        self.updateWindowList = updateWindowList
        self.exitProgram = exitProgram

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

        # self.mainloop()  # is blocking
        while self.running:
            self.update()
        self.destroy()

    def windowNamesWindow(self):
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
            database.add_program(name)
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

    def createListFrame(self):
        self.list_frame = Frame(master=self)
        self.list_frame.pack(side='left', padx=0,
                             pady=0, fill="both", expand=True)

        canvas = Canvas(self.list_frame, bg="gray")
        scroll_y = Scrollbar(self.list_frame, orient="vertical",
                             command=canvas.yview)
        scroll_frame = Frame(canvas, bg="gray")  # blue
        # for i in range(20):
        #     Label(scroll_frame, text='label %i' % i).pack()#

        # temp_frame = Frame(
        #     master=scroll_frame, height=20, width=400, bg="orange")
        # temp_frame.pack(side='bottom', padx='5',
        #                 pady='1', fill="x", expand=True)

        void_label = Label(master=scroll_frame,
                           text=" "*255, bg="gray")
        void_label.pack(padx=2, pady=2, side="bottom")

        for e in self.windowList:
            self.createWindowFrame(scroll_frame, windowObject=e)

        canvas.create_window(0, 0, anchor='nw', window=scroll_frame)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'),  # scrollregion=canvas.bbox('all') #TODO: #20 scrollregion
                         yscrollcommand=scroll_y.set)
        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')

        # scroll_frame.pack(fill='both', expand=True, side='left') # -> scrollbar funktioniert dann nicht!

        # self.list_frame = Frame(
        #     master=root, height=20, width=640, bg="gray")
        # self.list_frame.pack(side='left', padx='5', pady='5')

    def remove(self, windowObject):
        result = tkinter.messagebox.askquestion(
            "Delete", "Are You Sure?", icon='warning')
        if result == 'yes':
            pass
        else:
            return
        try:        #TODO: verbessern!!!
            self.windowList.remove(windowObject)
        except:
            print("deleted by name")
            for w in self.windowList:
                if w.getWindowName()==windowObject.getWindowName():
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

    def createWindowFrame(self, master, windowObject):  # TODO WindowObject...
        temp_frame = Frame(
            master=master, height=20, width=200, bg="darkgray")
        temp_frame.pack(side='bottom', padx=5,
                        pady=1, fill="x", expand=False)

# TODO: add on/off Button

        name_label = Label(master=temp_frame,
                           text=windowObject.getWindowName(), bg="gray")
        name_label.pack(padx=2, pady=2, side="left")

        name_label = Label(master=temp_frame,
                           text=windowObject.getTimeString(name=False), bg="gray")
        name_label.pack(padx=2, pady=2, side="left")

        # void_label = Label(master=temp_frame,
        #                    text="  "*60, bg="gray")
        # void_label.pack(padx=2, pady=2, side="left")

        btn = Button(temp_frame, text="remove",
                     bg="darkgray", command=lambda: self.remove(windowObject))
        btn.pack(padx=2, pady=2, side="right", fill="x")

        # return btn

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
