from stonks import get_symbols
from tkinter import Toplevel, Entry, Label, Listbox, Button, Frame

with open("src/api_key.txt", 'r') as f:
    API_KEY = f.read()

def getSymbol(root, parent_entry):
    def callRustApi(query):
        symbols = get_symbols(query, API_KEY)
        
        top_list.delete(0, "end")
        for i, (sym, name) in enumerate(symbols):
            top_list.insert(i, f"{sym}, {name}")

    def select_symbol(event):
        parent_entry.config(state="normal")
        parent_entry.delete(0, "end")
        parent_entry.insert(0, top_list.get(top_list.curselection()))
        parent_entry.config(state="disabled")

        top.grab_release()
        top.destroy()

    top = Toplevel(root)
    top.title("Symbol Search")
    top.resizable(False, False)
    top.grab_set()

    top_label = Label(top, text="Search for symbol")
    top_label.pack(pady=20)

    search_frame = Frame(top)

    search_entry = Entry(search_frame, width=21)
    search_entry.pack(side="left")

    search_button = Button(search_frame, text="Submit", command=lambda: callRustApi(search_entry.get()))
    search_button.pack(side="left")

    search_frame.pack(pady=10)

    top_list = Listbox(top, width=30)
    top_list.pack()

    top_list.bind("<<ListboxSelect>>", select_symbol)

    top.geometry("300x300")