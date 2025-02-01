import pygame

class Button:
    def __init__(self, x, y, width, height, text, font_size=36, text_color=(255, 255, 255), button_color=(0, 0, 255), hover_color=(0, 0, 200), border_color=(255, 255, 255), border_radius=10, border_width=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size
        self.text_color = text_color
        self.button_color = button_color
        self.hover_color = hover_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.border_width = border_width
        self.rect = pygame.Rect(x, y, width, height)
        self.hovered = False

    def draw(self, screen):
        color = self.hover_color if self.hovered else self.button_color
        pygame.draw.rect(screen, self.border_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, color, self.rect.inflate(-self.border_width*2, -self.border_width*2), border_radius=self.border_radius)
        font = pygame.font.Font(None, self.font_size)
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.hovered:
                return True
        return False