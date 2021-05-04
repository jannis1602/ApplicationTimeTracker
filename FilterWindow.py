import tkinter as tk
from tkinter import Label, Button, Frame, Canvas, Scrollbar, Entry, Text, Toplevel
from WindowObject import WindowObject
import database


class FilterWindow(tk.Tk):

    def __init__(self,windowObject):
        self.title("ApplicationTimeTracker - filter")
        # self.geometry('%dx%d+%d+%d' % (800, 400, pos[0], pos[1]))
        # self.geometry('800x400)
# TODO icon
        self.resizable(False, False)
        self.running = True

    def createFilterWindow(self,windowObject):
        # menu_bar_frame = Frame(
        #     master=self, height=20, width=640, bg="gray")
        # menu_bar_frame.pack(side='top', padx=2,
        #                     pady=2, fill="x", expand=False)
        frame = Frame(
            master=self, height=20, width=200, bg="darkgray")
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
        scroll_y = Scrollbar(self)
        filter_Text = Text(self, height=20,
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
        save_button.pack(side='right', padx=5, pady=5, expand=False)

        self.protocol("WM_DELETE_WINDOW", self.close)
        # self.createListFrame()
        self.after(1, lambda: self.focus_force())

        # self.mainloop()  # is blocking
        while self.running:
            self.update()
        self.destroy()

    def action(self):
        print("aktion")

    def close(self):
        self.running = False

    def addFilter(self):
        print("adding filter to list...")

    # def show(self):
    #     self.deiconify()

    # def hide(self):
    #     self.withdraw()

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


# FilterWindow().createFilterWindow(windowObject=WindowObject(windowName="test"))
