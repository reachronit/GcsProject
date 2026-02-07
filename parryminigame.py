import pygame
class ParryMinigame:
    def __init__(self, manager):
        self.manager = manager
        self.screen_width = 800
        self.screen_height = 600

        self.player_width = 30
        self.player_length = 35
        self.player_rect = pygame.Rect(((self.screen_width/2)-(self.player_width/2)), (self.screen_height - 25), self.player_width, self.player_length)

        self.enemy_width = 30
        self.enemy_length = 35
        self.enemy_rect = pygame.Rect(((self.screen_width/2)-(self.enemy_width/2)), 50, self.enemy_width, self.enemy_length)
        
        self.bullet_width = 9
        self.bullet_length = 9
        self.bullet_speed = 10
        self.bullet_rect = pygame.Rect(self.enemy_rect.x + self.enemy_width / 2, self.enemy_rect.y + self.enemy_length, self.bullet_width, self.bullet_length)

        self.parry_window = 13
        self.frame_counter = 0
        self.parries_left = 1
        self.active_parry = False
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.parries_left > 0:
                        self.parries_left -= 1
                        self.active_parry = True
                        self.frame_counter = 0

    def update(self):
        self.bullet_rect.y += self.bullet_speed

        if self.active_parry:
            self.frame_counter += 1
            if self.frame_counter >= self.parry_window:
                self.active_parry = False

        if self.bullet_rect.colliderect(self.player_rect):
            if self.active_parry:
                print("WIN MINIGAME")
                self.manager.change_scene("memory")
                if self.bullet_speed < 30:
                    self.bullet_speed += 2
                self.bullet_rect.y = self.enemy_rect.y + self.enemy_length
                self.bullet_rect.x = self.enemy_rect.x + self.enemy_width / 2
                self.parries_left = 1
                self.frame_counter = 0
                self.active_parry = False
            else:
                print("LOSE MINIGAME")
                self.manager.change_scene("parry")
                self.bullet_rect.y = self.enemy_rect.y + self.enemy_length
                self.bullet_rect.x = self.enemy_rect.x + self.enemy_width / 2
                self.parries_left = 1
                self.frame_counter = 0
                self.active_parry = False
    
    def draw(self, screen):
        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (255, 255, 255), self.player_rect)
        pygame.draw.rect(screen, (255, 0, 0), self.enemy_rect)
        pygame.draw.rect(screen, (139, 0, 0), self.bullet_rect)
        if self.active_parry:
            pygame.draw.rect(screen, (0, 255, 0), self.player_rect)
