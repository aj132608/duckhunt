import os
import sys
import pygame
import json
import pygame.transform
import numpy as np
import cv2
import tensorflow.keras
from PIL import Image
from time import sleep
from win32api import GetSystemMetrics
from game.registry import adjpos, adjheight
import game.driver

with open('./game/config.json') as json_file:
    data = json.load(json_file)


GAME_SPECS = data['game_specs']
COLORS = GAME_SPECS['colors']
RECTANGLES = GAME_SPECS['rectangles']
POSITIONS = GAME_SPECS['positions']

print("Width =", GetSystemMetrics(0))
print("Height =", GetSystemMetrics(1))

# Game parameters
# SCREEN_WIDTH, SCREEN_HEIGHT = adjpos(GAME_SPECS['screen_dimensions'].get('width'),
# #                                      GAME_SPECS['screen_dimensions'].get('height'))

SCREEN_WIDTH, SCREEN_HEIGHT = adjpos(GetSystemMetrics(0), GetSystemMetrics(1))

TITLE = GAME_SPECS['title']

FRAMES_PER_SEC = 50

BG_COLOR = (COLORS['FONT_WHITE'].get('R'),
            COLORS['FONT_WHITE'].get('G'),
            COLORS['FONT_WHITE'].get('B'))

FONT = os.path.join('media', 'arcadeclassic.ttf')

cap = cv2.VideoCapture(0)

# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5', compile=False)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Create the array of the right shape to feed into the keras model
# The 'length' or number of images you can put into the array is
# determined by the first position in the shape tuple, in this case 1.
data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

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

    def game_intro(self):

        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.surface.blit(self.background, (0, 0))
            large_text = pygame.font.Font(FONT, adjheight(20))
            my_title = large_text.render('DUCKHUNT', True, FONT)

    def init(self):
        self.surface = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
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

    def post_prediction_as_event(self):
        ret, frame = cap.read()

        # Our operations on the frame come here
        # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Flip the image
        frame = cv2.flip(frame, 1)

        # Slow down the imgages being get
        # sleep(0.04)

        # Get the img into PIL
        # image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)

        # Make sure to resize all images to 224, 224 otherwise they won't fit in the array
        image = image.resize((224, 224))
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data)
        # print(prediction)
        # prediction_value = np.where(prediction == np.amax(prediction))[0]
        pred_val = np.argmax(prediction)
        switcher = {
            0: [0, 0, 0],
            1: [119, 'w', 17],
            2: [115, 's', 31],
            3: [100, 'd', 32],
            4: [97, 'a', 30]
        }
        # print(switcher.get(pred_val, "Return Nothing"))
        event_vals = switcher.get(pred_val, [0, 0, 0])
        # event = pygame.event.Event(pygame.KEYDOWN, );
        event = pygame.event.Event(pygame.KEYDOWN, {'key': event_vals[0],
                                                    'unicode': event_vals[1],
                                                    'mod': 0,
                                                    'scancode': event_vals[2],
                                                    'window': None})

        if pred_val != 0:
            pygame.event.post(event)

    def execute(self):
        self.init()

        while self.running:

            self.post_prediction_as_event()

            # Display the resulting frame
            # cv2.imshow('Cur frame', frame)
            for event in pygame.event.get():
                # print(event)
                # mouse movements and button presses
                self.handle_event(event)
            self.loop()
            self.render()

        Game.cleanup()


if __name__ == "__main__":
    theGame = Game()
    theGame.execute()
