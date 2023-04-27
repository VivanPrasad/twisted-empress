from config import *
import pygame, random
from math import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = PLAYER_LAYER #Bottom BG, Enemies, Attacks, UI
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = pygame.Surface([self.width,self.height])
        self.image.fill(RED)

        self.x_change = 0 #x_vel
        self.y_change = 0 #y_vel

        self.facing = "down"

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
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
        print(f"({self.x_change},{self.y_change})")
