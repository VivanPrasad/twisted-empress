import pygame
from sprites import *
from config import *
import sys

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.background_tilemap = pygame.image.load("Assets/map.png").convert()
    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates() #Stores all wall sprites
        self.enemies = pygame.sprite.LayeredUpdates() #Stores all enemy sprites
        self.attacks = pygame.sprite.LayeredUpdates() #Stores all attack hitbox sprites

        self.player = Player(self, 1,2)
    
    def events(self):
        #game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
    def update(self):
        self.all_sprites.update()

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()
    def main(self):
        #game loop
        while self.playing == True:
            self.events()
            self.update()
            self.draw()
        self.running = False
    def game_over(self):
        pass
    def intro_screen(self):
        pass

g = Game()
g.intro_screen()
g.new()
while g.running == True:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()