

import os
import sys
import pgzrun
import pygame
import level
from random import randint, choice
import entite
from math import sin, cos

WIDTH = 1920
HEIGHT = 1080
TITLE = "Slimy!"
SPD_MAX = 14
hauteur_player = 40
largeur_player = 50
taille_projectil = 15
ZONES_AGLU = (680,560,400,260)

class Couleurs():
    """
    Propose une méthode permettant de renvoyer une couleur aléatoire
    Contient les constantes des couleurs utilisés
    """
    fond = (150,207,255)
    laser = (200,120,210)
    terre = (150,90,20)
    jungle = (100,120,20)
    terre_brule = (110,50,10)
    terre_contour = (110,50,0)
    jungle_contour = (60,80,0)
    terre_brule_contour = (70,10,0)
    slime = (255,110,110)
    projectil = (255,80,80)
    noir = (0,0,0)


    def color(c: str) -> tuple:
        """
        Renvoie une couleur de décor en fonction du monde actuel
        """
        if c == "noir" :
            return Couleurs.noir
        if c == "decor":
            if monde % 3 == 0:
                return Couleurs.terre_brule
            if monde % 3 == 1:
                return Couleurs.terre
            if monde % 3 == 2:
                return Couleurs.jungle

    def color_contour(c: str) -> tuple:
        """
        Renvoie la couleur du contour des décors en fonction du monde actuel
        """
        if c == "noir" :
            return Couleurs.noir
        if c == "decor":
            if monde % 3 == 0:
                return Couleurs.terre_brule_contour
            if monde % 3 == 1:
                return Couleurs.terre_contour
            if monde % 3 == 2:
                return Couleurs.jungle_contour


    @staticmethod
    def random() -> tuple:
        """
        Renvoie une couleur aléatoire au format (R,G,B)
        """
        return (randint(0,255),randint(0,255),randint(0,255))

def update():
    global force_gravite, w, count_frame,levels,stage, boss_kill, monde, anim_ciel, count_frame_inv, etat_game, player,laser_tir,charge_laser,tirs_ennemis,bulles, timer_zone_aglu, zone_aglu
    """
    """
    count_frame += 1

    check_keys()

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

    if check_collisions_tirs() == 2:
        liste_tirs.remove(liste_tirs[0])
        
    if boss_kill: 
        stage = 1
        monde += 1
        if player.spd < SPD_MAX :
            player.spd += 1
        boss_kill = False


    move_projectil()
    ennemi_tir(levels)
    if laser_tir : 
        charge_laser += 1 
        if charge_laser >= 45 :
            tirer_laser()
            charge_laser = 0
            laser_tir = False

    if monde % 3 == 2 and stage == 5 :
        tirer_bulle(levels[0].ennemis[0]) 
        move_bulles(bulles)

    if monde % 3 == 0 and stage == 5:
        timer_zone_aglu += 1 
        if timer_zone_aglu > 240 :
            zone_aglu = randint(0,3)
            timer_zone_aglu = 0
        aglu_tire(levels[0].ennemis[0])

    check_collisions_tirs_ennemis_decor(tirs_ennemis)

def scrolling():
    for lvl in levels :
        lvl.scroll(player.spd)       


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
            if pygame.Rect.colliderect(rect_player,rect_decor):
                if player.etat != "sol" and player.etat != "saut":
                    if x < v and y < w:
                        return v
                else:
                    if x < v:
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
            if pygame.Rect.colliderect(rect_player,rect_decor):
                if player.etat != "sol" and player.etat != "saut" :
                    if x > v and y < w:
                        return v
                else:
                    return v 
    return -1

def check_collisions_tirs():
    global liste_tirs
    for tir in liste_tirs:
        rect_tir = Rect(tir.pos,(taille_projectil,taille_projectil))
        for lvl in levels :
            for decor in lvl.get_decors():
                v = decor.get_pos()[0] 
                w = decor.get_pos()[1]
                largeur = decor.get_largeur()
                hauteur = decor.get_hauteur()
                rect_decor = Rect((v,w),(largeur,hauteur))
                if pygame.Rect.colliderect(rect_tir,rect_decor):
                    liste_tirs.remove(tir)
    return -1

def ennemi_tir(levels:list):
    for lvl in levels :
        if lvl.boss and lvl.ennemis != [] :
            boss_tir(lvl.ennemis[0])

def boss_tir(boss):
    global laser_tir,pos_laser
    if boss.peut_tirer :
        if monde % 3 == 1 :
            laser_tir = True
            pos_laser = choice((250,370,490,610))
            boss.peut_tirer = False
    else : 
        boss.rise_couldown()

def charger_laser():
    pos = (1500,pos_laser)
    screen.draw.filled_circle(pos,50,Couleurs.laser)

