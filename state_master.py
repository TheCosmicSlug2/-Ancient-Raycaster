from settings import *

class StateMaster:
    def __init__(self) -> None:
        self.map_shown = False
        self.tick_map_update = 0
        self.mouse_visible = False
        self.tick_mouse_visible = 0
    
    def check_map_update_possible(self):
        if self.tick_map_update < ticks_to_update_map:
            return 
        
        self.tick_map_update = 0
        self.map_shown = not(self.map_shown)
    
    def check_mouse_update_possible(self):
        if self.tick_mouse_visible < ticks_to_update_mouse:
            return 
        
        self.tick_mouse_visible = 0
        self.mouse_visible = not(self.mouse_visible)
    
    def update(self):
        self.tick_map_update += 1
        if self.tick_map_update > FPS * 5:
            self.tick_map_update = FPS

        self.tick_mouse_visible += 1
        if self.tick_mouse_visible > FPS * 5:
            self.tick_mouse_visible = FPS