# Plotting Pedro

## Overview
Plotting Pedro is a plotting software designed by FTC Team **#14840: DCS Mechwarriors** that allows you to develop Bezier Lines, and Curves, lastly outputting that into code which then you can use in Pedro Pathing developed by Team **#10158: Scott's Bots**.

## Features
- **Bezier Curve Manipulation**: Allows you to control start and end points, along with 2 control points
- **Configurable Settings**: Load and save configuration settings from a config.txt file
- **Support**: Able to export your paths to Pedro Pathing

## Installation
1. Ensure you have Python installed on your system.
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Ensure you have a **1080x1080** field image in your directory, if you need to edit the location of that image if you can do so in the auto-generated config file at startup.

## Usage
1. Run the [main.py]() script:
    ```bash
    python main.py
    ```
2. You can now click twice anywhere in the field location and it will generate a curve, you can drag on the 2 control points to modify them, or use the sliders on the right side. Press **"Linearize"** to make the line straight.

## Configuration
We use a **config.txt** file to store configuration settings. If the file does not exist, it will be generated with default values:
```json
{
    "scale": 1, // Higher is smaller, making the whole program smaller to make sure it fits on every screen
    "fieldImg": "field.png" // Location of the field image used to plot
}
```