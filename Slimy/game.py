
import os
import sys
import pgzrun
import pygame
import level
from random import randint, choice
import entite


WIDTH = 1920
HEIGHT = 1080
TITLE = "Slimy!"

class Couleurs():
    """
    Propose une méthode permettant de renvoyer une couleur aléatoire
    Contient les constantes des couleurs utilisés
    """
    fond = (150,207,255)
    terre = (150,90,20)
    slime = (255,110,110)


    def color(c):
    	if c == "terre":
    		return Couleurs.terre

    @staticmethod
    def random() -> tuple:
        """
        Renvoie une couleur aléatoire au format (R,G,B)
        """
        return (randint(0,255),randint(0,255),randint(0,255))

def update():
	"""
	"""
	check_keys()

def draw():
	"""
	"""
	screen.fill(Couleurs.fond)
	rect = Rect((500,800),(300,60))
	draw_levels()
	screen.draw.filled_rect(rect,(Couleurs.terre))
	draw_player()

def draw_player():
	x = player.pos[0]
	y = player.pos[1]
	screen.draw.filled_circle((x,y),50,Couleurs.slime)

def draw_levels():
	"""
	"""
	for lvl in levels :
		for decor in lvl.get_decors():
			draw_decor(decor)

def draw_decor(decor):
	topleft = decor.get_pos()
	largeur = decor.get_largeur()
	hauteur = decor.get_hauteur()
	couleur = Couleurs.color(decor.couleur())
	rect_decor = Rect(topleft,(largeur,hauteur))
	screen.draw.filled_rect(rect_decor,couleur)

def check_keys():
    """
    Verifie les touches enfoncée 
    Echap pour quitter le jeu
    """

    # Echap pour quitter le jeu
    if keyboard.ESCAPE:
        exit()

levels = [level.lvl]
player = entite.Joueur([0,0])

os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()
