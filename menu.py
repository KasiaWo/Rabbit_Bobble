import pygame
import numpy

import random
import os

import constants as const
from spritesheet_functions import SpriteSheet
import platforms
from player import Player
from player import Bullet
from player import Life
import enemy






class Menu(object):
 
 
    def __init__(self, screen, game):
       
        
        self.game = game
        self.screen = screen
        
        self.title= "Settings"
        
        
        sprite_sheet = SpriteSheet("spritesheet_jumper.png")
        self.player_image = [sprite_sheet.get_image(614, 1063, 120, 191,const.BLACK),
                             sprite_sheet.get_image(581, 1265, 120, 191,const.BLACK)]
        self.which_image = [0,0, 0]
        
        self.player_life = [3,4,5]
        self.difficult_level = ["EASY","HARD"]
        
        self.menu_icons = [self.player_image, self.player_life, self.difficult_level]
        
        self.which_icon = 0
        
        
        self.font_name = const.FONT_NAME2
        
        self.menu_open = True
        self.running = True
        self.settings = True
        
        img_life = SpriteSheet("life.png")
        self.life_image = img_life.get_image(42,
                                                54,
                                                119,
                                                102, const.BLACK, 2, 2)
        
    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game.menu_open = False
                    self.game.running = False
                    self.game.settings = False
               
                
 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.which_image[self.which_icon] = (self.which_image[self.which_icon] +1) % len(self.menu_icons[self.which_icon])
                       
                    if event.key == pygame.K_LEFT:
                        self.which_image[self.which_icon] = (self.which_image[self.which_icon] -1) % len(self.menu_icons[self.which_icon])
                    if event.key == pygame.K_DOWN:
                        self.which_icon = (self.which_icon + 1) % len(self.menu_icons)
                        prize_song=pygame.mixer.Sound( 'click.wav')
        
                        prize_song.play()
                    if event.key == pygame.K_UP:
                        self.which_icon = (self.which_icon - 1) % len(self.menu_icons)
                        prize_song=pygame.mixer.Sound( 'click.wav')
        
                        prize_song.play()
                    if event.key == pygame.K_SPACE:
                       
                        self.game.menu_open = False
                        self.game.running = True
                        self.game.settings = False
        self.game.which_character= self.which_image[0]            



        
          
 
    def draw(self):
        """ Draw menu. """
      
        self.screen.fill(const.BGCOLOR)
        self.draw_text("Settings", 80, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 10 )
        
        self.screen.blit(self.menu_icons[0][self.which_image[0]] , (50, const.SCREEN_HEIGHT / 4 ))
        self.draw_text(str(self.menu_icons[1][self.which_image[1]]), 55, const.WHITE, 50, const.SCREEN_HEIGHT / 4+240)
        self.screen.blit(self.life_image, (65,const.SCREEN_HEIGHT / 4+250))
        self.draw_text(str(self.menu_icons[2][self.which_image[2]]), 55, const.WHITE, 90, const.SCREEN_HEIGHT / 4+2*190 + 40)
        self.draw_text("Choose character", 50, const.WHITE,500, const.SCREEN_HEIGHT / 4 + 30)
        self.draw_text("Choose number of life", 50, const.WHITE,500, const.SCREEN_HEIGHT / 4+220)
        self.draw_text("Choose difficulty", 50, const.WHITE,500, const.SCREEN_HEIGHT / 4+2*200)
        
        a= 190
       
        pygame.draw.rect(self.screen, const.WHITE , (180,const.SCREEN_HEIGHT / 4 +20 + a* self.which_icon , 700,100), 6)
        
        self.draw_text("Arrows to choose, Space to return to menu", 30, const.WHITE,500, 7*const.SCREEN_HEIGHT / 8)
        pygame.display.flip()
            

    def run(self):
        self.events()
        self.draw()

        
        
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.SysFont(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
 
 