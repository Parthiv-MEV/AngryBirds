import pygame
class ToggleButton:
    def __init__(self, x, y, width, height, text, initial=False, color_on=(0,200,0), color_off=(200,0,0), font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.state = initial
        self.color_on = color_on
        self.color_off = color_off
        self.font = font or pygame.font.SysFont(None, 32)

    def draw(self, surface):
        color = self.color_on if self.state else self.color_off
        pygame.draw.rect(surface, color, self.rect, border_radius=self.rect.height//3)
        pygame.draw.rect(surface, (0,0,0), self.rect, 2, border_radius=self.rect.height//3)
        text_surface = self.font.render(self.text, True, (255,255,255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state  # Toggle state
                return True  # Indicates it was toggled
        return False