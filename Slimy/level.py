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

class Levels:

	def __init__(self,decors,type = None):
		self.decors = decors
		self.type = "Normal"

	def get_decors(self):
		return self.decors

decors = [Decors(0,700,1920,380,"terre"),Decors(900,500,450,50,"terre")]
lvl = Levels(decors)
