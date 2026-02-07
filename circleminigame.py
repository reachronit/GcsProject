import pygame
import random

class CircleMinigame:
    def __init__(self, manager):
        self.manager = manager
        self.screen_width = 800
        self.screen_height = 600

        self.circle_radius = 50
        self.circle_x = random.randint(50, self.screen_width - 50)
        self.circle_y = random.randint(50, self.screen_height - 50)

        self.font = pygame.font.SysFont(None, 36)

        self.clicks_done = 0
        self.required_clicks = 5
        self.time_limit = 20
        self.start_time = pygame.time.get_ticks()
        self.time_left = self.time_limit
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                distance = ((mx - self.circle_x)**2 + (my - self.circle_y)**2)**0.5
                if distance <= self.circle_radius:
                    self.clicks_done += 1
                    self.circle_x = random.randint(50, self.screen_width - 50)
                    self.circle_y = random.randint(50, self.screen_height - 50)



    def update(self):
        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        self.time_left = max(0, self.time_limit - elapsed)

        if self.clicks_done >= self.required_clicks:
            print("WIN MINIGAME")
            self.manager.change_scene("memory")
            self.start_time = pygame.time.get_ticks()
            self.time_left = self.time_limit
            self.circle_x = random.randint(50, self.screen_width - 50)
            self.circle_y = random.randint(50, self.screen_height - 50)
            self.time_left = self.time_limit
            self.clicks_done = 0
            if self.required_clicks < 17 and self.time_limit > 8:
                self.required_clicks += 1
                self.time_limit -= 1

        if self.time_left <= 0:
            print("LOSE MINIGAME")
            self.manager.change_scene("circle")
            
            self.start_time = pygame.time.get_ticks()
            self.time_left = self.time_limit
            self.circle_x = random.randint(50, self.screen_width - 50)
            self.circle_y = random.randint(50, self.screen_height - 50)
            self.time_left = self.time_limit
            self.clicks_done = 0


    def draw(self, screen):
        screen.fill((0, 0, 0))

        counter_text = self.font.render(f"Clicks: {self.clicks_done}/{self.required_clicks}", True, (255, 255, 255))
        screen.blit(counter_text, (self.screen_width - 150, 20))

        time_text = self.font.render(f"{int(self.time_left)} time left", True, (255, 255, 255))
        text_rect = time_text.get_rect(center=(self.screen_width // 2, 20))
        screen.blit(time_text, text_rect)

        pygame.draw.circle(screen, (255, 255, 255), (self.circle_x, self.circle_y), 50)
