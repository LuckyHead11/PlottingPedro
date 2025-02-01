# Plotting Pedro

## Overview
Plotting Pedro is a plotting software designed by FTC Team #14840 that allows you to drag points on a field and output that into code which then you can use in Pedro Pathing

## Features
- **Bezier Curve Drawing**: Draw Bezier curves by clicking on the start and end points.
- **Curve Manipulation**: Adjust control points of the Bezier curves using sliders.
- **Curve Selection**: Select and focus on different curves using mouse clicks or keyboard arrows.
- **Linearization**: Linearize the selected curve with a button click.
- **Clear Curves**: Clear all curves with a button click.
- **Mouse Position Display**: Display the current mouse position in inches on the screen.
- **Configurable Settings**: Load and save configuration settings from a `config.txt` file.

## Installation
1. Ensure you have Python installed on your system.
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the [main.py]() script:
    ```bash
    python main.py
    ```
2. The application window will open, displaying a field image.

## Configuration
The application uses a [config.txt](http://_vscodecontentref_/1) file to store configuration settings. If the file does not exist, it will be generated with default values:
```json
{
    "scale": 1,
    "fieldImg": "field.png"
}