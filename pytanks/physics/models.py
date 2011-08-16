'''A module for two dimensional positioning.'''
import math

from bluegear.models import Model

from vector import Vector

class Rotatable(Model):
    '''A rotable object.'''
    MAX_TURN = float("inf")

    @property
    def heading_radians(self):
        return math.radians(self.heading)

    @property
    def direction(self):
        #the y component is negative because pygame coordinates are flipped
        return Vector([math.sin(self.heading_radians),
                       math.cos(self.heading_radians)])
    
    def __init__(self, heading=0.0, angular_velocity=0.0):
        super(Rotatable, self).__init__()
        self.heading = heading
        self.angular_velocity = angular_velocity


class Projectile(Rotatable):
    '''A projectile.'''
    MAX_SPEED = float("inf")

    @property
    def speed(self):
        return abs(self.velocity)
    
    def __init__(self, heading=0.0, angular_velocity=0.0, position=(0, 0), velocity=0.0):
        super(Projectile, self).__init__(heading, angular_velocity)
        self.position = Vector(position)
        self.velocity = velocity
