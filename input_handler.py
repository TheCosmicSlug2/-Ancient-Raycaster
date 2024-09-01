import pygame as pg
from settings import *

class InputHandler:
    def __init__(self) -> None:
        self.last_player_angle = 0

    @staticmethod
    def get_mouse_event():
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return "quit_game"
    
    @staticmethod
    def get_keyboard_events():
        keys = pg.key.get_pressed()

        dic_keys = {
            pg.K_s: "bas",
            pg.K_q: "gauche",
            pg.K_z: "haut",
            pg.K_d: "droite",
            pg.K_m: "map",
            pg.K_c: "cmd",
            pg.K_ESCAPE: "esc"
        }

        pressed_keys = []            
        for key, value in dic_keys.items():
            if keys[key]:
                pressed_keys.append(value)

        return pressed_keys
    
    def get_mouse_x_direction(self, player) -> int:
        """ Retourne la direction du joueur en degrés """
        if pg.mouse.get_visible() == True:
            return self.last_player_angle
        mousex, mousey = pg.mouse.get_pos()
        if mousex < 50 or mousex > SCREEN_DIMS[0] - 50 or mousey < 50 or mousey > SCREEN_DIMS[0] - 50:
            pg.mouse.set_pos(HALF_SCREEN_DIMS)
        player.angle = pg.mouse.get_pos()[0] * 2 % 360  # on divise par 2 la sensibilité de la souris et on transforme en degrés
        if player.angle != self.last_player_angle:
            self.last_player_angle = player.angle
        return player.angle
            