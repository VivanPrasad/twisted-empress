from config import *
import pygame, random
from math import *

class Spritesheet:
    def __init__(self, file) -> None:
        self.sheet = pygame.image.load(file).convert_alpha()
    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface([width,height])
        sprite.blit(self.sheet, (0,0), (x,y,width,height))
        sprite.set_colorkey(BLACK)
        return sprite
class Background(pygame.sprite.Sprite):
    def __init__(self,game, x, y):
        self.game = game
        self._layer = 1
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = 0
        self.y = 0
        self.width = 128*6
        self.height = 128*6
        self.image = self.game.background_spritesheet.get_sprite(x*self.width,y*self.width,self.width,self.height)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y, power = 0):
        self.game = game
        self.power = power
        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.character_spritesheet.get_sprite(1,1,self.width,self.height)

        self.x_change = 0 #x_vel
        self.y_change = 0 #y_vel

        self.facing = "down"

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        self.animate()
        self.movement()
        self.rect.x += self.x_change
        self.rect.y += self.y_change

        self.x_change = 0
        self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.x_change = (PLAYER_SPEED) if self.y_change == 0 else (cos(radians(45)) * PLAYER_SPEED)
            self.facing = 'left'
        if keys[pygame.K_d]:
            self.x_change = (PLAYER_SPEED) if self.y_change == 0 else (cos(radians(45)) * PLAYER_SPEED)
            self.facing = 'right'
        
        if keys[pygame.K_w]:
            self.y_change -= (PLAYER_SPEED) if self.x_change == 0 else (cos(radians(45)) * PLAYER_SPEED)
            self.facing = 'up'
        if keys[pygame.K_s]:
            self.y_change += (PLAYER_SPEED) if self.x_change == 0 else (cos(radians(45)) * PLAYER_SPEED)
            self.facing = 'down'
        
        self.x_change = 0

        if keys[pygame.K_a]:
            self.x_change -= (PLAYER_SPEED) if self.y_change == 0 else (cos(radians(45)) * PLAYER_SPEED)
            self.facing = 'left'
        if keys[pygame.K_d]:
            self.x_change += (PLAYER_SPEED) if self.y_change == 0 else (cos(radians(45)) * PLAYER_SPEED)
            self.facing = 'right'
        #print(f"({self.x_change},{self.y_change})")
    
    def animate(self):
        down = self.game.character_spritesheet.get_sprite(0,self.power*48, self.width, self.height)
        left = self.game.character_spritesheet.get_sprite(48,(self.power)*48, self.width, self.height)
        right = self.game.character_spritesheet.get_sprite(48*2,self.power*48, self.width, self.height)
        up = self.game.character_spritesheet.get_sprite(48*3,self.power*48, self.width, self.height)

        if self.facing == "down":
            self.image = down
        if self.facing == "up":
            self.image = up
        if self.facing == "left":
            self.image = left
        if self.facing == "right":
            self.image = right