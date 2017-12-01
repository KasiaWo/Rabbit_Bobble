"""
This module is used to hold the Player class. The Player represents the user-
controlled sprite on the screen.
"""
import pygame
import numpy
 
import constants as const
import platforms 
from spritesheet_functions import SpriteSheet




class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """
 
    # -- Methods
    def __init__(self, game):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
        
        self.game = game
        self.which_character = self.game.which_character 
        
        self.load_images()
        
        self.image = self.standing_frames[0][self.which_character ]
        self.current_frame = 0
        self.last_update = 0
        self.rect = self.image.get_rect()
        
        
        self.radius = 35

 
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
 
        # List of sprites we can bump against
        self.level = None
        self.fall = False
      
        self.direction="R"
        self.life = 3
        
        self.diff = 0
        
        self.walking =  False
        self.jumping = False
        self.lost_life = False 

    def load_images(self):
        sprite_sheet = SpriteSheet("spritesheet_jumper.png")
        
        self.stand_01 = [sprite_sheet.get_image(614, 1063, 120, 191,const.BLACK,2, 2),
                         sprite_sheet.get_image(581, 1265, 120, 191,const.BLACK,2, 2)]
        self.stand_02 = [sprite_sheet.get_image(690, 406, 120, 201,const.BLACK,2, 2),
                         sprite_sheet.get_image(584, 0, 120, 201,const.BLACK,2, 2)]
        
        self.standing_frames = [self.stand_01,
                                self.stand_02]
        
        self.walk_r_01 = [sprite_sheet.get_image(678, 860, 120, 201,const.BLACK,2, 2),
                              sprite_sheet.get_image(584, 203, 120, 201,const.BLACK,2, 2)]

        self.walk_r_02 = [sprite_sheet.get_image(692, 1458, 120, 207,const.BLACK,2, 2),
                             sprite_sheet.get_image(678, 651, 120, 207,const.BLACK,2, 2)]
        
        self.walk_frames_r = [self.walk_r_01,
                              self.walk_r_02]
        
        self.walk_l_01 = []
        for frame in self.walk_r_01:
            frame.set_colorkey(const.BLACK)
            self.walk_l_01.append(pygame.transform.flip(frame, True, False))
            
        self.walk_l_02 = []
        for frame in self.walk_r_02:
            frame.set_colorkey(const.BLACK)
            self.walk_l_02.append(pygame.transform.flip(frame, True, False))
            
        self.walk_frames_l = [self.walk_l_01,
                              self.walk_l_02]
            
        self.jump_frame = [sprite_sheet.get_image(382, 763, 150, 181,const.BLACK,2, 2),
                           sprite_sheet.get_image(416, 1660, 150, 181,const.BLACK,2, 2)]
                           
        
        
    def animate(self):
        now = pygame.time.get_ticks()
        if self.change_x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 200:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.change_x > 0:
                    self.image = self.walk_frames_r[self.current_frame][self.which_character ]
                else:
                    self.image = self.walk_frames_l[self.current_frame][self.which_character ]
                
                self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame][self.which_character ]

                self.rect.bottom = bottom
        if self.jumping:
            bottom = self.rect.bottom
            self.image = self.jump_frame[self.which_character ]
            self.rect.bottom = bottom
        self.mask = pygame.mask.from_surface(self.image)    

    
 
    def update(self):
        """ Move the player. """
        if pygame.time.get_ticks() - self.level.start_time > const.LEVEL_WAITING:
            self.calc_grav()
            self.animate()
   
            # If the player gets near the right side, shift the world left (-x)
            if self.rect.right > const.SCREEN_WIDTH:
                self.rect.right = const.SCREEN_WIDTH

            # If the player gets near the left side, shift the world right (+x)
            if self.rect.left < 0:
                self.rect.left = 0

            # Move left/right
            self.rect.x += self.change_x

                # Move up/down
            self.rect.y += self.change_y


                # check if player hit  stone platform 
            self.transform = 10  

            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_stone_list, False)
            self.rect.x = self.rect.x + numpy.sign(self.change_x) * self.transform
            block_hit_list2 = pygame.sprite.spritecollide(self, self.level.platform_stone_list, False)
            self.rect.x = self.rect.x - numpy.sign(self.change_x) * self.transform
            
            
            for block in block_hit_list:
                if self.rect.bottom >= block.rect.top +10:
                    if self.change_x > 0 :
                       
                        if  len(block_hit_list2)>=1 :
                            
                            self.rect.right = block.rect.left
                            
                    elif self.change_x < 0 and  len(block_hit_list2)>=1:
                            # Otherwise if we are moving left, do the opposite.
                        self.rect.left = block.rect.right

                        
                if self.change_y > 0 :

                    if len(block_hit_list2)==1:
                        if block.rect.left >= self.rect.right - self.transform or block.rect.right <= self.rect.left + self.transform:

                            if self.change_y==0:
                                    self.change_y=2

                        else:
                            self.rect.bottom = block.rect.top
                            self.change_y = 0
                            self.jumping = False
                    else:
                        self.rect.bottom = block.rect.top
                        self.change_y = 0
                        self.jumping = False

                elif self.change_y < 0:
                    self.rect.top = block.rect.bottom + 2

                    self.change_y = 0

                # Check and see if we hit grass platform
                
                
            block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_grass_list, False)
            self.rect.x = self.rect.x + numpy.sign(self.change_x) * self.transform
            block_hit_list2 = pygame.sprite.spritecollide(self, self.level.platform_grass_list, False)
            self.rect.x = self.rect.x - numpy.sign(self.change_x) * self.transform
            
            for block in block_hit_list:
                if self.change_y > 0 :
                            #self.fall = True



                    if len(block_hit_list2)==1:
                        if block.rect.left >= self.rect.right - self.transform or block.rect.right <= self.rect.left + self.transform:

                            if self.change_y==0:
                                    self.change_y=2

                        elif  self.rect.bottom <=  block.rect.top + 30 :
                            
                            self.rect.bottom = block.rect.top
                            self.change_y = 0
                            self.jumping = False
                    elif  self.rect.bottom <=  block.rect.top + 30 :
                        
                        self.rect.bottom = block.rect.top
                        self.change_y = 0
                        self.jumping = False

        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0 :
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
      
 
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
                self.jumping=False
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0



            # Check we hit enemy

        enemy_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_list, False, pygame.sprite.collide_circle)

        for enemy in enemy_hit_list:
            if pygame.sprite.collide_mask(self, enemy) != None and self.lost_life==False:
                #if (enemy.rect.top <= self.rect.bottom + 180 or enemy.rect.left <= self.rect.right - 40) and self.lost_life==False:
                    
                self.life -= 1
                self.lost_life = True
                ghost = Player_lost(self)
                self.level.active_sprite.add(ghost)
                self.rect.x = 300
                self.rect.y = const.SCREEN_HEIGHT-200
                    


        enemy_bub_hit_list = pygame.sprite.spritecollide(self, self.level.enemy_bubble_list, False, pygame.sprite.collide_circle)

        for enemy in enemy_bub_hit_list:

            if enemy.rect.top <= self.rect.bottom + 180 or enemy.rect.left <= self.rect.right - 40:

                    prize = Prize(enemy, self)
                    self.level.active_sprite.remove(enemy)
                    self.level.enemy_bubble_list.remove(enemy)
                    #self.level.active_sprite.add(prize)
                    self.level.fruit_list.add(prize)
                    #self.level.active_sprite.remove(self)
        fruit_hit_list = pygame.sprite.spritecollide(self, self.level.fruit_list, False, pygame.sprite.collide_circle)

        for fruit in fruit_hit_list:
            if fruit.change_y ==0:
                self.level.active_sprite.remove(fruit)
                self.level.fruit_list.remove(fruit)
                self.game.score += 100
                prize_song=pygame.mixer.Sound( 'collectcoin.wav')
        
                prize_song.play()
        bullet_carrot_hit_list = pygame.sprite.spritecollide(self, self.level.bullet_carrot_list, False, pygame.sprite.collide_circle)    
        for bubble in bullet_carrot_hit_list:
            carrot = Carrot(bubble, self)
            self.level.active_sprite.remove(bubble)
            self.level.bullet_carrot_list.remove(bubble)
                   
            self.level.carrot_list.add(carrot)
        carrot_hit_list = pygame.sprite.spritecollide(self, self.level.carrot_list, False)
        for fruit in carrot_hit_list:
            if fruit.change_y ==0:
                self.level.active_sprite.remove(fruit)
                self.level.carrot_list.remove(fruit)
                self.game.score += 20
             
        if self.life==0: 
            self.kill()

          
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:    
            self.change_y += const.PLAYER_GRAV
 
        # See if we are on the ground.
        if self.rect.y >= const.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = const.SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
  
        if pygame.time.get_ticks() - self.level.start_time > const.LEVEL_WAITING:
            self.jumping = True

            self.rect.y += 2
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
            self.rect.y -= 2

                # If it is ok to jump, set our speed upwards
            if  (self.change_y ==0 or self.change_y ==1) and (len(platform_hit_list) > 0 or self.rect.bottom >= const.SCREEN_HEIGHT):
                self.change_y = const.PLAYER_JUMP_SPEED
                self.jumping = True
                song=pygame.mixer.Sound( 'jump.wav')
                song.play()
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        if pygame.time.get_ticks() - self.level.start_time > const.LEVEL_WAITING:
            self.change_x = -const.PLAYER_SPEED_X
            self.direction="L"
           

        
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        if pygame.time.get_ticks() - self.level.start_time > const.LEVEL_WAITING:
            self.change_x = const.PLAYER_SPEED_X
            self.direction="R"
            
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
        
        
        
class Player_lost(pygame.sprite.Sprite):
    
    def __init__(self, player):
        # Call the parent's constructor
        super().__init__()
        
        self.frames = sprite_sheet = SpriteSheet("spritesheet_jumper.png")
        
        self.dead_image = [sprite_sheet.get_image(382, 946, 150, 174,const.BLACK,2, 2),
                         sprite_sheet.get_image(411, 1866, 150, 174,const.BLACK,2, 2)]
        self.image = self.dead_image[player.which_character]
        self.image.set_alpha(90)
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.change_y = 5
        self.level = player.level
        self.player = player
    
    def update(self):
        
        self.rect.y += self.change_y
        if self.rect.top > const.SCREEN_HEIGHT:
            self.level.active_sprite.remove(self)
            self.player.lost_life = False

        
        
class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        
        self.radius = 20
        
        # Grab the image for this platform
        image_2 = pygame.image.load("bubble2.png").convert()
        image = pygame.Surface([300, 300]).convert()
        #image.set_alpha(40)
 
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(image_2, (0, 0), (0, 0, 300, 300))
 
        # Assuming black works as the transparent color
        image.set_colorkey(const.BLACK)
        self.image_left = image

         # scale image
        self.size = self.image_left.get_size()
        self.smaller_left = pygame.transform.scale(self.image_left, (int(self.size[0]*0.13), int(self.size[1]*0.13)))
       
        self.image = self.smaller_left
        
        self.rect = self.image.get_rect()
        
        
        self.start_time = pygame.time.get_ticks()
        self.time = self.start_time
        
        if player.direction == "R":
            self.sign = 1   
        else:
            self.sign = -1
            
        self.rect.x = player.rect.x + self.sign * player.rect.width/2 
        self.rect.y = player.rect.bottom  - 50
        self.change_x = 6
        self.acc_x = 0
        
        
        self.level = player.level
        self.change_y = 0
        
        self.poziom = True
        self.carrot = False
          
                                
    def update(self ):
        # update time life
        
        self.time += 1
        if self.change_x>0 :
            self.change_x  -=  self.acc_x
            
        if self.time - self.start_time > const.BUBBLE_START and self.poziom:
            self.change_y = -2
            self.change_x = 0
            
            image_2 = pygame.image.load("bubble.png").convert()
            image = pygame.Surface([220, 220]).convert()
            image.set_alpha(40)

            # Copy the sprite from the large sheet onto the smaller image
            image.blit(image_2, (0, 0), (0, 0, 220, 220))

            # Assuming black works as the transparent color
            image.set_colorkey(const.BLACK)
            self.image_left = image



             # scale image
            self.size = self.image_left.get_size()
            self.smaller_left = pygame.transform.scale(self.image_left, (int(self.size[0]*0.2), int(self.size[1]*0.2)))
            #self.smaller_left = pygame.transform.rotate(self.smaller_left, 90) 


            self.image = self.smaller_left

            self.poziom = False
            self.level.bullet_list.remove(self)
        if self.time - self.start_time < const.BUBBLE_START :   
            song2=pygame.mixer.Sound( 'bubble4.wav')
            song2.play()
        
        
        if self.time - self.start_time == const.BUBBLE_CARROT :   
            self.carrot = True
            self.level.bullet_carrot_list.add(self)
            
        # gravity - stone platform
        self.rect.x = self.rect.x + self.sign * self.change_x 
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_stone_list, False)
        for block in block_hit_list :
                # If we are moving right,
                # set our right side to the left side of the item we hit
            if self.change_x > 0 and self.poziom == False:
                self.rect.right = block.rect.left
                self.sign= - self.sign
            elif self.change_x < 0 and self.poziom == False:
                    # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
                self.sign= - self.sign


        self.rect.y += self.change_y 
            # check if player hit  stone platform 
        self.transform = 30    

        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_stone_list, False)

        for block in  block_hit_list :
            
                # Reset our position based on the top/bottom of the object.
            if self.change_y > 0 and self.rect.bottom >= block.rect.top and self.rect.top <= block.rect.top:
                 self.rect.bottom = block.rect.top -2
                 self.change_y = - self.change_y

            elif self.change_y < 0 and self.rect.top <= block.rect.bottom and self.rect.bottom >= block.rect.bottom:
                self.rect.top = block.rect.bottom +2
                if self.rect.y < 300:
                    self.change_y = 0
                else:    
                    self.change_y = - self.change_y

        if self.time - self.start_time == 500:   
            song2=pygame.mixer.Sound( 'bubble4.wav')
            song2.play() 
            self.level.active_sprite.remove(self)
 




        
        
class Life(pygame.sprite.Sprite):
    def __init__(self, player, screen):
        super().__init__()
        self.screen = screen
        img_life = SpriteSheet("life.png")
        self.image = img_life.get_image(42,
                                                54,
                                                119,
                                                102, const.BLACK, 4, 4)
        
        self.rect = self.image.get_rect()
        self.rect.x = const.SCREEN_WIDTH / 4 + 10
        self.rect.y =10
        self.ile = 0
        self.font_name = pygame.font.match_font(const.FONT_NAME)
        
        
    def update(self,player):
        
        self.ile = player.life
        
     
 

class Prize(pygame.sprite.Sprite):
    def __init__(self, enemy, player):
        super().__init__()
        
        img_life = SpriteSheet("coin_gold.png")
        self.image = img_life.get_image(0,
                                               0,
                                                60,
                                                60, const.BLACK)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_size()[0]*0.7), int(self.image.get_size()[1] *0.7)))
        
        self.rect = self.image.get_rect()
        
        self.rect.x = enemy.rect.x
        self.rect.y = enemy.rect.y - 30
        self.font_name = pygame.font.match_font(const.FONT_NAME)
        self.radius = 21
        self.level= enemy.level
        self.change_y = -3
        self.acc_y = 0.5
        self.change_x = 2 * numpy.sign(player.change_x)
        self.level.active_sprite.add(self)
        pygame.draw.circle(self.image, const.RED, self.rect.center , self.radius)
        
         
    def update(self):
        if self.change_y>0:
            
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        
            for platform in platform_hit_list:
                if platform.rect.top <= self.rect.bottom + 20 and platform.rect.top >= self.rect.top :
                    
                    self.change_y = 0
                    self.change_x = 0
                    self.acc_y=0
                    self.rect.bottom = platform.rect.top -20
        #print('szybkosc monety', self.change_y)
        self.change_y += self.acc_y
        self.rect.y +=  self.change_y
        self.rect.x +=  self.change_x
        #print('polozenie monety', self.rect.y)
 
       
class Carrot(pygame.sprite.Sprite):
    def __init__(self, bubble, player):
        super().__init__()
        
        sprite_sheet = SpriteSheet("spritesheet_jumper.png")
        self.image = sprite_sheet.get_image(812,
                                               554,
                                                54,
                                                49, const.BLACK)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_size()[0]*0.7), int(self.image.get_size()[1] *0.7)))
        
        self.rect = self.image.get_rect()
        
        self.rect.x = bubble.rect.x
        self.rect.y = bubble.rect.y -50
        self.font_name = pygame.font.match_font(const.FONT_NAME)
        self.radius = 21
        self.level= bubble.level
        self.change_y = -3
        self.acc_y = 0.5
        self.change_x = 3 * numpy.sign(player.change_x)
        self.level.active_sprite.add(self)
        
        
         
    def update(self):
        if self.change_y>0:
            
            platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        
            for platform in platform_hit_list:
                if platform.rect.top <= self.rect.bottom + 20 and platform.rect.top >= self.rect.top :
                    
                    self.change_y = 0
                    self.change_x = 0
                    self.acc_y=0
                    self.rect.bottom = platform.rect.top -20
        #print('szybkosc monety', self.change_y)
        self.change_y += self.acc_y
        self.rect.y +=  self.change_y
        self.rect.x +=  self.change_x
        #print('polozenie monety', self.rect.y)
                     
        
