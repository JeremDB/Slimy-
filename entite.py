

class Joueur:
	def __init__(self, pos, pv = 100, att = 1, spd = 1, head = None, body = None, first_arm = None, second_arm = None, first_leg = None, second_leg = None, etat = None):
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

class Ennemie:
	def __init__(self, pos, pv = 100, att_dist = 1, att_cac = 1):
		self.pv = pv
		self.att_dist = att_dist
		self.att_cac = att_cac
		self.pos = pos


class Boss:
	def __init__(self, pos, loot, name, pv = 100, att_dist = 1, att_cac = 1):
		self.name = name
		self.pv = pv
		self.att_dist = att_dist
		self.att_cac = att_cac
		self.pos = pos
		self.loot = None



