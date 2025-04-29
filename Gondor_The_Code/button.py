import pygame
class Button:
    def __init__(self, x, y, width, height, text, color=(0, 255, 0), hover_color=(0, 200, 0),font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = font
        self.is_hovered = False
        
    def draw(self, surface):
        # Use hover color if mouse is over button
        current_color = self.hover_color if self.is_hovered else self.color
        
        pygame.draw.rect(surface, current_color, self.rect, border_radius=self.rect.height//3)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=self.rect.height//3)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def update(self, mouse_pos):
        # Update hover state
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)