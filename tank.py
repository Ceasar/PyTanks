import pygame

from descartes import cartesian_angle
from vector import Vector

from bullet import Bullet
from game_object import Movable, Rotatable, Positionable, Collidable

import random


class Tank(Collidable):
    def __init__(self, world, controller, position, heading, name=None):
        super(Tank, self).__init__(position, heading, Tank.Meta.width)
        self.world = world
        self.controller = None
        self.gun = Gun(self)
        self.radar = Radar(self)
        self.power = 100.0
        self.name = name

        self.base_image = pygame.image.load(Tank.Meta.image)
        self.image = pygame.transform.rotate(
            self.base_image, self.heading.length())
        self.image_w, self.image_h = self.image.get_size()
        pygame.sprite.RenderPlain(self.image)

    def update(self, dt):
        super(Tank, self).update(dt)
        self.gun.update(dt)
        self.accelerate(random.gauss(0, 3))
        self.spin(random.gauss(0, 2))
        self.gun.spin(random.gauss(0, 5))
        try:
            self.gun.fire(3.0)
        except:
            pass
        self.radar.update(dt)

    def draw(self, screen):
        self.image = pygame.transform.rotate(
            self.base_image, self.heading.length())
        self.image_w, self.image_h = self.image.get_size()
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        #creen.blit(self.image, center)
        self.gun.draw(screen)
        self.radar.draw(screen)

    class Meta:
        image = 'images/body.png'
        width = 18.0

class Gun(Rotatable):
    def __init__(self, tank, heading=0.0, heat=5.0):
        super(Gun, self).__init__(heading)
        self.heat = heat
        self.tank = tank

        self.base_image = pygame.image.load(Gun.Meta.image)
        self.image = pygame.transform.rotate(
            self.base_image, self.heading.length())
        self.image_w, self.image_h = self.image.get_size()

    def fire(self, power):
        '''Fire the gun.'''
        if self.heat > 0:
            raise ValueError(self.heat)
        bullet = Bullet(self.tank, self.heading, power)
        self.tank.world.entities.insert(0, bullet)
        self.heat = 1 + power / 5.0

    def update(self, dt):
        super(Gun, self).update(dt)
        self.heat -= Gun.Meta.cooling_rate

    def draw(self, screen):
        self.image = pygame.transform.rotate(
            self.base_image, self.heading.length())
        self.image_w, self.image_h = self.image.get_size()
        center = self.image.get_rect().move(
            self.tank.position[0] - self.image_w / 2,
            self.tank.position[1] - self.image_h / 2)
        screen.blit(self.image, center) 

    class Meta:
        cooling_rate = 0.1
        image = 'images/turret.png'
        rpm = 20.0

class Radar(Rotatable):
    def __init__(self, tank, heading=0.0):
        super(Radar, self).__init__(heading)
        self.tank = tank

        self.base_image = pygame.image.load(Radar.Meta.image)
        self.image = pygame.transform.rotate(
            self.base_image, self.heading.length())
        self.image_w, self.image_h = self.image.get_size()

    def detect(self, other):
        '''Determine if a target is scanned.'''
        dtheta = cartesian_angle(self.tank.position, other.position)
        return abs(angle - self.heading) < Radar.Meta.scan_arc

    def collect(self, other):
        return {
            'distance': (other.position - self.position).length(),
            'angle': cartesian_angle(self.tank.position, other.position)
            }

    def scan(self, others):
        '''Scan ahead for any objects.'''
        return [collect(other) for other in others if detect(other)]

    def draw(self, screen):
        self.image = pygame.transform.rotate(
            self.base_image, self.heading.length())
        self.image_w, self.image_h = self.image.get_size()
        center = self.image.get_rect().move(
            self.tank.position[0] - self.image_w / 2,
            self.tank.position[1] - self.image_h / 2)
        screen.blit(self.image, center)

    class Meta:
        image = 'images/radar.png'
        scan_arc = 45.0
        rpm = 45.0
