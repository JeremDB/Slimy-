from random import randint
from copy import deepcopy

class Ennemi:
	"""
	Class des ennemis,
	Propose de les faire défiler
	"""
	def __init__(self, pos: list, taille: tuple, forme: str, pv: int = None, atk_dist: int = None, atk_cac:int  = None,vitesse = None):
		self.pv = pv
		self.atk_dist = atk_dist
		self.atk_cac = atk_cac
		self.taille = taille
		self.pos = pos
		self.type= forme
		self.vitesse= vitesse 

	def scroll(self, n: int):
		"""
		Permet de faire défiler les ennemis
		"""
		self.pos[0] -= n

	def prend_dgt(self, n: int):
		self.pv -= n

	def est_mort(self) -> bool :
		return self.pv <= 0

	def move(self) :
		if self.vitesse != None :
			self.pos[0] += self.vitesse[0]
			self.pos[1] += self.vitesse[1]

	@classmethod
	def creer_rond(cls,pos):
		return cls(pos,(40,40),"rond",pv = 20,atk_cac = 1)

	@classmethod
	def creer_ovale_haut(cls,pos):
		return cls(pos,(40,90),"ovale_haut",pv = 50, atk_cac = 5)
	
	@classmethod
	def creer_carapace(cls,pos):
		return cls(pos,(60,30),"carapace",pv = 15, atk_cac = 1, vitesse = [-1,0])



class Boss:
	"""
	Class des boss
	Propose de les faire défiler
	"""
	def __init__(self, pos: int, forme: tuple, name: str, loot: str = None, pv: int = None, atk_dist: int = None, atk_cac: int = None):
		self.name = name
		self.pv = pv
		self.atk_dist = atk_dist
		self.atk_cac = atk_cac
		self.taille = forme 
		self.pos = pos
		self.loot = None

	def scroll(self, n: int):
		"""
		Permet de faire défiler les boss
		"""
		self.pos[0] -= n

	def prend_dgt(self, n:int):
		self.pv -= n

	def est_mort(self) -> bool :
		return self.pv <= 0

class Decors:
	"""
	Class des décors
	"""
	def __init__(self, x, y, largeur, hauteur, couleur,forme = None):
		self.__x = x
		self.__y = y
		self.__forme = forme
		self.__largeur = largeur
		self.__hauteur = hauteur
		self.__couleur = couleur 

	def get_pos(self):
		"""
		Renvoie le topleft du décors sous forme de list
		"""
		return [self.__x, self.__y]

	def get_largeur(self):
		"""
		Renvoie la largeur du décor
		"""
		return self.__largeur

	def get_hauteur(self):
		"""
		Renvoie la hauteur du décor
		"""
		return self.__hauteur

	def couleur(self):
		"""
		Renvoie la couleur du décor
		"""
		return self.__couleur

	def scroll(self, n):
		"""
		Permet de faire défiler le décors
		"""
		self.__x -= n

	def __repr__(self):
		return f"{self.__x,self.__y,self.__largeur,self.__hauteur,self.__couleur}"

class Levels:
	"""
	Class des niveaux
	Propose de les décaler entierement et de les faire défiler
	"""
	def __init__(self,decors,ennemis,boss = None):
		self.pos_x = 1920
		self.ennemis = ennemis
		self.decors = decors

	def get_decors(self):
		"""
		Renvoie la liste des décors du niveau
		"""
		return self.decors


	def add_decor(self,decor):
		self.decors.append(decor)

	def scroll(self,n):
		"""
		Fait défiler les ennemis, les décors du niveau et modifie sa position 
		"""
		self.pos_x -= n
		for ennemi in self.ennemis :
			ennemi.scroll(n)
		for decor in self.decors:
			decor.scroll(n)

	def decalage(self,pos):
		"""
		Permets de faire décaler un niveau pour l'aligner avec le précedents
		"""
		decal = -1920 - pos
		for decor in self.decors :
			decor.scroll(decal)
		for ennemi in self.ennemis:
			ennemi.scroll(decal)

"""
Décors de tailles : 
(400,240,160,80)*1000,
(240,160,80)*
"""

#Premier niveau
niveau1 = Levels(
	[Decors(-80, 700, 160, 1000, 'decor','bloc'),
	Decors(320, 580, 160, 20, 'decor','plat'),
	Decors(480, 580, 160, 20, 'decor','plat'),
	Decors(640, 480, 240, 20, 'decor','plat'),
	Decors(960, 440, 160, 20, 'decor','plat'),
	Decors(1200, 360, 160, 20, 'decor','plat'),
	Decors(80, 700, 400, 1000, 'decor','bloc'),
	Decors(480, 700, 400, 1000, 'decor','bloc'),
	Decors(880, 700, 400, 1000, 'decor','bloc'),
	Decors(1280, 620, 160, 1000, 'decor','bloc'),
	Decors(1440, 620, 160, 1000, 'decor','bloc'),
	Decors(1440, 580, 280, 1000, 'decor','bloc'),
	Decors(1840, 700, 160, 1000, 'decor','bloc')]
	,[Ennemi.creer_carapace([1085,670])]
	)
	
