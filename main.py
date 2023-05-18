import tkinter as tk
from src.welcome import start, help

window = tk.Tk()

window.title("Welcome!")
window.geometry("400x150")
window.resizable(False, False)

start_frame = tk.Frame(window)
help_frame = tk.Frame(window)

start_frame.pack(expand=True, fill=tk.BOTH, side=tk.LEFT)
help_frame.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)

start_button = tk.Button(start_frame, text="Start", command=lambda: start(window))
help_button = tk.Button(help_frame, text="Help", command=lambda: help(window))

start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
help_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

window.mainloop()