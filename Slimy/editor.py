
import os
import sys
import pgzrun
import pygame
import level
from random import randint, choice

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
    pics = (150,150,150)

    def color(c):
        if c == "terre":
            return Couleurs.terre
        if c == "pics":
            return Couleurs.pics

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
    draw_levels()

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

def ajoute_decors(nv):
    global levels
    levels[0].add_decor(level.Decors(nv["x"],nv["y"],nv["largeur"],nv["hauteur"],"terre"))

def on_mouse_down(pos, button):
    global topleft,bottomright,decors
    if button == mouse.LEFT :
        topleft = pos
    if button == mouse.RIGHT :
        bottomright = pos 
    if button == mouse.MIDDLE and topleft != None and bottomright != None:
        nv = {
            "x" : topleft[0],
            "y" : topleft[1],
            "largeur" : bottomright[0] - topleft[0],
            "hauteur" : bottomright[1] - topleft[1]
            }
        decors.append(nv)
        ajoute_decors(nv)

def check_keys():
    """
    Verifie les touches enfoncée 
    Echap pour quitter le jeu
    """
    global topleft, bottomright
    if keyboard.C :
        topleft = None
        bottomright = None
    # Echap pour quitter le jeu
    if keyboard.ESCAPE:
        liste_decors()
        exit()


def liste_decors() :
    nouveau_decors = [level.Decors(0,700,80,380,"terre"),level.Decors(1840,700,80,380,"terre")]
    for decor in decors :  
        decor["x"] = ((decor["x"] // 80) - 1) * 80
        decor["y"] = ((decor["y"] // 20) - 1) * 20  
        decor["largeur"] = ((decor["largeur"] // 80) + 1) * 80
        decor["hauteur"] = ((decor["hauteur"] // 20) + 1) * 20
        nouveau_decors.append(level.Decors(decor["x"], decor["y"],decor["largeur"],decor["hauteur"],"terre"))

    for decor in nouveau_decors : 
        print(f"Decors{decor},")




#levels = level.niveau_vide
levels = level.nouveau_lvl
topleft = None
bottomright = None
decors=[]
print(decors)
os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()
