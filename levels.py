import pygame
import numpy

import random
import os

import constants as const
import platforms 
from platforms import Platform
from platforms import Platform_stone
from player import Player
from player import Bullet
from player import Life
import enemy




class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, screen, player, diff):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.screen = screen
        
        self.player = player
        
        self.init_difficulty = diff
        
        self.start_time = pygame.time.get_ticks()
        self.close = False
        self.close_time = 0
        
        self.platform_list = pygame.sprite.Group()
        self.platform_grass_list = pygame.sprite.Group()
        self.platform_stone_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.block_list = pygame.sprite.Group()
        self.active_sprite = pygame.sprite.Group()
        self.bullet_list = pygame.sprite.Group()
        self.enemy_bubble_list = pygame.sprite.Group()
        self.fruit_list = pygame.sprite.Group()
        self.bullet_carrot_list = pygame.sprite.Group()
        self.carrot_list = pygame.sprite.Group()
        
        self.name=None
         
        # Background image
        
        self.background = None
        
        self.font_name = pygame.font.match_font(const.FONT_NAME)

 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        if pygame.time.get_ticks() - self.start_time > const.LEVEL_WAITING:
            self.player.update()
            self.platform_list.update()
            self.platform_grass_list.update()
            self.platform_stone_list.update()
            self.enemy_list.update()
            self.bullet_list.update()
            self.active_sprite.update()
            self.enemy_bubble_list.update()
            self.fruit_list.update()
            for bullet in self.bullet_list:
                if bullet.rect.x > const.SCREEN_WIDTH + 10 or bullet.rect.x < -10:
                    self.bullet_list.remove(bullet)
                    self.active_sprite.remove(bullet)


            for guy in self.enemy_list:
                enemy_hit_list = pygame.sprite.spritecollide(guy, self.bullet_list, False, pygame.sprite.collide_circle)
                for hit in enemy_hit_list:
                    bub_enemy= enemy.Enemy_bubble(guy)
                    self.enemy_list.remove(guy)

                    self.bullet_list.remove(hit)
                    self.active_sprite.add(bub_enemy)
                    self.active_sprite.remove(hit)
                    self.active_sprite.remove(guy)

                    self.enemy_bubble_list.add(bub_enemy)


            if len(self.enemy_list) == 0 and len(self.enemy_bubble_list) == 0  and self.close_time == 0:
                self.close_time=pygame.time.get_ticks()

            if self.close_time > 0  and pygame.time.get_ticks()-self.close_time > 2000:
                self.close = True

        
          
 
    def draw(self):
        """ Draw everything on this level. """
        if  pygame.time.get_ticks() - self.start_time < const.LEVEL_WAITING: 
            
            self.screen.fill(const.BGCOLOR)
            self.draw_text(self.name, 48, const.WHITE, const.SCREEN_WIDTH / 2,  const.SCREEN_HEIGHT / 4)
            
            
        else:
            # Draw the background
            self.screen.fill(const.BGCOLOR)

            # Draw all the sprite lists that we have
            self.active_sprite.draw(self.screen)
            if self.player.lost_life == False:
                    self.screen.blit(self.player.image, self.player.rect)
        
        
    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
 
 
# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, screen, player, diff):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, screen, player, diff)

        self.name="Level 1"
        
        
        x = [[0,17,const.SCREEN_HEIGHT - 30],[200,8,const.SCREEN_HEIGHT - 280], [200,8,const.SCREEN_HEIGHT - 2*280]]
        ile = numpy.sum(x,axis=0)[1]
        
        level=[]
       
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level.append([platforms.GRASS_LEFT, x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level.append([platforms.GRASS_RIGHT, x_i[0]+i*70, x_i[2]])
                    else:
                        level.append([platforms.GRASS_MIDDLE, x_i[0]+i*70, x_i[2]])
                  
        
        x = [[0,17,-38]]
        level_stone=[]
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    else:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
        
        
        for platform in level:
            block = Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_grass_list.add(block)
        
        for platform in level_stone:
            block = Platform_stone(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_stone_list.add(block)
         
            
        
        level_enemy = [[500,const.SCREEN_HEIGHT - 280],[ 700, const.SCREEN_HEIGHT - 2*280 ]]
        for enemies in level_enemy:
            guy=enemy.Enemy(enemies[0],enemies[1], self, 1.5, self.init_difficulty)
            self.active_sprite.add(guy)
            self.enemy_list.add(guy)
        

            
class Level_02(Level):
    """ Definition for level 1. """
 
    def __init__(self, screen, player, diff):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, screen, player, diff)
 
        
        self.name="Level 2"
        x = [[0,17,const.SCREEN_HEIGHT - 30] ,[0,3,const.SCREEN_HEIGHT - 280], [const.SCREEN_WIDTH- 3*70,3,const.SCREEN_HEIGHT - 280],[140,3,const.SCREEN_HEIGHT - 2* 280],[const.SCREEN_WIDTH- 5*70,3,const.SCREEN_HEIGHT - 2* 280],[400,3,const.SCREEN_HEIGHT - 3*280]]
       
        level=[]
       
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level.append([platforms.GRASS_LEFT, x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level.append([platforms.GRASS_RIGHT, x_i[0]+i*70, x_i[2]])
                    else:
                        level.append([platforms.GRASS_MIDDLE, x_i[0]+i*70, x_i[2]])
                  
        
        x = [[0,17,-38]]
        level_stone=[]
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    else:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_grass_list.add(block)
            
        for platform in level_stone:
            block = platforms.Platform_stone(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_stone_list.add(block)
   
            
        
        level_enemy = [[120,520], [800, 200]]
        for enemies in level_enemy:
            guy=enemy.Enemy(enemies[0],enemies[1], self, 1.5,self.init_difficulty)
            self.active_sprite.add(guy)
            self.enemy_list.add(guy)
            
class Level_03(Level):
    """ Definition for level 1. """
 
    def __init__(self, screen, player, diff):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, screen, player, diff)

 
        
        self.name="Level 3"
        x = [ [0,17,const.SCREEN_HEIGHT - 30],[0,5,const.SCREEN_HEIGHT - 280], [const.SCREEN_WIDTH- 5*70,5,const.SCREEN_HEIGHT - 280],[0,4,const.SCREEN_HEIGHT - 2* 280],[const.SCREEN_WIDTH- 4*70,4,const.SCREEN_HEIGHT - 2* 280],[const.SCREEN_WIDTH/2 - 140 ,4,const.SCREEN_HEIGHT - 2* 280],[400,3,const.SCREEN_HEIGHT - 3*280]]
       
        level=[]
       
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level.append([platforms.GRASS_LEFT, x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level.append([platforms.GRASS_RIGHT, x_i[0]+i*70, x_i[2]])
                    else:
                        level.append([platforms.GRASS_MIDDLE, x_i[0]+i*70, x_i[2]])
                  
        
        x = [[0,17,-38] ]
        level_stone=[]
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    else:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_grass_list.add(block)
            
        for platform in level_stone:
            block = platforms.Platform_stone(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_stone_list.add(block)
            
            
        
        level_enemy = [[120,720], [const.SCREEN_WIDTH- 4*70,720],
                      [const.SCREEN_WIDTH/2 - 100,const.SCREEN_HEIGHT - 2* 280]]
        for enemies in level_enemy:
            guy=enemy.Enemy(enemies[0],enemies[1], self, 1.5,self.init_difficulty)
            self.active_sprite.add(guy)
            self.enemy_list.add(guy)
            
class Level_04(Level):
    """ Definition for level 1. """
 
    def __init__(self, screen, player, diff):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, screen, player, diff)
 
 
        
        self.name="Level 4"
        x = [ [0,17,const.SCREEN_HEIGHT - 30],[0,3,const.SCREEN_HEIGHT - 250], [290, 3,const.SCREEN_HEIGHT - 250],[585,3,const.SCREEN_HEIGHT - 250],[const.SCREEN_WIDTH- 3*70,3,const.SCREEN_HEIGHT - 250],[0,3,const.SCREEN_HEIGHT - 2*250-30], [290, 3,const.SCREEN_HEIGHT- 2*250-30],[585,3,const.SCREEN_HEIGHT - 2*250-30],[const.SCREEN_WIDTH- 3*70,3,const.SCREEN_HEIGHT - 2*250-30],
            [0,3,const.SCREEN_HEIGHT - 2*250-30], [0,3,const.SCREEN_HEIGHT - 3*250-30],[290, 3,const.SCREEN_HEIGHT- 3*250-30],[585,3,const.SCREEN_HEIGHT - 3*250-30],[const.SCREEN_WIDTH- 3*70,3,const.SCREEN_HEIGHT - 3*250-30]]
       
        level=[]
       
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level.append([platforms.GRASS_LEFT, x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level.append([platforms.GRASS_RIGHT, x_i[0]+i*70, x_i[2]])
                    else:
                        level.append([platforms.GRASS_MIDDLE, x_i[0]+i*70, x_i[2]])
                  
        
        x = [[0,17,-38] ]
        level_stone=[]
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    else:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_grass_list.add(block)
            
        for platform in level_stone:
            block = platforms.Platform_stone(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_stone_list.add(block)
            
            
        
        level_enemy = [[120,const.SCREEN_HEIGHT - 250], [600,const.SCREEN_HEIGHT - 250],
                      [125,const.SCREEN_HEIGHT - 2*250-30], [345,const.SCREEN_HEIGHT - 2*250-30], [630,const.SCREEN_HEIGHT - 2*250-30],[900,const.SCREEN_HEIGHT - 2*250-30],
                      [320,const.SCREEN_HEIGHT - 3*250-30], [850,const.SCREEN_HEIGHT - 3*250-30]]
        for enemies in level_enemy:
            guy=enemy.Enemy(enemies[0],enemies[1], self, 1.5,self.init_difficulty)
            self.active_sprite.add(guy)
            self.enemy_list.add(guy)
            
class Level_05(Level):
    """ Definition for level 1. """
 
    def __init__(self, screen, player, diff):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, screen, player, diff)
 
 
        
        self.name="Level 5"
        x = [[0,17,const.SCREEN_HEIGHT - 30],[70,4,const.SCREEN_HEIGHT - 250],[const.SCREEN_WIDTH- 5*70,4,const.SCREEN_HEIGHT - 250],
             [210,10,const.SCREEN_HEIGHT - 2*250-30], 
            [70,4,const.SCREEN_HEIGHT - 3*250-30],[const.SCREEN_WIDTH- 5*70,4,const.SCREEN_HEIGHT - 3*250-30]]
       
        level=[]
       
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level.append([platforms.GRASS_LEFT, x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level.append([platforms.GRASS_RIGHT, x_i[0]+i*70, x_i[2]])
                    else:
                        level.append([platforms.GRASS_MIDDLE, x_i[0]+i*70, x_i[2]])
                  
        
        x = [[0,17,-38] ]
        level_stone=[]
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    else:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_grass_list.add(block)
            
        for platform in level_stone:
            block = platforms.Platform_stone(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_stone_list.add(block)
            
            
        
        level_enemy = [[120,const.SCREEN_HEIGHT - 250], [700,const.SCREEN_HEIGHT - 250],
                       [345,const.SCREEN_HEIGHT - 2*250-30], [630,const.SCREEN_HEIGHT - 2*250-30],[900,const.SCREEN_HEIGHT - 2*250-30]
                      ]
        for enemies in level_enemy:
            guy=enemy.Enemy(enemies[0],enemies[1], self, 1.5,self.init_difficulty)
            self.active_sprite.add(guy)
            self.enemy_list.add(guy)
            
class Level_06(Level):
    """ Definition for level 1. """
 
    def __init__(self, screen, player, diff):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, screen, player, diff)
 
 
        
        self.name="Level 6"
        x = [[0,17,const.SCREEN_HEIGHT - 30],[0,4,const.SCREEN_HEIGHT - 250],[const.SCREEN_WIDTH- 4*70,4,const.SCREEN_HEIGHT - 250],
             [330,6,const.SCREEN_HEIGHT - 2*250-30], 
            [70,4,const.SCREEN_HEIGHT - 3*250-30],[const.SCREEN_WIDTH- 5*70,4,const.SCREEN_HEIGHT - 3*250-30]]
       
        level=[]
       
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level.append([platforms.GRASS_LEFT, x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level.append([platforms.GRASS_RIGHT, x_i[0]+i*70, x_i[2]])
                    else:
                        level.append([platforms.GRASS_MIDDLE, x_i[0]+i*70, x_i[2]])
                  
        
        x = [[0,17,-38] ]
        level_stone=[]
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    else:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_grass_list.add(block)
            
        for platform in level_stone:
            block = platforms.Platform_stone(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_stone_list.add(block)
            
            
        
        level_enemy = [[120,const.SCREEN_HEIGHT - 250], [850,const.SCREEN_HEIGHT - 250],
                       [900,const.SCREEN_HEIGHT - 3*250-30], [300,const.SCREEN_HEIGHT - 3*250-30]
                      ]
        for enemies in level_enemy:
            guy=enemy.Enemy(enemies[0],enemies[1], self, 1.5,self.init_difficulty)
            self.active_sprite.add(guy)
            self.enemy_list.add(guy)
 
class Level_07(Level):
    """ Definition for level 1. """
 
    def __init__(self, screen, player, diff):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, screen, player, diff)

 
        
        self.name="Level 7"
        x = [[0,17,const.SCREEN_HEIGHT - 30],[140,8,const.SCREEN_HEIGHT - 2*250 - 30]]
       
        level=[]
       
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level.append([platforms.GRASS_LEFT, x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level.append([platforms.GRASS_RIGHT, x_i[0]+i*70, x_i[2]])
                    else:
                        level.append([platforms.GRASS_MIDDLE, x_i[0]+i*70, x_i[2]])
                  
        
        x = [[0,17,-38] ]
        level_stone=[]
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    else:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
        x = [[400,5,const.SCREEN_HEIGHT - 250 - 30] ]   
        for x_i in x:
            for i in range(0,x_i[1]):
                if i==0:
                    level_stone.append([platforms.STONE_PLATFORM_LEFT , x_i[0], x_i[2]])
                elif i== x_i[1]-1:
                    level_stone.append([platforms.STONE_PLATFORM_RIGHT , x_i[0]+i*70, x_i[2]])
                else:
                    level_stone.append([platforms.STONE_PLATFORM_MIDDLE , x_i[0]+i*70, x_i[2]])

        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_grass_list.add(block)
            
        for platform in level_stone:
            block = platforms.Platform_stone(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_stone_list.add(block)
            
            
        
        level_enemy = [[900,const.SCREEN_HEIGHT -50], [650,const.SCREEN_HEIGHT - 250 -30],
                       [600,const.SCREEN_HEIGHT - 2*250-30]                    ]
        for enemies in level_enemy:
            guy=enemy.Enemy(enemies[0],enemies[1], self, 1.5,self.init_difficulty)
            self.active_sprite.add(guy)
            self.enemy_list.add(guy)
            
class Level_08(Level):
    """ Definition for level 1. """
 
    def __init__(self, screen, player, diff):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, screen, player, diff)
 
 
        
        self.name="Level 8"
        x = [[0,17,const.SCREEN_HEIGHT - 30],[0,3,const.SCREEN_HEIGHT - 250], [585,3,const.SCREEN_HEIGHT - 250], [290, 3,const.SCREEN_HEIGHT- 2*250-30],[const.SCREEN_WIDTH- 3*70,3,const.SCREEN_HEIGHT - 2*250-30],
            [0,3,const.SCREEN_HEIGHT - 2*250-30], [0,3,const.SCREEN_HEIGHT - 3*250-30],[290, 3,const.SCREEN_HEIGHT- 3*250-30],[585,3,const.SCREEN_HEIGHT - 3*250-30],[const.SCREEN_WIDTH- 3*70,3,const.SCREEN_HEIGHT - 3*250-30]]
       
        level=[]
       
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level.append([platforms.GRASS_LEFT, x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level.append([platforms.GRASS_RIGHT, x_i[0]+i*70, x_i[2]])
                    else:
                        level.append([platforms.GRASS_MIDDLE, x_i[0]+i*70, x_i[2]])
                  
        
        x = [[0,17,-38]]
        level_stone=[]
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    else:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
        x = [[290, 3,const.SCREEN_HEIGHT - 250],[const.SCREEN_WIDTH- 3*70,3,const.SCREEN_HEIGHT - 250],[0,3,const.SCREEN_HEIGHT - 2*250-30], [585,3,const.SCREEN_HEIGHT - 2*250-30]]   
        for x_i in x:
            for i in range(0,x_i[1]):
                if i==0:
                    level_stone.append([platforms.STONE_PLATFORM_LEFT , x_i[0], x_i[2]])
                elif i== x_i[1]-1:
                    level_stone.append([platforms.STONE_PLATFORM_RIGHT , x_i[0]+i*70, x_i[2]])
                else:
                    level_stone.append([platforms.STONE_PLATFORM_MIDDLE , x_i[0]+i*70, x_i[2]])

                    
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_grass_list.add(block)
            
        for platform in level_stone:
            block = platforms.Platform_stone(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_stone_list.add(block)
            
            
        
        level_enemy = [[120,const.SCREEN_HEIGHT - 250], [600,const.SCREEN_HEIGHT - 250],
                       [345,const.SCREEN_HEIGHT - 2*250-30], [900,const.SCREEN_HEIGHT - 2*250-30],
                      [320,const.SCREEN_HEIGHT - 3*250-30], [850,const.SCREEN_HEIGHT - 3*250-30]]
        for enemies in level_enemy:
            guy=enemy.Enemy(enemies[0],enemies[1], self, 1.5,self.init_difficulty)
            self.active_sprite.add(guy)
            self.enemy_list.add(guy)
            
class Level_09(Level):
    """ Definition for level 1. """
 
    def __init__(self, screen, player, diff):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, screen, player, diff)

 
        
        self.name="Level 9"
        x = [[0,17,const.SCREEN_HEIGHT - 30],[150,10,const.SCREEN_HEIGHT - 250], [150,5,const.SCREEN_HEIGHT - 300 - 3*70+30],
            [650,5,const.SCREEN_HEIGHT - 300 - 5*70+30]]
       
        level=[]
       
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level.append([platforms.GRASS_LEFT, x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level.append([platforms.GRASS_RIGHT, x_i[0]+i*70, x_i[2]])
                    else:
                        level.append([platforms.GRASS_MIDDLE, x_i[0]+i*70, x_i[2]])
                  
        
        x = [[0,17,-38] ]
        level_stone=[]
        
        for x_i in x:
            for i in range(0,x_i[1]):
                    if i==0:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0], x_i[2]])
                    elif i== x_i[1]-1:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
                    else:
                        level_stone.append([platforms.STONE_PLATFORM_FRAME , x_i[0]+i*70, x_i[2]])
        x = [[150, 3,const.SCREEN_HEIGHT - 300],[850-70, 5,const.SCREEN_HEIGHT - 300]]
        blocks=[]
        for x_i in x:
            for i in range(0,x_i[1]):
               
                 blocks.append([platforms.STONE_PLATFORM_FRAME , x_i[0], x_i[2] -i*70])

                    
        for platform in level:
            block = platforms.Platform(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_grass_list.add(block)
            
        for platform in level_stone:
            block = platforms.Platform_stone(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.platform_list.add(block)
            self.platform_stone_list.add(block)
        for platform in blocks:
            block = platforms.Block(platform[0])
            block.rect.x = platform[1]
            block.rect.y = platform[2]
            
            self.active_sprite.add(block)
            self.block_list.add(block)
            #self.platform_stone_list.add(block)
            
            
        
        level_enemy = [[120,const.SCREEN_HEIGHT - 250], [600,const.SCREEN_HEIGHT - 250],
                       [345,const.SCREEN_HEIGHT - 2*250-30], [900,const.SCREEN_HEIGHT - 2*250-30],
                      [320,const.SCREEN_HEIGHT - 3*250-30], [850,const.SCREEN_HEIGHT - 3*250-30]]
        for enemies in level_enemy:
            guy=enemy.Enemy(enemies[0],enemies[1], self, 1.5,self.init_difficulty)
            self.active_sprite.add(guy)
            self.enemy_list.add(guy)
            
 
 