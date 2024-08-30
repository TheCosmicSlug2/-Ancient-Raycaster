from random import randint
import pygame as pg


class Map:
    def __init__(self):
        self.map_data = [[0 if randint(0, 23) < 20 else randint(1, 5) for _ in range(50)] for i in range(50)]
        """
                    [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1],
                    [1, 0, 1, 0, 0, 3, 0, 0, 0, 1, 1],
                    [1, 0, 1, 2, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 5, 1, 1, 1, 1],
                    [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
                    [1, 1, 0, 0, 0, 3, 2, 0, 0, 1, 1],
                    [1, 0, 0, 0, 0, 3, 2, 0, 0, 0, 1],
                    [1, 0, 1, 5, 4, 1, 1, 0, 1, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0]]
        """

        self.nb_row_map_data = len(self.map_data)
        self.nb_column_map_data = len(self.map_data)

class MiniMap:
    def __init__(self, game):
        self.game = game
        self.background_2D = pg.Surface(SCREEN_lg, SCREEN_ht)
        self.draw_minimap(self.background_2D)

    def draw_minimap(self, surface):
        self.game.SCREEN.fill(WHITE2)
        for idx_row, row in enumerate(map_data):
            for idx_column, column in enumerate(row):

                if column != 0:
                    pg.draw.rect(surface, dic_colors[column], pg.Rect(idx_column * nb_column_map_data,
                                                                      idx_row * nb_row_map_data,
                                                                      CELLSIZE_X,
                                                                      CELLSIZE_Y))
    def show_minimap(self):
        self.game.SCREEN.blit(self.background_2D, (0, 0))




