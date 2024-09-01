from math import cos, sin, radians, sqrt
from settings import * 

class Physics:
    def __init__(self) -> None:
        pass


    @staticmethod            
    def trouver_longueurs_trigo(loc_angle_degres: int) -> tuple:
        """ Convertit un angle en radian et renvoie son sinus et cosinus """
        angle_radians = radians(loc_angle_degres)
        x = cos(angle_radians)
        y = sin(angle_radians)
        return x, y
    
    @staticmethod    
    def check_4_side_collision(top_left_pos, object_dims, cell_dims, map_data, map_data_dims) -> bool:
        """ Putain c'est chiant les collisions """

        # La "vrai" position du joueur est invisible

        top_left_pos = (round(top_left_pos[0]), round(top_left_pos[1]))

        # Obtenir la position absolue des 4 côtés
        top_right_pos = (top_left_pos[0] + object_dims[0], top_left_pos[1])
        bottom_left_pos = (top_left_pos[0], top_left_pos[1] + object_dims[1])
        bottom_right_pos = (top_right_pos[0], bottom_left_pos[1])

        cell_top_left_pos = (top_left_pos[0] // cell_dims[0], top_left_pos[1] // cell_dims[1])
        cell_top_right_pos = (top_right_pos[0] // cell_dims[0], top_left_pos[1] // cell_dims[1])
        cell_bottom_left_pos = (bottom_left_pos[0] // cell_dims[0], bottom_left_pos[1] // cell_dims[1])
        cell_bottom_right_pos = (bottom_right_pos[0] // cell_dims[0], bottom_right_pos[1] // cell_dims[1])

        if cell_top_left_pos[0] < 0 or cell_top_left_pos[1] < 0:
            return True
        
        if cell_bottom_right_pos[0] > map_data_dims[0] - 1 or cell_bottom_right_pos[1] > map_data_dims[1] - 1:
            return True

        cell_top_left = map_data[cell_top_left_pos[1]][cell_top_left_pos[0]]
        cell_top_right = map_data[cell_top_right_pos[1]][cell_top_right_pos[0]]
        cell_bottom_left = map_data[cell_bottom_left_pos[1]][cell_bottom_left_pos[0]]
        cell_bottom_right = map_data[cell_bottom_right_pos[1]][cell_bottom_right_pos[0]]

        return cell_top_left != 0 or cell_top_right != 0 or cell_bottom_left != 0 or cell_bottom_right != 0
    

    @staticmethod    
    def get_color_collided(top_left_pos, cell_dims, map_data, map_data_dims) -> tuple:
        """ Simplified collision detection """
        x, y = round(top_left_pos[0]), round(top_left_pos[1])
        cell_x, cell_y = x // cell_dims[0], y // cell_dims[1]
        
        if cell_x < 0:
            return (1, (0, y))
        if cell_y < 0:
            return (1, (x, 0))
        if cell_x >= map_data_dims[0]:
            return (1, (SCREEN_DIMS[0] - RAY_DIMS[0], y))
        if cell_y >= map_data_dims[1]:
            return (1, (x, SCREEN_DIMS[1] - RAY_DIMS[1]))
        

        cell_value = map_data[cell_y][cell_x]
        if cell_value != 0:
            return cell_value, (x, y)
        
        return 0, None
    
    @staticmethod    
    def get_wall_color(posx: int, posy: int, map_data) -> int:
        """ Checke la couleur d'un mur à position lambda """
        column_idx = int(posx // CELL_DIMS[0])
        row_idx = int(posy // CELL_DIMS[1])
        if row_idx >= grid_dims[1] or column_idx >= grid_dims[0]:
            return True
        return map_data[row_idx][column_idx]
    
    @staticmethod
    def calculate_dst_to_player(x: int, y: int, player) -> int:
        """ Renvoie la distance au joueur calculée avec pythagore """
        ray_width = abs(player.posx - x)
        ray_height = abs(player.posy - y)
        dst_to_player = sqrt(ray_width ** 2 + ray_height ** 2)
        # Éviter les divisions par zéro durant la modélisation 3D
        return dst_to_player if dst_to_player > 1 else 1
    
    @staticmethod
    def check_top_left_collision(top_left_pos, cell_dims, map_data, map_data_dims):
        """ Simplified collision detection """
        x, y = round(top_left_pos[0]), round(top_left_pos[1])
        cell_x, cell_y = x // cell_dims[0], y // cell_dims[1]

        if cell_x < 0 or cell_y < 0 or cell_x >= map_data_dims[0] or cell_y >= map_data_dims[1]:
            return True

        cell_value = map_data[cell_y][cell_x]
        if cell_value != 0:
            return True
        
        return False
    

