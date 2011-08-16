print "importing pygame..."
import pygame
from pygame.locals import *

from bluegear.screen import Screen

from pytanks.models import ENTITIES, BULLETS, TANKS, GUNS, RADARS

from settings import *


class Controller(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = False

    def setup(self):
        from pytanks.models import Tank
        self.tank = Tank(position=(100, 100))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_P:
                    self.unpaused = not self.unpaused

    def run(self):
        with View(BATTLEFIELD_SIZE, BG_COLOR) as view:
            print "starting game..."
            self.running = True
            while self.running:
                time_passed_ms = self.clock.tick(FRAMES_PER_SECOND)
                self.handle_events()
                self.tank.run()
                BULLETS.update(1)
                #backward any..?
                RADARS.update(1)
                GUNS.update(1)
                TANKS.update(1)
                view.draw(ENTITIES)


if __name__ == "__main__":
    controller = Controller()
    controller.setup()
    controller.run()
