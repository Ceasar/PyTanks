from bullet import Bullet

class Gun(object):
    max_rotation = 20.0
    cooling_rate = 1
    def __init__(self):
        self.heat = 0
        self.heading = 0

    def fire(self, power):
        if self.heat > 0:
            return False
        bullet = Bullet(self, power)
        self.heat = 1 + firepower / 5
        return True

    def update(self):
        self.heat -= cooling_rate
    
