import os
import json
from re import X
from sqlite3 import connect
import pygame
import sys
def generate_config():
    config = {
        "scale": 1,
        "fieldImg": "field.png",
        "linesPerCurve": 50
    }
    with open('config.txt', 'w') as file:
        json.dump(config, file)

# If there is no config file generate one
if not os.path.exists('config.txt'):
    generate_config()

#Making sure there is a config file before importing the classes
from Math.BezierCurve import BezierCurve
from UI.Slider import Slider
from UI.Button import Button
import tkinter as tk
from tkinter import scrolledtext


with open('config.txt', 'r') as file:
    config = json.load(file)
    scale = config.get('scale')
    field_img = config.get("fieldImg")
    lines_per_curve = config.get("linesPerCurve")

if scale > 3: scale = 3

divider = (1080 // scale) / 144
print(divider)
curves = []
current_curve = 0

STATES = {
    "START": 0,
    "END": 1
    
}

# Define colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_PURPLE = (255, 0, 255)
PURPLE = (128, 0, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
DARK_YELLOW = (200, 200, 0)
LIGHT_GRAY = (150, 150, 150)
DARK_GRAY = (30, 30, 30)
TRANSPARENT_WHITE = (255, 255, 255, 128)

# Initialize sliders and buttons
x1_slider = Slider(1100 // scale, 100 // scale, 300 // scale, 20 // scale, 0, 1080 // scale, 0, "x1", scale=scale)
y1_slider = Slider(1100 // scale, 200 // scale, 300 // scale, 20 // scale, 0, 1080 // scale, 0, "y1", scale=scale)
x2_slider = Slider(1100 // scale, 300 // scale, 300 // scale, 20 // scale, 0, 1080 // scale, 0, "x2", scale=scale)
y2_slider = Slider(1100 // scale, 400 // scale, 300 // scale, 20 // scale, 0, 1080 // scale, 0, "y2", scale=scale)

linear_button = Button(1100 // scale, 450 // scale, 300 // scale, 45 // scale, "Linearize (Bezier Line)", 36 // scale, BLACK, WHITE, LIGHT_GRAY, border_radius=10//scale, border_width=2//scale)
clear_button = Button(1100 // scale, 500 // scale, 140 // scale, 45 // scale, "Clear", 36 // scale, BLACK, WHITE, LIGHT_GRAY, border_radius=10//scale, border_width=2//scale)
delete_button = Button(1250 // scale, 500 // scale, 150 // scale, 45 // scale, "Delete", 36 // scale, BLACK, WHITE, LIGHT_GRAY, border_radius=10//scale, border_width=2//scale)
export_button = Button(1100 // scale, 550 // scale, 300 // scale, 45 // scale, "Export Pathchain", 36 // scale, BLACK, WHITE, LIGHT_GRAY, border_radius=10//scale, border_width=2//scale)
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
    screen.fill(DARK_GRAY) # Clear the screen
    #Draw the field
    screen.blit(field_image, (0, 0))
    for curve in curves:
        # Draw the curve
        lines = lines_per_curve * scale  # Increase the number of lines for smoother curves
        for i in range(lines):
            t = i / lines
            x0, y0 = curve.calculate_curve(t)
            t = (i + 1) / lines
            x1, y1 = curve.calculate_curve(t)
            if (current_curve == curves.index(curve)):
                if x0 < 1080 // scale and y0 < 1080 // scale and x1 < 1080 // scale and y1 < 1080 // scale:
                    pygame.draw.line(screen, WHITE, (int(x0), int(y0)), (int(x1), int(y1)), 3)
            else:
                if x0 < 1080 // scale and y0 < 1080 // scale and x1 < 1080 // scale and y1 < 1080 // scale:
                    pygame.draw.line(screen, LIGHT_GRAY, (int(x0), int(y0)), (int(x1), int(y1)), 3) 
                    
        
        pygame.draw.circle(screen, GREEN, (int(curve.x0), int(curve.y0)), 6 // scale) # Start point
        pygame.draw.circle(screen, RED, (int(curve.x3), int(curve.y3)), 6 // scale) # End Point
        
        if (current_curve == curves.index(curve)):
            if selected_point == "x1":
                pygame.draw.circle(screen, GREEN, (int(curve.x1), int(curve.y1)), 12 // scale) # Control point 1 focused
            else:
                pygame.draw.circle(screen, GREEN, (int(curve.x1), int(curve.y1)), 8 // scale) # Control point 1 unfocused
            if selected_point == "x2":
                pygame.draw.circle(screen, RED, (int(curve.x2), int(curve.y2)), 12 // scale) # Control point 2 focused
            else:
                pygame.draw.circle(screen, RED, (int(curve.x2), int(curve.y2)), 8 // scale) # Control point 2 unfocused
        
    if state == STATES["END"] and len(curves) == 0:
        pygame.draw.circle(screen, GREEN, (int(startX), int(startY)), 6)
    #Drawing text that shows the mouse position live like this (x,y)
    
    font = pygame.font.Font(None, 36 // (scale))
    font_medium = pygame.font.Font(None, 30 // (scale))
    font_small = pygame.font.Font(None, 26 // (scale))
    text = font.render(f"({current_mouseY},{current_mouseX})", True, (255, 255, 255))
    screen.blit(text, (1100 // scale,(1080-36) // scale))
    
    text = font_small.render("Created by Team #14840 DCS MechWarriors", True, (255, 255, 255))
    screen.blit(text, ((1600 // scale) - (1080 // scale) - (text.get_width() // 2), 5))
    
    if len(curves) != 0:
        path = curves[current_curve].to_pathchain(divider, indent=True)
        lines = path.split('\n')
        y_offset = 600 // scale  # Start drawing below the buttons
        for line in lines:
            text = font_small.render(line, True, WHITE)
            screen.blit(text, (1100 // scale, y_offset))
            y_offset += 20 // scale
    #On the right side of the screen, draw 2 sliders for the x1 and y1 values, and the x2 and y2 values
    x1_slider.draw(screen)
    y1_slider.draw(screen)
    x2_slider.draw(screen)
    y2_slider.draw(screen)
    linear_button.draw(screen)
    clear_button.draw(screen)
    delete_button.draw(screen)
    export_button.draw(screen)

def logic():
    global startX, startY, endX, endY, state, current_curve, selected_curve, selected_point, scale, divider
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
    if len(curves) >= 2:
        for curve in curves:
            if curve.connectingCurve not in curves and curves.index(curve) != 0:
                delete_certain_curve(curves.index(curve))
            
def clear():
    global curves, current_curve, startX, startY, endX, endY, selected_curve, selected_point, state
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
def delete():
    global curves, current_curve, selected_curve
    if current_curve != 0:
        for curve in curves:
            if curve.connectingCurve == curves[current_curve]:
                delete_certain_curve(curves.index(curve))
        curves.remove(curves[current_curve])
        current_curve -= 1
        selected_curve = curves[current_curve]
        x1_slider.value = curves[current_curve].x1
        y1_slider.value = curves[current_curve].y1
        x2_slider.value = curves[current_curve].x2
        y2_slider.value = curves[current_curve].y2
    else:
        clear()
def delete_certain_curve(curve):
    
    if curve != None:
        curves.pop(curve)
        x1_slider.value = curves[-1].x1
        y1_slider.value = curves[-1].y1
        x2_slider.value = curves[-1].x2
        y2_slider.value = curves[-1].y2
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
                    if len(curves) != 0:
                        curves[current_curve].linearize()
                        x1_slider.value = curves[current_curve].x1
                        y1_slider.value = curves[current_curve].y1
                        x2_slider.value = curves[current_curve].x2
                        y2_slider.value = curves[current_curve].y2
                elif clear_button.hovered:
                    clear()
                elif delete_button.hovered:
                    delete()
                elif export_button.hovered:
                    path = "PathChain pathChain = follower.pathBuilder()"
                    for curve in curves:
                        path += f"\n    {curve.to_pathchain(divider)}"
                    path += "\n.build();"
                    root = tk.Tk()
                    root.title("Exported Pathchain")
                    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20)
                    text_area.pack(padx=10, pady=10)
                    text_area.insert(tk.INSERT, path)
                    text_area.config(state=tk.DISABLED)
                    root.mainloop()
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
                                curves.append(BezierCurve(startX, startY, startX+15, startY, endX+15, endY,endX, endY, None))
                            else:
                                last_curve = curves[-1]
                                curves.append(BezierCurve(curves[-1].x3, curves[-1].y3, startX-15,startY, endX-15, endY,endX, endY, last_curve))
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
            if event.key == pygame.K_DELETE:
                delete()
                    
        if event.type == pygame.MOUSEBUTTONUP:
            selected_point = None
            selected_curve = None
        if event.type == pygame.MOUSEMOTION:
            x,y = pygame.mouse.get_pos()
            if x < 1080 // scale and y < 1080 // scale:
                new_x, new_y = field_to_inches(x, y)
                current_mouseX = new_x
                current_mouseY = new_y
            
            if x > 1080 // scale: x = 1080 // scale
            if y > 1080 // scale: y = 1080 // scale
            if x < 0: x = 0
            if y < 0: y = 0
            
            
            if selected_point == "x0" and selected_curve != None:

                
                #If we move the bottom curve, also update the end curve that it is connected to
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
        delete_button.handle_event(event)
        export_button.handle_event(event)
        
    # Fill the screen with a color (optional)
    draw()
    logic()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()