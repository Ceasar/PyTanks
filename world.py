import math
import sys

import pygame
from pygame.locals import *

from vector import Vector

from tank import Tank

BG_COLOR = 0, 0, 0
FRAMES_PER_SECOND = 20

pygame.init()

class Main(object):
    def __init__(self):
        self.running = True
        self.entities = [Tank(self, None, Vector([100, 100]), 0), Tank(self, None, Vector([500,500]), 0)]
        self.size = self.width, self.height = 800, 600
        self.clock = pygame.time.Clock()
        self.screen = None

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
    
    def run(self):
        #screen.blit(self.background, (0,0))
        self.screen = pygame.display.set_mode(self.size, 0, 32)
        while self.running:
            try:
                time_passed = self.clock.tick(FRAMES_PER_SECOND)
                for event in pygame.event.get():
                    self.on_event(event)
                self.screen.fill(BG_COLOR)
                for entity in self.entities:
                    entity.update(time_passed / (1000.0 / FRAMES_PER_SECOND))
                    entity.draw(self.screen)
                pygame.display.flip()
            except Exception as e:
                print e
                break
        sys.exit()

if __name__ == '__main__':
    main = Main()
    main.run()
