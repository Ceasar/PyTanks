'''A module for two dimensional positioning.'''

import math

from vector import Vector

TAU = math.pi * 2

def get_resistance(velocity):
    '''Get the (air) resistance vector.'''
    speed = velocity.length()
    direction = velocity.unit()
    return speed ** 2 / 20.0 * -direction

FRICTION = 1.0
def get_friction(velocity):
    '''Get the friction vector.'''
    speed = velocity.length()
    direction = velocity.unit()
    if speed > 0:
        return FRICTION * -direction
    return 0 * velocity


class Rotatable(object):
    '''A rotable object.'''
    MAX_SPIN = None
    def __init__(self, heading=0.0, a_vel=0.0, a_acc=0.0):
        self.heading = Vector([heading])
        self.angular_velocity = Vector([a_vel])
        self.angular_acceleration = Vector([a_acc])

    def spin(self, alpha=1.0):
        '''Increase angular acceleration by alpha.'''
        vector = Vector([alpha])
        MAX_SPIN = self.__class__.MAX_SPIN
        if MAX_SPIN is None or vector.length() < Rotatable.MAX_SPIN:
            self.angular_acceleration += vector

    def update(self, dt):
        '''Update the state of the object.'''
        self.angular_velocity += get_resistance(self.angular_velocity) * dt
        #self.angular_velocity += get_friction(self.angular_velocity)
        
        self.angular_velocity += self.angular_acceleration * dt
        self.heading += self.angular_velocity * dt
        self.heading %= 360
        self.angular_acceleration *= 0

class Movable(object):
    '''A movable object.'''
    def __init__(self, velocity=0.0, acceleration=0.0):
        self.velocity = Vector([velocity])
        self.acceleration = Vector([acceleration])

    def accelerate(self, rate=1.0):
        '''Increase acceleration.'''
        self.acceleration += Vector([rate])

    def update(self, dt):
        '''Update the state of the object.'''
        self.velocity += get_resistance(self.velocity) * dt
        #self.velocity += get_friction(self.velocity)
        
        self.velocity += self.acceleration * dt
        self.acceleration *= 0

class Positionable(Movable, Rotatable):
    '''A positionable object.'''
    def __init__(self, position, heading):
        Movable.__init__(self)
        Rotatable.__init__(self, heading=heading)
        self.position = position

    def update(self, dt):
        '''Update the state of the object.'''
        Movable.update(self, dt)
        Rotatable.update(self, dt)
        scalar = -self.velocity.length()
        heading = math.radians(self.heading.length()) #This is kind of dumb...
        direction = Vector([math.sin(heading), math.cos(heading)])
        self.position += scalar * direction * dt


class Collidable(Positionable):
    '''A collidable object.'''
    def __init__(self, position, heading, radius):
        super(Collidable, self).__init__(position, heading)
        self.radius = radius

    def update(self, dt):
        super(Collidable, self).update(dt)
        x, y = self.position
        if x < self.radius or y < self.radius or x > 800 - self.radius or y > 600 - self.radius:
            self.velocity *= 0
            self.acceleration *= 0
        self.position = Vector([max(min(x, 800 - self.radius), self.radius),
                                max(min(y, 600 - self.radius), self.radius)])
    
    def collided(self, other):
        '''Check if the object has collided with another.'''
        return (self.position - other.position).length() < self.radius + other.radius

    def collisions(self, others):
        '''Get all collisions with this object.'''
        return filter(collided, others)

    
