from random import randint
from copy import deepcopy

class Ennemi:
	"""
	Class des ennemis,
	Propose de les faire défiler
	"""
	def __init__(self, pos: list, taille: tuple,forme: str, pv: int = 100, att_dist: int = 1, att_cac: int = 1):
		self.pv = pv
		self.att_dist = att_dist
		self.att_cac = att_cac
		self.taille = taille
		self.pos = pos
		self.type= forme

	def scroll(self, n: int):
		self.pos[0] -= n


class Boss:
	"""
	Class des boss
	Propose de les faire défiler
	"""
	def __init__(self, pos: list, loot: str = None, name: str = None, pv: int = 100, att_dist: int = 1, att_cac: int = 1):
		self.name = name
		self.pv = pv
		self.att_dist = att_dist
		self.att_cac = att_cac
		self.pos = pos
		self.loot = None

	def scroll(self, n: int):
		self.pos[0] -= n

class Decors:
	"""
	Class des décors
	"""
	def __init__(self, x: int, y: int, largeur: int, hauteur: int, couleur: "str"):
		self.__x = x
		self.__y = y
		self.__largeur = largeur
		self.__hauteur = hauteur
		self.__couleur = couleur 

	def get_pos(self) -> list:
		"""
		Renvoie le topleft du décors sous forme de list
		"""
		return [self.__x, self.__y]

	def get_largeur(self)-> int:
		"""
		Renvoie la largeur du décor
		"""
		return self.__largeur

	def get_hauteur(self) -> int:
		"""
		Renvoie la hauteur du décor
		"""
		return self.__hauteur

	def couleur(self) -> str:
		"""
		Renvoie la couleur du décor
		"""
		return self.__couleur

	def scroll(self, n:int):
		"""
		Permet de faire défiler le décors
		"""
		self.__x -= n

	def __repr__(self):
		return f"{self.__x,self.__y,self.__largeur,self.__hauteur,self.__couleur}"

class Levels:
	"""
	Class des niveaux
	"""
	def __init__(self,decors: list,ennemis:list,type = None):
		self.pos_x = 1920
		self.ennemis = ennemis
		self.decors = decors
		self.type = "Normal"

	def get_decors(self) -> list:
		"""
		Renvoie la liste des décors du niveau
		"""
		return self.decors

	def scroll(self,n: int):
		"""
		Fait défiler les ennemis, les décors du niveau et modifie sa position 
		"""
		self.pos_x -= n
		for ennemi in self.ennemis:
			ennemi.scroll(n)
		for decor in self.decors:
			decor.scroll(n)

	def decalage(self,pos: int):
		"""
		Permets de faire décaler un niveau pour l'aligner avec le précedents
		"""
		decal = -1920 - pos
		for decor in self.decors:
			decor.scroll(decal)
		for ennemi in self.ennemis:
			ennemi.scroll(decal)

#Premier niveau
niveau1 = Levels(
	[Decors(-80, 700, 160, 400, 'decor'),Decors(320, 580, 320, 20, 'decor'),Decors(640, 480, 240, 20, 'decor'),Decors(960, 440, 160, 20, 'decor'),Decors(1200, 360, 160, 20, 'decor'),Decors(80, 700, 880, 400, 'decor'),Decors(960, 700, 400, 400, 'decor'),Decors(1280, 620, 320, 480, 'decor'),Decors(1860, 700, 160, 400, 'decor'),Decors(1440, 580, 280, 520, 'decor')]
	,[Ennemi([1085,660],(40,40),"rond")]
	)
	
#Liste des niveaux bosss	
niveaux_boss = [
Levels(
	[Decors(-80, 700, 160, 400, 'decor'),Decors(800, 680, 80, 100, 'decor'),Decors(80, 660, 480, 480, 'decor'),Decors(560, 760, 320, 340, 'decor'),Decors(880, 780, 900, 320, 'decor'),Decors(640, 560, 280, 20, 'decor'),Decors(880, 440, 160, 20, 'decor'),Decors(1040, 320, 240, 20, 'decor'),Decors(1860, 700, 160, 400, 'decor'),Decors(1040, 560, 160, 20, 'decor')]
	,[]
	)
]

#Liste des niveaux
niveaux = [ 
Levels([#Niveau 1
	Decors(-80, 700, 160, 400, 'decor'),Decors(320, 860, 240, 20, 'decor'),Decors(320, 560, 240, 20, 'decor'),Decors(640, 800, 160, 20, 'decor'),Decors(640, 460, 240, 20, 'decor'),Decors(800, 740, 160, 20, 'decor'),Decors(960, 380, 240, 20, 'decor'),Decors(1320, 840, 160, 20, 'decor'),Decors(1520, 780, 80, 20, 'decor'),Decors(1680, 740, 200, 20, 'decor'),Decors(1360, 360, 240, 20, 'decor'),Decors(80, 700, 400, 420, 'decor'),Decors(1860, 700, 160, 400, 'decor'),Decors(880, 700, 480, 380, 'decor')]
	,[Ennemi([700,760],(40,40),"rond"),Ennemi([990,660],(40,40),"rond"),Ennemi([1245,610],(40,90),"ovale_haut")]
	),
Levels([#Niveau 2
	Decors(-80, 700, 160, 380, 'decor'),Decors(1440, 780, 160, 20, 'decor'),Decors(1680, 780, 200, 20, 'decor'),Decors(1040, 800, 320, 300, 'decor'),Decors(960, 740, 240, 600, 'decor'),Decors(80, 700, 480, 480, 'decor'),Decors(960, 700, 160, 400, 'decor'),Decors(640, 620, 400, 480, 'decor'),Decors(240, 580, 480, 520, 'decor'),Decors(1860, 700, 160, 400, 'decor'),Decors(380, 540, 480, 600, 'decor')]
	,[Ennemi([290,540],(40,40),"rond"),Ennemi([495,500],(40,40),"rond"),Ennemi([710,450],(40,90),"ovale_haut"),Ennemi([1490,690],(40,90),"ovale_haut")]
	)
]

def init_niveau():
	"""
	Renvoie la liste des deux premiers niveaux
	"""
	niv2 = deepcopy(niveaux[randint(0,len(niveaux)-1)])
	niv2.decalage(0)
	return [niveau1, niv2]

def ajuste_niveaux(levels: list,pos: int):
	"""
	Ajoute un niveau a la liste des niveaux et retire celui ayant complétement défilé
	"""
	nouveau = deepcopy(niveaux[randint(0,len(niveaux)-1)])
	nouveau.decalage(pos)
	levels.append(nouveau)
	levels.pop(0)
	return levels

def ajuste_niveaux_boss(levels: list,pos: int):
	"""
	Ajoute un niveau boss a la liste des niveaux et retire le précédent niveau
	"""
	nouveau = deepcopy(niveaux_boss[randint(0,len(niveaux_boss)-1)])
	nouveau.decalage(pos)
	levels.append(nouveau)
	levels.pop(0)
	return levels



nouveau_lvl = [
niveaux[1]
]
decors_de_base = [Decors(0,700,80,380,"decor"),Decors(1840,700,80,380,"decor")]
niveau_vide = [Levels(decors_de_base,[])]
