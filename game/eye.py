import os
import pygame


class Gun(object):
    def __init__(self, registry):
        self.registry = registry
        self.rounds = 3
        # Starting position
        self.mousePos = (0, 0)
        self.mouseImg = pygame.image.load(os.path.join('media', 'crosshairs.png'))

    def render(self):
        surface = self.registry.get('surface')
        surface.blit(self.mouseImg, self.mousePos)

    def reload_it(self):
        self.rounds = 3

    def move_cross_hairs(self, pos):
        xOffset = self.mouseImg.get_width() / 2
        yOffset = self.mouseImg.get_height() / 2
        x, y = pos
        self.mousePos = (x - xOffset), (y - yOffset)

    def shoot(self):
        if self.rounds <= 0:
            return False

        self.registry.get('soundHandler').enqueue('blast')
        self.rounds = self.rounds - 1
        return True