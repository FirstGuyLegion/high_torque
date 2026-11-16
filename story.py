#story.py
class Story:

	def __init__(self):
		with open("assets/story.txt") as file:
			self.story = file.read().split("\n")
		self.index = -1
		self.line_i = 0
		self.started = False
		self.end = False
		self.End = False
		self.sprites = {
			"|p|" : "empty",
			"|h|" : "phone",
			"|m|" : "mechanic"
		}

	def line(self):
		if self.line_i == len(self.story)-1: self.End = True
		name = self.sprites[self.story[self.line_i][:3]]
		line = self.story[self.line_i][4:]
		if self.index < len(line): 
			self.index += 1
			self.end = True
		to_return = line[:self.index]

		return name, to_return
	
	def start(self):
		if self.end:
			self.line_i += 1
			self.index = -1
			self.end = False