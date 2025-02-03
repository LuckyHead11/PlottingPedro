class BezierCurve:
    def __init__(self, x0, y0, x1, y1, x2, y2, x3, y3, connectingCurve  ):
        self.x0 = x0    
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.connectingCurve = connectingCurve
        
    def calculate_curve(self, t):
        x = (1 - t)**3 * self.x0 + 3 * (1 - t)**2 * t * self.x1 + 3 * (1 - t) * t**2 * self.x2 + t**3 * self.x3
        y = (1 - t)**3 * self.y0 + 3 * (1 - t)**2 * t * self.y1 + 3 * (1 - t) * t**2 * self.y2 + t**3 * self.y3
        return x, y
    def linearize(self):
        self.x1 = self.x0
        self.y1 = self.y0
        self.x2 = self.x3
        self.y2 = self.y3
    def is_line(self):
        if self.x1 == self.x0 and self.y1 == self.y0 and self.x2 == self.x3 and self.y2 == self.y3: return True
        else: return False
    def to_pathchain(self, divider):
        # .addPath(new BezierLine(new Point(scorePose), new Point(pickup1Pose)))
        # .addPath (new.BezierCurve(new Point(scorePose), new Point(parkControlPose), new Point(parkPose)))
        x0 = round(self.x0 / divider, 2)
        y0 = round(self.y0 / divider, 2)
        x1 = round(self.x1 / divider, 2)
        y1 = round(self.y1 / divider, 2)
        x2 = round(self.x2 / divider, 2)
        y2 = round(self.y2 / divider, 2)
        x3 = round(self.x3 / divider, 2)
        y3 = round(self.y3 / divider, 2)
        
        if self.is_line():
            return f".addPath(new BezierLine(new Point(new Pose({x0}, {y0}, 0)), new Point(new Pose({x3}, {y3}, 0)))"
        else:
            return f".addPath(new BezierCurve(new Point(new Pose({x0}, {y0}, 0)), new Point(new Pose({x1}, {y1}, 0)), new Point(new Pose({x2}, {y2}, 0)), new Point(new Pose({x3}, {y3}, 0)))"