from PIL import Image, ImageTk
from src.get_symbol import getSymbol
from stonks import get_daily_historical_data, graph
from tkinter import Toplevel, Frame, Label, Entry, Button, Scale, IntVar, StringVar, Canvas, PhotoImage

with open("src/api_key.txt", 'r') as f:
    API_KEY = f.read()

def config(root):
    global date, data, img
    def setMinDate(event):
        minVal = slider_minScale.get()
        maxVal = slider_maxScale.get()
        if maxVal - minVal < 10:
            slider_maxScale.set(minVal+10)
        minDate = date[int((len(date)-10)*slider_minScale.get()/100)]
        maxDate = date[int((len(date)-10)*slider_maxScale.get()/100)]
        Label(slider_frame, text=minDate).place(relx=0.8, rely=0.25, anchor="w")
        Label(slider_frame, text=maxDate).place(relx=0.8, rely=0.75, anchor="w")

    def setMaxDate(event):
        minVal = slider_minScale.get()
        maxVal = slider_maxScale.get()
        if maxVal - minVal < 10:
            slider_minScale.set(maxVal-10)
        minDate = date[int((len(date)-10)*slider_minScale.get()/100)]
        maxDate = date[int((len(date)-10)*slider_maxScale.get()/100)]
        Label(slider_frame, text=minDate).place(relx=0.8, rely=0.25, anchor="w")
        Label(slider_frame, text=maxDate).place(relx=0.8, rely=0.75, anchor="w")

    def getHistoricalData(symbolVar):
        global date, data
        symbol = symbol_entry.get().split(",")[0]
        date, data = get_daily_historical_data(symbol, API_KEY)
        date.reverse()
        data.reverse()
        slider_minScale.config(state="active")
        slider_maxScale.config(state="active")

    def plot_graph():
        global img
        minIdx = int((len(date)-10)*slider_minScale.get()/100)
        maxIdx = int((len(date)-10)*slider_maxScale.get()/100)
        date_copy = date[minIdx:maxIdx]
        date_copy.reverse()
        data_copy = data[minIdx:maxIdx]
        data_copy.reverse()
        graph(date_copy, data_copy)
        img = ImageTk.PhotoImage(Image.open("./plotters-doc-data/0.png"))
        image_label.configure(image=img)


    top = Toplevel(root)
    top.title("Config")
    top.resizable(False, False)
    top.grab_set()

    symbol_frame = Frame(top, height=60)
    symbol_label = Label(symbol_frame, text="Select Symbol")
    symbolVar = StringVar()
    symbolVar.trace_variable("w", lambda name, index, mode, symbolVar=symbolVar: getHistoricalData(symbolVar))
    symbol_entry = Entry(symbol_frame, state="disabled", textvariable=symbolVar, disabledbackground="#3D3736")
    symbol_button = Button(symbol_frame, text="Select", command=lambda: getSymbol(top, symbol_entry))

    symbol_label.place(relx=0.15, rely=0.5, anchor="center")
    symbol_entry.place(relx=0.7, rely=0.5, anchor="center")
    symbol_button.place(relx=0.92, rely=0.5, anchor="center")

    slider_frame = Frame(top, height=100)
    slider_label = Label(slider_frame, text="Select Date Range")
    minVar = IntVar()
    maxVar = IntVar()
    minVar.set(0)
    maxVar.set(100)
    slider_minScale = Scale(slider_frame, orient="horizontal", state="disabled", from_=0, to=90, showvalue=0, length=200, variable=minVar)
    slider_minScale.bind("<ButtonRelease-1>", setMinDate)
    slider_maxScale = Scale(slider_frame, orient="horizontal", state="disabled", from_=10, to=100, showvalue=0, length=200, variable=maxVar)
    slider_maxScale.bind("<ButtonRelease-1>", setMaxDate)

    slider_label.place(relx=0.15, rely=0.5, anchor="center")
    Label(slider_frame, text="From Date").place(relx=0.42, rely=0.25, anchor="e")
    Label(slider_frame, text="To Date").place(relx=0.42, rely=0.75, anchor="e")
    slider_minScale.place(relx=0.6, rely=0.25, anchor="center")
    slider_maxScale.place(relx=0.6, rely=0.75, anchor="center")

    submit_frame = Frame(top, height=30)
    submit_button = Button(submit_frame, text="Submit", command=plot_graph)

    submit_button.pack()
    
    graph_frame = Frame(top, height=480, width=700, highlightbackground="blue", highlightthickness=2)
    image_label = Label(graph_frame)

    image_label.pack()

    symbol_frame.pack(expand=True, fill="x", side="top")
    slider_frame.pack(expand=True, fill="x", side="top")
    submit_frame.pack(expand=True, fill="x", side="top")
    graph_frame.pack(expand=True, fill="y", side="top")
    graph_frame.pack_propagate(False)


    top.geometry("700x680")