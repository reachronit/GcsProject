import pygame
import scenemanager

class PlatformerMiniGame:
    def __init__(self, manager):
        self.manager = manager
        self.player_rect = pygame.Rect(391, 291, 18, 18)
        self.player_speed = 8
        self.box_rect = pygame.Rect(80, 60, 640, 480)

        self.vel_y = 0
        self.gravity = 0.9
        self.jump_strength = -18

        self.obstacles = []
        self.spawn_timer = pygame.time.get_ticks()
        self.spawn_interval = 2500
        self.phase = 0
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if abs(self.player_rect.bottom - self.box_rect.bottom) < 3:
                        self.vel_y = self.jump_strength

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player_rect.x -= self.player_speed
        if keys[pygame.K_d]:
            self.player_rect.x += self.player_speed

        if pygame.time.get_ticks() - self.spawn_timer >= self.spawn_interval and self.phase < 5:
            self.spawn_obstacle()
            self.phase += 1
            self.spawn_timer = pygame.time.get_ticks()
        elif self.phase >= 5 and len(self.obstacles) == 0:
            print("WIN MINIGAME")
            self.manager.change_scene("memory")
            self.vel_y = 0
            self.player_rect.y = self.box_rect.bottom - self.player_rect.height
            self.spawn_interval = max(500, self.spawn_interval - 250)
            self.phase = 0
            self.spawn_timer = pygame.time.get_ticks()
            self.obstacles = []

        
        self.vel_y += self.gravity
        self.player_rect.y += self.vel_y
        
        if self.player_rect.right > self.box_rect.right:
            self.player_rect.x = self.box_rect.right - self.player_rect.width

        if self.player_rect.left < self.box_rect.left:
            self.player_rect.x = self.box_rect.left

        if self.player_rect.top < self.box_rect.top:
            self.player_rect.y = self.box_rect.top
            self.vel_y = 0

        if self.player_rect.bottom > self.box_rect.bottom:
            self.player_rect.y = self.box_rect.bottom - self.player_rect.height
            self.vel_y = 0

        for obs in self.obstacles[:]: 
            obs['rect'].x += obs['vx']
            obs['rect'].y += obs['vy']
            if self.is_off_screen(obs['rect']):
                self.obstacles.remove(obs)
            if self.player_rect.colliderect(obs['rect']):
                print("LOSE MINIGAME")
                self.manager.change_scene("platformer")
                self.vel_y = 0
                self.player_rect.y = self.box_rect.bottom - self.player_rect.height
                self.obstacles = []
                self.phase = 0
                self.spawn_timer = pygame.time.get_ticks()

            
    def is_off_screen(self, rect):
        screen_w = 800
        screen_h = 600
        return ( rect.right < 0
                 or rect.left > screen_w
                 or rect.bottom < 0
                 or rect.top > screen_h )

    def spawn_right_obstacle(self):
        rect = pygame.Rect(self.box_rect.right + 40, self.box_rect.bottom - self.box_rect.height / 4, self.box_rect.width / 4, self.box_rect.height / 4)
        rect_vx = -10
        rect_vy = 0
        rect_dict = {'rect': rect, 'vx': rect_vx, 'vy': rect_vy}
        self.obstacles.append(rect_dict)
    def spawn_ceiling_obstacle(self):
        rect = pygame.Rect(self.box_rect.left, self.box_rect.top - self.box_rect.height / 3, self.box_rect.width / 2, self.box_rect.height / 3)
        rect_vx = 0
        rect_vy = 10
        rect_dict = {'rect': rect, 'vx': rect_vx, 'vy': rect_vy}
        self.obstacles.append(rect_dict)
    def spawn_bottom_middle_obstacle(self):
        rect = pygame.Rect(self.box_rect.centerx - (self.box_rect.width / 3) / 2 , self.box_rect.bottom + 40, self.box_rect.width / 3, self.box_rect.height / 4)
        rect_vx = 0
        rect_vy = -10
        rect_dict = {'rect': rect, 'vx': rect_vx, 'vy': rect_vy}
        self.obstacles.append(rect_dict)

    def spawn_obstacle(self):
        if self.phase == 0:
            self.spawn_right_obstacle()
        elif self.phase == 1:
            self.spawn_bottom_middle_obstacle()
        elif self.phase == 2:
            self.spawn_ceiling_obstacle()
        elif self.phase == 3:
            self.spawn_right_obstacle()
        elif self.phase == 4:
            self.spawn_bottom_middle_obstacle()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), self.box_rect, 3)
        pygame.draw.rect(screen, (0, 0, 139), self.player_rect)

        for obs in self.obstacles:
            pygame.draw.rect(screen, (255, 255, 255), obs['rect'])
