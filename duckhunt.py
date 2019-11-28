import os
import sys
import pygame
import json
import pygame.transform
from game.registry import adjpos
import game.driver
from game.states import BaseState

with open('./game/data.json') as json_file:
    data = json.load(json_file)

GAME_SPECS = data['game_specs']
COLORS = GAME_SPECS['colors']
RECTANGLES = GAME_SPECS['rectangles']
POSITIONS = GAME_SPECS['positions']

# Game parameters
SCREEN_WIDTH, SCREEN_HEIGHT = adjpos(GAME_SPECS['screen_dimensions'].get('width'),
                                     GAME_SPECS['screen_dimensions'].get('height'))

TITLE = GAME_SPECS['title']

FRAMES_PER_SEC = 50

BG_COLOR = (COLORS['FONT_WHITE'].get('R'),
            COLORS['FONT_WHITE'].get('G'),
            COLORS['FONT_WHITE'].get('B'))

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()
pygame.display.set_caption(TITLE)
pygame.mouse.set_visible(False)


class Game(object):
    def __init__(self):
        self.running = True
        self.surface = None
        self.clock = pygame.time.Clock()
        self.size = SCREEN_WIDTH, SCREEN_HEIGHT
        background = os.path.join('media', 'background.jpg')
        bg = pygame.image.load(background)
        self.background = pygame.transform.smoothscale(bg, self.size)
        self.driver = None

    def init(self):
        self.surface = pygame.display.set_mode(self.size)
        self.driver = game.driver.Driver(self.surface)

    def handle_event(self, event):
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key is 27):
            self.running = False
        else:
            self.driver.handle_event(event)

    def loop(self):
        self.clock.tick(FRAMES_PER_SEC)
        self.driver.update()

    def render(self):
        self.surface.blit(self.background, (0, 0))
        self.driver.render()
        pygame.display.flip()

    @staticmethod
    def cleanup():
        pygame.quit()
        sys.exit(0)

    def execute(self):
        self.init()

        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.loop()
            self.render()

        Game.cleanup()


if __name__ == "__main__":
    theGame = Game()
    theGame.execute()
