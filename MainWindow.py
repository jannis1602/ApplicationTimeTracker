from tkinter import Tk, Label, Button, Frame, Canvas, Scrollbar, Entry
# import applicationTimeTracker as apptt


class MainWindow:

    windowFrameList = []
    global root, list_frame

    def __init__(self):
        print("hallo")
        self.windowFrameList.append("test1")
        self.windowFrameList.append("test2")
        self.windowFrameList.append("test3")
        self.windowFrameList.append("test4")
        self.windowFrameList.append("test5")
        self.windowFrameList.append("test6")
        self.windowFrameList.append("test11")
        self.windowFrameList.append("test22")
        self.windowFrameList.append("test33")
        self.windowFrameList.append("test44")
        self.windowFrameList.append("test55")
        self.windowFrameList.append("test66")

    def createMainWindow(self):
        global root
        root = Tk()
        root.title("Window")
        root.geometry('800x400')
        root.resizable(False, False)

        menu_bar_frame = Frame(
            master=root, height=20, width=640, bg="gray")
        menu_bar_frame.pack(side='top', padx='5',
                            pady='5', fill="x", expand=False)
    # String-Entry
        string_entry = Entry(menu_bar_frame, bd=2, width=40)
        string_entry.pack(side='left', padx='5', pady='5', expand=False)
    # Add-Button
        addfilter_button = Button(
            master=menu_bar_frame, text="Add to Filter", command=self.action)
        addfilter_button.pack(side='left', padx='5', pady='5', expand=False)
    # reload-Button
        reload_button = Button(
            master=menu_bar_frame, text="reload", command=self.action)
        reload_button.pack(side='left', padx='5', pady='5', expand=False)
    # Exit-Button
        exit_button = Button(
            master=menu_bar_frame, text="EXIT", command=self.action)
        exit_button.pack(side='right', padx='5', pady='5', expand=False)

        # self.createWindowFrame(self.root) # test

    # ------------------------ list ------------------------

        self.createListFrame(root)

        root.mainloop()

    def createListFrame(self, root):
        global list_frame
        list_frame = Frame(master=root)
        list_frame.pack(side='left', padx=1,
                        pady=1, fill="both", expand=True)

        canvas = Canvas(list_frame, bg="green")
        scroll_y = Scrollbar(list_frame, orient="vertical",
                             command=canvas.yview)
        scroll_frame = Frame(canvas, bg="blue")
        # for i in range(20):
        #     Label(scroll_frame, text='label %i' % i).pack()#

        # temp_frame = Frame(
        #     master=scroll_frame, height=20, width=400, bg="orange")
        # temp_frame.pack(side='bottom', padx='5',
        #                 pady='1', fill="x", expand=True)
        for e in self.windowFrameList:
            self.createWindowFrame(scroll_frame)

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

        # for i in range(10):
        #     self.createWindowFrame(self.list_frame)

    def remove(self, frame):
        self.windowFrameList.pop()
        global root, list_frame
        list_frame.destroy()
        self.createListFrame(root)

        # global canvas, scroll_y
        # canvas.pack(fill='both', expand=True, side='left')
        # scroll_y.pack(fill='y', side='right')

    def createWindowFrame(self, master):
        temp_frame = Frame(
            master=master, height=20, width=200, bg="red")
        temp_frame.pack(side='bottom', padx=5,
                        pady=1, fill="x", expand=False)

        name_label = Label(master=temp_frame, text="window", bg="gray")
        name_label.pack(padx=2, pady=2, side="left")

        name_label = Label(master=temp_frame,
                           text="time: 40 Sekunden", bg="gray")
        name_label.pack(padx=2, pady=2, side="left")

        # void_label = Label(master=temp_frame,
        #                    text="  "*60, bg="gray")
        # void_label.pack(padx=2, pady=2, side="left")

        btn = Button(temp_frame, text="remove",
                     bg="darkgray", command=lambda: self.remove(temp_frame))
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
