import math

import pygame

from physics.managers import RotatableManager, ProjectileManager


class BulletManager(ProjectileManager):
    pass


class TankManager(ProjectileManager):
    pass


class GunManager(RotatableManager):

    def fire(self, sprite, power):
        '''Fire the gun.'''
        if sprite.heat > 0.0:
            raise ValueError("(%s) Gun is still hot." % sprite.heat)
        if power > sprite.MAX_POWER or power <= sprite.MIN_POWER:
            raise ValueError("(%s) Power must be between %s and %s."
                             % (power, sprite.MAX_POWER, sprite.MIN_POWER))
        sprite.heat = 1.0 + power / 5.0
        sprite.tank.power -= power
        bullet = Bullet(sprite.tank, power)

    def update(self, sprite, context):
        super(GunManager, self).update(sprite, context)
        sprite.heat -= sprite.COOLING_RATE


class RadarManager(RotatableManager):
    def scan(self, sprite):
        '''Scan ahead for any objects.'''
        raise NotImplemented
