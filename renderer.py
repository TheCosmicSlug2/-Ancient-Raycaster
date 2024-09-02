import pygame as pg
from settings import *


class Renderer:
    def __init__(self, level_master) -> None:
        self.level_master = level_master
        self.SCREEN = pg.display.set_mode(SCREEN_DIMS)
        self.clock = pg.time.Clock()
        pg.display.set_caption("2.5D")

        pg.font.init()
        self.font = pg.font.SysFont('Arial', 30)

        self.render_background_command()
        self.render_minimap()
        self.render_3D_background()


    def render_background_command(self):
        self.background_command = pg.Surface(SCREEN_DIMS)
        self.background_command.fill(BLACK)
        # Créer une surface de texte
        text = "Exécutez la commande dans le cmd"
        text_color = GREEN
        text_surface = self.font.render(text, True, text_color)

        # Définir la position du texte
        text_rect = text_surface.get_rect()
        text_rect.center = (self.background_command.get_width() // 2, self.background_command.get_height() // 2)
        self.background_command.blit(text_surface, text_rect)


    def render_3D_background(self):
        self._3D_background = pg.Surface(SCREEN_DIMS)

        up_rect = pg.Rect(0, 0, SCREEN_DIMS[0], HALF_SCREEN_DIMS[1])
        down_rect = pg.Rect(0, HALF_SCREEN_DIMS[1], SCREEN_DIMS[0], HALF_SCREEN_DIMS[1])

        pg.draw.rect(self._3D_background, LIGHTGRAY, up_rect)
        pg.draw.rect(self._3D_background, DARKGRAY, down_rect)
    

    def render_3D_foreground(self, liste_raycast: list, wall_colors: list):
        """ Dessine en 3D avec une liste des distances + "couleurs" pour chque distance """

        default_wall_height = 5000 # Constante pour dimensionner les murs

        self._3D_foreground = pg.Surface(SCREEN_DIMS)

        # Mettre l'arrière plan 3d
        self._3D_foreground.blit(self._3D_background, (0, 0))

        nb_of_rays = len(liste_raycast)
        ray_width = SCREEN_DIMS[0] / nb_of_rays


        for ray_idx, ray_dst in enumerate(liste_raycast):
            if ray_dst is None:  # ne pas dessiner les rayons qui vont à l'infini
                continue

            # Calculer la hauteur à l'écran du mur
            wall_height = default_wall_height / ray_dst

            # Calculer la position et la largeur du rayon en flottant
            ray_x = ray_idx * ray_width
            ray_x_int = int(ray_x)
            next_ray_x_int = int(ray_x + ray_width)

            # Calculer la largeur en pixels
            ray_width_int = next_ray_x_int - ray_x_int

            # Calculer la couleur
            wall_color = dic_colors[wall_colors[ray_idx]]

            wall_color_with_shades = (max(0, wall_color[0] - ray_dst), max(0, wall_color[1] - ray_dst), max(0, wall_color[2] - ray_dst))

            # Dessiner le mur
            wall_slice = pg.Rect(ray_x_int, HALF_SCREEN_DIMS[1] - int(wall_height / 2), ray_width_int, int(wall_height))
            pg.draw.rect(self._3D_foreground, wall_color_with_shades, wall_slice)



    def render_minimap(self):
        self.minimap = pg.Surface(SCREEN_DIMS)
        self.minimap.fill(WHITE1)

        for idx_row, row in enumerate(self.level_master.map_data):
            for idx_column, column in enumerate(row):

                if column == 0:
                    continue

                rect_color = dic_colors[column]
                rect = pg.Rect(idx_column * CELL_DIMS[0], idx_row * CELL_DIMS[1], CELL_DIMS[0], CELL_DIMS[1])
                pg.draw.rect(self.minimap, rect_color, rect)
    
    def show_minimap(self):
        self.SCREEN.blit(self.minimap)

    def render_minimap_on_screen(self, player, raycaster):

        # Render les rays
        self.SCREEN.blit(self.minimap, (0, 0))

        for ray_pos in raycaster.rays_final_pos:
            pg.draw.rect(self.SCREEN, BLUE, pg.Rect(ray_pos[0], ray_pos[1], RAY_DIMS[0], RAY_DIMS[1]))

        # Render le joueur
        pg.draw.rect(self.SCREEN, BLACK, pg.Rect(player.posx, player.posy, PLAYER_DIMS[0], PLAYER_DIMS[1]))
    
    def render_command_background_on_screen(self):
        self.SCREEN.blit(self.background_command, (0, 0))
    
    def render_3D_foreground_on_screen(self):
        self.SCREEN.blit(self._3D_foreground, (0, 0))
    

    def update(self):
        pg.display.flip()
        self.clock.tick(FPS)
