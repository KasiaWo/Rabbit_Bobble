#!usr/bin/env python3


import pygame
import numpy

import random
from os import path
 
    
import constants as const
from spritesheet_functions import SpriteSheet
import platforms
from player import Player
from player import Bullet
from player import Life
import enemy
import levels
from levels import Level 
from levels import Level_01 
from levels import Level_02 
from levels import Level_03 
from menu import Menu 


 




class Game:
    def __init__(self):
        # initialize game window

        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((const.SCREEN_WIDTH, const.SCREEN_HEIGHT))
        pygame.display.set_caption(const.TITLE)
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.settings = False
       
        self.font_name = pygame.font.match_font(const.FONT_NAME2)
       
        self.load_data()
        
        self.level_list=[]
        self.current_level_no = None
        self.current_level = None
        
        self.init_player_life = 3
        self.which_character = 0
        self.init_difficulty =0
        
        self.game_paused = False
        self.menu_open = False
        

    def load_data(self):
        # load high score
   
        with open( const.HS_FILE) as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

        

    def new(self):
        if self.running:
            start=pygame.time.get_ticks() 
            self.score = 0
            self.player = Player(self)

            self.player.life = self.init_player_life
            self.life = Life(self.screen, self.player) 
            self.level_list = []

            self.level_list.append( Level_01(self.screen, self.player, self.init_difficulty) )
            self.level_list.append( Level_02(self.screen, self.player,self.init_difficulty) )
            self.level_list.append( Level_03(self.screen, self.player, self.init_difficulty) )
            self.level_list.append( levels.Level_04(self.screen, self.player, self.init_difficulty) )
            self.level_list.append( levels.Level_05(self.screen, self.player, self.init_difficulty) )
            self.level_list.append( levels.Level_06(self.screen, self.player, self.init_difficulty) )
            self.level_list.append( levels.Level_07(self.screen, self.player, self.init_difficulty) )
            self.level_list.append( levels.Level_08(self.screen, self.player, self.init_difficulty) )
            self.level_list.append( levels.Level_09(self.screen, self.player, self.init_difficulty) )

            self.current_level_no = 0


            self.current_level = self.level_list[self.current_level_no]    
            self.current_level.start_time = pygame.time.get_ticks() 
            self.player.level = self.level_list[self.current_level_no]

            self.player.rect.x = 300
            self.player.rect.y = const.SCREEN_HEIGHT-300

            self.sound1=pygame.mixer.Sound( 'Green_Hills.wav')
            self.sound1.play(-1)
            self.game_win = False
            stop = pygame.time.get_ticks() 

            self.run()

    def run(self):
        # Game Loop

        self.playing = True
        while self.playing:
            self.clock.tick(const.FPS)
            self.events()
            self.update()
            self.draw()
        pygame.mixer.music.fadeout(300)

    def update(self):
        # Game Loop - Update

      
        if self.player.life >0 and self.current_level_no < len(self.level_list) and self.game_paused == False:
            
            self.player.update()
            self.current_level.update()
            self.life.update( self.player)
            if self.current_level.close :
                if self.current_level_no +1 < len(self.level_list):
                    self.current_level_no += 1
                    self.current_level = self.level_list[self.current_level_no]    
                    self.current_level.start_time = pygame.time.get_ticks() 
                    self.player.level = self.current_level

                    self.player.rect.x = 300
                    self.player.rect.y = const.SCREEN_HEIGHT-300
                else:
                    self.playing = False
                    self.game_win = True
        if self.player.life == 0:
            self.playing = False
            
        
        
        
        self.screen.blit(self.life.image, [50,80])
        

    def events(self):
        # Game Loop - events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.go_left()
                if event.key == pygame.K_RIGHT:
                    self.player.go_right()
                if event.key == pygame.K_UP:
                    self.player.jump()
                if event.key == pygame.K_SPACE:
                    if pygame.time.get_ticks() - self.current_level.start_time > const.LEVEL_WAITING and self.player.lost_life == False:
                        bullet = Bullet(self.player)
                        self.current_level.bullet_list.add(bullet)
                        self.current_level.active_sprite.add(bullet)
                if event.key == pygame.K_p and self.game_paused == False:
                    self.game_paused = True
                    
                elif event.key == pygame.K_p and self.game_paused == True:
                    self.game_paused = False
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.player.change_x < 0:
                    self.player.stop()
                if event.key == pygame.K_RIGHT and self.player.change_x > 0:
                    self.player.stop()

    def draw(self):
        # Game Loop - draw
        if self.game_paused == False:
            self.screen.fill(const.BGCOLOR)
            self.current_level.draw()
           

            self.draw_text(str(self.score), 30, const.BLACK, const.SCREEN_WIDTH / 2, 3)
            self.draw_text(str(self.life.ile), 26, const.BLACK, const.SCREEN_WIDTH / 4, 3)
            self.screen.blit(self.life.image, self.life.rect)
            
            pygame.display.flip()
        else:
            self.screen.fill(const.BGCOLOR)
            self.draw_text("Paused", 60, const.WHITE, const.SCREEN_WIDTH / 2, 500)
            pygame.display.flip()

    def show_start_screen(self):
        # game splash/start screen

        self.screen.fill(const.BGCOLOR)
        self.draw_text(const.TITLE, 80, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 4)
        self.draw_text("Arrows to move, Space to throw bubble, P to pause", 30, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2)
        self.draw_text("Press a h to settings", 30, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT * 3 / 4 - 20)
        self.draw_text("Press a space key to play", 30, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT * 3 / 4 + 50 )
        self.draw_text("High Score: " + str(self.highscore), 20, const.WHITE, const.SCREEN_WIDTH / 2, 15)
        pygame.display.flip()
        self.wait_for_key()
        
        

        

    def show_go_screen(self):
        # game over/continue
        if not  self.running:
            return
        
        self.sound1.stop()
        self.screen.fill(const.BGCOLOR)
        self.draw_text("GAME OVER", 80, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 30, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2)
        self.draw_text("Press a key to play again", 30, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 60, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2 + 40)
            with open( const.HS_FILE,'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 30, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2 + 40)
        pygame.display.flip()
        self.wait_for_key()
        
        
    def show_win_screen(self):
        # game over/continue
        if not  self.game_win :
            return

        self.screen.fill(const.BGCOLOR)
        self.draw_text("YOU WIN !!!", 100, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 30, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2)
        self.draw_text("Press a key to play again", 30, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 80, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2 + 40)
            with open( const.HS_FILE,'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 30, const.WHITE, const.SCREEN_WIDTH / 2, const.SCREEN_HEIGHT / 2 + 40)
        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(const.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                    self.settings = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
                    waiting = False
                    self.running = True
                    self.settings = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False
                    self.settings = False
                    self.running = True
                    
    def close_menu(self):
        self.menu_open = True
        menu_tile=Menu(self.screen,self)
        while self.menu_open:
            
            self.clock.tick(const.FPS)
            menu_tile.run()
 
            self.init_player_life =menu_tile.player_life[ menu_tile.which_image[1] ]
            self.init_difficulty =menu_tile.difficult_level[ menu_tile.which_image[2] ]   
            if self.init_difficulty =='EASY':
                self.init_difficulty =0
            else:
                self.init_difficulty =1

    def draw_text(self, text, size, color, x, y):

        font = pygame.font.SysFont(const.FONT_NAME2, size, True, False)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.settings:
    g.close_menu()
while g.running:
    g.show_start_screen()
    while g.settings:
        g.close_menu()
    g.new()
    g.show_win_screen()
    g.show_go_screen()

pygame.quit()



 