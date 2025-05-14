

class Joueur:
	def __init__(self, pos, pv = 100, att = 1, spd = 2, head = None, body = None, first_arm = None, second_arm = None, first_leg = None, second_leg = None, etat = None):
		self.pv = pv
		self.att = att
		self.spd = spd
		self.head = head
		self.body = body
		self.first_arm = first_arm
		self.second_arm = second_arm
		self.first_leg = first_leg
		self.second_leg = second_leg
		self.etat = etat
		self.pos = pos

class Projectil:

	def __init__(self, pos, spd = 1):
		self.pos = pos
		self.spd = spd 

	def move(self):
		self.pos[0] += self.spd


