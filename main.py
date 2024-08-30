import pygame as pg
from math import radians, cos, sin, sqrt
from map import Map

liste_map = Map().map_data
nb_row_liste_map = Map().nb_row_map_data
nb_column_liste_map = Map().nb_column_map_data


# Pygame :
pg.init()
pg.font.init()
font = pg.font.SysFont('Arial', 30)
pg.display.set_caption("3D renderer")
pg.mouse.set_visible(False)
DEFAULT_SCREEN_lg, DEFAULT_SCREEN_ht = 800, 600
clock = pg.time.Clock()
FPS = 30


# Game settings :
MAP = False
BLACK = (0, 0, 0)
DARKGRAY = (100, 100, 100)
LIGHTGRAY = (200, 200, 200)
WHITE2 = (230, 230, 230)
WHITE1 = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
dic_colors = {0: None, 1: BLACK, 2: WHITE1, 3: RED, 4: BLUE, 5: GREEN}

if True:#input("ZQSD or Arrows ? (1/2): \n >> ") == "1":
    key_up, key_down, key_left, key_right = pg.K_z, pg.K_s, pg.K_q, pg.K_d
else:
    key_up, key_down, key_left, key_right = pg.K_UP, pg.K_DOWN, pg.K_LEFT, pg.K_RIGHT

if False:#input("Fullscreen ? (y/n) : \n >> ") == "y":
    SCREEN_lg, SCREEN_ht = pg.display.Info().current_w, pg.display.Info().current_h
    SCREEN = pg.display.set_mode((SCREEN_lg, SCREEN_ht), pg.FULLSCREEN)
else:
    SCREEN_lg, SCREEN_ht = DEFAULT_SCREEN_lg, DEFAULT_SCREEN_ht
    SCREEN = pg.display.set_mode((SCREEN_lg, SCREEN_ht))

HALF_SCREEN_lg = SCREEN_lg // 2 # Dimensions de moitié d'écran
HALF_SCREEN_ht = SCREEN_ht // 2

CELLSIZE_X = SCREEN_lg // nb_column_liste_map # Dimensions des cellules pour la carte 2D
CELLSIZE_Y = SCREEN_ht // nb_row_liste_map

# Commandes :
command_mode = False
command_input = ""


# Joueur :
PLAYER_SPAWN_TYPE = "random"
PLAYER_SIZE = 5
PLAYER_SPEED = 1


# Raycaster :
RAYCASTER_SIZE = 3
RAYCASTER_RES = 1
RAYCASTER_MAX_DST = 300
RAYCASTER_GAP = 1


# FOV_MAX pour calculer la FOV
FOV_MAX = 60  # Plus réaliste pour réduire l'effet fisheye




def draw_rectangle(surface, x, y, sizex, sizey, color):
    pg.draw.rect(surface, color, pg.Rect(x, y, sizex, sizey))


def trouver_longueurs_trigo(loc_angle_degres: int) -> tuple:
    """ Convertit un angle en radian et renvoie son sinus et cosinus """
    angle_radians = radians(loc_angle_degres)
    x = cos(angle_radians)
    y = sin(angle_radians)
    return x, y


def get_mouse_x_direction() -> int:
    """ Retourne la direction du joueur en degrés """
    mousex, mousey = pg.mouse.get_pos()
    if mousex < 50 or mousex > SCREEN_lg - 50 or mousey < 50 or mousey > SCREEN_lg - 50:
        pg.mouse.set_pos(HALF_SCREEN_lg, HALF_SCREEN_ht)
    PLAYER_.angle = pg.mouse.get_pos()[0] * 2 % 360  # on divise par 2 la sensibilité de la souris et on transforme en degrés
    return PLAYER_.angle


