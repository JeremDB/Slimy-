from random import randint
from copy import deepcopy

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

niveau1 = Levels([Decors(0, 700, 80, 380, 'decor'),Decors(1840, 700, 80, 380, 'decor'),Decors(80, 700, 880, 380, 'decor'),Decors(320, 560, 320, 20, 'decor'),Decors(960, 700, 400, 380, 'decor'),Decors(1280, 620, 320, 480, 'decor'),Decors(1440, 580, 280, 520, 'decor'),Decors(640, 480, 240, 20, 'decor'),Decors(960, 440, 160, 20, 'decor'),Decors(1200, 360, 160, 20, 'decor')])
	
niveaux_boss = [Levels([Decors(0, 700, 80, 380, 'decor'),Decors(1840, 700, 80, 380, 'decor'),Decors(80, 660, 500, 480, 'decor'),Decors(480, 760, 400, 340, 'decor'),Decors(880, 780, 900, 320, 'decor'),Decors(640, 560, 160, 20, 'decor'),Decors(800, 680, 80, 100, 'decor'),Decors(800, 560, 160, 20, 'decor'),Decors(880, 440, 160, 20, 'decor'),Decors(1040, 320, 240, 20, 'decor'),Decors(1040, 560, 160, 20, 'decor')	])]

niveaux = [
	Levels([Decors(0, 700, 80, 380, 'decor'),Decors(1840, 700, 80, 380, 'decor'),Decors(0, 700, 400, 420, 'decor'),Decors(880, 700, 480, 380, 'decor'),Decors(320, 860, 240, 20, 'decor'),Decors(640, 800, 160, 20, 'decor'),Decors(800, 740, 160, 20, 'decor'),Decors(1360, 840, 160, 20, 'decor'),Decors(1520, 780, 80, 20, 'decor'),Decors(1680, 740, 160, 20, 'decor'),Decors(320, 520, 240, 20, 'decor'),Decors(640, 460, 240, 20, 'decor'),Decors(960, 380, 240, 20, 'decor'),Decors(1360, 360, 240, 20, 'decor')]),
	Levels([Decors(0, 700, 80, 380, 'decor'),Decors(1840, 700, 80, 380, 'decor'),Decors(80, 700, 480, 480, 'decor'),Decors(240, 580, 480, 480, 'decor'),Decors(640, 620, 400, 480, 'decor'),Decors(1040, 800, 320, 300, 'decor'),Decors(960, 700, 160, 400, 'decor'),Decors(1440, 780, 160, 20, 'decor'),Decors(1680, 780, 160, 20, 'decor'),Decors(960, 740, 240, 600, 'decor'),Decors(380, 540, 480, 600, 'decor'),Decors(420,560,200,600, 'decor')])
	]

def init_niveau():
	niv2 = deepcopy(niveaux[randint(0,len(niveaux)-1)])
	niv2.decalage()
	return [niveau1, niv2]

def ajuste_niveaux(levels):
	nouveau = deepcopy(niveaux[randint(0,len(niveaux)-1)])
	nouveau.decalage()
	levels.append(nouveau)
	levels.pop(0)
	return levels

def ajuste_niveaux_boss(levels):
	nouveau = deepcopy(niveaux_boss[randint(0,len(niveaux_boss)-1)])
	nouveau.decalage()
	levels.append(nouveau)
	levels.pop(0)
	return levels



nouveau_lvl = [
Levels([Decors(0, 700, 80, 380, 'decor'),
Decors(1840, 700, 80, 380, 'decor'),
Decors(80, 660, 500, 480, 'decor'),
Decors(480, 760, 400, 340, 'decor'),
Decors(880, 780, 900, 320, 'decor'),
Decors(640, 560, 160, 20, 'decor'),
Decors(800, 680, 80, 100, 'decor'),
Decors(800, 560, 160, 20, 'decor'),
Decors(880, 440, 160, 20, 'decor'),
Decors(1040, 320, 240, 20, 'decor'),
Decors(1040, 560, 160, 20, 'decor')
	])
	]
nb_niveau = len(niveaux)
decors_de_base = [Decors(0,700,80,380,"decor"),Decors(1840,700,80,380,"decor")]
niveau_vide = [Levels(decors_de_base)]
