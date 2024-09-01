from random import randint
import pygame as pg
from settings import *


class LevelMaster:
    def __init__(self):
        self.map_data = [[0 if randint(0, 23) < 20 else randint(1, 5) for _ in range(grid_dims[0])] for i in range(grid_dims[1])]
        self.map_data_dims = (len(self.map_data[0]), len(self.map_data))




