import pygame
from sprites import *
from config import *
import sys

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT),pygame.RESIZABLE)
        self.title = pygame.display.set_caption("Twisted Empress")
        self.icon = pygame.display.set_icon(pygame.image.load("Assets\icon.png"))
        self.clock = pygame.time.Clock()
        self.running = True
        self.background_spritesheet = Spritesheet("Assets\map2.png")
        self.character_spritesheet = Spritesheet("Assets\player.png")
    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates() #Stores all wall sprites
        self.enemies = pygame.sprite.LayeredUpdates() #Stores all enemy sprites
        self.attacks = pygame.sprite.LayeredUpdates() #Stores all attack hitbox sprites

        self.background = Background(self,4,3) #0 plains | 1 desert | 2 forest | 3 castle
        self.player = Player(self, 1,2,1)
    
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