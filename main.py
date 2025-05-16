import os
import json
from re import X
from sqlite3 import connect
from turtle import update
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
from UI.TextInput import TextInput
import tkinter as tk
from tkinter import scrolledtext



with open('config.txt', 'r') as file:
    config = json.load(file)
    scale = config.get('scale')
    field_img = config.get("fieldImg")
    lines_per_curve = config.get("linesPerCurve")

if scale > 3: scale = 3

divider = (1080 // scale) / 144
curves = []
current_curve = 0
current_beziercurve = None

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
# x1_slider = Slider(1100 // scale, 100 // scale, 300 // scale, 20 // scale, 0, 1080 // scale, 0, "x1", scale=scale)
# y1_slider = Slider(1100 // scale, 200 // scale, 300 // scale, 20 // scale, 0, 1080 // scale, 0, "y1", scale=scale)
# x2_slider = Slider(1100 // scale, 300 // scale, 300 // scale, 20 // scale, 0, 1080 // scale, 0, "x2", scale=scale)
# y2_slider = Slider(1100 // scale, 400 // scale, 300 // scale, 20 // scale, 0, 1080 // scale, 0, "y2", scale=scale)

value_slider = Slider(1160 // scale, 275 // scale, 300 // scale, 20 // scale, 0, 144, 0, "Value", scale=scale)
# Start point inputs
startXInput = TextInput(1200 // scale, 50 // scale, 100 // scale, 45 // scale, font_size=36 // scale, text_color=WHITE, bg_color=DARK_GRAY, border_color=WHITE, border_radius=10//scale, border_width=2//scale, scale=scale, connectedSlider=value_slider)
startYInput = TextInput(1325 // scale, 50 // scale, 100 // scale, 45 // scale, font_size=36 // scale, text_color=WHITE, bg_color=DARK_GRAY, border_color=WHITE, border_radius=10//scale, border_width=2//scale, scale=scale, connectedSlider=value_slider)

# First control point inputs
x1Input = TextInput(1200 // scale, 100 // scale, 100 // scale, 45 // scale, font_size=36 // scale, text_color=WHITE, bg_color=DARK_GRAY, border_color=WHITE, border_radius=10//scale, border_width=2//scale, scale=scale, connectedSlider=value_slider)
y1Input = TextInput(1325 // scale, 100 // scale, 100 // scale, 45 // scale, font_size=36 // scale, text_color=WHITE, bg_color=DARK_GRAY, border_color=WHITE, border_radius=10//scale, border_width=2//scale, scale=scale, connectedSlider=value_slider)

# Second control point inputs
x2Input = TextInput(1200 // scale, 150 // scale, 100 // scale, 45 // scale, font_size=36 // scale, text_color=WHITE, bg_color=DARK_GRAY, border_color=WHITE, border_radius=10//scale, border_width=2//scale, scale=scale, connectedSlider=value_slider)
y2Input = TextInput(1325 // scale, 150 // scale, 100 // scale, 45 // scale, font_size=36 // scale, text_color=WHITE, bg_color=DARK_GRAY, border_color=WHITE, border_radius=10//scale, border_width=2//scale, scale=scale, connectedSlider=value_slider)

# End point inputs
endXInput = TextInput(1200 // scale, 200 // scale, 100 // scale, 45 // scale, font_size=36 // scale, text_color=WHITE, bg_color=DARK_GRAY, border_color=WHITE, border_radius=10//scale, border_width=2//scale, scale=scale, connectedSlider=value_slider)
endYInput = TextInput(1325 // scale, 200 // scale, 100 // scale, 45 // scale, font_size=36 // scale, text_color=WHITE, bg_color=DARK_GRAY, border_color=WHITE, border_radius=10//scale, border_width=2//scale, scale=scale, connectedSlider=value_slider)



linear_button = Button(1160 // scale, 325 // scale, 300 // scale, 45 // scale, "Linearize (Bezier Line)", 36 // scale, BLACK, WHITE, LIGHT_GRAY, border_radius=10//scale, border_width=2//scale)
clear_button = Button(1160 // scale, 375 // scale, 140 // scale, 45 // scale, "Clear", 36 // scale, BLACK, WHITE, LIGHT_GRAY, border_radius=10//scale, border_width=2//scale)
delete_button = Button(1310 // scale, 375 // scale, 150 // scale, 45 // scale, "Delete", 36 // scale, BLACK, WHITE, LIGHT_GRAY, border_radius=10//scale, border_width=2//scale)
export_button = Button(1160 // scale, 425 // scale, 300 // scale, 45 // scale, "Export Pathchain", 36 // scale, BLACK, WHITE, LIGHT_GRAY, border_radius=10//scale, border_width=2//scale)
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
selected_input = "none"
# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1600 // scale, 1080 // scale
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Plotting Pedro")

def check_if_text_input_active():
    global startxInput, startYInput, endXInput, endYInput, x1Input, y1Input, x2Input, y2Input
    none_active = True
    if startXInput.active or startYInput.active or endXInput.active or endYInput.active or x1Input.active or y1Input.active or x2Input.active or y2Input.active:
        none_active = False
    return none_active

def update_active_textbox():
    global startXInput, startYInput, endXInput, endYInput, x1Input, y1Input, x2Input, y2Input, selected_input
    match True:
        case startXInput.active:
            if selected_input != "startX": value_slider.value = field_to_inches_single(startXInput.getValue())
            selected_input = "startX"
        case startYInput.active:
            if selected_input != "startY": value_slider.value = field_to_inches_single(startYInput.getValue())
            selected_input = "startY"
        case endXInput.active:
            if selected_input != "endX": value_slider.value = field_to_inches_single(endXInput.getValue())
            selected_input = "endX"
        case endYInput.active:
            if selected_input != "endY": value_slider.value = field_to_inches_single(endYInput.getValue())
            selected_input = "endY"
        case x1Input.active:
            if selected_input != "x1": value_slider.value = field_to_inches_single(x1Input.getValue())
            selected_input = "x1"
        case y1Input.active:
            if selected_input != "y1": value_slider.value = field_to_inches_single(y1Input.getValue())
            selected_input = "y1"
        case x2Input.active:
            if selected_input != "x2": value_slider.value = field_to_inches_single(x2Input.getValue())
            selected_input = "x2"
        case y2Input.active:
            if selected_input != "y2": value_slider.value = field_to_inches_single(y2Input.getValue())
            selected_input = "y2"
        case _:
            selected_input = "none"
def field_to_inches(x, y):
    return round(x / divider, 2), round(y / divider, 2)

def field_to_inches_single(a):
    return round(a / divider, 2)

def inches_to_field(x, y):
    return round(x * divider, 2), round(y * divider, 2)

def inches_to_field_single(a):
    return round(a * divider, 2)

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
    startXInput.draw(screen)
    startYInput.draw(screen)
    endXInput.draw(screen)
    endYInput.draw(screen)
    x1Input.draw(screen)
    y1Input.draw(screen)
    x2Input.draw(screen)
    y2Input.draw(screen)
    
    linear_button.draw(screen)
    clear_button.draw(screen)
    delete_button.draw(screen)
    export_button.draw(screen)
    
    start_label = font.render("Start", True, WHITE)
    screen.blit(start_label, (1100 // scale, 60 // scale))

    first_label = font.render("Point 1", True, WHITE)
    screen.blit(first_label, (1100 // scale, 110 // scale))

    second_label = font.render("Point 2", True, WHITE)
    screen.blit(second_label, (1100 // scale, 160 // scale))

    end_label = font.render("End", True, WHITE)
    screen.blit(end_label, (1100 // scale, 210 // scale))
    
    x_label = font.render("X", True, WHITE)
    screen.blit(x_label, (1240 // scale, 15 // scale))
    y_label = font.render("Y", True, WHITE)
    screen.blit(y_label, (1360 // scale, 15 // scale))
    
    if selected_input != "none":
        value_slider.draw(screen)
        # Draw a label above the slider
        test_label = font.render(selected_input, True, WHITE)
        test_label_x = (value_slider.x + (value_slider.width // 2)) - (test_label.get_width() // 2)
        test_label_y = value_slider.y - (test_label.get_height())
        screen.blit(test_label, (test_label_x, test_label_y))

def logic():
    global startX, startY, endX, endY, state, current_curve, selected_curve, selected_point, scale, divider, current_beziercurve, curves
    if len(curves) != 0:
        x1_value = x1Input.getValue()
        y1_value = y1Input.getValue()
        x2_value = x2Input.getValue()
        y2_value = y2Input.getValue()
        
        current_beziercurve = curves[current_curve]
        
        current_beziercurve.x1 = x1_value
        current_beziercurve.y1 = y1_value
        current_beziercurve.x2 = x2_value
        current_beziercurve.y2 = y2_value
    if len(curves) >= 2:
        for curve in curves:
            if curve.connectingCurve not in curves and curves.index(curve) != 0:
                delete_certain_curve(curves.index(curve))

    if current_beziercurve != None and len(curves) != 0:
        current_beziercurve = curves[current_curve]
        
        if field_to_inches_single(startXInput.getValue()) != field_to_inches_single(current_beziercurve.x0) and selected_input == "startX":
            value_slider.value = field_to_inches_single(startXInput.getValue())
        elif field_to_inches_single(startYInput.getValue()) != field_to_inches_single(current_beziercurve.y0) and selected_input == "startY":
            value_slider.value = field_to_inches_single(startYInput.getValue())
        elif field_to_inches_single(endXInput.getValue()) != field_to_inches_single(current_beziercurve.x3) and selected_input == "endX":
            value_slider.value = field_to_inches_single(endXInput.getValue())
        elif field_to_inches_single(endYInput.getValue()) != field_to_inches_single(current_beziercurve.y3) and selected_input == "endY":
            value_slider.value = field_to_inches_single(endYInput.getValue())
        elif x1Input.getValue() != current_beziercurve.x1 and selected_input == "x1":
            value_slider.value = field_to_inches_single(x1Input.getValue())
        elif y1Input.getValue() != current_beziercurve.y1 and selected_input == "y1":
            value_slider.value = field_to_inches_single(y1Input.getValue())
        elif x2Input.getValue() != current_beziercurve.x2 and selected_input == "x2":
            value_slider.value = field_to_inches_single(x2Input.getValue())
        elif y2Input.getValue() != current_beziercurve.y2 and selected_input == "y2":
            value_slider.value = field_to_inches_single(y2Input.getValue())

            
        if field_to_inches_single(startXInput.getValue()) != current_beziercurve.x0 or field_to_inches_single(startYInput.getValue()) != current_beziercurve.y0:
            current_beziercurve.x0 = startXInput.getValue()
            current_beziercurve.y0 = startYInput.getValue()
            startX = startXInput.getValue()
            startY = startYInput.getValue()
            # Update the end of the previous curve if it exists
            if current_curve > 0:
                curves[current_curve - 1].x3 = startX
                curves[current_curve - 1].y3 = startY
        if field_to_inches_single(endXInput.getValue()) != current_beziercurve.x3 or field_to_inches_single(endYInput.getValue()) != current_beziercurve.y3:
            current_beziercurve.x3 = endXInput.getValue()
            current_beziercurve.y3 = endYInput.getValue()
            endX = endXInput.getValue()
            endY = endYInput.getValue()
            # Update the start of the next curve if it exists
            if current_curve < len(curves) - 1:
                curves[current_curve + 1].x0 = endX
                curves[current_curve + 1].y0 = endY  
            
        
        
    if value_slider.has_moved():
        if selected_input == "startX":
            startXInput.setValue(inches_to_field_single(value_slider.value))
            startX = startXInput.getValue()
        elif selected_input == "startY":
            startYInput.setValue(inches_to_field_single(value_slider.value))
            startY = startYInput.getValue()
        elif selected_input == "endX":
            endXInput.setValue(inches_to_field_single(value_slider.value))
            endX = endXInput.getValue()
        elif selected_input == "endY":
            endYInput.setValue(inches_to_field_single(value_slider.value))
            endY = endYInput.getValue()
        elif selected_input == "x1":
            x1Input.setValue(inches_to_field_single(value_slider.value))
        elif selected_input == "y1":
            y1Input.setValue(inches_to_field_single(value_slider.value))
        elif selected_input == "x2":
            x2Input.setValue(inches_to_field_single(value_slider.value))
        elif selected_input == "y2":
            y2Input.setValue(inches_to_field_single(value_slider.value)) 
def clear():
    global curves, current_curve, startX, startY, endX, endY, selected_curve, selected_point, state
    curves = []
    current_curve = 0
    startXInput.setValue(0)
    startYInput.setValue(0)
    x1Input.setValue(0)
    y1Input.setValue(0)
    x2Input.setValue(0)
    y2Input.setValue(0)
    endXInput.setValue(0)
    endYInput.setValue(0)
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
        
        startXInput.setValue(curves[current_curve].x0)
        startYInput.setValue(curves[current_curve].y0)
        x1Input.setValue(curves[current_curve].x1)
        y1Input.setValue(curves[current_curve].y1)
        x2Input.setValue(curves[current_curve].x2)
        y2Input.setValue(curves[current_curve].y2)
        endXInput.setValue(curves[current_curve].x3)
        endYInput.setValue(curves[current_curve].y3)
    else:
        clear()
def delete_certain_curve(curve):
    
    if curve != None:
        curves.pop(curve)
    
        x1Input.setValue(curves[-1].x1)
        y1Input.setValue(curves[-1].y1)
        x2Input.setValue(curves[-1].x2)
        y2Input.setValue(curves[-1].y2)
def change_curve(current_curve_id, new_curve_id):
    global current_curve, current_beziercurve
    if new_curve_id < 0:
        new_curve_id = len(curves) - 1
    elif new_curve_id > len(curves) - 1:
        new_curve_id = 0
    
    startXInput.setValue(curves[new_curve_id].x0)
    startYInput.setValue(curves[new_curve_id].y0)
    x1Input.setValue(curves[new_curve_id].x1)
    y1Input.setValue(curves[new_curve_id].y1)
    x2Input.setValue(curves[new_curve_id].x2)
    y2Input.setValue(curves[new_curve_id].y2)
    endXInput.setValue(curves[new_curve_id].x3)
    endYInput.setValue(curves[new_curve_id].y3)
    current_curve = new_curve_id
    
    current_beziercurve = curves[current_curve]

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.button == 1:
                if current_beziercurve != None:
                    if (mouse_x - current_beziercurve.x0)**2 + (mouse_y - current_beziercurve.y0)**2 < 36:
                        selected_point = "x0"
                        selected_curve = current_beziercurve
                    elif (mouse_x - current_beziercurve.x1)**2 + (mouse_y - current_beziercurve.y1)**2 < 36:
                        selected_point = "x1"
                        selected_curve = current_beziercurve
                    elif (mouse_x - current_beziercurve.x2)**2 + (mouse_y - current_beziercurve.y2)**2 < 36:
                        selected_point = "x2"
                        selected_curve = current_beziercurve
                    elif (mouse_x - current_beziercurve.x3)**2 + (mouse_y - current_beziercurve.y3)**2 < 36:
                        selected_point = "x3"
                        selected_curve = current_beziercurve
                        
                if linear_button.hovered:
                    if len(curves) != 0:
                        curves[current_curve].linearize()
                        
                        x1Input.setValue(curves[current_curve].x1)
                        y1Input.setValue(curves[current_curve].y1)
                        x2Input.setValue(curves[current_curve].x2)
                        y2Input.setValue(curves[current_curve].y2)
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
                    root.title("Exported PathChain")

                    text_area = scrolledtext.ScrolledText(root, width=60, height=20)
                    text_area.pack(padx=10, pady=10)
                    text_area.insert(tk.INSERT, path)
                    text_area.config(state=tk.DISABLED)
                    root.mainloop()
                elif selected_point != None:
                    pass
                elif state == STATES["START"]:
                    #If the mouse position is in the image
                    x0, y0 = pygame.mouse.get_pos()
                    if x0 < 1080 // scale and y0 < 1080 // scale:
                        startX = x0
                        startY = y0
                        state = STATES["END"]
                        
                        startXInput.setValue(round(startX, 2))
                        startYInput.setValue(round(startY, 2))
                              
                            
                elif state == STATES["END"]:
                    x3, y3 = pygame.mouse.get_pos()
                    if x3 < 1080 // scale and y3 < 1080 // scale:
                        if endX and endY != 0:
                            startX = endX
                            startY = endY

                            startXInput.setValue(round(startX, 2))
                            startYInput.setValue(round(startY, 2))
                        endX = x3
                        endY = y3
                        
                        endXInput.setValue(round(endX, 2))
                        endYInput.setValue(round(endY, 2))
                        
                        if (len(curves) == 0):
                            curves.append(BezierCurve(startX, startY, startX+15, startY, endX+15, endY,endX, endY, None))
                        else:
                            last_curve = curves[-1]
                            curves.append(BezierCurve(curves[-1].x3, curves[-1].y3, startX-15,startY, endX-15, endY,endX, endY, last_curve))
                        current_curve = len(curves) - 1
                        
                        x1Input.setValue(curves[current_curve].x1)
                        y1Input.setValue(curves[current_curve].y1)
                        x2Input.setValue(curves[current_curve].x2)
                        y2Input.setValue(curves[current_curve].y2)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and check_if_text_input_active():
                change_curve(current_curve, current_curve - 1)
            if event.key == pygame.K_RIGHT and check_if_text_input_active():
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

                    startXInput.setValue(x)
                    startYInput.setValue(y)

            elif selected_point == "x1" and selected_curve != None:
                selected_curve.x1 = x
                selected_curve.y1 = y
                
                x1Input.setValue(x)
                y1Input.setValue(y)
            elif selected_point == "x2" and selected_curve != None:
                selected_curve.x2 = x
                selected_curve.y2 = y
                
                x2Input.setValue(x)
                y2Input.setValue(y)
                
            elif selected_point == "x3" and selected_curve != None:
                selected_curve.x3 = x
                selected_curve.y3 = y
                
                endX = x
                endY = y
                
                endXInput.setValue(x)
                endYInput.setValue(y)
                
                    
                
                
            
        linear_button.handle_event(event)
        clear_button.handle_event(event)
        delete_button.handle_event(event)
        export_button.handle_event(event)
        
        x1Input.handle_event(event)
        y1Input.handle_event(event)
        x2Input.handle_event(event)
        y2Input.handle_event(event)
        startXInput.handle_event(event)
        startYInput.handle_event(event)
        endXInput.handle_event(event)
        endYInput.handle_event(event)
        
        value_slider.handle_event(event)
        
    # Update loops
    draw()
    logic()
    update_active_textbox()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()

#