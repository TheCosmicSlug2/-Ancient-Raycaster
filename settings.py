
# Game settings :

BLACK = (0, 0, 0)
DARKGRAY = (100, 100, 100)
LIGHTGRAY = (200, 200, 200)
WHITE2 = (230, 230, 230)
WHITE1 = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
dic_colors = {0: None, 1: BLACK, 2: WHITE2, 3: RED, 4: BLUE, 5: GREEN}


DEFAULT_SCREEN_DIMS = (800, 600)

grid_dims = (100, 100)


SCREEN_DIMS = DEFAULT_SCREEN_DIMS

HALF_SCREEN_DIMS = (SCREEN_DIMS[0] // 2, SCREEN_DIMS[1] // 2) # Dimensions de moitié d'écran


CELL_DIMS = (SCREEN_DIMS[0] // grid_dims[0], SCREEN_DIMS[1] // grid_dims[1])

average_cell_size = (CELL_DIMS[0] + CELL_DIMS[1]) // 2

# Commandes :
command_mode = False
command_input = ""


# Joueur :
PLAYER_SPAWN_TYPE = "random"
player_side_size = max(1, (average_cell_size // 3))
PLAYER_DIMS = (player_side_size, player_side_size)
PLAYER_SPEED = max(1, average_cell_size / 10)


RAY_DIMS = (3, 3)

# Raycaster :
RAYCASTER_SIZE = 3
RAYCASTER_RES = 1
RAYCASTER_MAX_DST = average_cell_size * 10
RAYCASTER_GAP = 1


# FOV_MAX pour calculer la FOV
FOV_MAX = 60  # Plus réaliste pour réduire l'effet fisheye
HALF_FOV = FOV_MAX // 2

FPS = 30


ticks_to_update_map = FPS // 3
ticks_to_update_mouse = FPS // 3