#Liste des niveaux boss
niveaux_boss = [
Levels(
	[Decors(-80, 700, 160, 400, 'decor','bloc'),
	Decors(620, 560, 240, 20, 'decor','plat'),
	Decors(840, 440, 160, 20, 'decor','plat'),
	Decors(1000, 560, 160, 20, 'decor','plat'),
	Decors(1000, 320, 240, 20, 'decor','plat'),
	Decors(80, 660, 240, 1000, 'decor','bloc'),
	Decors(320,660,240,1000,'decor','bloc'),
	Decors(560, 760, 240, 1000, 'decor','bloc'),
	Decors(800, 680, 80, 1000, 'decor','bloc'),
	Decors(880, 780, 400, 1000, 'decor','bloc'),	
	Decors(1280, 780, 240, 1000, 'decor','bloc'),	
	Decors(1520, 780, 160, 1000, 'decor','bloc'),	
	Decors(1680, 780, 160, 1000, 'decor','bloc'),
	Decors(1840, 700, 160, 1000, 'decor','bloc')]
	,[Boss([1680,400],(80,400),"Roi_Gluant", pv= 250, atk_cac =15 )]
	)
]

#Liste des niveaux
niveaux = [
#Niveau 1 
Levels([
	Decors(-80, 700, 160, 400, 'decor','bloc'),
	Decors(480, 860, 80, 20, 'decor','plat'),
	Decors(320, 560, 240, 20, 'decor','plat'),
	Decors(640, 800, 160, 20, 'decor','plat'),
	Decors(640, 460, 240, 20, 'decor','plat'),
	Decors(800, 740, 80, 20, 'decor','plat'),
	Decors(960, 380, 240, 20, 'decor','plat'),
	Decors(1360, 840, 160, 20, 'decor','plat'),
	Decors(1560, 780, 80, 20, 'decor','plat'),
	Decors(1680, 740, 160, 20, 'decor','plat'),
	Decors(1360, 360, 240, 20, 'decor','plat'),
	Decors(80, 700, 400, 420, 'decor','bloc'),# termine en 480
	Decors(880, 700, 240, 380, 'decor','bloc'),# commence en 880
	Decors(1120, 700, 240, 380, 'decor','bloc'), # termine en 1360
	Decors(1840, 700, 160, 400, 'decor','bloc')]
	,[Ennemi.creer_rond([700,760]),
	Ennemi.creer_rond([990,660]),
	Ennemi.creer_ovale_haut([1245,610])]
	),

#Niveau 2
Levels([
	Decors(-80, 700, 160, 380, 'decor','bloc'),
	Decors(1440, 780, 160, 20, 'decor','plat'),
	Decors(1760, 780, 80, 20, 'decor','plat'),
	Decors(1200, 800, 160, 1000, 'decor','bloc'),
	Decors(1120, 740, 80, 1000, 'decor','bloc'),
	Decors(80, 700, 160, 1000, 'decor','bloc'),
	Decors(1040, 700, 80, 1000, 'decor','bloc'),
	Decors(880, 620, 160, 1000, 'decor','bloc'),
	Decors(240, 580, 160, 1000, 'decor','bloc'),
	Decors(400, 540, 240, 1000, 'decor','bloc'),#debut 380
	Decors(640, 540, 240, 1000, 'decor','bloc'),#fin 860
	Decors(1840, 700, 160, 1000, 'decor','bloc')]
	,[Ennemi.creer_rond([290,540]),
	Ennemi.creer_rond([495,500]),
	Ennemi.creer_ovale_haut([710,450]),
	Ennemi.creer_ovale_haut([1490,690])]
	),
Levels([
	Decors(-80, 700, 160, 380, 'decor','bloc'),
	Decors(120, 660, 240, 20, 'decor','plat'),
	Decors(640, 580, 320, 20, 'decor','plat'),
	Decors(480, 860, 160, 20, 'decor','plat'),
	Decors(880, 780, 160, 20, 'decor','plat'),
	Decors(1200, 740, 320, 20, 'decor','plat'),
	Decors(1040, 520, 320, 20, 'decor','plat'),
	Decors(1440, 640, 240, 20, 'decor','plat'),
	Decors(1840, 700, 160, 1000, 'decor','bloc')],
	[]
	)
]

def init_niveau():
	"""
	Renvoie la liste des deux premiers niveaux
	"""
	niv2 = deepcopy(niveaux[randint(0,len(niveaux)-1)])
	niv2.decalage(0)
	return [niveau1, niv2]

def ajuste_niveaux(levels,pos):
	"""
	Ajoute un niveau a la liste des niveaux et retire celui ayant complétement défilé
	"""
	nouveau = deepcopy(niveaux[randint(0,len(niveaux)-1)])
	nouveau.decalage(pos)
	levels.append(nouveau)
	levels.pop(0)
	return levels

def ajuste_niveaux_boss(levels,pos):
	"""
	Ajoute un niveau boss a la liste des niveaux et retire le précédent niveau
	"""
	nouveau = deepcopy(niveaux_boss[randint(0,len(niveaux_boss)-1)])
	nouveau.decalage(pos)
	levels.append(nouveau)
	levels.pop(0)
	return levels



nouveau_lvl = [
niveaux[2]
]


decors_de_base = [Decors(-80,700,80,1000,"decor",'bloc'),Decors(1840,700,160,1000,"decor",'bloc')]
niveau_vide = [Levels(decors_de_base,[])]
