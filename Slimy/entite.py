class Joueur:
	def __init__(self, pos, pv = 100, atk = 1, spd = 2, head = None, body = None, first_arm = None, second_arm = None, first_leg = None, second_leg = None, etat = None):
		self.pv = pv
		self.atk = atk
		self.spd = spd
		self.head = head
		self.body = body
		self.first_arm = first_arm
		self.second_arm = second_arm
		self.first_leg = first_leg
		self.second_leg = second_leg
		self.etat = etat
		self.pos = pos
		self.invincible = False

	def prend_dgt(self,n: int):
		self.pv -= n

	def est_mort(self) -> bool:
		return self.pv <= 0

class Projectil:

	def __init__(self, pos,atk,direction,spd = 1,taille: tuple = None ):
		self.pos = pos
		self.atk = atk
		self.direction = direction
		self.spd = spd 
		self.taille = taille

	def move(self):
		self.pos[0] += self.spd*self.direction[0]
		self.pos[1] += self.spd*self.direction[1]


