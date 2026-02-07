import pygame
import parryminigame
import platformerminigame
import circleminigame
import memorygame

class SceneManager:
    def __init__(self):
        self.minigame_cycle = ["circle", "parry", "platformer"]
        self.current_index = 0
        self.scenes = {"circle": circleminigame.CircleMinigame(self),
                       "parry": parryminigame.ParryMinigame(self),
                       "platformer": platformerminigame.PlatformerMiniGame(self),
                       "memory": memorygame.MemoryGame(self)
                       }
        self.current_scene = self.scenes[self.minigame_cycle[self.current_index]]

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def change_scene(self, name):
        if name == "memory":
            mem = self.scenes["memory"]
            mem.showing_sequence = True
            mem.sequence_start_time = pygame.time.get_ticks()
        self.current_scene = self.scenes[name]

    def next_minigame(self):
        self.current_index = (self.current_index + 1) % len(self.minigame_cycle)
        next_name = self.minigame_cycle[self.current_index]
        self.current_scene = self.scenes[next_name]

    def handle_events(self, events):
        if self.current_scene:
            self.current_scene.handle_events(events)

    def update(self):
        if self.current_scene:
            self.current_scene.update()
    
    def draw(self, screen):
        if self.current_scene:
            self.current_scene.draw(screen)
        
    
        
