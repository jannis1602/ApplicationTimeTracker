import tkinter as tk
from tkinter import Label, Button, Frame, Canvas, Scrollbar, Entry, Text, Toplevel

class FilterWindow(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("ApplicationTimeTracker - filter")
        # self.geometry('%dx%d+%d+%d' % (800, 400, pos[0], pos[1]))
        # self.geometry('800x400)
# TODO icon
        self.resizable(False, False)
        self.running = True

        # self.subWindows = [] # unused
        # init all subwindows:
        self.settings_Window = None
        self.allWindowNames_Window = None
        self.stats_Window = None
        self.edit_Window = None

    def createFilterWindow(self):
        menu_bar_frame = Frame(
            master=self, height=20, width=640, bg="gray")
        menu_bar_frame.pack(side='top', padx=2,
                            pady=2, fill="x", expand=False)

    # ShowNames-Button
        show_names_button = Button(
            master=menu_bar_frame, text="show all titles", command=self.action)
        show_names_button.pack(side='left', padx='5', pady='5', expand=False)
    # String-Entry
        self.string_entry = Entry(
            menu_bar_frame, bd=2, width=40, bg="lightgray")
        self.string_entry.pack(side='left', padx='5', pady='5', expand=False)
    # Add-Button
        addfilter_button = Button(
            master=menu_bar_frame, text="Add Filter", command=self.addFilter)
        addfilter_button.pack(side='left', padx='5', pady='5', expand=False)

        self.protocol("WM_DELETE_WINDOW", self.close)
        # self.createListFrame()
        self.after(1, lambda: self.focus_force())

        # self.mainloop()  # is blocking
        while self.running:
            self.update()
        self.destroy()

    def action(self):
        print("aktion")


    def stopRunning(self):
        print("quit MainWindow...")
        self.running = False

    def close(self):
        self.running = False

    def addFilter(self):
        print("adding filter to list...")

    # def show(self):
    #     self.deiconify()

    # def hide(self):
    #     self.withdraw()



FilterWindow().createFilterWindow()
