print "importing pygame..."
import pygame
from pygame.locals import *

from bluegear.screen import Screen
from bluegear.models import Manager

from settings import *


class Controller(object):
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = False
        self.managers = []

    def setup(self):
        tank = Tank(position=(100, 100))

    def register(self, *entities):
        for entity in entities:
            self.managers.append(entity.objects)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_P:
                    self.unpaused = not self.unpaused

    def update(self, context):
        for manager in self.managers:
            manager.update_all(context)

    def run(self):
        with Screen(BATTLEFIELD_SIZE) as screen:
            from pytanks.models import Bullet, Radar, Gun, Tank
            self.register(Bullet, Radar, Gun, Tank)
            screen.register(Bullet, Radar, Gun, Tank)
            tank = Tank(position=(100, 100))
            tank2 = Tank(position=(300, 300))
            print "starting game..."
            self.running = True
            while self.running:
                time_passed_ms = self.clock.tick(FRAMES_PER_SECOND)
                self.handle_events()
                self.update({'dt':1})
                screen.refresh()


if __name__ == "__main__":
    controller = Controller()
    controller.run()
