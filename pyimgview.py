#! /usr/bin/env python

"""
Copyright (c) 2016, Miguel Angel Astor Romero
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted according to the terms in the LICENSE file.

-------------------------------------------------------------------------

Execute as 'pyimgview.py IMAGE'. Use the arrow keys to change between
the images in the working directory. Quit with the esc key.

"""

import sys
import os
import pygame
import pygame.image as pyimg
import pygame.transform as pytrans

SCREEN_SIZE = (640, 480)
TITLE = "Image Viewer"
FPS = 60

def read_img(path):
    """ Attempts to load the file found in path as an image.
    returns None on failure, or a Pygame surface on success. """

    try:
        # Load the image.
        img = pyimg.load(path)
        w, h = img.get_size()

        # Resize the image to fit the screen.
        if w >= h:
            sf = 0
            if SCREEN_SIZE[0] < w:
                sf = float(SCREEN_SIZE[0]) / float(w)
            else:
                sf = float(w) / float(SCREEN_SIZE[0])
            img = pytrans.scale(img, (SCREEN_SIZE[0], int(float(h) * sf)))
        else:
            if SCREEN_SIZE[1] < h:
                sf = float(SCREEN_SIZE[1]) / float(h)
            else:
                sf = float(h) / float(SCREEN_SIZE[1])
            img = pytrans.scale(img, (int(float(w) * sf), SCREEN_SIZE[1]))

    except Exception as e:
        print e
        print "Error: could not load " + path + ". It may not be a valid image file."
        return None

    else:
        return img

def main():
    """ Main game loop. """
    global SCREEN_SIZE

    # Check command line arguments and if the input file exists.
    if len(sys.argv) < 2:
        print "Usage: " + sys.argv[0] + " IMAGE"
        return

    if not os.access(sys.argv[1], os.R_OK):
        print "Error: image file " + sys.argv[1] + " cannot be opened for reading."
        return

    # Get a list of all the files in the current working directory.
    d, f = os.path.split(sys.argv[1])
    d = os.getcwd() if d == '' else d
    files = sorted(os.listdir(d))
    img_ind = files.index(f)

    # Read the image and get it's dimensions.
    img = read_img(sys.argv[1])
    if img is None:
        return
    w, h = img.get_size()
    pos = ((SCREEN_SIZE[0] - w) / 2, (SCREEN_SIZE[1] - h) / 2)

    # Initialize Pygame.
    pygame.init()
    clock = pygame.time.Clock()
    screen  = pygame.display.set_mode(SCREEN_SIZE)
    pygame.mouse.set_visible(False)
    done = False

    # Main game loop.
    try:
        while(not done):
            fps = clock.get_fps() + 0.001
            pygame.display.set_caption(TITLE + ": " + f)
            
            # Render cycle.
            screen.fill((0, 0, 0))
            screen.blit(img, pos)

            pygame.display.update()
            clock.tick(FPS)

            # Input capture.
            event = pygame.event.wait()

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or event.type == pygame.QUIT:
                # Quit on escape key.
                done = True

            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT):
                # Load the next image on right arrow key.
                # Try with all following files until an image is found, wich may be
                # the same one that is already loaded.
                img = None
                while img is None:
                    img_ind = (img_ind + 1) % len(files)
                    f = files[img_ind]
                    path = os.path.join(d, f)
                    img = read_img(path)

                # Get the image dimensions.
                w, h = img.get_size()
                pos = ((SCREEN_SIZE[0] - w) / 2, (SCREEN_SIZE[1] - h) / 2)
                    
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT):
                # Load the previous image on left arrow key.
                # Try with all previous files until an image is found, wich may be
                # the same one that is already loaded.
                img = None
                while img is None:
                    img_ind -= 1
                    if img_ind < 0:
                        img_ind = len(files) - 1
                    f = files[img_ind]
                    path = os.path.join(d, f)
                    img = read_img(path)

                # Get the image dimensions.
                w, h = img.get_size()
                pos = ((SCREEN_SIZE[0] - w) / 2, (SCREEN_SIZE[1] - h) / 2)
            
    except Exception:
        pass

    pygame.quit()

if __name__ == "__main__":
    main()

