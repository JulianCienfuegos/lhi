import os
try:
	import tkinter
except:
	import Tkinter
	tkinter = Tkinter
	del Tkinter
from PIL import Image, ImageTk

a = Image.open("cat.png")
master = tkinter.Tk()
photo = ImageTk.PhotoImage(a)
tkinter.Label(master, image=photo).pack()
master.mainloop()