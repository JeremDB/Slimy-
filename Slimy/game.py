 
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
    Update le jeu 60 fois par seconde :
    Défilement des niveaux, 
    Mouvement et physique du personnage
    Gestion des tirs
    """
    count_frame += 1
    if player.invincible :
        count_frame_inv += 1
        if count_frame_inv > 4 :
            player.invincible = False
            count_frame_inv = 0

    #Vérifie les inputs
    check_keys()


    #Gère le défilement des niveaux et les colisions due au défilement
    if stage < 5 and etat_game == "jeu":
        scrolling()
        if check_collisions_droite() == True :
            player.pos[0] = v - largeur_player
    #Gère la suppressions des niveaux entièrement défilée et la créations des suivants
    if levels[1].pos_x <= 0 :
        if stage == 3 :
            level.ajuste_niveaux_boss(levels,levels[1].pos_x,monde)
            stage += 1 
        else :
            level.ajuste_niveaux(levels,levels[1].pos_x)
            stage += 1

    if etat_game == "jeu":
        #Déplace les projectiles
        move_projectil()
        projectil_touche(liste_tirs)
        #Supprimes les tirs qui entrent en contact avec un décors
        check_collisions_tirs_decor(liste_tirs)
        check_collisions_tirs_ennemis_decor()

        ennemi_move(levels)
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
            check_collisions_bulles_tirs()
        if monde % 3 == 0 and stage == 5:
            timer_zone_aglu += 1 
            if timer_zone_aglu > 240 :
                zone_aglu = randint(0,3)
                timer_zone_aglu = 0
            aglu_tire(levels[0].ennemis[0])

        #Supprime les ennemis morts :
        ennemi_mort(levels)
        #Vérifie si un ennemis touche le joueur
        ennemi_contact(levels,player)
        bulles_touche(bulles)
        projectil_touche_player(tirs_ennemis)

        #Permet au joueur de sauter et gère la gravité qui lui est appliqué
        if player.etat == "saut":
            gravite()
        if check_collisions_down() == -1 : #Ne touche pas le sol
            calc_speed()
            gravite()
        if check_collisions_top() == -1: #Ne touche pas le bas d'un décor
            if check_collisions_down() == w: # si tu touche le haut d'un décor
                player.pos[1] = w - hauteur_player
                player.etat = "sol"
                force_gravite = 2
            
                
        #Physique du joueur dans les airs
        if check_collisions_top() == w and player.etat == "saut" : # Si tu touche le bas du décor
            player.pos[1] = w
            player.etat = "air"
            force_gravite = -0.2
            gravite()


    #Relance le défilement des niveaux après la mort du boss et augmente la vitesse du joueur
    if boss_kill: 
        stage = 1
        monde += 1
        bulles = []
        if player.spd < SPD_MAX :
            player.spd += 1
            player.atk += 1
        boss_kill = False

    if sort() == True and check_collisions_droite() == True:
        player.pv = 0



    sort()
    if player.est_mort():
        etat_game = "mort"

def scrolling():
    """
    Fait défiler les niveaux de la vitesse du joueur
    """
    for lvl in levels :
        lvl.scroll(player.spd)       


def check_collisions_down() -> float:
    """
    """
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

def check_collisions_top() -> float:
    """
    """
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

def check_collisions_droite() -> float:
    """
    """
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
                        v = decor.get_pos()[0]
                        return True
                else:
                    v = decor.get_pos()[0]
                    return True
    return -1

def check_collisions_gauche() -> float:
    """
    """
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
                        v = decor.get_pos()[0]
                        return True
                else:
                    v = decor.get_pos()[0]
                    return True
    return -1

def sort():
    """
    """
    global player
    if player.pos[0] < 0 :
        player.pos[0] = 0
        return True 
    if player.pos[0] > 1920 - largeur_player:
        player.pos[0] = 1920 - largeur_player 
    if player.pos[1] > 1080 :
        player.pv = 0

def check_collisions_tirs_decor(liste_tirs: list):
    """
    Vérifie les colisions entre les tirs et les décors et supprime les tirs qui entrent en contact avec un décors
    """
    for tir in liste_tirs:
        rect_tir = Rect(tir.pos,(taille_projectil,taille_projectil))
        if tir.pos[0] >= 1920 :
            liste_tirs.remove(tir)
        else :
            for lvl in levels :
                for decor in lvl.get_decors():
                    v = decor.get_pos()[0] 
                    w = decor.get_pos()[1]
                    largeur = decor.get_largeur()
                    hauteur = decor.get_hauteur()
                    rect_decor = Rect((v,w),(largeur,hauteur))
                    if pygame.Rect.colliderect(rect_tir,rect_decor):
                        if tir in liste_tirs :
                            liste_tirs.remove(tir)

def check_collisions_tirs_ennemis_decor():
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
    for bulle in bulles:
        tir = bulle[0]
        if (tir.pos[0]+ tir.taille[0]) <= 0: 
            bulles.remove(bulle)

def check_collisions_bulles_tirs():
    for tir in liste_tirs :
        rect_tir = Rect(tir.pos,(taille_projectil,taille_projectil))
        for bulle in bulles :
            b = bulle[0]
            rect_bulle = Rect(b.pos,b.taille)
            if rect_tir.colliderect(rect_bulle) :
                if tir in liste_tirs :
                    liste_tirs.remove(tir)
                if bulle in bulles :
                    bulles.remove(bulle)


def projectil_touche(liste_tirs: list):
    """
    Vérifie les collisions entre les tirs et les ennemis
    """
    pass
    for lvl in levels :
        for ennemi in lvl.ennemis:
            for tir in liste_tirs:
                rect_tir = Rect(tir.pos,tir.taille)
                rect_ennemi = Rect(ennemi.pos,ennemi.taille)
                if rect_tir.colliderect(rect_ennemi):
                    ennemi.prend_dgt(tir.atk)
                    liste_tirs.remove(tir)

def projectil_touche_player(tirs_ennemis: list):
    """
    Vérifei les collisions entre les tirs ennemis et le joueur
    """
    for tir in tirs_ennemis:
        rect_tir = Rect(tir.pos,tir.taille)
        rect_joueur = Rect(player.pos,(largeur_player,hauteur_player))
        if rect_tir.colliderect(rect_joueur) and not player.invincible:
            player.prend_dgt(tir.atk)
            player.invincible = True
            if monde %3 == 0 :
                tirs_ennemis.remove(tir)

def bulles_touche(bulles):
    for bulle in bulles:
        tir = bulle[0]
        rect_tir = Rect(tir.pos,tir.taille)
        rect_joueur = Rect(player.pos,(largeur_player,hauteur_player))
        if rect_tir.colliderect(rect_joueur) and not player.invincible:
            player.prend_dgt(tir.atk)
            bulles.remove(bulle)
            player.invincible = True

def ennemi_move(levels:list):
    for lvl in levels:
        for ennemi in lvl.ennemis:
            ennemi.move()

def ennemi_tir(levels:list):
    for lvl in levels :
        if lvl.boss and lvl.ennemis != [] and stage == 5:
            boss_tir(lvl.ennemis[0])

def boss_tir(boss):
    global laser_tir,pos_laser
    if boss.peut_tirer :
        if boss.name == 'Roi_Gluant' :
            laser_tir = True
            pos_laser = choice((250,390,510,630))
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

def ennemi_mort(levels: list):
    """
    Si un ennemi est mort, le supprime de la liste des ennemis
    """
    global boss_kill
    for lvl in levels :
        for ennemi in lvl.ennemis:
            if ennemi.est_mort():
                if isinstance(ennemi, level.Boss):
                    boss_kill = True 
                lvl.ennemis.remove(ennemi)

def ennemi_contact(levels: list,player):
    """
    Si un ennemi touche le joueur, le joueur prend des dgt
    """
    for lvl in levels :
        for ennemi in lvl.ennemis:
            rect_ennemi = Rect(ennemi.pos,ennemi.taille)
            rect_joueur = Rect(player.pos,(largeur_player,hauteur_player))
            if rect_ennemi.colliderect(rect_joueur):
                if not player.invincible :
                    player.invincible = True
                    player.prend_dgt(ennemi.atk_cac)

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

def gravite():
    """
    Applique au personnage la force de la gravité
    """
    global force_gravite
    player.pos[1] += force_gravite

def calc_speed():
    """
    Calcule la force de la gravitée appliqué au personnage
    """
    global force_gravite
    v_y = force_gravite
    v_y = v_y + 0.10*gravity
    force_gravite = v_y

def draw():
    global etat_game
    """
    Dessine les éléments a l'écran dans l'ordre : 
    - Fond
    - Niveaux (décors et ennemis)
    - Joueur
    - Projectiles
    - UI
    """
    if etat_game == "mort":
        draw_mort()
    else:
        if etat_game == "menu":
            draw_menu()
        else:
            draw_ciel()
            draw_projectil()
            draw_tirs_ennemis()
            if laser_tir : 
                charger_laser()
            draw_player()
            draw_levels()
            draw_ui()
    if etat_game == "pause" :
        draw_pause()

def draw_mort():
    screen.blit("mort",(0,0))

def draw_pause():
    screen.blit("pause",(0,0))

def draw_ciel():
    """
    Dessine et anime le ciel en fonction du monde actuel
    """
    if monde % 3 == 1 :
        screen.blit("ciel_clair",(0,0))
    if monde % 3 == 2:
        screen.blit("jungle",(0,0))
    if monde % 3 == 0 :
        screen.blit("volcan",(0,0))

def draw_menu():
    """
    Dessine le menu
    """
    screen.blit("menu",(0,0))

def draw_ui():
    """
    Dessine l'interface utilisateur 
    """
    screen.draw.text(("Stage :"), (25, 100), fontsize=60, color = Couleurs.noir)
    screen.draw.text((str(stage)), (170, 100), fontsize=60, color = Couleurs.noir)
    screen.draw.text(("Monde :"), (25, 150), fontsize=60, color = Couleurs.noir)
    screen.draw.text((str(monde)), (200, 150), fontsize=60, color = Couleurs.noir)
    screen.draw.text((str(player.pv)),(1700,150), fontsize=60,color = Couleurs.noir)

def draw_player():
    """
    Dessine le sprite de Slimy! à son emplacement
    """
    x = player.pos[0]
    y = player.pos[1]
    s = Actor("slimy", topleft=(x,y))
    s.draw()

def draw_projectil():
    """
    Dessine les tirs
    """
    global liste_tirs
    for tir in liste_tirs:
        x,y = tir.pos
        p = Actor("projectil", topleft=(x,y))
        p.draw()

def draw_tirs_ennemis():
    for tir in tirs_ennemis:
        pos = tir.pos
        taille = tir.taille
        rect_tir= Rect(pos,taille)
        screen.draw.filled_rect(rect_tir,Couleurs.laser)    
    for tir in bulles:
        draw_bulle(tir[0])

def draw_bulle(bulle):
    x = bulle.pos[0] -12
    y = bulle.pos[1] -12
    b = Actor('bulle',(x,y))
    b.draw()

def draw_levels():
    """
    Pour chaque niveau, dessine l'ensemble de ses décors et de ses ennemis
    """
    for lvl in levels :
        if lvl.boss == True :
            if lvl.ennemis != []:
                draw_boss(lvl.ennemis[0])
        else :
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
        y = ennemi.pos[1]-5
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
        x = boss.pos[0] -320
        y = boss.pos[1] -30
        b = Actor('gluantbulle', topleft = (x,y))
        b.draw()
    if boss.name == "Agluantin" :
        x = boss.pos[0] -9
        y = boss.pos[1] 
        b = Actor('aggluantin', topleft = (x,y))
        b.draw()
'''
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
'''

def draw_decor(decor):
    """
    Dessine les decors
    """
    if decor.get_forme() == 'bloc' :
        draw_bloc(decor)
    if decor.get_forme() == 'plat':
        draw_plat(decor)

def draw_bloc(decor):
    """
    Dessine les decors de type bloc
    """
    x, y = decor.get_pos()
    if decor.get_largeur() == 400 :
        if monde % 3 == 1 :
            d = Actor('sol_400',topleft = (x,y))
            d.draw()
        if monde % 3 == 2 :
            d = Actor('sol_400_jungle',topleft = (x,y))
            d.draw()
        if monde % 3 == 0 :
            d = Actor('sol_400_volcan',topleft = (x,y))
            d.draw()

    if decor.get_largeur() == 240 :
        if monde % 3 == 1 :
            d = Actor('sol_240',topleft = (x,y))
            d.draw()
        if monde % 3 == 2 :
            d = Actor('sol_240_jungle',topleft = (x,y))
            d.draw()
        if monde % 3 == 0 :
            d = Actor('sol_240_volcan',topleft = (x,y))
            d.draw()

    if decor.get_largeur() == 160 :
        if monde % 3 == 1 :
            d = Actor('sol_160',topleft = (x,y))
            d.draw()
        if monde % 3 == 2 :
            d = Actor('sol_160_jungle',topleft = (x,y))
            d.draw()
        if monde % 3 == 0 :
            d = Actor('sol_160_volcan',topleft = (x,y))
            d.draw()

    if decor.get_largeur() == 80 :
        if monde % 3 == 1 :
            d = Actor('sol_80',topleft = (x,y))
            d.draw()
        if monde % 3 == 2 :
            d = Actor('sol_80_jungle',topleft = (x,y))
            d.draw()
        if monde % 3 == 0 :
            d = Actor('sol_80_volcan',topleft = (x,y))
            d.draw()


def draw_plat(decor): 
    """
    Dessine les decors de type plat
    """
    x, y = decor.get_pos()
    if decor.get_largeur() == 240 :
        if monde % 3 == 1 :
            d = Actor('plateforme_240',topleft = (x,y))
            d.draw()
        if monde % 3 == 2 :
            d = Actor('plateforme_240_jungle',topleft = (x,y))
            d.draw()
        if monde % 3 == 0 :
            d = Actor('plateforme_240_volcan',topleft = (x,y))
            d.draw()

    if decor.get_largeur() == 160 :
        if monde % 3 == 1 :
            d = Actor('plateforme_160',topleft = (x,y))
            d.draw()
        if monde % 3 == 2 :
            d = Actor('plateforme_160_jungle',topleft = (x,y))
            d.draw()
        if monde % 3 == 0:
            d = Actor('plateforme_160_volcan',topleft = (x,y))
            d.draw()

    if decor.get_largeur() == 80 :
        if monde % 3 == 1 :
            d = Actor('plateforme_80',topleft = (x,y))
            d.draw()
        if monde % 3 == 2 :
            d = Actor('plateforme_80_jungle',topleft = (x,y))
            d.draw()
        if monde % 3 == 0 :
            d = Actor('plateforme_80_volcan',topleft = (x,y))
            d.draw()

def slimy_tire(pos):
    """
    Crée un tir de Slimy! à sa position actuelle
    """
    global liste_tirs
    x,y = player.pos[0], player.pos[1]
    x += largeur_player // 2  - taille_projectil // 2
    y += hauteur_player//2 -taille_projectil// 2
    direction = [pos[0] - x, pos[1] - y]
    direction = normalise_direction(direction)
    liste_tirs.append(entite.Projectil([x,y],(player.atk*3),direction,(player.spd+6),taille = (taille_projectil,taille_projectil)))

def normalise_direction(direction: list):
    """
    Normalise le vecteur direction pour que l'une de ses deux valeur soit égale a 1 
    """
    diviseur = ((direction[0]**2+direction[1]**2)**(1/2))
    direction[0] /= diviseur
    direction[1] /= diviseur

    return direction

def move_projectil():
    """
    Pour chaque tir, le déplace
    """
    global liste_tirs
    for tir in liste_tirs:
        tir.move()
    for tir in tirs_ennemis:
        tir.move()
    
def on_mouse_down(button,pos):
    """
    A chaque clic gauche : fait tirer Slimy!
    """
    if button == mouse.LEFT:
        slimy_tire(pos)
       
def init_game():
    """
    """
    global levels, player, stage, monde
    levels = level.init_niveau()
    player = entite.Joueur([50,660], spd = 3)
    stage = 1
    monde = 1

def check_keys():
    global count_frame,force_gravite,boss_kill,etat_game,player,stage,monde,levels, tirs_ennemis, bulles
    """
    Verifie les touches enfoncée 
    Echap pour quitter le jeu
    P pour tricher et compter comme avoir tué un boss
    Space pour sauter
    Q et D pour se déplacer
    
    """

    # Echap pour quitter le jeu
    if keyboard.ESCAPE:
        exit()
        
    if keyboard.M :
        boss_kill = True
    
    if keyboard.P and player :
        etat_game = "pause"

    if keyboard.SPACE:  
        if etat_game == "menu" or etat_game == "pause":
            etat_game = "jeu"

    if etat_game == "jeu":
        if keyboard.SPACE:  
            if etat_game == "menu":
                etat_game = "jeu"
                count_frame = 0
            else:
                if count_frame > 10 and player.etat == "sol" and player.etat != "air":
                    force_gravite = -1
                    player.etat = "saut"
                    force_gravite -= 4.3
                    count_frame = 0
        if keyboard.D:
            if check_collisions_droite() == -1:
                player.pos[0] +=5
            if check_collisions_gauche() == True:
                player.pos[0] = v - largeur_player
        if keyboard.Q:
            if check_collisions_gauche() == -1:
                player.pos[0] -=5
            if check_collisions_gauche() == True:
                if stage == 5:
                    player.pos[0] = v + largeur
                else:
                    player.pos[0] = v + largeur - player.spd
                
    if keyboard.R:
        if etat_game == "mort":
            levels = []
            levels = level.init_niveau()
            player = entite.Joueur([50,660],spd = 3) 
            force_gravite = -1
            stage = 1
            monde = 1
            etat_game = "jeu"
            tirs_ennemis = []
            bulles = []
        
# Globals

etat_game = "menu"

levels = level.init_niveau()
player = entite.Joueur([50,660],spd = 5,atk = 2)
gravity = 2
force_gravite = -1 
largeur = 0
w = 0
v = 0
count_frame_inv = 0
count_frame = 0
stage = 1
monde = 1
liste_tirs = []
tirs_ennemis = []
pos_laser = None
laser_tir = False
charge_laser = 0
a_tire = False
boss_kill = False
bulles = []
timer_zone_aglu = 1
zone_aglu = 0

os.environ['SDL_VIDEO_CENTERED'] = '1'
pgzrun.go()
