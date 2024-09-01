import pygame as pg
from math import radians, cos, sin, sqrt
from level_master import LevelMaster
from settings import *
from input_handler import InputHandler
from player import Player
from renderer import Renderer
from raycaster import Raycaster
from command_prompt import GameCommand
from state_master import StateMaster

#from profilehooks import profile
#@profile(stdout=False, filename='g.prof')  # <== Profiling

def main():
    # Pygame :
    pg.init()
    pg.mouse.set_visible(False)

    level_master = LevelMaster()
    renderer = Renderer(level_master=level_master)

    player = Player(spawn_type=PLAYER_SPAWN_TYPE, level_master=level_master)

    raycaster = Raycaster(player=player, level_master=level_master, renderer=renderer)

    input_handler = InputHandler()

    command_prompt = GameCommand(raycaster=raycaster, player=player, level_master=level_master)

    state_master = StateMaster()

    game_running = True


    while game_running:
        # Mettre à jour la direction de la FOV
        mouse_x = input_handler.get_mouse_x_direction(player)
        FOV = (mouse_x - FOV_MAX // 2, mouse_x + FOV_MAX // 2)

        mouse_event = input_handler.get_mouse_event()
        if mouse_event == "quit_game":
            game_running = False

        # Handling des keys
        pressed_keys = input_handler.get_keyboard_events()
        
        if "haut" in pressed_keys:
            player.move(0)
        if "bas" in pressed_keys:
            player.move(-180)
        if "gauche" in pressed_keys:
            player.move(-90)
        if "droite" in pressed_keys:
            player.move(90)
        

        if "map" in pressed_keys:
            state_master.check_map_update_possible()

        if "cmd" in pressed_keys:
            pg.mouse.set_visible(True)
            pg.display.update()

            input_command = input(
                f"\nListe des commandes : \n"
                f" => change_wall_coord \"x\" \"y\" \"couleur\"\n"
                f" => change_wall_dir \"couleur\"\n"
                f" => add_wall_dir \"couleur\"\n"
                f" => change_every_wall_in_dir \"couleur\"\n"
                f"\n >> ")
            command_prompt.receive_command(input_command)

            if command_prompt.command_title == "change_wall_coord":
                command_prompt.change_wall_coord()
            if command_prompt.command_title in ["change_wall_dir", "add_wall_dir"]:
                command_prompt.alter_wall_dir()
            if command_prompt.command_title == "change_every_wall_in_dir":
                command_prompt.change_every_wall_in_dir()
            

            if command_prompt.execution_sucess:
                renderer.render_minimap()
                print("Commande executée avec succès - Changement de la carte")
            else:
                print("Commande non exécutée")

            pg.mouse.set_visible(False)
        
        if "esc" in pressed_keys:
            state_master.check_mouse_update_possible()
            pg.mouse.set_visible(state_master.mouse_visible)

        # Raycasting et dessin
        liste_raycast_dst, liste_wall_colors = raycaster.raycast(fov=FOV, map_shown=state_master.map_shown)

        if state_master.map_shown:
            renderer.render_minimap_on_screen(player, raycaster)
        else:
            renderer.render_3D_foreground(liste_raycast_dst, liste_wall_colors)
            renderer.render_3D_foreground_on_screen()
        
        renderer.update()
        state_master.update()

    pg.quit()

    # ajouter buffer pour "menu" (touches de déplacement + touches commandes)


if __name__ == "__main__":
    main()
