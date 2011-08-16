import math

import pygame

from physics.models import Rotatable, Projectile

ENTITIES = pygame.sprite.LayeredUpdates()
BULLETS = pygame.sprite.Group()
RADARS = pygame.sprite.Group()
GUNS = pygame.sprite.Group()
TANKS = pygame.sprite.Group()

class Bullet(Projectile):
    _image = pygame.image.load('images/bullet.png')
    _layer = 1

    @property
    def damage(self):
        return 4 * self.power + 2 * max(self.power - 1, 0)

    @property
    def leech(self):
        return 3 * self.power

    def __init__(self, tank, power):
        super(Bullet, self).__init__(position=tank.position,
                                     heading=tank.gun.heading,
                                     velocity=(20.0 - 3.0 * power) * -1.0)
        self.tank = tank
        self.power = power
        self.velocity = (20.0 - 3.0 * power) * -1.0 #not sure why...
Bullet.groups = ENTITIES, BULLETS

import random
class Tank(Projectile):
    '''A tank object.'''
    _image = pygame.image.load('images/tank/body.png')
    _layer = 0
    
    MAX_SPEED = 8.0

    @property
    def MAX_TURN(self):
        #TODO: Make this an instance property.
        return 10.0 - 0.75 * abs(self.velocity)

    def __init__(self, heading=0.0, position=(0, 0), power=100.0, name=None):
        super(Tank, self).__init__(position=position, heading=heading)
        self.power = power
        self.name = name

        self.gun = Gun(self, heading)
        self.radar = Radar(self, heading)

    def run(self):
        '''Override this.'''
        try:
            self.accelerate(random.gauss(0, 1))
        except:
            pass
        self.rotate(-3)
        self.gun.rotate(3)
        self.radar.rotate(44)
        try:
            self.gun.fire(1.0)
        except ValueError as e:
            pass
Tank.groups = ENTITIES, TANKS


class TankPart(Rotatable):
    '''An abstract tank component.'''

    @property
    def position(self):
        '''The position of the tank.'''
        return self.tank.position

    def __init__(self, tank, heading=0.0):
        super(TankPart, self).__init__(heading)
        self.tank = tank


class Gun(TankPart):
    '''A tank gun.'''
    _image = pygame.image.load('images/tank/gun.png')
    _layer = 2
    
    MAX_TURN = 20.0
    COOLING_RATE = 0.1
    MAX_POWER = 3.0
    MIN_POWER = 0.0
    
    def __init__(self, tank, heading=0.0, heat=5.0):
        super(Gun, self).__init__(tank, heading)
        self.heat = heat

    def fire(self, power):
        '''Fire the gun.'''
        if self.heat > 0.0:
            raise ValueError("(%s) Gun is still hot." % self.heat)
        if power > self.MAX_POWER or power <= self.MIN_POWER:
            raise ValueError("(%s) Power must be between %s and %s."
                             % (power, self.MAX_POWER, self.MIN_POWER))
        self.heat = 1.0 + power / 5.0
        self.tank.power -= power
        bullet = Bullet(self.tank, power)

    def update(self, dt):
        super(Gun, self).update(dt)
        self.heat -= self.COOLING_RATE
Gun.groups = ENTITIES, GUNS

class Radar(TankPart):
    '''A tank radar.'''
    _image = pygame.image.load('images/tank/radar.png')
    _layer = 3
    
    MAX_TURN = 45.0
    scan_arc = 45.0

    def scan(self):
        '''Scan ahead for any objects.'''
        raise NotImplemented
Radar.groups = ENTITIES, RADARS
