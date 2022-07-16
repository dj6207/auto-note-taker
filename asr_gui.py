import tkinter as tk
from tkinter import ttk, filedialog
import os
import mic_server_revised as msr
import threading

WINDOW = tk.Tk()

def init():
    WINDOW.geometry("360x180")
    WINDOW.config(bg="white")

def start():
    tab()
    # server_thread = threading.Thread(target=msr.start)
    # server_thread.start()

def select_button(entry):
    current_dir = os.getcwd()
    dir = filedialog.askdirectory(initialdir=current_dir, title="Select a directory")
    entry.insert(0, dir)

def make_path_select(tab, path_name, row, column):
    path = tk.StringVar()
    ttk.Label(tab, text= path_name).grid(column=column, row=row, sticky=tk.EW, padx=5, pady=5)
    entry = ttk.Entry(tab, textvariable=path)
    entry.grid(column=column + 1, row=row, sticky=tk.EW, padx=5, pady=5)
    ttk.Button(tab, text="Select", command= lambda: select_button(entry)).grid(column=column + 2, row=row, sticky=tk.EW, padx=5, pady=5)

def tab():
    tab_control = ttk.Notebook(WINDOW)
    tab1 = tk.Frame(tab_control)
    tab1.columnconfigure(1, weight=1)
    tab_control.add(tab1, text= "Client")
    tab_control.pack(expand=True, fill='both')

    make_path_select(tab1, "Base Path:", 0, 0)
    make_path_select(tab1, "Transcribe Path:", 1, 0)

    ttk.Button(tab1, text="Record", command=record_button).grid(column=0, row=3, padx=5, pady=5, sticky=tk.W, columnspan=3)
    ttk.Button(tab1, text="Stop", command=stop_button).grid(column=1, row=3, padx=5, pady=5, sticky=tk.W)
    ttk.Button(tab1, text="Time", command=time_button).grid(column=1, row=3, padx=5, pady=5, sticky=tk.E)
    ttk.Button(tab1, text="Quit", command=quit_button).grid(column=0, row=3, padx=5, pady=5, sticky=tk.E, columnspan=3)

def record_button():
    print("record")

def stop_button():
    print("stop")

def quit_button():
    print("quit")

def time_button():
    print("time")

if __name__ == "__main__":
    init()
    start()
    WINDOW.mainloop()