import os
import pygame
from game.registry import Registry, adjpos
from game.sounds import SoundHandler
from game.states import StartState


class Driver(object):
    def __init__(self, surface):
        # Set a global registry
        self.registry = Registry()
        self.registry.set('surface', surface)
        self.registry.set('soundHandler', SoundHandler())

        controls = pygame.image.load(os.path.join ('media', 'controls.png'))
        self.registry.set('control_images', pygame.transform.smoothscale (controls, adjpos(*controls.get_size())))

        sprites = pygame.image.load(os.path.join ('media', 'sprites.png'))
        sprites = pygame.transform.scale (sprites, adjpos(*sprites.get_size()))
        self.registry.set('sprites', sprites)
        
        rsprites = pygame.transform.flip(sprites, True, False)
        self.registry.set('rsprites', rsprites)

        self.registry.set('score', 0)
        self.registry.set('round', 1)

        # Start the game
        self.state = StartState(self.registry)
        self.state = self.state.start()

    def handle_event(self, event):
        # Toggle sound
        if event.type == pygame.KEYDOWN and event.key is pygame.K_s:
            self.registry.get('soundHandler').toggleSound()

        self.state.execute(event)

    def update(self):
        new_state = self.state.update()

        if new_state:
            self.state = new_state

    def render(self):
        self.state.render()
        self.registry.get('soundHandler').flush()
