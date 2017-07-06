from arm import *
from gui import *
import Tkinter as tk

if __name__ == '__main__':
	cups = []
	for i in range(3):
		cups.append(Cup(i,TEN_CUP_MAP[i+1]))

	root = tk.Tk()
	table = Table(root, 1000, 1000, cups)
	root.mainloop()