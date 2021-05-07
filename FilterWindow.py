import tkinter as tk
from tkinter import Label, Button, Frame, Canvas, Scrollbar, Entry, Text, Toplevel
from WindowObject import WindowObject
import database


class FilterWindow:

    def __init__(self,windowObject):
        self.root = tk.Tk()
        self.root.title("ApplicationTimeTracker - filter")
        self.windowObject = windowObject
        self.window()

    def window(self):


        def widget_design():
            frame1()

        def frame1():
            self.top_frame = Frame(
                master=self.root, height=20, width=200, bg="darkgray")
            self.top_frame.pack(side='top', pady=1, fill="x", expand=False)
            name_entry = Entry(self.top_frame, bd=2, width=40, bg="lightgray")
            name_entry.pack(side='left', padx=5, pady=1, expand=False)
            name_entry.insert(tk.END, self.windowObject.getWindowName())

            def rename():
                database.rename_program(
                    self.windowObject.getWindowName(), name_entry.get())
                self.windowObject.windowName = name_entry.get()
                self.root.reload()
                text = ""
                for s in self.windowObject.getFilterStringList():
                    text += s + "\n"
                filter_Text.insert(tk.END, text)

            rename_button = Button(
                master=self.top_frame, text="rename filter name", command=rename)
            rename_button.pack(side='left', padx=5, pady=5, expand=False)
            bg_tracking_button = Button(
                master=self.top_frame, text="bg-tracking off", command=lambda: self.switch_bg_tracking_State(bg_tracking_button, self.windowObject))
            if self.windowObject.getBgTracking():
                bg_tracking_button.configure(text="bg-tracking on")
            bg_tracking_button.pack(side='left', padx=5, pady=5, expand=False)
            # TODO info: what is bg_tracking...
            scroll_y = Scrollbar(self.root)
            filter_Text = Text(self.root, height=20,
                               width=80, bg="lightgray")
            scroll_y.pack(side="right", fill="y")
            filter_Text.pack(side="left", fill="y")
            scroll_y.config(command=filter_Text.yview)
            filter_Text.config(yscrollcommand=scroll_y.set)
            text = ""
            for s in self.windowObject.getFilterStringList():
                text += s + "\n"
            filter_Text.insert(tk.END, text)

            save_button = Button(
                master=self.top_frame, text="save Filter", command=lambda: self.updateStringFilter(self.windowObject, text=filter_Text.get("1.0", "end-1c")))
            save_button.pack(side='right', padx=5, pady=5, expand=False)

        # def listbox():
        #     "The listbox in the frame1"
        #     self.lbx = tk.Listbox(self.frm1, bg="gold")
        #     self.lbx.grid(column=0, row=0)

        widget_design()

    # def createFilterWindow(self,windowObject):
    #     # menu_bar_frame = Frame(
    #     #     master=self, height=20, width=640, bg="gray")
    #     # menu_bar_frame.pack(side='top', padx=2,
    #     #                     pady=2, fill="x", expand=False)

    #     self.protocol("WM_DELETE_WINDOW", self.close)
    #     # self.createListFrame()
    #     self.after(1, lambda: self.focus_force())

    #     # self.mainloop()  # is blocking
    #     while self.running:
    #         self.update()
    #     self.destroy()

    def action(self):
        print("aktion")

    def close(self):
        self.running = False

    def addFilter(self):
        print("adding filter to list...")

    def switch_bg_tracking_State(self, button, windowObject):
        if windowObject.getBgTracking() == True:
            button.configure(text="bg-tracking off")
            windowObject.setBgTracking(False)
        elif windowObject.getBgTracking() == False:
            button.configure(text="bg-tracking on")
            windowObject.setBgTracking(True)
        # time.sleep(2)   # -> bug...
        # self.updateWindowList()  # -> update list in apptt...

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

if __name__ == '__main__':
    filterWindow = FilterWindow(WindowObject(windowName="Opera"))
    filterWindow.root.mainloop()
