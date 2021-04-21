from tkinter import Tk, Label, Button, Frame, Canvas, Scrollbar, Entry
from WindowObject import WindowObject


class MainWindow:

    windowObjectList = []
    global root, list_frame

    def __init__(self,windowObjectList):
        print("hallo")

        self.createMainWindow(windowObjectList)
        # hier create?

    def createMainWindow(self, windowObjectList):
        print("create...")
        self.windowObjectList = windowObjectList
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
            master=menu_bar_frame, text="EXIT", command=self.action)  # TODO: #21 @superxyxy add end methode
        exit_button.pack(side='right', padx='5', pady='5', expand=False)

        # self.createWindowFrame(self.root) # test
        root.protocol("WM_DELETE_WINDOW", self.hide)


    # ------------------------ list ------------------------

        self.createListFrame()
        root.mainloop()

    def show(self):
        try:
            global root
            root.deiconify()
        except:
            print("error while showing mainWindow!")
    
    def hide(self):
        global root
        root.withdraw()

    def createListFrame(self):
        global root, list_frame
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

        void_label = Label(master=scroll_frame,
                           text="  "*100, bg="gray")
        void_label.pack(padx=2, pady=2, side="bottom")

        for e in self.windowObjectList:
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

        # for i in range(10):
        #     self.createWindowFrame(self.list_frame)

    def remove(self, windowObject):
        self.windowObjectList.remove(windowObject)
        global list_frame
        list_frame.destroy()
        self.createListFrame()

    def reload(self):
        global list_frame
        list_frame.destroy()
        self.createListFrame()

    def add(self, name):
        self.windowObjectList.append(name)
        global list_frame
        list_frame.destroy()
        self.createListFrame()

    def createWindowFrame(self, master, windowObject):  # TODO WindowObject...
        temp_frame = Frame(
            master=master, height=20, width=200, bg="red")
        temp_frame.pack(side='bottom', padx=5,
                        pady=1, fill="x", expand=False)

        name_label = Label(master=temp_frame,
                           text=windowObject.getWindowName(), bg="gray")
        name_label.pack(padx=2, pady=2, side="left")

        name_label = Label(master=temp_frame,
                           text="time: "+str(windowObject.getFullTime())+" Sekunden", bg="gray")
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


# windowList = []
# for i in range(20):
#     windowList.append(WindowObject("test"+str(i)))
# windowList.append(WindowObject("Opera"))
# windowList.append(WindowObject("VScode"))

# MainWindow(windowList)
