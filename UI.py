import pyaudio

__author__ = "Ethan Garza"

import pygame
import os
# import pyaudio
import wave

pygame.init()

# As there are 6 rows and 7 columns, leads to a nice 6 to 7 ratio, each by a factor of 84 (6*7*2)
width = 588
# the additional 200 was to have 100 pixels free above and below the board
height = 504+200
# delta represents the factor mentioned earlier (dimen of box to hold circle for conect four)
delta = 84
radius = delta // 2

# colors stored in RGB tuple format
WHITE = (255,255,255)
BLUE = (0,0,255)
YELLOW = (255,255,153)
RED = (255,0,0)
BLACK = (0, 0, 0)

# determines the start and end positions of the board (upper left-hand corner anyways)
start_x = 0
start_y = 100
# start is a boolean whether or not to start a game. This allows the restart function seen later
start = True
end_x = width
end_y = height

gameDisplay = pygame.display.set_mode((width, height))
gameDisplay.fill(YELLOW)


def text_objects(text, font):
    """
    Creates a text object
    :param text: a string to represent the message
    :param font: an associated font
    :return: A text Surface and its associated rectangle
    """
    textSurface = font.render(text, True, BLACK)
    return textSurface, textSurface.get_rect()

# displays center of text centered around location with font size 'size'
def message_display(text, loc, size):
    """
    To display a message on the window given a text/message at a specified area and size
    :param text: a string
    :param loc: a tuple (x, y) format
    :param size: the size of the text
    :return: None
    """
    # gameDisplay = pygame.display.set_mode((width, height))
    largeText = pygame.font.Font('freesansbold.ttf', size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (loc[0],loc[1])
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()


# filename is a string and in a .wav format
def record(filename, pygame):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = filename
    full_dir = os.path.join(dir_path, filename)
    if os.path.exists(full_dir):
        os.remove(full_dir)
        print("Popped")

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")
    frames = []

    i = 0
    end = False

    while i < int(RATE / CHUNK * RECORD_SECONDS) and not end:
        data = stream.read(CHUNK)
        frames.append(data)
        for event in pygame.event.get():
            if event.type == pygame.K_s:
                end = True
        i += 1

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(full_dir, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def init_messages():
    message = "press r to record (will automatically stop recording after 5 seconds)"
    loc = (250, 400)
    font_size = 12
    message_display(message, loc, font_size)
    message = "press s to stop recording (or wait for the 5 second duration to end)"
    loc = (250, 450)
    font_size = 12
    message_display(message, loc, font_size)
    message = "Results will show once processed"
    loc = (150, 500)
    font_size = 12
    message_display(message, loc, font_size)

"""
Holds actual interactive gameplay of Connect Four that allows the game to be played several times! (hence two while loops)
"""

init_messages()
pygame.display.set_caption('Had too much to drink?')
clock = pygame.time.Clock()

while True:

    """
    For loop reads the keyboard for inputs
    """
    # print("?")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            # print("here?")
            if event.key == pygame.K_r:
                # print("r")re
                record("test_sound_file", pygame)

    pygame.display.update()
    clock.tick(60)
