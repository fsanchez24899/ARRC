import Tkinter as tk
import time

class viewCup(object):
	def __init__(self, canvas, *args, **kwargs):
		self.canvas = canvas
		self.id = canvas.create_oval(*args, **kwargs)

	def update(self, new_place=None):
		if new_place:
			pass
		else:
			return

class Table(object):
	"""
	Table obect meant to represent beer pong table. Holds information about all cups.
	Has methods to update and dispaly their position as they are re-racked.
	"""
	def __init__(self, master, width, height, cups):
		"""
		Initializes table as a Tkinter Canvas widget.

		Args:
			width(int): width of table
			height(int): height of table
			cups(Cup): cup objects on the table
		"""
		self.master = master
		self.width = width
		self.height = height
		self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bg='#8B4513')
		self.canvas.pack()
		self.cups = cups
		self.rendered_cups = self.render_cups()
		self.canvas.pack()
		self.master.after(0,self.update) 

	def render_cups(self):
		"""
		Renders cups in canvas based on the information in the cup objects in self.cups.

		Args:
			past_renders(list): list of past renders
		"""
		renders = []
		for i in range(len(self.cups)):
			renders.append(viewCup(self.canvas, self.cups[i].ncs, fill='red'))
		return renders

	def update(self):
		"""
		Updates canvas.
		"""
		for c in self.rendered_cups:
			c.update()


