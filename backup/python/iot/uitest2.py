#https://docs.python.org/2/library/tkinter.html
from Tkinter import *
win=Tk()
win.title("Tk GUI")
label=Label(win, text="Hello World!")
button=Button(win, text="OK")
button1=Button(win, text="OK")
label.grid(column=0,row=0)
button.grid(column=1,row=0)
button1.grid(column=0,row=1)
win.mainloop() 
