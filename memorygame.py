import pygame
import random
import scenemanager

class MemoryGame:
    def __init__(self, manager):
        self.manager = manager
        self.font = pygame.font.SysFont(None, 48)
        new_num = random.randint(1, 4)
        self.sequence = []
        self.sequence.append(new_num)
        self.direction_map = {
            1: "up",
            2: "down",
            3: "left",
            4: "right"
        }
        self.user_input = []
        self.showing_sequence = True
        self.sequence_start_time = pygame.time.get_ticks()
        self.sequence_flash_time = 3000
        self.sequence_index = 0
        self.sequence_text = ""

        self.up_rect = pygame.Rect(360, 120, 80, 80)
        self.down_rect = pygame.Rect(360, 360, 80, 80)
        self.left_rect = pygame.Rect(240, 240, 80, 80)
        self.right_rect = pygame.Rect(480, 240, 80, 80)



        self.loss_text_displayed = False

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.showing_sequence == False:
                    mx, my = event.pos
                    if self.up_rect.collidepoint(mx, my):
                        self.user_input.append(1)
                    elif self.down_rect.collidepoint(mx, my):
                        self.user_input.append(2)
                    elif self.left_rect.collidepoint(mx, my):
                        self.user_input.append(3)
                    elif self.right_rect.collidepoint(mx, my):
                        self.user_input.append(4)

    def loss_text(self, screen):
        screen.fill((0, 0, 0))
        text_surface = self.font.render("YOU LOST", True, (255, 0, 0))
        text_rect = text_surface.get_rect(center=(400, 300))
        screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.delay(3500)

    def update(self):
        if self.showing_sequence and self.sequence_start_time == 0:
            self.sequence_start_time = pygame.time.get_ticks()

        if self.showing_sequence:
            if pygame.time.get_ticks() - self.sequence_start_time >= 3000:
                self.showing_sequence = False

        if self.showing_sequence:
            words = []
            for n in self.sequence:
                words.append(self.direction_map[n])
            self.sequence_text = ",".join(words)

        if self.showing_sequence:
            return
        
        if len(self.user_input) == 0:
            return

        expected = self.sequence[len(self.user_input) - 1]
        actual = self.user_input[-1]

        if actual != expected: 
            print("YOU LOST")
            self.loss_text_displayed = True
            return
        
        if len(self.user_input) == len(self.sequence):
            print("WIN ROUND")
            self.sequence.append(random.randint(1, 4))
            self.user_input = []
            self.showing_sequence = True
            self.sequence_start_time = pygame.time.get_ticks()
            self.manager.next_minigame()

    def draw(self, screen):
        screen.fill((0, 0, 0))

        pygame.draw.rect(screen, (255, 255, 255), self.up_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.down_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.left_rect)
        pygame.draw.rect(screen, (255, 255, 255), self.right_rect)

        if self.loss_text_displayed:
            self.loss_text(screen)
            pygame.quit()
            import sys
            sys.exit()

        if self.showing_sequence:
            if self.showing_sequence:
                text_surface = self.font.render(self.sequence_text, True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(400, 50))
                screen.blit(text_surface, text_rect)