def collide_something(x: int, y: int) -> bool:
    """ Checke si une position lambda intersecte avec un mur """
    # obtenir la position suivante du joueur
    column_idx = int(x // CELLSIZE_X)
    row_idx = int(y // CELLSIZE_Y)
    if row_idx >= nb_row_liste_map or column_idx >= nb_column_liste_map:
        return True  # Si le raycast atterit sur un bord est en dehors de la grille, il y a collision
    return liste_map[row_idx][column_idx] != 0


def get_wall_color(x: int, y: int) -> int:
    """ Checke la couleur d'un mur à position lambda """
    column_idx = int(x // CELLSIZE_X)
    row_idx = int(y // CELLSIZE_Y)
    if row_idx >= nb_row_liste_map or column_idx >= nb_column_liste_map:
        return 1 # le bord est blanc
    return liste_map[row_idx][column_idx]







class Player:
    def __init__(self, size, spawn_type):
        self.size = size
        self.angle = 0
        self.posx = 0
        self.posy = 0

        # On essaye de le faire apparaître à un endroit quasirandom, sinon on le force au centre

        if spawn_type == "random":
            if not self.spawn_player_random():
                self.spawn_player_center()

        else:
            self.spawn_player_center()


    def spawn_player_random(self):
        """ Fait appraître le joueur dans un endroit aléatoire et vide """
        for row_idx in range(nb_row_liste_map):
            for column_idx in range(nb_column_liste_map):
                if liste_map[row_idx][column_idx] == 0:

                    self.posx = column_idx * CELLSIZE_X + CELLSIZE_X // 2
                    self.posy = row_idx * CELLSIZE_Y + CELLSIZE_Y // 2
                    return True

        return False


    def spawn_player_center(self):
        """ Supprime un possible mur central et fait appraître le joueur à cet endroit """

        center_row = nb_column_liste_map // 2
        center_column = nb_column_liste_map // 2
        liste_map[center_row][center_column] = 0

        self.posx = center_column * CELLSIZE_X // 2
        self.posy = center_row * CELLSIZE_Y // 2

        return True


    def move_player(self, direction: int) -> None:
        """ Déplace le joueur selon un angle """
        lg_x, lg_y = trouver_longueurs_trigo(get_mouse_x_direction() + direction)
        next_x, next_y = self.posx + (lg_x * PLAYER_SPEED), self.posy + (lg_y * PLAYER_SPEED)
        # si le movement suivant collide un mur
        if collide_something(next_x, next_y):
            return
        self.posx, self.posy = next_x, next_y
        self.check_collisions_border()

    def check_collisions_border(self) -> None:
        """ Checke les collisions avec les bordures de la carte """
        # collisions horizontales
        if self.posx > SCREEN_lg - self.size:
            self.posx = SCREEN_lg - self.size
        if self.posx < 0:
            self.posx = 0
        # collisions verticales
        if self.posy > SCREEN_ht - self.size:
            self.posy = SCREEN_ht - self.size
        if self.posy < 0:
            self.posy = 0


    def hide(self) -> None:
        draw_rectangle(SCREEN, self.posx, self.posy, self.size, self.size, WHITE2)


    def show(self) -> None:
        draw_rectangle(SCREEN, self.posx, self.posy, self.size, self.size, BLACK)


class Raycaster:
    def __init__(self, size: int, resolution: int, gap: int, max_raycast_distance: int):
        self.size = size
        self.resolution = resolution
        self.gap = gap
        self.max_raycast_distance = max_raycast_distance


    @staticmethod
    def calculate_dst_to_player(x: int, y: int) -> int:
        """ Renvoie la distance au joueur calculée avec pythagore """
        ray_width = abs(PLAYER_.posx - x)
        ray_height = abs(PLAYER_.posy - y)
        dst_to_player = sqrt(ray_width ** 2 + ray_height ** 2)
        # Éviter les divisions par zéro durant la modélisation 3D
        return dst_to_player if dst_to_player > 1 else 1

    @staticmethod
    def wall_front_player_coord():
        """ Envoie un ray depuis la direction du joueur jusqu'à un mur """
        posx, posy = PLAYER_.posx, PLAYER_.posy
        lg_x, lg_y = trouver_longueurs_trigo(PLAYER_.angle)

        while not collide_something(posx, posy):
            posx += lg_x # comme on est en mode "console", pas besoin de checher la rapidité
            posy += lg_y # on fait juste des petits pas précis

        return posx, posy

    @staticmethod
    def last_space_before_wall_front_player_coord():
        """ Envoie un ray depuis la direction du joueur jusqu'à l'espace situé avant le mur devant le joueur """
        posx, posy = PLAYER_.posx, PLAYER_.posy
        lg_x, lg_y = trouver_longueurs_trigo(PLAYER_.angle)

        next_x, next_y = posx + lg_x, posy + lg_y

        while not collide_something(next_x, next_y):
            posx, posy = next_x, next_y

            next_x += lg_x
            next_y += lg_y

        return posx, posy

    @staticmethod
    def every_wall_in_player_direction():
        """ Envoie un ray et retourne tous les murs qu'il a croisé """
        liste_murs = []

        posx, posy = PLAYER_.posx, PLAYER_.posy
        player_row, player_column = int(posy // CELLSIZE_Y), int(posx // CELLSIZE_X)
        lg_x, lg_y = trouver_longueurs_trigo(PLAYER_.angle)

        while 0 < posx < SCREEN_lg and 0 < posy < SCREEN_ht:

            # calculer les coordonnées sur la grille
            row = int(posy // CELLSIZE_Y)
            column = int(posx // CELLSIZE_X)

            if not(player_row == row and player_column == column): # si le ray n'est pas dans la même case que le joueur
                if (row, column) not in liste_murs: # Si le mur n'a pas déjà été ajouté à la liste
                    liste_murs.append((row, column))


            posx += lg_x
            posy += lg_y



        return liste_murs



    def raycast_one_ray(self, angle: int) -> tuple:
        """ Envoie un ray dans une direction en degrés """
        posx, posy = PLAYER_.posx, PLAYER_.posy
        lg_x, lg_y = trouver_longueurs_trigo(angle)

        #while not(collide_wall(posx, posy)): <= utiliser si on en a r à foutre de max_distance
        for distance in range(0, self.max_raycast_distance, self.gap):
            x, y = posx + lg_x * distance, posy + lg_y * distance
            if collide_something(x, y):
                if MAP:
                    self.show(x, y)
                    pg.display.update()
                # On met le minimum à 1 millième pour ne pas avoir des dimensions qui vont à l'infini durant la modélisation
                corrected_distance = max(0.001, distance * cos(radians(angle - PLAYER_.angle)))  # Correction anti-fisheye
                wall_color = get_wall_color(x, y)
                return corrected_distance, wall_color
            distance += self.gap
        return None, None


    def raycast(self, fov: tuple) -> tuple:
        raycast_distances = []
        wall_colors = []
        current_angle = fov[0]
        while current_angle <= fov[1]:
            ray_info = self.raycast_one_ray(angle=current_angle)
            raycast_distances.append(ray_info[0])
            wall_colors.append(ray_info[1])
            current_angle += self.resolution
        return raycast_distances, wall_colors


    def show(self, x: int, y: int) -> None:
        draw_rectangle(SCREEN, x, y, self.size, self.size, BLUE)


def execute_game_command(command_txt):
    """ La commande est donnée par l'user : ici tentative d'éxecution de cette commande """
    liste_command_args = command_txt.split(" ")
    message_erreur = "Commande non executée"
    message_reussite = "Commande exécutée avec succès"

    if not liste_command_args:
        return message_erreur

    if liste_command_args[0] == "change_wall_coord":
        if len(liste_command_args) != 4:
            print("Mauvais nombre d'arguments")
            return message_erreur

        # Eh oui : column = "position x" / row = "position y"
        column_idx, row_idx, color = liste_command_args[1], liste_command_args[2], liste_command_args[3]

        if not(column_idx.isdigit() and row_idx.isdigit() and color.isdigit()):
            print("Arguments non valides (doivent être nombres)")
            return message_erreur

        column_idx, row_idx, color = int(column_idx), int(row_idx), int(color)

        if not(0 <= column_idx < nb_column_liste_map and 0 <= row_idx < nb_row_liste_map):
            print("Les coordonnées dépassent la grille")
            return message_erreur

        if not(0 <= color <= 5):
            print("Mauvaise couleur")
            return message_erreur

        print(f"Changement du mur ({column_idx},{row_idx}) à \"{dic_colors[color]}\"")

        liste_map[row_idx][column_idx] = color

        print("Changement de la carte...")

        # On update le cache de la carte car il a été changé
        draw_2d_background(background_2D, liste_map)

        return message_reussite

    # En vrai c'est 2 actions différentes mais elles ont beacoup en commun dcp on va les "merger"
    if liste_command_args[0] == "change_wall_dir" or liste_command_args[0] == "add_wall_dir":
        if len(liste_command_args) != 2:
            print("Mauvais nombre d'arguments")
            return message_erreur

        color = liste_command_args[1]

        if not color.isdigit():
            print("La couleur n'est pas un chiffre")
            return message_erreur

        color = int(color)

        if not 0 <= color <= 5:
            print(f"{color} : Couleur non compatible")
            return message_erreur


        if liste_command_args[0] == "change_wall_dir":
            x, y = Raycaster.wall_front_player_coord()
        else:
            x, y = Raycaster.last_space_before_wall_front_player_coord()

        if x <= 0 or x >= SCREEN_lg or y <= 0 or y >= SCREEN_ht:  # On touche le bord
            print("Un bord ne peut pas être changé")
            return message_erreur

        row = int(y // CELLSIZE_Y)
        column = int(x // CELLSIZE_X)

        player_row, player_column = int(PLAYER_.posy // CELLSIZE_Y), int(PLAYER_.posx // CELLSIZE_X)

        if player_row == row and player_column == column:
            print("Vous ne pouvez pas ajouter un mur au même endroit que votre personnage")
            return message_erreur

        liste_map[row][column] = color

        print("Changement de la carte...")

        # On update le cache de la carte car il a été changé
        draw_2d_background(background_2D, liste_map)

        return message_reussite

    if liste_command_args[0] == "change_every_wall_in_dir":
        if not len(liste_command_args) == 2:
            print("Mauvais nombre d'arguments")
            return message_erreur

        color = liste_command_args[1]

        if not color.isdigit():
            print("La couleur n'est pas un chiffre")
            return message_erreur

        color = int(color)

        if not 0 <= color <= 5:
            print(f"{color} : Couleur non compatible")
            return message_erreur

        liste_murs_a_changer = Raycaster.every_wall_in_player_direction()

        for (row, column) in liste_murs_a_changer:
            print(row, column)
            liste_map[row][column] = color

        print("Changement de la carte...")

        # On update le cache de la carte car il a été changé
        draw_2d_background(background_2D, liste_map)

        return message_reussite




    print("Commande non reconnue")
    return message_erreur



def draw_command_executing(surface):
    surface.fill(BLACK)
    # Créer une surface de texte
    text = "Exécutez la commande dans le cmd"
    text_color = GREEN
    text_surface = font.render(text, True, text_color)

    # Définir la position du texte
    text_rect = text_surface.get_rect()
    text_rect.center = (surface.get_width() // 2, surface.get_height() // 2)
    surface.blit(text_surface, text_rect)


def draw_2d_background(surface, liste_world):
    for idx_row, row in enumerate(liste_world):
        for idx_column, column in enumerate(row):

            if column != 0:
                color = dic_colors[column]
            else:
                color = WHITE2 # Nous remplaçons ici le transparent par du blanc pur (sur la carte bien sûr)

            draw_rectangle(surface, idx_column * CELLSIZE_X, idx_row * CELLSIZE_Y, CELLSIZE_X, CELLSIZE_Y,
                           color)
def show_map():
    """ Dessine une carte à partir d'une liste de dimension 2 (x et y) """
    SCREEN.blit(background_2D, (0, 0))
    PLAYER_.show()


def draw_3d_background(surface):
    # Remplir l'écran du haut
    draw_rectangle(surface, 0, 0, SCREEN_lg, HALF_SCREEN_ht, LIGHTGRAY)

    # Remplir l'écran du bas
    draw_rectangle(surface, 0, HALF_SCREEN_ht, SCREEN_lg, HALF_SCREEN_ht, DARKGRAY)

def show_3d(liste_raycast: list, wall_colors: list) -> None:
    """ Dessine en 3D avec une liste des distances + "couleurs" pour chque distance """

    default_wall_height = 5000 # Constante pour dimensionner les murs

    # Mettre l'arrière plan 3d
    SCREEN.blit(background_3D, (0, 0))

    nb_of_rays = len(liste_raycast)
    ray_width = SCREEN_lg / nb_of_rays


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
        draw_rectangle(SCREEN, ray_x_int, HALF_SCREEN_ht - int(wall_height / 2), ray_width_int, int(wall_height),
                       wall_color_with_shades)


background_command_is_executing = pg.Surface((SCREEN_lg, SCREEN_ht))
draw_command_executing(background_command_is_executing)

background_2D = pg.Surface((SCREEN_lg, SCREEN_ht))
draw_2d_background(background_2D, liste_map)

background_3D = pg.Surface((SCREEN_lg, SCREEN_ht))
draw_3d_background(background_3D)




PLAYER_ = Player(size=PLAYER_SIZE, spawn_type=PLAYER_SPAWN_TYPE)

RAYCASTER_ = Raycaster(size=RAYCASTER_SIZE,
                       resolution=RAYCASTER_RES,
                       max_raycast_distance=RAYCASTER_MAX_DST,
                       gap=RAYCASTER_GAP)


running = True


while running:
    # Mettre à jour la direction de la FOV
    mouse_x = get_mouse_x_direction()
    FOV = (mouse_x - FOV_MAX // 2, mouse_x + FOV_MAX // 2)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    # Handling des keys
    keys = pg.key.get_pressed()
    if keys[key_up]:
        PLAYER_.move_player(0)
    if keys[key_down]:
        PLAYER_.move_player(-180)
    if keys[key_left]:
        PLAYER_.move_player(-90)
    if keys[key_right]:
        PLAYER_.move_player(90)
    if keys[pg.K_m]:
        MAP = True
    if keys[pg.K_l]:
        MAP = False
    if keys[pg.K_c]:
        pg.mouse.set_visible(True)
        SCREEN.blit(background_command_is_executing, (0, 0))
        pg.display.update()
        print(execute_game_command(input(f"\nListe des commandes : \n"
                                         f" => change_wall_coord \"x\" \"y\" \"couleur\"\n"
                                         f" => change_wall_dir \"couleur\"\n"
                                         f" => add_wall_dir \"couleur\"\n"
                                         f" => change_every_wall_in_dir \"couleur\"\n"
                                         f"\n>> ")))
        pg.mouse.set_visible(False)

    # Raycasting et dessin
    liste_raycast_dst, liste_wall_colors = RAYCASTER_.raycast(fov=FOV)

    if MAP:
        show_map()
    else:
        show_3d(liste_raycast_dst, liste_wall_colors)


    pg.display.update()
    clock.tick(FPS)

pg.quit()

# ajouter buffer pour "menu" (touches de déplacement + touches commandes)
