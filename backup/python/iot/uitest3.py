#http://yhhuang1966.blogspot.tw/2016/05/python-gui-tkinter.html
#https://docs.python.org/2/library/ttk.html
#https://docs.python.org/2/library/tkinter.html

from Tkinter import *
win=Tk()
win.title("Tk GUI")
label=Label(win, text="Hello World!")
count=0
def clickOK():
    global count
    count=count + 1
    label.configure(text="Click OK " + str(count) + " times")
button=Button(win, text="OK", command=clickOK)
label.pack()
button.pack()
win.mainloop()
