import pygame
from sprites import *
from config import *
import sys

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) #Displays the screen size properly
        self.title = pygame.display.set_caption("Twisted Empress")
        self.icon = pygame.display.set_icon(pygame.image.load("Assets/icon.png"))
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font('Assets/Font/royal-intonation.ttf',48)
        self.font = pygame.font.Font('Assets/Font/royal-intonation.ttf',32)
        self.running = True
        
        self.background_spritesheet = Spritesheet("Assets/map.png")
        self.character_spritesheet = Spritesheet("Assets/Entities/player.png")
        self.enemy_spritesheet = Spritesheet("Assets/Entities/enemies.png")
        self.attack_spritesheet = Spritesheet("Assets/Objects/attacks.png")
        self.weapon_spritesheet = Spritesheet("Assets/Objects/weapons.png")
        self.profile_spritesheet = Spritesheet("Assets/UI/profile.png")
        #self.health_spritesheet = Spritesheet("Assets\UI\hp.png")
        
        self.intro_background = pygame.image.load("Assets/map.png").convert()
        self.intro_background.set_alpha(25)

        self.level = 1
        self.area = 1
        self.level_cleared = True
        self.player_power = 0
        self.enemies_remaining = 0
    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.LayeredUpdates() #Stores all wall sprites
        self.enemies = pygame.sprite.LayeredUpdates() #Stores all enemy sprites
        self.attacks = pygame.sprite.LayeredUpdates() #Stores all attack hitbox sprites for the player
        self.profile = pygame.sprite.LayeredUpdates() #Stores the Player's HP, MP and XP
        self.background = Background(self,self.level-1,self.area-1) #0 plains | 1 desert | 2 forest | 3 castle
        self.player = Player(self, 7, 7, self.player_power)
    def events(self):
        #game loop events

        mouse_pos = pygame.mouse.get_pos()
        self.mouse_pos = mouse_pos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
        if pygame.mouse.get_pressed()[0]:
            self.player.basic_attack()
        elif pygame.mouse.get_pressed()[2]:
            self.player.special_attack()
        elif pygame.mouse.get_pressed()[1]: #Right Click
            pass
                    
    def update(self):
        self.all_sprites.update()
        self.enemies.update()
        self.attacks.update()
        self.profile.update()
        
        if self.enemies_remaining == 0:
            self.level_cleared = True
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.enemies.draw(self.screen)
        self.attacks.draw(self.screen)
        self.profile.draw(self.screen)
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

    def fade(self,width=WIN_WIDTH, height=WIN_HEIGHT): 
        fade = pygame.Surface((width, height))
        fade.fill((0,0,0))
        for alpha in range(0, 300):
            fade.set_alpha(alpha)
            self.playing = False
            self.screen.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(5)
            self.playing = True
            
    def next_level(self):
        levels = [0,
                  [lambda:Thief(self,8,2),lambda:Thief(self,2,2)],
                  [lambda:Thief(self)]
                  ]
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
        if self.level == 5:
            self.background.image.set_alpha(180)
        else:
            self.background.image.set_alpha(255)
        
        self.fade()

        self.enemies_remaining = 0
        self.level_cleared = False
        try:
            for enemy in levels[self.level-1]:
                enemy()
                self.enemies_remaining += 1
        except:
            pass
        
    def intro_screen(self):
        title = self.title_font.render('Twisted Empress', True, BLACK)
        title_rect = title.get_rect(x=WIN_WIDTH/2-160,y=WIN_HEIGHT/2-170)
        play_button = Button(WIN_WIDTH/2-50,WIN_HEIGHT/2-50,100,50,WHITE,BLACK,'Play',32)

        version = self.font.render('v0.0.1', True, BLACK)
        version_rect = version.get_rect(x=WIN_WIDTH-90,y=WIN_HEIGHT-50)

        main_menu = True
        while main_menu == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    main_menu = False
                    self.running = False
            
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if play_button.is_pressed(mouse_pos, mouse_pressed):
                main_menu = False
            if play_button.is_hovered(mouse_pos, mouse_pressed):
                play_button.image.set_alpha(255)
            else:
                play_button.image.set_alpha(int(255/4))
            self.screen.blit(self.intro_background, (0,0))
            self.screen.blit(title, title_rect)
            self.screen.blit(version, version_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()
        if self.running:
            self.fade()
            self.power_select()
    def power_select(self):
        # Power Select Menu
        lionheart = self.character_spritesheet.get_sprite(0,48*3,TILESIZE*2,TILESIZE).convert() #converts the images to save space
        odyssey = self.character_spritesheet.get_sprite(48*2,48*3,TILESIZE*2,TILESIZE).convert()
        acuity = self.character_spritesheet.get_sprite(96*2,48*3,TILESIZE*2,TILESIZE).convert()

        character = [lionheart,odyssey,acuity]
        quote = self.font.render('So much to do... so little time.', True, WHITE)
        quote2 = self.font.render('What is it that you seek?', True, WHITE)

        button1 = Button(58,128*3.7,190,50,(94, 253, 247),(50,49,59),'Power of Lionheart',20)
        button2 = Button(274,128*3.7,190,50,(253, 254, 137),(50,49,59),'Power of Odyssey',20)
        button3 = Button(494,128*3.7,190,50,(255, 93, 204),(50,49,59),'Power of Acuity',20)
        buttons = [button1,button2,button3]
    
        power_select = True
        while power_select == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    power_select = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            self.screen.fill(BLACK)

            self.screen.blit(quote, (WIN_WIDTH/4,96))
            self.screen.blit(quote2, (WIN_WIDTH/3.5,96+72))

            self.screen.blit(lionheart,(128,128*3))
            self.screen.blit(button1.image,button1.rect)
            
            self.screen.blit(odyssey,(128*2+84,128*3))
            self.screen.blit(button2.image,button2.rect)

            self.screen.blit(acuity,(128*3+84*2,128*3))
            self.screen.blit(button3.image,button3.rect)
            for button in buttons:
                if button.is_pressed(mouse_pos, mouse_pressed):
                    power_select = False
                    self.player_power = buttons.index(button) #gives the chosen power via button index (which aligns with the power enumeration)
                if button.is_hovered(mouse_pos, mouse_pressed):
                    button.image.set_alpha(255)
                    character[buttons.index(button)].set_alpha(255)
                else:
                    button.image.set_alpha(int(255/1.5))
                    character[buttons.index(button)].set_alpha(int(255/2))
            self.clock.tick(FPS)
            pygame.display.update()
        if self.running:
            self.fade()

g = Game()
g.intro_screen()
g.new()
while g.running == True:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()