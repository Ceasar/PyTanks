import math

from physics.models import Rotatable, Projectile

from managers import *
from views import *

class Bullet(Projectile):
    '''A bullet object.'''
    objects = BulletManager()
    views = [BulletView()]
    
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
    objects = GunManager()
    views = [GunView()]
    
    MAX_TURN = 20.0
    COOLING_RATE = 0.1
    MAX_POWER = 3.0
    MIN_POWER = 0.0

    def __init__(self, tank, heading=0.0, heat=5.0):
        super(Gun, self).__init__(tank, heading)
        self.heat = heat

class Radar(TankPart):
    '''A tank radar.'''
    objects = RadarManager()
    views = [RadarView()]
    
    MAX_TURN = 45.0
    scan_arc = 45.0


class Tank(Projectile):
    '''A tank object.'''
    objects = TankManager()
    views = [TankView()]
    
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

