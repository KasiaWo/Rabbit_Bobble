"""
Module for managing enemies.
"""
import random
import constants as const
import pygame
import random
import platforms 
 
from spritesheet_functions import SpriteSheet



class Enemy(pygame.sprite.Sprite):
    # -- Methods
    def __init__(self, x_cord, y_cord,level, x_speed=2, char_type=0):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        
        self.direction="R"
        self.load_images()
        
        self.image = self.standing_frames[0]
        self.current_frame = 0
        self.last_update = 0
        self.rect = self.image.get_rect()
        self.radius= 20
        
        self.walking =  False
        self.jumping = False
       
        self.type = char_type
        
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        
        self.radius = 35
        #
        
        self.rect.x = x_cord
        self.rect.y = y_cord
        
        
        self.change_x = x_speed
        self.change_y = 0
        
        self.sign_direc = 1
 
        # List of sprites we can bump against
        self.level = level
        self.platforms = level.platform_list
        
    def load_images(self):
        sprite_sheet = SpriteSheet("spritesheet_players.png")
        self.standing_frames = [sprite_sheet.get_image(156, 101, 45,54,const.WHITE)]
        for frame in self.standing_frames:
            frame.set_colorkey(const.BLACK)
        self.walk_frames_r = [sprite_sheet.get_image(156, 156, 45,54,const.BLACK),
                              sprite_sheet.get_image(115, 48, 45, 52,const.BLACK),
                              sprite_sheet.get_image(156, 101, 45, 54,const.BLACK)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(const.BLACK)
            self.walk_frames_l.append(pygame.transform.flip(frame, True, False))
        self.jump_frame = sprite_sheet.get_image(156, 101, 45, 54,const.BLACK)
        self.jump_frame.set_colorkey(const.BLACK)
        
    def animate(self):
        now = pygame.time.get_ticks()
        if self.change_x != 0:
            self.walking = True
        else:
            self.walking = False
        # show walk animation
        if self.walking:
            if now - self.last_update > 400:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                #bottom = self.rect.bottom
                if self.sign_direc > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                
                #self.rect.bottom = bottom
        # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                #bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                #self.rect = self.image.get_rect()
                #self.rect.bottom = bottom
        self.mask = pygame.mask.from_surface(self.image)    
        # Set a referance to the image rect.
        #self.rect = self.image.get_rect()
    
            
    def update(self):
        self.animate()
        self.calc_grav()
        # If the player gets near the right side, shift the world left (-x)
        if self.rect.right > const.SCREEN_WIDTH:
            self.rect.right = const.SCREEN_WIDTH
            self.sign_direc = -self.sign_direc
 
        # If the player gets near the left side, shift the world right (+x)
        if self.rect.left < 0:
            self.rect.left = 0
            self.sign_direc = -self.sign_direc
            
         # If the player gets near the right side, shift the world left (-x)
        if self.rect.bottom > const.SCREEN_HEIGHT:
            self.rect.bottom = const.SCREEN_HEIGHT
 
        # If the player gets near the left side, shift the world right (+x)
        if self.rect.top < 0:
            
            self.rect.top = 0    
           
        self.rect.x += self.sign_direc * self.change_x
        
        
            

        
        
        # Check where is the enemy  
       
            # Check if enemy is on the platform  
        platform_hit_list = pygame.sprite.spritecollide(self, self.platforms, False)
        self.rect.x += self.sign_direc * 1
            # Check if there if another platform next to
        platform_hit_list_2 = pygame.sprite.spritecollide(self, self.platforms, False)
        
            
        self.rect.y -= 2 
        self.rect.x -= self.sign_direc * 1
        
        # if enemy is only on one platform we have to check if there is on an edge
        if platform_hit_list == platform_hit_list_2 and len(platform_hit_list)==1:
            for block in platform_hit_list:
                if self.sign_direc > 0:
                    
                    if self.rect.right  >=  block.rect.right  :

                        self.sign_direc = -self.sign_direc
                        #self.image = self.smaller_left
                elif self.sign_direc < 0:

                     if self.rect.left  <=  block.rect.left  :

                        self.sign_direc = -self.sign_direc
                        #self.image=self.smaller_right
                       
                    
                    #self.rect.top = block.rect.bottom

                else:
                     self.sign_direc=self.sign_direc
        for block in platform_hit_list:
                        
                if self.change_y > 0 and self.rect.bottom >= block.rect.top and self.rect.top <= block.rect.top:
                    
                    self.rect.bottom = block.rect.top
                    self.change_y = 0
        if self.type and random.uniform(0,1)<0.1 and len(platform_hit_list)>0:
            self.change_y = -3
            
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_stone_list, False)
       
        for block in  block_hit_list :
            
                # Reset our position based on the top/bottom of the object.
          

            if self.change_y < 0 and self.rect.top <= block.rect.bottom and self.rect.bottom >= block.rect.bottom:
                
                self.rect.top = block.rect.bottom +2
                self.change_y = -self.change_y
    
        block_hit_list = pygame.sprite.spritecollide(self, self.level.block_list, False)
        if len(block_hit_list)>=1:
            if len(block_hit_list)>=1:
                block= block_hit_list[0]

                if self.sign_direc > 0:
                    self.rect.right = block.rect.left
                    self.sign_direc = -self.sign_direc
                elif self.sign_direc < 0:
                    
                    # Otherwise if we are moving left, do the opposite.
                    self.rect.left = block.rect.right
                    self.sign_direc = -self.sign_direc
        self.rect.y += self.change_y
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:    
            self.change_y += .15
 
        # See if we are on the ground.
        if self.rect.y >= const.SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = const.SCREEN_HEIGHT - self.rect.height
    
