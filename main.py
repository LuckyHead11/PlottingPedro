from re import X
import pygame
import sys
from BezierCurve import BezierCurve
import Slider
        
curves = []
current_curve = 0

STATES = {
    "START": 0,
    "END": 1
    
}
padding = 100
x1_slider = Slider.Slider(1100, 100, 100, 20, 0, 10, 0, "x1")
y1_slider = Slider.Slider(1100, 100 + padding, 100, 20, 0, 10, 0, "y1")
x2_slider = Slider.Slider(1100, 100 + (padding * 2), 100, 20, 0, 10, 0, "x2")
y2_slider = Slider.Slider(1100, 100 + (padding * 3), 100, 20, 0, 10, 0, "y2")
state = STATES["START"]
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
startX = 0
startY = 0

endX = 0
endY = 0



field_image = pygame.image.load("photos/dark.png")
field_image = pygame.transform.scale(field_image, (1080, 1080))

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1600, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Basic Pygame Window")

def draw():
    screen.fill((0, 0, 0)) # Clear the screen
    #Draw the field
    screen.blit(field_image, (0, 0))

    if state == STATES["END"]:
        pygame.draw.circle(screen, GREEN, (int(startX), int(startY)), 6)
    for curve in curves:
        #Draw a small circle at the start and end points
        pygame.draw.circle(screen, RED, (int(curve.x0), int(curve.y0)), 6)
        pygame.draw.circle(screen, RED, (int(curve.x3), int(curve.y3)), 6)
        #Draw the curve
        for i in range(100):
            t = i / 100
            x0, y0 = curve.calculate_curve(t)
            t = (i + 1) / 100
            x1, y1 = curve.calculate_curve(t)
            pygame.draw.line(screen, BLUE, (int(x0), int(y0)), (int(x1), int(y1)), 2)
    #On the right side of the screen, draw 2 sliders for the x1 and y1 values, and the x2 and y2 values
    x1_slider.draw(screen)
    y1_slider.draw(screen)
    x2_slider.draw(screen)
    y2_slider.draw(screen)

def logic():
    if len(curves) != 0:
        x1_value = x1_slider.value
        y1_value = y1_slider.value
        x2_value = x2_slider.value
        y2_value = y2_slider.value
        
        current_beziercurve = curves[current_curve]
        current_beziercurve.x1 = x1_value
        current_beziercurve.y1 = y1_value
        current_beziercurve.x2 = x2_value
        current_beziercurve.y2 = y2_value
    
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if state == STATES["START"]:
                #If thed mouse position is in the image
                x0, y0 = pygame.mouse.get_pos()
                if x0 < 1080 and y0 < 1080:
                    startX = x0
                    startY = y0
                    state = STATES["END"]
                    
            elif state == STATES["END"]:
                x3, y3 = pygame.mouse.get_pos()
                if x3 < 1080 and y3 < 1080:
                    if endX and endY != 0:
                        startX = endX
                        startY = endY
                    endX = x3
                    endY = y3
                    
                    curves.append(BezierCurve(startX, startY, x0, y3, x3, y3, endX, endY))
        x1_slider.handle_event(event)
        y1_slider.handle_event(event)
        x2_slider.handle_event(event)
        y2_slider.handle_event(event)
    # Fill the screen with a color (optional)
    draw()
    logic()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()