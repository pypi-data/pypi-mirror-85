import pygame
import os

from . import tools, prepare, player


def main():
	prepare.game_loop()
	pygame.quit()

if __name__ == '__main__':
    main()