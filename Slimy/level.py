from random import randint
from copy import deepcopy

class Ennemi:
	"""
	Class des ennemis,
	Propose de les faire défiler
	"""
	def __init__(self, pos: list, taille: tuple, forme: str, pv: int = None, atk_dist: int = None, atk_cac:int  = None,vitesse: list = None):
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
	def __init__(self, pos: int, forme: tuple, name: str, loot: str = None, pv: int = None, atk_dist: int = None, atk_cac: int = None,vitesse: list = None):
		self.name = name
		self.pv = pv
		self.atk_dist = atk_dist
		self.atk_cac = atk_cac
		self.taille = forme 
		self.peut_tirer = True
		self.couldown = 0
		self.pos = pos
		self.loot = loot
		self.vitesse = vitesse

	def scroll(self, n: int):
		"""
		Permet de faire défiler les boss
		"""
		self.pos[0] -= n

	def prend_dgt(self, n:int):
		self.pv -= n

	def est_mort(self) -> bool :
		return self.pv <= 0

	def rise_couldown(self):
		if not self.peut_tirer: 	
			self.couldown += 1 
		if self.couldown > 120 :
			self.couldown = 0
			self.peut_tirer = True

	def move(self) :
		if self.vitesse != None :
			self.pos[0] += self.vitesse[0]
			self.pos[1] += self.vitesse[1]

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

	def get_forme(self):
		return self.__forme

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
		self.boss = boss

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
(240,160,80)*20
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
	,[Ennemi.creer_carapace([1085,670])], 
	)
	
#Liste des niveaux boss
niveaux_boss = [
#Roi_Gluant
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
	,[Boss([1680,400],(80,430),"Roi_Gluant", pv= 250, atk_cac =15 )],
	boss = True
	),
#Gluant_Bulle
Levels(
	[Decors(-80, 700, 160, 1000, 'decor','bloc'),
	Decors(80,700,240,1000,'decor','bloc'),
	Decors(320,660,400,1000,'decor','bloc'),
	Decors(720,700,400,1000,'decor','bloc'),
	Decors(1120,700,400,1000,'decor','bloc'),
	Decors(1520,700,320,1000,'decor','bloc'),
	Decors(620,540,240,20,'decor','plat'),
	Decors(860,540,240,20,'decor','plat'),
	Decors(1100,540,240,20,'decor','plat'),
	Decors(820,420,160,20,'decor','plat'),
	Decors(980,420,160,20,'decor','plat'),
	Decors(1840, 700, 160, 1000, 'decor','bloc')],
	[Boss([1680,600],(80,230),"Roi_Gluant", pv= 250, atk_cac =15 )],
	boss = True
	),
#Agluantin
Levels(
	[Decors(-80, 700, 160, 1000, 'decor','bloc'),
	Decors(80,700,240,1000,'decor','bloc'),
	Decors(320,660,240,1000,'decor','bloc'),
	Decors(1520,700,320,1000,'decor','bloc'),
	Decors(540,540,240,20,'decor','plat'),
	Decors(860,420,240,20,'decor','plat'),
	Decors(1180,300,240,20,'decor','plat'),
	Decors(1840, 700, 160, 1000, 'decor','bloc')],
	[Boss([1680,120],(80,1000),"Roi_Gluant", pv= 250, atk_cac =15 )],
	boss = True
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
	Decors(1680, 720, 160, 20, 'decor','plat'),
	Decors(1360, 340, 240, 20, 'decor','plat'),
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
#Niveau 3
Levels([
	Decors(-80, 700, 160, 1000, 'decor','bloc'),
	Decors(120, 660, 240, 20, 'decor','plat'),
	Decors(640, 580, 320, 20, 'decor','plat'),
	Decors(480, 860, 160, 20, 'decor','plat'),
	Decors(880, 780, 160, 20, 'decor','plat'),
	Decors(1200, 740, 320, 20, 'decor','plat'),
	Decors(1040, 520, 320, 20, 'decor','plat'),
	Decors(1440, 640, 240, 20, 'decor','plat'),
	Decors(1840, 700, 160, 1000, 'decor','bloc')],
	[]
	),
#Niveau 4 
Levels([
	Decors(-80,700,160,1000,'decor','bloc'),
	Decors(80,700,160,1000,'decor','bloc'),
	Decors(240,640,240,1000,'decor','bloc'),
	Decors(480,580,160,1000,'decor','bloc'),
	Decors(640,500,160,1000,'decor','bloc'),
	Decors(800,800,240,20,'decor','plat'),
	Decors(1160,740,160,20,'decor','plat'),
	Decors(1000,420,240,20,'decor','plat'),
	Decors(1380,440,160,20,'decor','plat'),
	Decors(1600,720,240,20,'decor','plat'),
	Decors(1840,700,160,1000,'decor','bloc')],
	[Ennemi.creer_rond([340,600]),
	Ennemi.creer_ovale_haut([1090,330])]
	),
#Niveau 5
Levels([
	Decors(-80,700,160,1000,'decor','bloc'),
	Decors(80,720,160,1000,'decor','bloc'),
	Decors(240,780,240,1000,'decor','bloc'),
	Decors(480,880,400,1000,'decor','bloc'),
	Decors(880,920,400,1000,'decor','bloc'),
	Decors(1280,860,240,1000,'decor','bloc'),
	Decors(1520,800,160,1000,'decor','bloc'),
	Decors(1680,760,160,1000,'decor','bloc'),
	Decors(300,600,240,20,'decor','plat'),
	Decors(680,540,240,20,'decor','plat'),
	Decors(1000,520,240,20,'decor','plat'),
	Decors(1400,440,160,20,'decor','plat'),
	Decors(1840,700,160,1000,'decor','bloc')],
	[Ennemi.creer_rond([750,840]),
	Ennemi.creer_rond([1050,480]),
	Ennemi.creer_rond([860,500]),
	Ennemi.creer_ovale_haut([1420,770]),
	Ennemi.creer_ovale_haut([1720,670])]
	)
]

def init_niveau():
	"""
	Renvoie la liste des deux premiers niveaux
	"""
	niv2 = deepcopy(niveaux[randint(0,len(niveaux)-1)])
	niv2.decalage(0)
	return [deepcopy(niveau1), niv2]

def ajuste_niveaux(levels,pos):
	"""
	Ajoute un niveau a la liste des niveaux et retire celui ayant complétement défilé
	"""
	nouveau = deepcopy(niveaux[randint(0,len(niveaux)-1)])
	nouveau.decalage(pos)
	levels.append(nouveau)
	levels.pop(0)
	return levels

def ajuste_niveaux_boss(levels,pos,monde):
	"""
	Ajoute un niveau boss a la liste des niveaux et retire le précédent niveau
	"""
	nouveau = deepcopy(niveaux_boss[(monde+2)%3])
	nouveau.decalage(pos)
	levels.append(nouveau)
	levels.pop(0)
	return levels



nouveau_lvl = [
niveaux_boss[2]
]


decors_de_base = [Decors(-80,700,80,1000,"decor",'bloc'),Decors(1840,700,160,1000,"decor",'bloc')]
niveau_vide = [Levels(decors_de_base,[])]
