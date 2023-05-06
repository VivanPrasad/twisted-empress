import pygame
from sprites import *
from config import *
from audio import *
import sys

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)) #Displays the screen size properly
        self.title = pygame.display.set_caption("Twisted Empress")
        self.icon = pygame.display.set_icon(pygame.image.load("Assets/icon.png"))
        self.clock = pygame.time.Clock()
        self.title_font = pygame.font.Font('Assets/Font/royal-intonation.ttf',48)
        self.font = pygame.font.Font('Assets/Font/royal-intonation.ttf',32)
        self.running = True
        
        Music.title_music.play()
        
        self.background_spritesheet = Spritesheet("Assets/map.png") #All the several backgrounds for each of the 20 levels
        
        self.character_spritesheet = Spritesheet("Assets/Entities/player.png") #Sprite for player movement

        self.attack_spritesheet = Spritesheet("Assets/Objects/attacks.png")
        self.weapon_spritesheet = Spritesheet("Assets/Objects/weapons.png")
        self.profile_spritesheet = Spritesheet("Assets/UI/profile.png") #Spritesheet all UI related things for the player! (HP, MP, XP, Spells)
        
        self.enemy_spritesheet = Spritesheet("Assets/Entities/enemies.png")
        self.drops_spritesheet = Spritesheet("Assets/Objects/drops.png")
        
        self.intro_background = pygame.image.load("Assets/map.png").convert()
        self.intro_background.set_alpha(3)

        self.level = 1
        self.area = 1
        self.level_cleared = True
        self.player_power = 0
        self.enemies_remaining = 0

        self.level_data = [
            [ #AREA 1 - MIGHTY MEADOWS
                [], #Level 1-1 (Empty)
                [lambda:Thief(self),lambda:Archer(self,5,0),lambda:Archer(self,14,0)], #Level 1-2
                [lambda:Thief(self,4,2),lambda:Thief(self,10,2),lambda:Archer(self,2,2)], #Level 1-3
                [lambda:Thief(self,3,4),lambda:Thief(self,4,4),lambda:Archer(self,1,1),lambda:Archer(self,8,1),lambda:Thief(self,10,4)], #Level 1-4
                [lambda: Thief(self,7,5),lambda: Thief(self,4,7),lambda:Thief(self,12,7),lambda: Archer(self,12,2),lambda: Archer(self,1,2),lambda: Archer(self,13,2),lambda: Thief(self,13,13)]
            ], #Boss Level 1-5
            [ #AREA 2 - DESERT
                [],
                [lambda:Defender(self,7,7),lambda:Sentry(self,9,1),lambda:Defender(self,3,7)],
                [lambda:Sentry(self,1,1),lambda:Defender(self,7,4),lambda:Sentry(self,13,1),lambda:Sentry(self,13,13),lambda:Sentry(self,1,13)],
                [lambda:Warrior(self,8,1),lambda:Sentry(self,4,2),lambda:Defender(self,3,5),lambda:Warrior(self,10,10)],
                [lambda:Warrior(self,8,1),lambda:Warrior(self,2,1),lambda:Defender(self,7,7),lambda:Sentry(self,7,2),lambda:Sentry(self,13,2),lambda:Sentry(self,13,13),lambda:Warrior(self,5,10),lambda:Defender(self,3,5)],
            ],
            [ #AREA 3 - THE ENCHANTED FOREST
                [],
                [],
                [],
                [],
                [],
            ],
            [ #AREA 4 - THE CASTLE
                [],
                [],
                [],
                [],
                [],
            ],
            [ #AREA 5 - THE HEART
                [],
                [],
                [],
                [],
                [],
            ],]

        self.new()
    def new(self):
        self.intro_screen()
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.players = pygame.sprite.LayeredUpdates() #Stores all players (for future implementation)
        self.walls = pygame.sprite.LayeredUpdates() #Stores all wall sprites
        self.enemies = pygame.sprite.LayeredUpdates() #Stores all enemy sprites
        self.drops = pygame.sprite .LayeredUpdates() #Stores all the prize drops 
        self.attacks = pygame.sprite.LayeredUpdates() #Stores all attack hitbox sprites for the player
        self.profile = pygame.sprite.LayeredUpdates() #Stores the Player's HP, MP and XP
        self.background = Background(self,self.level-1,self.area-1) #0 plains | 1 desert | 2 forest | 3 castle
        self.player = Player(self, 7, 7, self.player_power)

        while self.running == True:
            self.main()
            self.game_over()
        pygame.quit()
        sys.exit()
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
        self.players.update()
        self.enemies.update()
        self.attacks.update()
        self.drops.update()
        self.profile.update()
        
        if self.enemies_remaining == 0:
            self.level_cleared = True
        if self.player.health < 1:
            SFX.low_hp_alert.stop()
            SFX.death.play(0,0,100)
            SFX.death.fadeout(5000)
            self.fade()
            self.playing = False
    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.players.draw(self.screen)
        self.enemies.draw(self.screen)
        self.attacks.draw(self.screen)
        self.drops.draw(self.screen)
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
        for song in Music.boss_music:
                song.fadeout(100)
        for song in Music.area_music:
                song.fadeout(100)
        game_over = True
        text = self.font.render('GAME OVER', True, WHITE)
        text2 = self.font.render('Press R to Retry', True, WHITE)
        while game_over == True and self.player.health == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    self.running = False
                if pygame.key.get_pressed()[pygame.K_r]:
                    game_over = False
                    global g
                    g = Game()
                    
            self.screen.fill(BLACK)
            self.screen.blit(text,(WIN_WIDTH/3,WIN_HEIGHT/3))
            self.screen.blit(text2,(WIN_WIDTH/3,WIN_HEIGHT/2))
            pygame.display.update()

    def fade(self,width=WIN_WIDTH, height=WIN_HEIGHT): 
        fade = pygame.Surface((width, height))
        self.playing = False
        fade.fill((0,0,0))
        for alpha in range(1, 60):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0,0))
            pygame.display.update()
            pygame.time.delay(10)
        self.playing = True
        pygame.display.update()
            
    def next_level(self):
        
        self.level_cleared = False
        
        if self.level == 5:
            for song in Music.boss_music:
                song.fadeout(2000)
            self.area += 1
            Music.area_music[self.area-1].play(-1,0,5000)
        if self.level == 4:
            for song in Music.area_music:
                song.fadeout(2000)
            Music.boss_music[self.area-1].play(-1,0,5000)
        if self.level < 5 and self.area <= 4:
            self.level += 1
        else:
            self.level = 1
        if self.area == 5 and self.level == 2:
            self.playing = False
            self.running = False
        
        self.background.kill()
        self.background = Background(self,self.level-1,self.area-1)
        if self.level == 5:
            self.background.image.set_alpha(180)
        else:
            self.background.image.set_alpha(255)
        
        self.fade()
        self.spawn_enemies()

    def spawn_enemies(self):
        self.enemies_remaining = 0
        try:
            for enemy in self.level_data[self.area-1][self.level-1]:
                enemy() #tries to call the enemy
                self.enemies_remaining += 1

        except: pass
        
    def intro_screen(self):
        title = self.title_font.render('Twisted Empress', True, WHITE, BLACK)
        title_rect = title.get_rect(x=WIN_WIDTH/2-160,y=WIN_HEIGHT/2-170)
        play_button = Button(WIN_WIDTH/2-50,WIN_HEIGHT/2-50,100,50,WHITE,BLACK,'Play',32)

        version = self.font.render('v0.0.1', True, WHITE,BLACK)
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
                SFX.ui_confirm.play()
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
        select_sound_played = False

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
                    SFX.game_begin.play()
                    Music.title_music.fadeout(1000)
                    Music.area_music[self.area-1].play(-1,0,5000)
                    self.player_power = buttons.index(button) #gives the chosen power via button index (which aligns with the power enumeration)
                if button.is_hovered(mouse_pos, mouse_pressed):
                    if button.image.get_alpha() != 255:
                        select_sound_played = True
                        SFX.ui_select.play(0,100)
                    button.image.set_alpha(255)
                    character[buttons.index(button)].set_alpha(255)
                        
                else:
                    if button.image.get_alpha() == 255 and select_sound_played:
                        select_sound_played = False
                    button.image.set_alpha(int(255/1.5))
                    character[buttons.index(button)].set_alpha(int(255/2))
            self.clock.tick(FPS)
            pygame.display.update()
        if self.running:
            self.fade()


g = Game()