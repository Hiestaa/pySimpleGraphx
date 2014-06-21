# -*- coding: utf8 -*-

from __future__ import unicode_literals

from math import radians
import pygame

from mathobj.matrix44 import *
from mathobj.vector3 import *


class Camera(object):
    """Represent the camera of the graphics engine"""
    def __init__(self, initial_position):
        super(Camera, self).__init__()

        # Camera transform matrix
        self.camera_matrix = Matrix44()
        self.camera_matrix.translate = initial_position

        # Initialize speeds and directions
        self.rotation_direction = Vector3()
        self.rotation_speed = radians(90.0)
        self.movement_direction = Vector3()
        self.movement_speed = 5.0

        self.key_bindings = {
            'right': pygame.K_a,
            'left': pygame.K_d,
            'forward': pygame.K_w,
            'backward': pygame.K_s,
            'up': pygame.K_r,
            'down': pygame.K_f,
            'look_left': pygame.K_LEFT,
            'look_right': pygame.K_RIGHT,
            'look_up': pygame.K_UP,
            'look_down': pygame.K_DOWN,
            'roll_right': pygame.K_e,
            'roll_left': pygame.K_q
        }

    def keyPress(self, pressed):
        """
            Manage pressed key
            pressed -- dict: for each key hold a boolean set to true
                       if the key is pressed
        """
        if pressed[self.key_bindings['look_left']]:
            self.rotation_direction.y = +1.0
        if pressed[self.key_bindings['look_right']]:
            self.rotation_direction.y = -1.0
        if pressed[self.key_bindings['look_up']]:
            self.rotation_direction.x = +1.0
        if pressed[self.key_bindings['look_down']]:
            self.rotation_direction.x = -1.0
        if pressed[self.key_bindings['roll_right']]:
            self.rotation_direction.z = -1.0
        if pressed[self.key_bindings['roll_left']]:
            self.rotation_direction.z = +1.0
        if pressed[self.key_bindings['forward']]:
            self.movement_direction.z = -1.0
        if pressed[self.key_bindings['backward']]:
            self.movement_direction.z = +1.0
        if pressed[self.key_bindings['right']]:
            self.movement_direction.x = -1.0
        if pressed[self.key_bindings['left']]:
            self.movement_direction.x = +1.0
        if pressed[self.key_bindings['up']]:
            self.movement_direction.y = +1.0
        if pressed[self.key_bindings['down']]:
            self.movement_direction.y = -1.0

    def event(self, e):
        """
            Handle the event.
            e -- the event to handle
        """
        pass

    def update(self, frame_time):
        """
        Update the internal state of the camera. This need to be called
        once per frame.
        frame_time -- float: the time passed since the last drawed frame in milliseconds
                      (computed by the pygame.time.Clock tick call)
        """
        # Calculate rotation matrix and multiply by camera matrix
        rotation = self.rotation_direction * self.rotation_speed * frame_time / 1000
        rotation_matrix = Matrix44.xyz_rotation(*rotation)
        self.camera_matrix *= rotation_matrix

        # Calcluate movment and add it to camera matrix translate
        heading = Vector3(self.camera_matrix.forward)
        movement = heading * self.movement_direction.z * self.movement_speed
        self.camera_matrix.translate += movement * frame_time / 1000

        horiz = Vector3(self.camera_matrix.x_axis)
        movement = horiz * self.movement_direction.x * self.movement_speed
        self.camera_matrix.translate += movement * frame_time / 1000

        vert = Vector3(self.camera_matrix.y_axis)
        movement = vert * self.movement_direction.y * self.movement_speed
        self.camera_matrix.translate += movement * frame_time / 1000

        # Reset rotation and movement directions
        self.rotation_direction.set(0.0, 0.0, 0.0)
        self.movement_direction.set(0.0, 0.0, 0.0)
