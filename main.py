import os
import json
from re import X
from sqlite3 import connect
import pygame
import sys
def generate_config():
    config = {
        "scale": 1,
        "fieldImg": "field.png"
    }
    with open('config.txt', 'w') as file:
        json.dump(config, file)

# If there is no config file generate one
if not os.path.exists('config.txt'):
    generate_config()

#Making sure there is a config file before importing the classes
from BezierCurve import BezierCurve
from Slider import Slider
from Button import Button



with open('config.txt', 'r') as file:
    config = json.load(file)
    scale = config.get('scale')
    field_img = config.get("fieldImg")
divider = (1080 / scale) / 144
curves = []
current_curve = 0

STATES = {
    "START": 0,
    "END": 1
    
}

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_PURPLE = (255, 0, 255)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 200, 0)
LIGHT_GRAY = (200, 200, 200)

padding = 100 // scale
x1_slider = Slider(1100 // scale, 100 // scale, 100, 20 // scale, 0, 1080 // scale, 0, "x1", scale=scale)
y1_slider = Slider(1100 // scale, 100 // scale + padding, 100 // scale, 20 // scale, 0, 1080 // scale, 0, "y1", scale=scale)
x2_slider = Slider(1100 // scale, 100 // scale + (padding * 2), 100 // scale, 20 // scale, 0, 1080 // scale, 0, "x2", scale=scale)
y2_slider = Slider(1100 // scale, 100 // scale + (padding * 3), 100 // scale, 20 // scale, 0, 1080 // scale, 0, "y2", scale=scale)
linear_button = Button(1100 // scale, 100 // scale + (padding * 4), 150 // scale, 45 // scale, "Linearize", 36 // scale,BLACK, WHITE, LIGHT_GRAY)
clear_button = Button(1100 // scale, 100 // scale + (padding * 4.5), 100 // scale, 45 // scale, "Clear", 36 // scale,BLACK, WHITE, LIGHT_GRAY)
state = STATES["START"]

startX = 0
startY = 0

endX = 0
endY = 0

current_mouseX = 0
current_mouseY = 0

field_image = pygame.image.load(field_img)
field_image = pygame.transform.scale(field_image, (field_image.get_width() // scale, field_image.get_height() // scale))
selected_point = None
selected_curve = None
# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1600 // scale, 1080 // scale
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Plotting Pedro")

def field_to_inches(x, y):
    return round(x / divider, 1), round(y / divider, 1)

def draw():
    screen.fill((0, 0, 0)) # Clear the screen
    #Draw the field
    screen.blit(field_image, (0, 0))
    for curve in curves:
        #Draw the curve
        lines = 50
        for i in range(lines):
            t = i / lines
            x0, y0 = curve.calculate_curve(t)
            t = (i + 1) / lines
            x1, y1 = curve.calculate_curve(t)
            if (current_curve == curves.index(curve)):
                if x0 < 1080 // scale and y0 < 1080 // scale and x1 < 1080 // scale and y1 < 1080 // scale:
                    pygame.draw.line(screen, WHITE, (int(x0), int(y0)), (int(x1), int(y1)), 4)
            else:
                if x0 < 1080 // scale and y0 < 1080 // scale and x1 < 1080 // scale and y1 < 1080 // scale:
                    pygame.draw.line(screen, RED, (int(x0), int(y0)), (int(x1), int(y1)), 4)
                    
        #Draw a small circle at the start and end points
        pygame.draw.circle(screen, RED, (int(curve.x0), int(curve.y0)), 6) # Start point
        pygame.draw.circle(screen, GREEN, (int(curve.x3), int(curve.y3)), 6) # End Point
        
        if (current_curve == curves.index(curve)):
            if selected_point == "x1":
                pygame.draw.circle(screen, GREEN, (int(curve.x1), int(curve.y1)), 12) # Control point 1 focused
            else:
                pygame.draw.circle(screen, GREEN, (int(curve.x1), int(curve.y1)), 8) # Control point 1 unfocused
            if selected_point == "x2":
                pygame.draw.circle(screen, RED, (int(curve.x2), int(curve.y2)), 12) # Control point 2 focused
            else:
                pygame.draw.circle(screen, RED, (int(curve.x2), int(curve.y2)), 8) # Control point 2 unfocused
        
    if state == STATES["END"] and len(curves) == 0:
        pygame.draw.circle(screen, GREEN, (int(startX), int(startY)), 6)
    #Drawing text that shows the mouse position live like this (x,y)
    
    font = pygame.font.Font(None, 36 // (scale))
    font_small = pygame.font.Font(None, 26 // (scale))
    text = font.render(f"({current_mouseX},{current_mouseY})", True, (255, 255, 255))
    screen.blit(text, (1100 // scale,(1080-36) // scale))
    
    text = font_small.render("Created by Team #14840 DCS MechWarriors", True, (255, 255, 255))
    screen.blit(text, ((1600 // scale) - (1080 // scale) - (text.get_width() // 2), 5))
    
    #On the right side of the screen, draw 2 sliders for the x1 and y1 values, and the x2 and y2 values
    x1_slider.draw(screen)
    y1_slider.draw(screen)
    x2_slider.draw(screen)
    y2_slider.draw(screen)
    linear_button.draw(screen)
    clear_button.draw(screen)

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

def change_curve(current_curve_id, new_curve_id):
    global current_curve
    if new_curve_id < 0:
        new_curve_id = len(curves) - 1
    elif new_curve_id > len(curves) - 1:
        new_curve_id = 0
        
    x1_slider.value = curves[new_curve_id].x1
    y1_slider.value = curves[new_curve_id].y1
    x2_slider.value = curves[new_curve_id].x2
    y2_slider.value = curves[new_curve_id].y2
    
    current_curve = new_curve_id
    
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.button == 1:
                for curve in curves:
                    if (mouse_x - curve.x0)**2 + (mouse_y - curve.y0)**2 < 36:
                        selected_point = "x0"
                        selected_curve = curve
                    elif (mouse_x - curve.x1)**2 + (mouse_y - curve.y1)**2 < 36:
                        selected_point = "x1"
                        selected_curve = curve
                    elif (mouse_x - curve.x2)**2 + (mouse_y - curve.y2)**2 < 36:
                        selected_point = "x2"
                        selected_curve = curve
                    elif (mouse_x - curve.x3)**2 + (mouse_y - curve.y3)**2 < 36:
                        selected_point = "x3"
                        selected_curve = curve
                        
                if linear_button.hovered:
                    curves[current_curve].linearize()
                    x1_slider.value = curves[current_curve].x1
                    y1_slider.value = curves[current_curve].y1
                    x2_slider.value = curves[current_curve].x2
                    y2_slider.value = curves[current_curve].y2
                elif clear_button.hovered:
                    curves = []
                    current_curve = 0
                    x1_slider.value = 0
                    y1_slider.value = 0
                    x2_slider.value = 0
                    y2_slider.value = 0
                    startX = 0
                    startY = 0
                    endX = 0
                    endY = 0
                    selected_curve = None
                    selected_point = None
                    state = STATES["START"]
                elif selected_point != None:
                    pass
                else:
                    if state == STATES["START"]:
                        #If thed mouse position is in the image
                        x0, y0 = pygame.mouse.get_pos()
                        if x0 < 1080 // scale and y0 < 1080 // scale:
                            startX = x0
                            startY = y0
                            state = STATES["END"]
                            
                    elif state == STATES["END"]:
                        x3, y3 = pygame.mouse.get_pos()
                        if x3 < 1080 // scale and y3 < 1080 // scale:
                            if endX and endY != 0:
                                startX = endX
                                startY = endY
                            endX = x3
                            endY = y3
                            
                            if (len(curves) == 0):
                                curves.append(BezierCurve(startX, startY, startX, startY+15, endX, endY+15,endX, endY, None))
                            else:
                                last_curve = curves[-1]
                                curves.append(BezierCurve(curves[-1].x3, curves[-1].y3, startX,startY+15, endX, endY+15,endX, endY, last_curve))
                            current_curve = len(curves) - 1
                            x1_slider.value = curves[current_curve].x1
                            y1_slider.value = curves[current_curve].y1
                            x2_slider.value = curves[current_curve].x2
                            y2_slider.value = curves[current_curve].y2
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change_curve(current_curve, current_curve - 1)
            if event.key == pygame.K_RIGHT:
                change_curve(current_curve, current_curve + 1)
        if event.type == pygame.MOUSEBUTTONUP:
            selected_point = None
            selected_curve = None
        if event.type == pygame.MOUSEMOTION:
            x,y = pygame.mouse.get_pos()
            if x < 1080 and y < 1080:
                new_x, new_y = field_to_inches(x, y)
                current_mouseX = new_x
                current_mouseY = new_y
            
            if selected_point == "x0" and selected_curve != None:

                
                #Check if another startpoint of a curve is interessting the endpoint, if so then set the startpoint to the endpoint
                if selected_curve.connectingCurve != None:
                    selected_curve.x0 = x
                    selected_curve.y0 = y
                    
                    selected_curve.connectingCurve.x3 = x
                    selected_curve.connectingCurve.y3 = y
            elif selected_point == "x1" and selected_curve != None:
                selected_curve.x1 = x
                selected_curve.y1 = y
                
                x1_slider.value = x
                y1_slider.value = y
            elif selected_point == "x2" and selected_curve != None:
                selected_curve.x2 = x
                selected_curve.y2 = y
                
                x2_slider.value = x
                y2_slider.value = y
                
            elif selected_point == "x3" and selected_curve != None:
                selected_curve.x3 = x
                selected_curve.y3 = y
                
                endX = x
                endY = y
                
                    
                
                
            
        x1_slider.handle_event(event)
        y1_slider.handle_event(event)
        x2_slider.handle_event(event)
        y2_slider.handle_event(event)
        linear_button.handle_event(event)
        clear_button.handle_event(event)
        
    # Fill the screen with a color (optional)
    draw()
    logic()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()