def tirer_laser():
    global tirs_ennemis
    pos = [1500,(pos_laser)-40]
    tirs_ennemis.append(entite.Projectil(pos,( 20),[-1,0],80,taille = (700,80)))

def gravite():
    global force_gravite
    player.pos[1] += force_gravite

def calc_speed():
  global force_gravite
  v_y = force_gravite
  v_y = v_y + 0.10*gravity
  force_gravite = v_y
  return

def check_collisions_tirs_ennemis_decor(tirs_ennemis: list):
    """
    Vérifie les colisions entre les tirs et les décors et supprime les tirs qui entrent en contact avec un décors
    """
    for tir in tirs_ennemis:
        rect_tir = Rect(tir.pos,(taille_projectil,taille_projectil))
        if (tir.pos[0] + tir.taille[0]) < 0 :
            tirs_ennemis.remove(tir)
        else :
            for lvl in levels :
                for decor in lvl.get_decors():
                    v = decor.get_pos()[0] 
                    w = decor.get_pos()[1]
                    largeur = decor.get_largeur()
                    hauteur = decor.get_hauteur()
                    rect_decor = Rect((v,w),(largeur,hauteur))
                    if pygame.Rect.colliderect(rect_tir,rect_decor):
                        if tir in tirs_ennemis :
                            tirs_ennemis.remove(tir)
def aglu_tire(boss):
    if boss.peut_tirer :
        x = 1660
        y = ZONES_AGLU[zone_aglu]
        y -= randint(5,95)
        tirs_ennemis.append(entite.Projectil([x,y],15,(-1,0),spd = 7,taille= (15,15)))
        boss.peut_tirer = False
    else :
        boss.rise_couldown()

def tirer_bulle(boss):
    if boss.peut_tirer :
        pos = choice(([1600,600],[1630,470],[1690,350]))
        bulles.append([entite.Projectil(pos,15,None,taille=(42,42)),
            #randint(1,3)
            3
            ,pos[1]])
        print("bulle")
        boss.peut_tirer = False
    else :
        boss.rise_couldown()

def move_bulles(bulles):
    for bulle in bulles:
        if bulle[1] == 1 :
            pos = bulle[0].pos
            bulle[0].deplacer([pos[0]-1,(sin(pos[0]/20)*14)+bulle[2]])
        if bulle[1] == 2 :
            pos = bulle[0].pos
            bulle[0].deplacer([pos[0]-1,(cos(pos[0]/12)*17)+bulle[2]])
        if bulle[1] == 3 :
            pos = bulle[0].pos
            bulle[0].deplacer([pos[0]-1,(sin(pos[0]/20)*cos(pos[0]/15)*25)+bulle[2]])

def draw():
    """
    """
    draw_ciel()
    draw_levels()
    draw_player()
    draw_tirs_ennemis()
    if laser_tir : 
        charger_laser()
    draw_projectil()
    draw_ui()

def draw_ciel():
    if monde % 3 == 1 :
        screen.blit("ciel_clair",(0,0))
    if monde % 3 == 2:
        screen.blit("ciel_clair",(0,0))
    if monde % 3 == 0 :
        screen.blit("ciel_clair",(0,0))


def draw_ui():
    screen.draw.text(("Stage :"), (25, 100), fontsize=60, color = Couleurs.noir)
    screen.draw.text((str(stage)), (170, 100), fontsize=60, color = Couleurs.noir)
    screen.draw.text(("Monde :"), (25, 150), fontsize=60, color = Couleurs.noir)
    screen.draw.text((str(monde)), (200, 150), fontsize=60, color = Couleurs.noir)


def draw_player():
    x = player.pos[0]
    y = player.pos[1]
    s = Actor("slimy", topleft=(x,y))
    s.draw()

def draw_projectil():
    global liste_tirs
    for tir in liste_tirs:
        x,y = tir.pos
        p = Actor("projectil", topleft=(x,y))
        p.draw()

def draw_levels():
    """
    Pour chaque niveau, dessine l'ensemble de ses décors et de ses ennemis
    """
    for lvl in levels :
        if lvl.boss == True :
            if lvl.ennemis != []:
                draw_boss(lvl.ennemis[0])
        for ennemi in lvl.ennemis :
            draw_ennemi(ennemi)
        for decor in lvl.get_decors():
            draw_decor(decor)


def draw_ennemi(ennemi):
    """
    Dessine l'ennemi
    """
    if ennemi.taille[1] == 40 :
        x = ennemi.pos[0]
        y = ennemi.pos[1] + 5
        e = Actor('ennemi1',topleft = (x,y)) 
        e.draw()
    if ennemi.taille[1] == 30 :
        x = ennemi.pos[0]
        y = ennemi.pos[1] + 5
        e = Actor('ennemi2',topleft = (x,y)) 
        e.draw()
    if ennemi.taille[1] == 90 :
        x = ennemi.pos[0]
        y = ennemi.pos[1] + 5
        e = Actor('ennemi3',topleft = (x,y)) 
        e.draw()

