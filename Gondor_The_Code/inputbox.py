
import pygame

class InputBox:
    def __init__(self, x, y, width, height, text='',font=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 0, 0)
        self.text = text
        self.active = False
        self.font = font
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False
            self.color = (255, 0, 0) if self.active else (0, 0, 0)
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    # Limit name length to 15 characters
                    if len(self.text) < 15:
                        self.text += event.unicode
        return None
    def draw(self, surface):
        # Render text and background
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 0,border_radius=int(self.rect.height//3))
        pygame.draw.rect(surface, self.color, self.rect, 2,border_radius=int(self.rect.height//3))
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        # Existing drawing code
        display_text = self.text if self.text else "Enter name"
        text_color = (0, 0, 0) if self.text else (180, 180, 180)
        text_surface = self.font.render(display_text, True, text_color)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))