import os
import webbrowser
from src.config import config
from tkinter import Toplevel, Entry, CENTER, Button, Label

def submit(root, entry):
    api_key = entry.get()
    with open("./src/api_key.txt", 'w') as f:
        f.write(api_key)
    root.grab_release()
    root.destroy()

def get_api_key(root):
    top = Toplevel(root)
    top.title("API Key")
    top.resizable(False, False)
    top.grab_set()

    api_key_entry = Entry(top, width=45)
    api_key_entry.place(relx=0.5, rely=0.3, anchor=CENTER)

    submit_button = Button(top, text="Submit", command=lambda: submit(top, api_key_entry))
    submit_button.place(relx=0.84, rely=0.7, anchor=CENTER)

    top.geometry("500x100")

def start(root):
    if not os.path.exists("./plotters-doc-data"):
        os.makedirs("./plotters-doc-data")
    
    if os.path.isfile("./src/api_key.txt"):
        config(root)
    else:
        get_api_key(root)

def help(root):
    def open_browser(event):
        webbrowser.open_new_tab("https://rapidapi.com/alphavantage/api/alpha-vantage")

    top = Toplevel(root)
    top.title("Help")
    top.resizable(False, False)
    top.grab_set()

    Label(top, text="Login to RapidAPI and subscribe to AlphaVantage").pack()
    hyperlink = Label(top, text="here", underline=3, fg="#0563C1")
    hyperlink.pack()
    hyperlink.bind("<Button-1>", open_browser)
    Label(top, text="Copy the now generated API key").pack()

    top.geometry("400x80")