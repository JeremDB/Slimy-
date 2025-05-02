

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
		return [self.__x + n, self.__y]

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

niveaux = [
	Levels([Decors(0, 700, 80, 380, 'terre'),Decors(1840, 700, 80, 380, 'terre'),Decors(80, 700, 880, 380, 'terre'),Decors(320, 560, 320, 20, 'terre'),Decors(960, 700, 400, 380, 'terre'),Decors(1280, 620, 320, 480, 'terre'),Decors(1440, 580, 280, 520, 'terre'),Decors(640, 480, 240, 20, 'terre'),Decors(960, 440, 160, 20, 'terre'),Decors(1200, 360, 160, 20, 'terre')])
	]

nouveau_lvl = [
Levels([Decors(0, 700, 80, 380, 'terre'),
Decors(1840, 700, 80, 380, 'terre'),
Decors(400, 680, 240, 380, 'terre'),
Decors(880, 700, 160, 360, 'terre'),
Decors(560, 540, 480, 0, 'terre'),
Decors(560, 540, 480, 0, 'terre'),
Decors(560, 480, 320, 120, 'terre'),
Decors(160, 500, 320, 60, 'terre'),
Decors(1120, 700, 480, 20, 'terre'),
Decors(1200, 940, 400, 60, 'terre')])
	]

decors_de_base = [Decors(0,700,80,380,"terre"),Decors(1840,700,80,380,"terre")]
niveau_vide = [Levels(decors_de_base)]

"""
dico = [{'x': 78, 'y': 705, 'largeur': 250, 'hauteur': 374}, {'x': 554, 'y': 717, 'largeur': 212, 'hauteur': 362}, {'x': 1018, 'y': 727, 'largeur': 151, 'hauteur': 352}, {'x': 647, 'y': 561, 'largeur': 417, 'hauteur': -4}, {'x': 647, 'y': 561, 'largeur': 417, 'hauteur': -4}, {'x': 716, 'y': 509, 'largeur': 314, 'hauteur': 107}, {'x': 281, 'y': 529, 'largeur': 284, 'hauteur': 58}, {'x': 1243, 'y': 735, 'largeur': 412, 'hauteur': 6}, {'x': 1280, 'y': 965, 'largeur': 399, 'hauteur': 49}, {'x': 537, 'y': 390, 'largeur': 1142, 'hauteur': 624}]

for decor in dico:	
	decor["x"] = ((decor["x"] // 80) - 1) * 80
	decor["y"] = ((decor["y"] // 20) - 1) * 20	
	decor["largeur"] = ((decor["largeur"] // 80) + 1) * 80
	decor["hauteur"] = ((decor["hauteur"] // 20) + 1) * 20
	decors_de_base.append(Decors(decor["x"], decor["y"],decor["largeur"],decor["hauteur"],"terre"))

for decor in decors_de_base : 
	print(f"Decors{decor},")

"""
