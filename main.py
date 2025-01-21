
import pygame
import random
import sys

class app:
	def __init__(self, sizeX, sizeY, mines):
		pygame.init()
		
		self.gridScale = 40
		
		self.sizeX = sizeX
		self.sizeY = sizeY
		self.mines = mines
		
		self.font = pygame.font.SysFont("arial", int(self.gridScale * 0.75))
		
		self.screen = pygame.display.set_mode((self.sizeX * self.gridScale, self.sizeY * self.gridScale))
		self.clock = pygame.time.Clock()
		
		self.grid = []
		
		for x in range(0, self.sizeX):
			self.grid.append([])
			for y in range(0, self.sizeY):
				self.grid[x].append(False)
				
		self.field = self.gridSetEmpty()
		self.field = self.generateMines()
		self.field = self.numerateEmpty()
		
		pygame.display.set_caption(f"grid: {self.sizeX}x{self.sizeY}, mines: {self.mines}")
		
		self.running = True
		self.dead = False
		
		self.main()
		
		pygame.quit()
		
	def main(self):
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.MOUSEBUTTONDOWN and not self.dead:
					x = event.pos[0] // self.gridScale
					y = event.pos[1] // self.gridScale
					
					if not self.grid[x][y]:
						self.uncover(x, y)
					
			self.screen.fill("gray")
			
			for x in range(self.sizeX):
				for y in range(self.sizeY):
					rect = pygame.Rect(x * self.gridScale, y * self.gridScale, self.gridScale, self.gridScale)
					
					if not self.grid[x][y]:
						pygame.draw.rect(self.screen, "darkgray", rect, 3)
					elif self.field[x][y] != 9:
						pygame.draw.rect(self.screen, "darkgreen", rect, 3)
						txt = self.font.render(str(self.field[x][y]), True, "black")
						txtRect = txt.get_rect(center=rect.center)
						self.screen.blit(txt, txtRect)
					else:
						pygame.draw.rect(self.screen, "red", rect, 3)
						txt = self.font.render('*', True, "red")
						txtRect = txt.get_rect(center=rect.center)
						self.screen.blit(txt, txtRect)
						
			if self.dead:
				rect = pygame.Rect(x * self.gridScale, y * self.gridScale, self.gridScale, self.gridScale)
				txt = self.font.render("You died!", True, "black")
				txtRect = txt.get_rect(center=self.screen.get_rect().center)
				pygame.draw.rect(self.screen, "darkgray", txtRect, 0)
				self.screen.blit(txt, txtRect)
			
			pygame.display.flip()
			
			self.clock.tick(60)
			
	def uncover(self, x, y):
		self.grid[x][y] = True
		
		if self.field[x][y] == 0:
			if x != 0:
				if y != 0:
					if not self.grid[x - 1][y - 1]:
						self.uncover(x - 1, y - 1)
				if y != self.sizeY - 1:
					if not self.grid[x - 1][y + 1]:
						self.uncover(x - 1, y + 1)
				if not self.grid[x - 1][y]:
					self.uncover(x - 1, y)
			if x != self.sizeX - 1:
				if y != 0:
					if not self.grid[x + 1][y - 1]:
						self.uncover(x + 1, y - 1)
				if y != self.sizeY - 1:
					if not self.grid[x + 1][y + 1]:
						self.uncover(x + 1, y + 1)
				if not self.grid[x + 1][y]:
					self.uncover(x + 1, y)
			if y != 0:
				if not self.grid[x][y - 1]:
					self.uncover(x, y - 1)
			if y != self.sizeY - 1:
				if not self.grid[x][y + 1]:
					self.uncover(x, y + 1)
		elif self.field[x][y] == 9:
			for _x in range(self.sizeX):
				for _y in range(self.sizeY):
					if self.field[_x][_y] == 9:
						self.grid[_x][_y] = True
			self.dead = True
			
	def gridSetEmpty(self):
		tmp = []
		
		for x in range(self.sizeX):
			tmp.append([])
			
			for y in range(self.sizeY):
				tmp[x].append(0)
				
		return tmp
		
	def generateMines(self):
		tmp = self.field
		
		for i in range(self.mines):
			while True:
				x = random.randint(0, self.sizeX - 1)
				y = random.randint(0, self.sizeY - 1)
				
				if tmp[x][y] != 9:
					tmp[x][y] = 9
					break
					
		return tmp
		
	def numerateEmpty(self):
		tmp = self.field
		
		for x in range(self.sizeX):
			for y in range(self.sizeY):
				if tmp[x][y] >= 9:
					if x != 0:
						if y != 0:
							tmp[x - 1][y - 1] += 1
						if y != self.sizeY - 1:
							tmp[x - 1][y + 1] += 1
						tmp[x - 1][y] += 1
					if x != self.sizeX - 1:
						if y != 0:
							tmp[x + 1][y - 1] += 1
						if y != self.sizeY - 1:
							tmp[x + 1][y + 1] += 1
						tmp[x + 1][y] += 1
					if y != 0:
						tmp[x][y - 1] += 1
					if y != self.sizeY - 1:
						tmp[x][y + 1] += 1
						
		for x in range(self.sizeX):
			for y in range(self.sizeY):
				if tmp[x][y] >= 9:
					tmp[x][y] = 9
		
		return tmp

def _help():
	print("Usage: python3 main.py [options]...")
	print("    options:")
	print("        -h, --help                  Show this help screen.")
	print("        -g, --grid sizeX [sizeY]    Specify the size of the grid. (Default: 10 10)")
	print("        -m, --mines amount          Specify the amount of mines on the grid. (Default: 10)")
	quit(0)
	
def _grid():
	try:
		sizeX = int(sys.argv[i + 1])
		sizeY = int(sys.argv[i + 2])
	except (ValueError, IndexError):
		try:
			sizeX = int(sys.argv[i + 1])
			sizeY = sizeX
		except (ValueError, IndexError):
			print("Invalid grid size.")
			quit(-1)
	return (sizeX, sizeY)
			
def _mines():
	try:
		mines = int(sys.argv[i + 1])
		return mines
	except ValueError:
		print("Invalid amount of mines.")
		quit(-1)

if __name__ == "__main__":
	sizeX = 10
	sizeY = 10
	mines = 10
	
	for i in range(len(sys.argv)):
		match sys.argv[i]:
			case "--help":
				_help()
			
			case "-h":
				_help()
			
			case "--grid":
				sizeX, sizeY = _grid()
			
			case "-g":
				sizeX, sizeY = _grid()
			
			case "--mines":
				mines = _mines()
			
			case "-m":
				mines = _mines()
					
	if mines > sizeX * sizeY:
		print("More mines than cells in grid.")
		quit(-1)
		
	try:
		app = app(sizeX, sizeY, mines)
	except KeyboardInterrupt:
		pass
