from tkinter import Tk, Label, Button, Frame, Canvas, Scrollbar


class MainWindow():
    def __init__(self, root):
        self.root = root
        self.root.title("Window")
        self.root.geometry('800x400')
        self.root.resizable(False, False)

        self.menu_bar_frame = Frame(
            master=root, height=20, width=640, bg="gray")
        self.menu_bar_frame.pack(side='top', padx='5', pady='5')

        self.greet_button = Button(
            master=self.menu_bar_frame, text="EXIT", command=self.action)
        self.greet_button.pack(side='left', padx='5', pady='5')

# ------------------------ list ------------------------
        canvas = Canvas(self.root,bg="gray")
        scroll_y = Scrollbar(self.root, orient="vertical",
                             command=canvas.yview)
        scroll_frame = Frame(canvas)
        # for i in range(20):
        #     Label(scroll_frame, text='label %i' % i).pack()
        for i in range(20):
            self.createWindowFrame(scroll_frame)
        canvas.create_window(0, 0, anchor='nw', window=scroll_frame)
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'),
                         yscrollcommand=scroll_y.set)
        canvas.pack(fill='both', expand=True, side='left')
        scroll_y.pack(fill='y', side='right')


        # self.list_frame = Frame(
        #     master=root, height=20, width=640, bg="gray")
        # self.list_frame.pack(side='left', padx='5', pady='5')

        # for i in range(10):
        #     self.createWindowFrame(self.list_frame)

        root.mainloop()

    def createWindowFrame(self, master):
        temp_frame = Frame(
            master=master, height=20, width=200, bg="gray")
        temp_frame.pack(side='bottom', padx='5', pady='1',expand=True)

        name_label = Label(master=temp_frame, text="window", bg="gray")
        name_label.pack(padx=2, pady=2, side="left")

        name_label = Label(master=temp_frame,
                           text="time: 40 Sekunden", bg="gray")
        name_label.pack(padx=2, pady=2, side="left")

        btn = Button(temp_frame, text="remove",
                     bg="darkgray", command=self.action)
        btn.pack(padx=2, pady=2, side="left")

        return btn

    def action(self):
        print("action")

        # self.label = Label(root, text="GUI")
        # self.label.pack()

        # self.greet_button = Button(root, text="Greet", command=self.greet)
        # self.greet_button.pack()

        # self.close_button = Button(root, text="Close", command=root.quit)
        # self.close_button.pack()


MainWindow(Tk())
