import pygame

class Slider:
    def __init__(self, x, y, width, height, min_val=0, max_val=100, initial_val=0, name="Slider", scale=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.name = name
        self.dragging = False
        self.scale = scale

        self.divider = (1080 / scale) / 144

    def field_to_inches(self, a):
        return round(a / self.divider, 1)

    def draw(self, screen):
        # Draw a rectangle for the slider track
        pygame.draw.rect(screen, (200, 200, 200), (self.x, self.y, self.width, self.height))
        # Draw a rect for the slider handle
        handle_x = self.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.width
        pygame.draw.rect(screen, (50, 150, 255), (int(handle_x), self.y, 16//self.scale, self.height))
        # Draw the name of the slider and its value
        font = pygame.font.Font(None, 36 // (self.scale))
        changed_value = self.field_to_inches(self.value)
        text = font.render(f"{self.name}: {changed_value:.2f}", True, (255, 255, 255))
        screen.blit(text, (self.x, self.y - 40 // self.scale))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (self.x <= mouse_x <= self.x + self.width and
                self.y <= mouse_y <= self.y + self.height):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.value = self.min_val + (mouse_x - self.x) / self.width * (self.max_val - self.min_val)
                self.value = max(self.min_val, min(self.max_val, self.value))