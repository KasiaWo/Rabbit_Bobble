"""
Module for managing platforms.
"""
import pygame

import constants as const
from spritesheet_functions import SpriteSheet
 



GRASS_LEFT            = (576, 360, 70, 40)
GRASS_RIGHT           = (576, 216, 70, 40)
GRASS_MIDDLE          = (576, 288, 70, 40)
STONE_PLATFORM_LEFT   = (432, 720, 70, 40)
STONE_PLATFORM_MIDDLE = (648, 648, 70, 40)
STONE_PLATFORM_RIGHT  = (792, 648, 70, 40)
STONE_PLATFORM_FRAME  = (504, 288, 70, 70)


class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, sprite_sheet_data):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        sprite_sheet = SpriteSheet("tiles_spritesheet.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3],const.BLACK)
 
        self.rect = self.image.get_rect()
    
    
class Platform_stone(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, sprite_sheet_data):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        sprite_sheet = SpriteSheet("tiles_spritesheet.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3],const.BLACK)
 
        self.rect = self.image.get_rect()
class Block(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, sprite_sheet_data):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super().__init__()
 
        sprite_sheet = SpriteSheet("tiles_spritesheet.png")
        # Grab the image for this platform
        self.image = sprite_sheet.get_image(sprite_sheet_data[0],
                                            sprite_sheet_data[1],
                                            sprite_sheet_data[2],
                                            sprite_sheet_data[3],const.BLACK)
 
        self.rect = self.image.get_rect()
     
 