'''A module for two dimensional positioning.'''
import math

import bluegear


class RotatableManager(bluegear.models.Manager):
    '''Manages rotatable objects.'''

    def rotate(self, sprite, degrees):
        '''Turn the object by the given amount of degrees.'''
        if degrees < sprite.MAX_TURN:
            sprite.heading += degrees
            sprite.heading %= 360
        else:
            raise ValueError('Degrees (%s) exceeded MAX_TURN (%s).'
                             % (degrees, sprite.MAX_TURN))

    def update(self, sprite, context):
        '''Update the state of the object.'''
        sprite.heading += sprite.angular_velocity * context['dt']


class ProjectileManager(RotatableManager):
    '''Manages projectiles.'''

    def accelerate(self, sprite, rate=1.0):
        '''Accelerate.'''
        new_velocity = sprite.velocity + rate
        if abs(new_velocity) < sprite.MAX_SPEED:
            sprite.velocity = new_velocity
        else:
            raise ValueError("(%s). Tried to exceed maximum speed (%s)."
                             % (abs(new_velocity), sprite.MAX_SPEED))

    def update(self, sprite, context):
        '''Update the state of the object.'''
        super(ProjectileManager, self).update(sprite, context)
        sprite.position += sprite.velocity * sprite.direction * context['dt']
