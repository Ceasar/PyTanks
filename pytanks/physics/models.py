'''A module for two dimensional positioning.'''
import math

from pygame.sprite import Sprite

from pygame_tools.sprites import RotatableSprite

from vector import Vector

class Rotatable(RotatableSprite):
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
        super(Rotatable, self).__init__(heading)
        self.angular_velocity = angular_velocity

    def rotate(self, degrees):
        '''Turn the object by the given amount of degrees.'''
        if degrees < self.MAX_TURN:
            self.heading += degrees
            self.heading %= 360
        else:
            raise ValueError('Degrees (%s) exceeded MAX_TURN (%s).'
                             % (degrees, self.MAX_TURN))

    def update(self, dt=1.0):
        '''Update the state of the object.'''
        super(Rotatable, self).update()
        self.heading += self.angular_velocity


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

    def accelerate(self, rate=1.0):
        '''Accelerate.'''
        new_velocity = self.velocity + rate
        if abs(new_velocity) < self.MAX_SPEED:
            self.velocity = new_velocity
        else:
            raise ValueError("(%s). Tried to exceed maximum speed (%s)."
                             % (abs(new_velocity), self.MAX_SPEED))

    def update(self, dt=1.0):
        '''Update the state of the object.'''
        super(Projectile, self).update(dt)
        self.position += self.velocity * dt * self.direction
