# -*- coding: utf8 -*-

from __future__ import unicode_literals

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from camera import Camera


class Graphx(object):
    """Master class of the graphics engine"""
    def __init__(self, screen_size=(800, 600), clear_color=(0, 0, 0),
                 camera_initial_position=(0, 0, 0),
                 camera_initial_direction=(0, 0, 1)):
        """
            Initialize the graphics engine
            screen_size -- tuple(width, height): represents the size of the screen
        """
        super(Graphx, self).__init__()
        pygame.init()
        screen = pygame.display.set_mode(screen_size, HWSURFACE|OPENGL|DOUBLEBUF)
        self.camera = Camera(camera_initial_position)
        self.screen_width, self.screen_height = self.screen_size = screen_size

        glEnable(GL_DEPTH_TEST)

        glShadeModel(GL_FLAT)
        glClearColor(*clear_color)

        glEnable(GL_COLOR_MATERIAL)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glLight(GL_LIGHT0, GL_POSITION,  (0, 1, 1, 0))

        self.resize(*screen_size)

        glMaterial(GL_FRONT, GL_AMBIENT, (0.1, 0.1, 0.1, 1.0))
        glMaterial(GL_FRONT, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

    def resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, float(width)/height, .1, 1000.)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def event(self, e):
        """
            Handle the event. Propagate it to the camera object.
            e -- the event to handle
        """
        self.camera.event(e)

    def keyPress(self, pressed=None):
        """
            Manage pressed keys.
        """
        if pressed is None:
            pressed = pygame.key.get_pressed()
        self.camera.keyPress(pressed)

    def update(self, frame_time=5, key_pressed=None):
        """
        Update the internal state of the camera. This need to be called
        once per frame.
        pressed -- dict: (optional) for each key hold a boolean set to true
                   if the key is pressed
                   If not provided, call pygame.key.get_pressed() to
                   retrieve it
        frame_time -- float (optional): the time passed since the last drawed frame in milliseconds
                      (computed by the pygame.time.Clock tick call)
                      If not provided, assume that 5 milliseconds have passed
        """
        self.keyPress(key_pressed)
        self.camera.update(frame_time)

        # Upload the inverse camera matrix to OpenGL
        glLoadMatrixd(self.camera.camera_matrix.get_inverse().to_opengl())
        # Light must be transformed as well
        glLight(GL_LIGHT0, GL_POSITION,  (0, 1.5, 1, 0))

        # Show the screen
        pygame.display.flip()

        self.__clear()

    def __clear(self):
        """ Clear the screen. Should be called before any drawing. """
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

