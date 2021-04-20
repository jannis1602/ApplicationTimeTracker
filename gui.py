from tkinter import Tk, Label, Button, Frame


class MainWindow():
    def __init__(self, root):
        self.root = root
        self.root.title("Window")
        self.root.geometry('350x200')

        self.menu_bar_frame = Frame(
            master=root, height=20, width=640, bg="gray")
        self.menu_bar_frame.pack(side='right', padx='5', pady='5')

        self.greet_button = Button(
            master=self.menu_bar_frame, text="EXIT", command=self.action)
        self.greet_button.pack(side='right', padx='5', pady='5')
        
        
        root.mainloop()

    def action(self):
        print("action")

        # self.label = Label(root, text="GUI")
        # self.label.pack()

        # self.greet_button = Button(root, text="Greet", command=self.greet)
        # self.greet_button.pack()

        # self.close_button = Button(root, text="Close", command=root.quit)
        # self.close_button.pack()



MainWindow(Tk())
