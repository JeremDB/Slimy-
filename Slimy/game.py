
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
    projectil = (255,80,80)


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
    global force_gravite, w, count_frame,levels,stage, a_tire
    """
    """
    count_frame += 1

    check_keys()

    if stage <= level.nb_niveau +1  :
        scrolling()
    if levels[1].get_decors()[0].get_pos()[0] <= 0 :
        if stage < level.nb_niveau :
            level.ajuste_niveaux(levels)

    if player.etat == "saut":
        gravite()
    if check_collisisons_down() == -1:
        calc_speed()
        gravite()
    if check_collisisons_down() == w:
        player.pos[1] = w - hauteur_player
        player.etat = None
    if a_tire == True:
		move_projectil()
	if count_frame >= 5 :
		count_frame = 0
	count_frame += 1

def scrolling():
    for lvl in levels :
        lvl.scroll(5)       

    
def check_collisisons_down():
    global w 
    x = player.pos[0]
    y = player.pos[1] + force_gravite
    rect_player = Rect((x,y),(50,40))
    for lvl in levels :
        for decor in lvl.get_decors():
            v = decor.get_pos()[0]
            w = decor.get_pos()[1]
            largeur = decor.get_largeur()
            hauteur = decor.get_hauteur()
            rect_decor = Rect((v,w),(largeur,hauteur))
            if pygame.Rect.colliderect(rect_player,rect_decor):
                return w
    return -1

def gravite():
    global force_gravite
    player.pos[1] += force_gravite

def calc_speed():
  global force_gravite
  v_y = force_gravite
  v_y = v_y + 0.10*gravity
  force_gravite = v_y
  return

def draw():
    """
    """
    screen.fill(Couleurs.fond)
    draw_levels()
    draw_player()
    draw_projectil()

def draw_player():
    x = player.pos[0]
    y = player.pos[1]
    rect = Rect((x,y),(50,hauteur_player))
    screen.draw.filled_rect(rect,Couleurs.slime)

def draw_projectil():
	global liste_tirs
	for tirs in liste_tirs:
		print(tirs)
		x = tirs[0]
		y = tirs[1] 
		rect = Rect((x,y),(15,15))
		screen.draw.filled_rect(rect, Couleurs.projectil)

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

def slimy_tire():
	global liste_tirs, player
	liste_tirs.append([player.pos[0] + 50, player.pos[1] + 13])

def move_projectil():
	global liste_tirs
	for tir in liste_tirs:
		tir[0] += player.spd + 5
	print(liste_tirs)

	
def on_mouse_down(button):
	global a_tire
	#if a_tire == False:
	if button == mouse.LEFT:
		slimy_tire()
		a_tire = True

def check_keys():
    global count_frame,force_gravite
    """
    Verifie les touches enfoncée 
    Echap pour quitter le jeu
    """

    # Echap pour quitter le jeu
    if keyboard.ESCAPE:
        exit()
    if keyboard.SPACE:
        if count_frame > 10 and player.etat != "saut":
            force_gravite = -1
            player.etat = "saut"
            force_gravite -= 4
            count_frame = 0
    if keyboard.D:
        player.pos[0] += 5
    if keyboard.Q:
        player.pos[0] -= 5

levels = level.init_niveau()
player = entite.Joueur([50,660])
gravity = 2
force_gravite = -1 
hauteur_player = 40
w = 0
count_frame = 0
stage = 1
liste_tirs = []
a_tire = False

os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()
