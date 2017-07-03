from Tkinter import *

class Table(object):
	"""
	Table obect meant to represent beer pong table. Holds information about all cups.
	Has methods to update and dispaly their position as they are re-racked.
	"""
	def __init__(self, width, height, cups):
		"""
		Initializes table as a Tkinter Canvas widget.

		Args:
			width(int): width of table
			height(int): height of table
			cups(Cup): cup objects on the table
		"""
		self.master = Tk()
		self.width = width
		self.height = height
		self.canvas = Canvas(self.master, self.width, self.height)
		self.cups = cups
		self.rendered_cups = self.render_cups() 

	def render_cups(self, past_renders=None):
		"""
		Renders cups in canvas based on the information in the cup objects in self.cups.

		Args:
			past_renders(list): list of past renders
		"""
		if past_renders:
			for i in range(self.cups):
				self.canvas.coords(past_renders[i], self.cups[i].center)
		else:
			past_renders = []
			for i in range(self.cups):
				past_renders.append(self.canvas.create_oval(self.cups[i].center, width=self.cups[i].radius))

	def update(self):
		"""
		Updates canvas.
		"""
		self.render_cups(self.rendered_cups)
		self.master.update_idletasks()
		self.master.update()

