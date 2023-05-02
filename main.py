import pygame
from sprites import *
from config import *
import sys

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT),pygame.RESIZABLE)
        self.title = pygame.display.set_caption("Twisted Empress")
        self.icon = pygame.display.set_icon(pygame.image.load("Assets/icon.png"))
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font('Assets/Font/royal-intonation.ttf',48)
        self.font = pygame.font.Font('Assets/Font/royal-intonation.ttf',32)
        self.running = True
        
        self.background_spritesheet = Spritesheet("Assets/map.png")
        self.character_spritesheet = Spritesheet("Assets/Entities/player.png")
        self.attack_spritesheet = Spritesheet("Assets/Objects/attacks.png")
        self.weapon_spritesheet = Spritesheet("Assets/Objects/weapons.png")
        self.profile_spritesheet = Spritesheet("Assets/UI/profile.png")
        #self.health_spritesheet = Spritesheet("Assets\UI\hp.png")
        
        self.intro_background = pygame.image.load("Assets/map.png").convert()
        self.intro_background.set_alpha(100)

        self.level = 1
        self.area = 1

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.LayeredUpdates() #Stores all wall sprites
        self.enemies = pygame.sprite.LayeredUpdates() #Stores all enemy sprites
        self.attacks = pygame.sprite.LayeredUpdates() #Stores all attack hitbox sprites

        self.background = Background(self,self.level-1,self.area-1) #0 plains | 1 desert | 2 forest | 3 castle
        self.player = Player(self, 7, 7, 1)
    def events(self):
        #game loop events

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.basic = BasicAttack(self, self.player.x+32,self.player.y, mouse_pos)
                else:
                    self.special = SpecialAttack(self, self.player.x+32,self.player.y, mouse_pos)
    def update(self):
        self.all_sprites.update()
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)

        self.screen.blit(self.player.weapon_copy,(self.player.x+32,self.player.y))
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

    def fade(self,width, height): 
        fade = pygame.Surface((width, height))
        fade.fill((0,0,0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            self.playing = False
            self.screen.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(1)
            self.playing = True
    def next_level(self):
        if self.level == 5:
            if self.area < 4:
                self.area += 1
            else:
                self.area = 1
        
        if self.level < 5:
            self.level += 1
        else:
            self.level = 1
        self.background.kill()
        self.background = Background(self,self.level-1,self.area-1)
        self.fade(WIN_WIDTH,WIN_HEIGHT)
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
                play_button.image.set_alpha(255)
            else:
                play_button.image.set_alpha(255/2)
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