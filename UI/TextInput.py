from dataclasses import field
import pygame

class TextInput:
    def __init__(self, x, y, width, height, font_size=36, text_color=(255, 255, 255), bg_color=(50, 50, 50), border_color=(255, 255, 255), border_radius=10, border_width=2, max_chars=3, scale=1, text="0.0"):
        pygame.font.init()  # Initialize fonts
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_size = font_size
        self.text_color = text_color
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.border_width = border_width
        self.max_chars = max_chars
        self.realValue = 0
        self.text = text
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_position = 0
        self.offset = 0
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, self.font_size)  # Use default
        self.active = False  # Track if the text box is active
        
        self.scale = scale

        self.divider = (1080 / scale) / 144
    def field_to_inches(self, a):
        return round(a / self.divider, 1)
    def inches_to_field(self, a):
        return round(a * self.divider, 1)
    def draw(self, screen):
        # Draw the background and border
        pygame.draw.rect(screen, self.border_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.bg_color, self.rect.inflate(-self.border_width * 2, -self.border_width * 2), border_radius=self.border_radius)

        # Render the visible portion of the text
        visible_text = self.text[self.offset:]
        text_surface = self.font.render(visible_text, True, self.text_color)
        text_rect = text_surface.get_rect(midleft=(self.x + 10, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)

        # Draw the cursor
        if self.active and self.cursor_visible:
            cursor_x = self.x + 10 + self.font.size(self.text[:self.cursor_position])[0] - self.font.size(self.text[:self.offset])[0]
            if self.rect.left + 10 <= cursor_x <= self.rect.right - 10:
                pygame.draw.line(screen, self.text_color, (cursor_x, self.y + 5), (cursor_x, self.y + self.height - 5), 2)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is inside the text box
            if self.rect.collidepoint(event.pos):
                self.active = True
                # Set cursor position based on click location
                click_x = event.pos[0] - (self.x + 10)
                self.cursor_position = self.get_cursor_from_click(click_x)
                self.adjust_offset()
            else:
                self.active = False

        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_position > 0:
                    self.text = self.text[:self.cursor_position - 1] + self.text[self.cursor_position:]
                    self.cursor_position -= 1
                self.adjust_offset()
            elif (event.unicode.isdigit() or event.unicode == '.'):
                new_value = float(self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:])
                if new_value <= 144 and new_value >= 0:
                    # Allow only one decimal point
                    if event.unicode == '.' and '.' in self.text:
                        return
                    self.text = self.text[:self.cursor_position] + event.unicode + self.text[self.cursor_position:]
                    self.cursor_position += 1
                    self.adjust_offset()
            elif event.key == pygame.K_LEFT:
                if self.cursor_position > 0:
                    self.cursor_position -= 1
                self.adjust_offset()
            elif event.key == pygame.K_RIGHT:
                if self.cursor_position < len(self.text):
                    self.cursor_position += 1
                self.adjust_offset()

    def get_cursor_from_click(self, click_x):
        # Determine the cursor position based on the click location
        total_width = 0
        for i, char in enumerate(self.text):
            char_width = self.font.size(char)[0]
            if total_width + char_width // 2 > click_x:
                return i
            total_width += char_width
        return len(self.text)

    def adjust_offset(self):
        # Ensure the cursor is visible within the text box
        cursor_x = self.font.size(self.text[:self.cursor_position])[0]
        if cursor_x - self.font.size(self.text[:self.offset])[0] > self.width - 20:
            self.offset += 1
        elif self.offset > 0 and cursor_x - self.font.size(self.text[:self.offset])[0] < 0:
            self.offset -= 1

    def update(self):
        # Blink the cursor
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
    def getValue(self):
        try:
            return self.inches_to_field(float(self.text))
        except ValueError:
            return 0.0
    def setValue(self, value):
        self.text = str(self.field_to_inches(value))
        self.cursor_position = len(self.text)
        self.offset = 0