def draw_boss(boss : list):
    """
    Dessine les boss
    """
    if boss.name == 'Roi_Gluant':
        x = boss.pos[0] -320
        y = boss.pos[1] 
        b = Actor('roi_gluant', topleft = (x,y))
        b.draw()
    if boss.name == "Gluant_Bulle" :
        pass
    if boss.name == "Agluantin" :
        pass
def draw_decor(decor):
    draw_contour(decor)
    x , y = decor.get_pos()
    x += 5
    y += 5 
    topleft = (x,y)
    largeur = decor.get_largeur() -10
    hauteur = decor.get_hauteur() -10
    couleur = Couleurs.color(decor.couleur())
    rect_decor = Rect(topleft,(largeur,hauteur))
    screen.draw.filled_rect(rect_decor,couleur)

def draw_contour(decor):
    topleft = decor.get_pos()
    largeur = decor.get_largeur()
    hauteur = decor.get_hauteur()
    couleur = Couleurs.color_contour(decor.couleur())
    rect_decor = Rect(topleft,(largeur,hauteur))
    screen.draw.filled_rect(rect_decor,couleur)


def draw_tirs_ennemis():
    for tir in tirs_ennemis:
        pos = tir.pos
        taille = tir.taille
        rect_tir= Rect(pos,taille)
        screen.draw.filled_rect(rect_tir,Couleurs.laser)
    for tir in bulles:
        tir = tir[0]
        pos = tir.pos
        taille = tir.taille
        rect_tir= Rect(pos,taille)
        screen.draw.filled_rect(rect_tir,Couleurs.laser)


def slimy_tire():
    global liste_tirs
    x,y = player.pos[0], player.pos[1]
    x += largeur_player - 5
    y += hauteur_player//2 -taille_projectil// 2
    liste_tirs.append(entite.Projectil([x,y],((player.spd+1)*2.5)))

def move_projectil():
    """
    Pour chaque tir, le déplace
    """
    global liste_tirs
    for tir in liste_tirs:
        tir.move()
    for tir in tirs_ennemis:
        tir.move()

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

def liste_decors():
    nouveau_decors = [level.Decors(0,700,80,380,"terre",None),level.Decors(1840,700,80,380,"terre",None)]
    for decor in decors :  
        decor["x"] = ((decor["x"] // 80) - 1) * 80
        decor["y"] = ((decor["y"] // 20) - 1) * 20  
        decor["largeur"] = ((decor["largeur"] // 80) + 1) * 80
        decor["hauteur"] = ((decor["hauteur"] // 20) + 1) * 20
        nouveau_decors.append(level.Decors(decor["x"], decor["y"],decor["largeur"],decor["hauteur"],"terre"))

    for decor in nouveau_decors : 
        print(f"Decors{decor},")
       
def check_keys():
    global count_frame,force_gravite,boss_kill,topleft, bottomright
    """
    Verifie les touches enfoncée 
    Echap pour quitter le jeu
    """

    # Echap pour quitter le jeu
    if keyboard.ESCAPE:
        liste_decors()
        exit()
        
    if keyboard.P :
        boss_kill = True
    

    if keyboard.C :
        topleft = None
        bottomright = None
        print(player.pos)


    if keyboard.SPACE:
        if count_frame > 10 and player.etat == "sol":
            force_gravite = -1
            player.etat = "saut"
            force_gravite -= 4.3
            count_frame = 0
    if keyboard.D:
        if check_collisisons_droite() == -1:
            player.pos[0] +=5
        if check_collisisons_gauche() == v:
            player.pos[0] = v - largeur_player
    if keyboard.Q:
        if check_collisisons_gauche() == -1:
            player.pos[0] -=5
        if check_collisisons_gauche() == v:
            if stage == 5:
                player.pos[0] = v + largeur
            else:
                player.pos[0] = v + largeur - player.spd
        
# Globals

etat_game = "menu"
levels = level.nouveau_lvl
#levels = level.niveau_vide
topleft = None
bottomright = None
decors=[]
print(decors)
player = entite.Joueur([50,660],spd = 2)
gravity = 2
force_gravite = -1 
largeur = 0
w = 0
v = 0
count_frame2 = 0
count_frame = 0
stage = 1
monde = 3
tirs_ennemis = []
pos_laser = None
laser_tir = False
charge_laser = 0
liste_tirs = []
a_tire = False
boss_kill = False
bulles = []
timer_zone_aglu = 1
zone_aglu = 0

os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()
