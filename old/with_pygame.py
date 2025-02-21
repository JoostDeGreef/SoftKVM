import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys
import ctypes

camera = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("SoftKVM")
#screen = pygame.display.set_mode([1280,720])
#monitor_size = pygame.display.get_desktop_sizes()[0]
user32 = ctypes.windll.user32
monitor_size = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
screen = pygame.display.set_mode(monitor_size, flags=pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN, vsync=True)

try:
    while True:

        ret, frame = camera.read()
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.fliplr(frame)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.fill([0,0,0])
        screen.blit(frame, (0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == KEYDOWN:
                sys.exit(0)
                
except KeyboardInterrupt:
    pygame.quit()
    cv2.destroyAllWindows()