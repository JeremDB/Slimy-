
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
    jungle = (100,120,20)
    terre_brule = (110,50,10)
    slime = (255,110,110)
    projectil = (255,80,80)
    noir = (0,0,0)


    def color(c):
        if c == "decor":
            if monde % 3 == 0:
                return Couleurs.terre_brule
            if monde % 3 == 1:
                return Couleurs.terre
            if monde % 3 == 2:
                return Couleurs.jungle

    @staticmethod
    def random() -> tuple:
        """
        Renvoie une couleur aléatoire au format (R,G,B)
        """
        return (randint(0,255),randint(0,255),randint(0,255))

def update():
    global force_gravite, w, count_frame,levels,stage, a_tire, count_frame2, boss_kill, monde
    """
    """
    count_frame += 1

    check_keys()

    if stage < 5 :
        scrolling()
        if check_collisisons_droite() == v :
            player.pos[0] = v - largeur_player
    if levels[1].get_decors()[0].get_pos()[0] <= 0 :
        if stage == 3 :
            level.ajuste_niveaux_boss(levels)
            stage += 1 
        else :
            level.ajuste_niveaux(levels)
            stage += 1

    if player.etat == "saut":
        gravite()
    if check_collisisons_down() == -1 : #Ne touche pas le sol
        calc_speed()
        gravite()
    if check_collisisons_top() == -1: #Ne touche pas le bas d'un décor
        if check_collisisons_down() == w: # si tu touche le haut d'un décor
            player.pos[1] = w - hauteur_player
            player.etat = "sol"
            
            
    if check_collisisons_top() == w and player.etat == "saut" : # Si tu touche le bas du décor
        player.pos[1] = w
        player.etat = "air"
        force_gravite = -0.2
        gravite()
        print(check_collisisons_down())
        
    if boss_kill: 
        stage = 0
        monde += 1
        boss_kill = False


    if a_tire == True:
        move_projectil()
    if count_frame2 >= 5 :
        count_frame2 = 0
    count_frame2 += 1

def scrolling():
    for lvl in levels :
        lvl.scroll(2)       


def check_collisisons_down():
    global w, largeur
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
            if pygame.Rect.colliderect(rect_player,rect_decor) and y < w:
                return w
    return -1

def check_collisisons_top():
    global w, largeur
    x = player.pos[0]
    y = player.pos[1] - force_gravite
    rect_player = Rect((x,y),(50,40))
    for lvl in levels :
        for decor in lvl.get_decors():
            v = decor.get_pos()[0]
            w = decor.get_pos()[1] + decor.get_hauteur()
            largeur = decor.get_largeur()
            hauteur = decor.get_hauteur()
            rect_decor = Rect((v,w),(largeur,hauteur))
            if pygame.Rect.colliderect(rect_player,rect_decor):
                return w
    return -1

def check_collisisons_droite():
    global v, largeur
    x = player.pos[0]
    y = player.pos[1] 
    rect_player = Rect((x,y),(50,40))
    for lvl in levels :
        for decor in lvl.get_decors():
            v = decor.get_pos()[0]
            w = decor.get_pos()[1]
            largeur = decor.get_largeur()
            hauteur = decor.get_hauteur()
            rect_decor = Rect((v,w),(largeur,hauteur))
            if pygame.Rect.colliderect(rect_player,rect_decor) and y < w:
                return v
    return -1

def check_collisisons_gauche():
    global v, largeur
    x = player.pos[0]
    y = player.pos[1] 
    rect_player = Rect((x,y),(50,40))
    for lvl in levels :
        for decor in lvl.get_decors():
            v = decor.get_pos()[0] 
            w = decor.get_pos()[1]
            largeur = decor.get_largeur()
            hauteur = decor.get_hauteur()
            rect_decor = Rect((v,w),(largeur,hauteur))
            if pygame.Rect.colliderect(rect_player,rect_decor) and y < w:
                    return v 
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
    draw_ui()

def draw_ui():
    screen.draw.text(("Stage :"), (25, 100), fontsize=60, color = Couleurs.noir)
    screen.draw.text((str(stage)), (170, 100), fontsize=60, color = Couleurs.noir)
    screen.draw.text(("Monde :"), (25, 150), fontsize=60, color = Couleurs.noir)
    screen.draw.text((str(monde)), (200, 150), fontsize=60, color = Couleurs.noir)

def draw_player():
    x = player.pos[0]
    y = player.pos[1]
    rect = Rect((x,y),(largeur_player,hauteur_player))
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
        
    if keyboard.P :
        boss_kill = True
    
    if keyboard.SPACE:
        if count_frame > 10 and player.etat == "sol":
            force_gravite = -1
            player.etat = "saut"
            force_gravite -= 4
            count_frame = 0
    if keyboard.D:
        player.pos[0] += 5
    if keyboard.Q:
        if check_collisisons_gauche() == -1:
            player.pos[0] -=5
        if check_collisisons_gauche() == v:
            player.pos[0] = v + largeur - 2
        

levels = level.init_niveau()
player = entite.Joueur([50,660])
gravity = 2
force_gravite = -1 
hauteur_player = 40
largeur_player = 50
largeur = 0
w = 0
v = 0
count_frame2 = 0
count_frame = 0
stage = 1
monde = 1
liste_tirs = []
a_tire = False
boss_kill = False

os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()
