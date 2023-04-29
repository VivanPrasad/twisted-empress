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
        self.title_font = pygame.font.Font('Assets/royal-intonation.ttf',48)
        self.font = pygame.font.Font('Assets/royal-intonation.ttf',32)
        self.running = True
        self.background_spritesheet = Spritesheet("Assets\map2.png")
        self.character_spritesheet = Spritesheet("Assets\player2.png")
        self.intro_background = pygame.image.load("Assets\map2.png")
        self.intro_background.set_alpha(25)
        
        self.level = 1
        self.area = 1
    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates() #Stores all wall sprites
        self.enemies = pygame.sprite.LayeredUpdates() #Stores all enemy sprites
        self.attacks = pygame.sprite.LayeredUpdates() #Stores all attack hitbox sprites

        self.background = Background(self,0,0) #0 plains | 1 desert | 2 forest | 3 castle
        self.player = Player(self, 1, 2, 0)
    
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
        intro = True

        title = self.title_font.render('Twisted Empress', True, BLACK)
        title_rect = title.get_rect(x=WIN_WIDTH/2-160,y=WIN_HEIGHT/2-170)
        play_button = Button(WIN_WIDTH/2-50,WIN_HEIGHT/2-50,100,50,WHITE,BLACK,'Play',32)
        
        version = self.font.render('v0.0.1', True, BLACK)
        version_rect = version.get_rect(x=WIN_WIDTH-90,y=WIN_HEIGHT-50)
        
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False
            if play_button.is_hovered(mouse_pos, mouse_pressed):
                play_button.content = "hi"
            else:
                play_button.content = "no"
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(version, version_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
g = Game()
g.intro_screen()
g.new()
while g.running == True:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()