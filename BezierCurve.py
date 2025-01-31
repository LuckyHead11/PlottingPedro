class BezierCurve:
    def __init__(self, x0, y0, x1, y1, x2, y2, x3, y3):
        self.x0 = x0    
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.id = id
    def calculate_curve(self, t):
        x = (1 - t)**3 * self.x0 + 3 * (1 - t)**2 * t * self.x1 + 3 * (1 - t) * t**2 * self.x2 + t**3 * self.x3
        y = (1 - t)**3 * self.y0 + 3 * (1 - t)**2 * t * self.y1 + 3 * (1 - t) * t**2 * self.y2 + t**3 * self.y3
        return x, y