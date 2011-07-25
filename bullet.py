import pygame
from pygame.sprite import Sprite

from vector import Vector

from game_object import Collidable

class Bullet2(Sprite):
    image = 'images/bullet.png'
    def __init__(self, shooter, power):
        pygame.sprite.Sprite.__init__(self)
        self.shooter = shooter
        self.power = power
        self.position = shooter.position
        self.heading = shooter.gun.heading
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position #eh..


class Bullet(Collidable):
    def __init__(self, tank, heading, power):
        super(Bullet, self).__init__(tank.position, heading.length(), Bullet.Meta.width)
        self.tank = tank
        self.power = power
        self.velocity = Vector([20 - 3 * power])

        self.base_image = pygame.image.load(Bullet.Meta.image)
        self.image = pygame.transform.rotate(self.base_image, self.heading.length())
        self.image_w, self.image_h = self.image.get_size()

    def update(self, dt):
        super(Bullet, self).update(dt)
        self.velocity = Vector([20 - 3 * self.power])

    def draw(self, screen):
        self.image = pygame.transform.rotate(
            self.base_image, self.heading.length())
        self.image_w, self.image_h = self.image.get_size()
        center = self.image.get_rect().move(
            self.position[0] - self.image_w / 2,
            self.position[1] - self.image_h / 2)
        screen.blit(self.image, center)

    def on_collide(self, target=None):
        if target:
            self.target.power -= 4 * power
        self.tank.power += 3 * self.power

    class Meta:
        image = 'images/bullet.png'
        width = 3.0
