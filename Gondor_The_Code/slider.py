import pygame
import Gondor_The_Code.const as c
class Slider:
    def __init__(self, x, y, width, height, min_value=0, max_value=1, initial=0, color=(200,200,200), handle_color=(0,0,0), font=None, label=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.min = min_value
        self.max = max_value
        self.value = initial if initial is not None else 0
        self.color = color
        self.handle_color = handle_color
        self.dragging = False
        self.font = font or pygame.font.SysFont(None, 24)
        self.label = label
        self.drawrect=pygame.Rect(x - height//2, y, width + height, height)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.get_handle_rect().collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mx = event.pos[0]
            # Clamp mouse x to slider bounds
            mx = max(self.rect.left, min(mx, self.rect.right))
            percent = (mx - self.rect.left) / self.rect.width
            self.value = self.min + percent * (self.max - self.min)

        c.windpower=self.value

    def get_handle_rect(self):
        percent = (self.value - self.min) / (self.max - self.min)
        handle_x = int(self.rect.left + percent * self.rect.width)
        handle_radius = self.rect.height // 2
        return pygame.Rect(handle_x - handle_radius, self.rect.centery - handle_radius, handle_radius*2, handle_radius*2)

    def draw(self, surface):
        # Draw line

        pygame.draw.rect(surface, self.color, self.drawrect, border_radius=self.rect.height//2)
        # Draw handle
        handle_rect = self.get_handle_rect()
        pygame.draw.ellipse(surface, self.handle_color, handle_rect)
        # Draw value as text
        value_text = self.font.render(f"{self.label}{self.value:.2f}", True, (0,0,0))
        surface.blit(value_text, (self.drawrect.right + 10, self.drawrect.centery - value_text.get_height()//2))

