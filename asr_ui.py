from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os

class Server_GUI:
    def __init__(self, root):
        self.window = root
        self.window.title(f"Server")

        self.menu()
        self.tab()


    def menu(self):
        menu_control = Menu(self.window)
        self.window.config(menu=menu_control)
        self.file_menu = Menu(menu_control, tearoff=False)

        menu_control.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", font=("Arial",10,"bold","italic"), compound=LEFT)

    def browse_file():
        current_dir = os.getcwd()
        dir = filedialog.askdirectory(initialdir=current_dir, title="Select a directory")
        print(dir)

    def tab(self):
        tab_control = ttk.Notebook(self.window)

        tab1 = Frame(tab_control)
        tab2 = Frame(tab_control)

        tab_control.add(tab1, text = 'Settings')
        # base_path_text = Text(self.window, height=5, width=20)
        # base_path_label = Label(self.window, text="Base Path")
        # base_path_label.config(font=("Arial",10,"bold","italic"))
        # base_path_text.pack()
        # base_path_label.pack()
    
    




        tab_control.add(tab2, text = 'Tab 2')

        tab_control.pack(expand=1, fill='both')

        # ttk.Label(tab1, text="Settings").grid(column=0, row=0, padx=30, pady=30)
        # ttk.Label(tab2, text="Stuff").grid(column=0, row=0, padx=30, pady=30)
        ttk.Button(tab1, text="Browse", command=self.browse_file()).grid(column=0, row=0, padx=30, pady=30)

    
if __name__ == "__main__":
    window = Tk()
    window.geometry("1280x720")
    window.maxsize(800, 600)
    window.minsize(640, 480)
    window.config(bg="white")
    Server_GUI(window)
    window.mainloop()