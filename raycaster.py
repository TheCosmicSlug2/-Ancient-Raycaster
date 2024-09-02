
from physics import Physics
from math import cos, radians
from settings import *
import random

class Raycaster:
    def __init__(self, player, level_master, renderer):
        self.resolution = RAYCASTER_RES
        self.gap = RAYCASTER_GAP
        self.max_raycast_distance = RAYCASTER_MAX_DST
        self.physics = Physics()
        self.player = player
        self.level_master = level_master
        self.renderer = renderer
        self.green_wall_ray_counter = 0

        self.rays_final_pos = []

    def raycast_one_ray(self, angle: int, map_shown) -> tuple:
        """ Envoie un ray dans une direction en degrés """
        posx, posy = self.player.posx, self.player.posy
        delta_x, delta_y = self.physics.trouver_longueurs_trigo(angle)

        angle_radians = cos(radians(angle - self.player.angle))

        for distance in range(0, self.max_raycast_distance, self.gap):
            posx += delta_x
            posy += delta_y
            
            wall_color_collided_with, collide_pos = self.physics.get_color_collided(
                top_left_pos=(posx, posy),
                cell_dims=CELL_DIMS,
                map_data=self.level_master.map_data, 
                map_data_dims=self.level_master.map_data_dims)
            
            if wall_color_collided_with != 0:        
                if wall_color_collided_with == 5:
                    self.green_wall_ray_counter += 1    
                if map_shown:
                    self.rays_final_pos.append(collide_pos)
                corrected_distance = max(0.001, distance * angle_radians)  # Correction anti-fisheye
                return corrected_distance, wall_color_collided_with
            
        return None, None


    def raycast(self, fov: tuple, map_shown) -> tuple:
        self.green_wall_ray_counter = 0
        raycast_distances = []
        wall_colors = []
        start_angle, end_angle = fov
        self.rays_final_pos = []
        while start_angle <= end_angle:
            ray_info = self.raycast_one_ray(angle=start_angle, map_shown=map_shown)
            raycast_distances.append(ray_info[0])
            wall_colors.append(ray_info[1])
            start_angle += self.resolution
        
        return raycast_distances, wall_colors
    

    def wall_front_player_coord(self):
        """ Envoie un ray depuis la direction du joueur jusqu'à un mur """
        posx, posy = self.player.posx, self.player.posy
        lg_x, lg_y = self.physics.trouver_longueurs_trigo(self.player.angle)

        while not self.physics.check_top_left_collision((posx, posy), CELL_DIMS, self.level_master.map_data, self.level_master.map_data_dims):
            posx += lg_x # comme on est en mode "console", pas besoin de checher la rapidité
            posy += lg_y # on fait juste des petits pas précis

        return posx, posy
    

    def last_space_before_wall_front_player_coord(self):
        """ Envoie un ray depuis la direction du joueur jusqu'à l'espace situé avant le mur devant le joueur """
        posx, posy = self.player.posx, self.player.posy
        lg_x, lg_y = self.physics.trouver_longueurs_trigo(self.player.angle)

        next_x, next_y = posx + lg_x, posy + lg_y

        while not self.physics.check_top_left_collision((next_x, next_y), CELL_DIMS, self.level_master.map_data, self.level_master.map_data_dims):
            posx, posy = next_x, next_y

            next_x += lg_x
            next_y += lg_y

        return posx, posy
    

    def every_wall_in_player_direction(self):
        """ Envoie un ray et retourne tous les murs qu'il a croisé """
        liste_murs = []

        posx, posy = self.player.posx, self.player.posy

        top_left_pos = (posx, posy)
        bottom_right_pos = (posx + self.player.dims[0], posy + self.player.dims[1])

        x_grid_positions  = top_left_pos[0] // CELL_DIMS[0], bottom_right_pos[0] // CELL_DIMS[0]
        y_grid_pos = top_left_pos[1] // CELL_DIMS[1], bottom_right_pos[1] // CELL_DIMS[1]

        lg_x, lg_y = self.physics.trouver_longueurs_trigo(self.player.angle)


        while 0 < posx < SCREEN_DIMS[0] and 0 < posy < SCREEN_DIMS[1]:

            # calculer les coordonnées sur la grille
            row = int(posy // CELL_DIMS[1])
            column = int(posx // CELL_DIMS[0])

            if column in x_grid_positions and row in y_grid_pos:
                posx += lg_x
                posy += lg_y
                continue

            if (row, column) not in liste_murs: # Si le mur n'a pas déjà été ajouté à la liste
                liste_murs.append((row, column))

            posx += lg_x
            posy += lg_y

        return liste_murs
