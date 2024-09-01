from settings import *

class GameCommand:
    def __init__(self, raycaster, player, level_master) -> None:
        self.raycaster = raycaster
        self.player = player
        self.level_master = level_master
        self.command_txt = ""
        self.execution_sucess = False
        self.supported_commands = [
            "change_wall_coord", 
            "change_wall_dir", 
            "add_wall_dir", 
            "change_every_wall_in_dir"
        ]
    

    def receive_command(self, command_txt: str):
        if not command_txt or not command_txt.isascii():
            self.execution_sucess = False
            return

        command_txt = command_txt.lower()
        self.command_args = command_txt.split(" ")
        self.command_title = self.command_args[0]

        if self.command_title not in self.supported_commands:
            print(f"Commande \"{self.command_title}\" non reconnue")
            self.execution_sucess = False
            return 

        self.command_lenght = len(self.command_args)

    
    def change_wall_coord(self):
        if self.command_lenght != 4:
            self.execution_sucess = False
            return
        
        # Eh oui : column = "position x" / row = "position y"
        column_idx, row_idx, color = self.command_args[1], self.command_args[2], self.command_args[3]

        if not(column_idx.isdigit() and row_idx.isdigit() and color.isdigit()):
            print("Arguments non valides (doivent être nombres)")
            self.execution_sucess = False
            return

        column_idx, row_idx, color = int(column_idx), int(row_idx), int(color)

        if not(0 <= column_idx < self.level_master.map_data_dims[0] and 0 <= row_idx < self.level_master.map_data_dims[1]):
            print("Les coordonnées dépassent la grille")
            self.execution_sucess = False
            return

        if not(0 <= color <= 5):
            print("Mauvaise couleur")
            self.execution_sucess = False
            return

        print(f"Changement du mur ({column_idx},{row_idx}) à \"{dic_colors[color]}\"")

        self.level_master.map_data[row_idx][column_idx] = color

        self.execution_sucess = True

        return
    

    def alter_wall_dir(self):
        if self.command_lenght != 2:
            print("Mauvais nombre d'arguments")
            self.execution_sucess = False
            return
        
        color = self.command_args[1]

        if not color.isdigit():
            print("La couleur n'est pas un chiffre")
            return
        
        color = int(color)

        if not 0 <= color <= 5:
            print(f"{color} : Couleur non compatible")
            self.execution_sucess = False
            return
        
        if self.command_title == "change_wall_dir":
            wall_posx, wall_posy = self.raycaster.wall_front_player_coord()
        else:
            wall_posx, wall_posy = self.raycaster.last_space_before_wall_front_player_coord()
        
        if wall_posx <= 0 or wall_posx >= SCREEN_DIMS[0] or wall_posy <= 0 or wall_posy >= SCREEN_DIMS[1]:  # On touche le bord
            print("Un bord ne peut pas être changé")
            self.execution_sucess = False
            return
        
        row = int(wall_posy // CELL_DIMS[1])
        column = int(wall_posx // CELL_DIMS[0])

        player_row, player_column = int(self.player.posy // CELL_DIMS[1]), int(self.player.posx // CELL_DIMS[0])

        if player_row == row and player_column == column:
            print("Vous ne pouvez pas ajouter un mur au même endroit que votre personnage")
            self.execution_sucess = False
            return

        self.level_master.map_data[row][column] = color

        print("Changement de la carte...")

        self.execution_sucess = True

        return

    
    def change_every_wall_in_dir(self):
        if self.command_lenght != 2:
            print("Mauvais nombre d'arguments")
            self.execution_sucess = False
            return
        
        color = self.command_args[1]
        if not color.isdigit():
            print("La couleur n'est pas un chiffre")
            self.execution_sucess = False
            return
        
        color = int(color)

        if not 0 <= color <= 5:
            print(f"{color} : Couleur non compatible")
            self.execution_sucess = False
            return
        

        walls_changing = self.raycaster.every_wall_in_player_direction()

        for (row, column) in walls_changing:
            self.level_master.map_data[row][column] = color

        print("Changement de la carte...")

        self.execution_sucess = True

        return