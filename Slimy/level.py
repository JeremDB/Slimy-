class Decors:

	def __init__(self, x, y, largeur, hauteur, couleur):
		self.__x = x
		self.__y = y
		self.__largeur = largeur
		self.__hauteur = hauteur
		self.__couleur = couleur 

	def get_pos(self):
		return [self.__x, self.__y]

	def scroll(self, n):
		return [self.__x + n, self.__y]
