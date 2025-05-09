from random import randint

class Decors:

	def __init__(self, x, y, largeur, hauteur, couleur):
		self.__x = x
		self.__y = y
		self.__largeur = largeur
		self.__hauteur = hauteur
		self.__couleur = couleur 

	def get_pos(self):
		return [self.__x, self.__y]

	def get_largeur(self):
		return self.__largeur

	def get_hauteur(self):
		return self.__hauteur

	def couleur(self):
		return self.__couleur

	def scroll(self, n):
		self.__x -= n

	def __repr__(self):
		return f"{self.__x,self.__y,self.__largeur,self.__hauteur,self.__couleur}"

class Levels:

	def __init__(self,decors,type = None):
		self.decors = decors
		self.type = "Normal"

	def get_decors(self):
		return self.decors

	def add_decor(self,decor):
		self.decors.append(decor)

	def scroll(self,n):
		for decor in self.decors:
			decor.scroll(n)

	def decalage(self):
		for decor in self.decors :
			decor.scroll(-1920)

niveau1 = Levels([Decors(0, 700, 80, 380, 'terre'),Decors(1840, 700, 80, 380, 'terre'),Decors(80, 700, 880, 380, 'terre'),Decors(320, 560, 320, 20, 'terre'),Decors(960, 700, 400, 380, 'terre'),Decors(1280, 620, 320, 480, 'terre'),Decors(1440, 580, 280, 520, 'terre'),Decors(640, 480, 240, 20, 'terre'),Decors(960, 440, 160, 20, 'terre'),Decors(1200, 360, 160, 20, 'terre')]),
	

niveaux = [
	Levels([Decors(0, 700, 80, 380, 'terre'),Decors(1840, 700, 80, 380, 'terre'),Decors(0, 700, 400, 420, 'terre'),Decors(880, 700, 480, 380, 'terre'),Decors(320, 860, 240, 20, 'terre'),Decors(640, 800, 160, 20, 'terre'),Decors(800, 740, 160, 20, 'terre'),Decors(1360, 840, 160, 20, 'terre'),Decors(1520, 780, 80, 20, 'terre'),Decors(1680, 740, 160, 20, 'terre'),Decors(320, 520, 240, 20, 'terre'),Decors(640, 460, 240, 20, 'terre'),Decors(960, 380, 240, 20, 'terre'),Decors(1360, 360, 240, 20, 'terre')]),
	Levels([Decors(0, 700, 80, 380, 'terre'),Decors(1840, 700, 80, 380, 'terre'),Decors(-80, 640, 560, 480, 'terre'),Decors(240, 580, 480, 480, 'terre'),Decors(640, 620, 400, 480, 'terre'),Decors(1040, 800, 320, 300, 'terre'),Decors(960, 700, 160, 400, 'terre'),Decors(1440, 780, 160, 20, 'terre'),Decors(1680, 780, 160, 20, 'terre'),Decors(960, 740, 240, 600, 'terre'),Decors(380, 540, 480, 600, 'terre'),Decors(420,560,200,600, 'terre')
	])
	]
def premiers_niveaux():
	niv2 = niveaux[randint(len(niveaux)-1)]
	niv2.decalage()
	return [niveau1, niv2]

def ajuste_niveaux():
	pass


nouveau_lvl = [
Levels([Decors(0, 700, 80, 380, 'terre'),
Decors(1840, 700, 80, 380, 'terre'),
Decors(-80, 640, 560, 480, 'terre'),
Decors(240, 580, 480, 480, 'terre'),
Decors(640, 620, 400, 480, 'terre'),
Decors(1040, 800, 320, 300, 'terre'),
Decors(960, 700, 160, 400, 'terre'),
Decors(1440, 780, 160, 20, 'terre'),
Decors(1680, 780, 160, 20, 'terre'),
Decors(960, 740, 240, 600, 'terre'),
Decors(380, 540, 480, 600, 'terre'),
Decors(420,560,200,600, 'terre')
	])
	]

decors_de_base = [Decors(0,700,80,380,"terre"),Decors(1840,700,80,380,"terre")]
niveau_vide = [Levels(decors_de_base)]