class Enemy_bubble(pygame.sprite.Sprite):
    # -- Methods
    def __init__(self, enemy):
        """ Constructor function """
 
        # Call the parent's constructor
        super().__init__()
 
        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        
        self.direction= enemy.direction
        sprite_sheet_left = SpriteSheet("playerBlue_dead.png")
        # Grab the image for this platform
        self.image_left = sprite_sheet_left.get_image(0,
                                            0,
                                            45,
                                            47, const.BLACK)
 
        # Set a referance to the image rect.
        
        self.size = self.image_left.get_size()
        self.smaller_left = pygame.transform.scale(self.image_left, (int(self.size[0]*0.7), int(self.size[1]*0.7)))
        
        self.type=enemy.type
        self.x_speed=enemy.change_x
        
        bub_2 = pygame.image.load("bubble.png").convert()
        bub = pygame.Surface([225, 225]).convert()
        #bub_2.set_alpha(90)
 
        # Copy the sprite from the large sheet onto the smaller image
        bub.blit(bub_2, (0, 0))
        
        bub=pygame.transform.scale(bub, (int(bub.get_size()[0]*0.2), int(bub.get_size()[1]*0.2)))
 
        # Assuming black works as the transparent color
        bub.set_colorkey(const.BLACK)
        bub.set_alpha(150)
        pygame.Surface.blit(bub,self.smaller_left, (6, 4))
        
        #self.smaller_right.blit(bub,(-100,-100))
        bub.set_colorkey(const.BLACK)
        #bub.set_alpha(90)
        
        self.image = bub
        #self.image.set_alpha(90)
        
        
        # Set a referance to the image rect.
        self.rect = self.image.get_rect()
        
        self.radius = 35
        #pygame.draw.circle(self.image, RED, self.rect.center , self.radius)
        
        self.start_time = pygame.time.get_ticks()
        self.time = self.start_time
        
        self.rect.x = enemy.rect.x
        self.rect.y = enemy.rect.y
        self.platforms = enemy.platforms
        self.change_y  = -3
        self.level = enemy.level
        
    def update(self):
        
        # If the player gets near the right side, shift the world left (-x)
        if self.rect.right > const.SCREEN_WIDTH:
            self.rect.right = const.SCREEN_WIDTH
            self.speedy=-self.speedy
 
        # If the player gets near the left side, shift the world right (+x)
        if self.rect.left < 0:
            self.rect.left = 0
            # If the player gets near the right side, shift the world left (-x)
        if self.rect.bottom > const.SCREEN_HEIGHT:
            self.rect.bottom = const.SCREEN_HEIGHT
 
        # If the player gets near the left side, shift the world right (+x)
        if self.rect.top < 0:
            self.rect.top = 0   
           
        # life time
        self.time += 1
    
        
         
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_stone_list, False)

        for block in  block_hit_list :
            
            if self.change_y > 0 and self.rect.bottom >= block.rect.top and self.rect.top <= block.rect.top:
                 self.rect.bottom = block.rect.top -2
                 self.change_y = 0

            elif self.change_y < 0 and self.rect.top <= block.rect.bottom and self.rect.bottom >= block.rect.bottom:
                self.rect.top = block.rect.bottom +2
                self.change_y = 0
        
        
 
        self.rect.y += self.change_y 
        
        if  self.time - self.start_time > 500:
            enemy=Enemy(self.rect.x, self.rect.y, self.level,self.x_speed,self.type)
            self.level.enemy_list.add(enemy)
            self.level.active_sprite.add(enemy)
            self.level.active_sprite.remove(self)
            self.kill()
            
    
        
 