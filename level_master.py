from random import randint
import pygame as pg
from settings import *
from algorythms import DepthFirst


class LevelMaster:
    def __init__(self):
        #self.map_data = [[0 if randint(0, 23) < 20 else randint(1, 5) for _ in range(grid_dims[0])] for i in range(grid_dims[1])]
        depth_first = DepthFirst(grid_dims=grid_dims)
        depth_first.generate_maze()
        self.map_data = depth_first.map_data
        self.player_starting_pos = depth_first.furthest_pos

        for row_idx, row in enumerate(self.map_data):
            for column_idx, column in enumerate(row):
                if column == 1:
                    self.map_data[row_idx][column_idx] = randint(1, 4)
        
        end = depth_first.starting_cell

        self.map_data[end[1]][end[0]] = 5
                    
        self.map_data_dims = (len(self.map_data[0]), len(self.map_data))




