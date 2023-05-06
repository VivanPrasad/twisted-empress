import pygame

pygame.mixer.init()

class Music:
    title_music = pygame.mixer.Sound("Assets/Audio/Music/menu.mp3")
    
    the_plains = pygame.mixer.Sound("Assets/Audio/Music/Areas/the_plains.mp3"); the_plains.set_volume(0.4)
    the_desert = pygame.mixer.Sound("Assets/Audio/Music/Areas/the_desert.mp3"); the_desert.set_volume(0.4)
    the_enchanted_forest = pygame.mixer.Sound("Assets/Audio/Music/Areas/the_enchanted_forest.mp3") ; the_enchanted_forest.set_volume(0.4)
    the_castle = pygame.mixer.Sound("Assets/Audio/Music/Areas/the_castle.mp3"); the_castle.set_volume(0.4)

    area_music = [the_plains,the_desert,the_enchanted_forest,the_castle] #make sure to have it minus of the other area due to the index!

    the_rogue = pygame.mixer.Sound("Assets/Audio/Music/Bosses/the_rogue.mp3"); the_rogue.set_volume(0.6)
    the_guardian = pygame.mixer.Sound("Assets/Audio/Music/Bosses/the_guardian.mp3"); the_guardian.set_volume(0.6)
    the_wizard = pygame.mixer.Sound("Assets/Audio/Music/Bosses/the_wizard.mp3"); the_wizard.set_volume(0.6)
    the_prince = pygame.mixer.Sound("Assets/Audio/Music/Bosses/the_prince.mp3"); the_prince.set_volume(0.6)
    the_empress = pygame.mixer.Sound("Assets/Audio/Music/Bosses/the_empress.mp3"); the_empress.set_volume(0.6)
    boss_music = [the_rogue,the_guardian,the_wizard,the_prince,the_empress]
class SFX:
    health_orb = pygame.mixer.Sound('Assets/Audio/SFX/Objects/health_orb.wav')
    mana_orb = pygame.mixer.Sound('Assets/Audio/SFX/Objects/mana_orb.wav')
    
    throw_one = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/throw_one.wav')
    throw_two = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/throw_two.wav')
    throw_circle = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/throw_circle.wav')
    
    hit1 = pygame.mixer.Sound('Assets/Audio/SFX/Player/Lionheart/hit.wav'); hit1.set_volume(0.3)
    hit2 = pygame.mixer.Sound('Assets/Audio/SFX/Player/Lionheart/hit2.wav'); hit1.set_volume(0.3)

    sword_hit = pygame.mixer.Sound('Assets/Audio/SFX/Player/Lionheart/sword_hit.wav'); sword_hit.set_volume(0.4)
    
    laser = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/laser.wav')
    
    player_hurt = pygame.mixer.Sound('Assets/Audio/SFX/Player/player_hurt.wav')
    death = pygame.mixer.Sound('Assets/Audio/SFX/Player/death.wav')
    
    enemy_death = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/enemy_death.wav')
    low_hp_alert = pygame.mixer.Sound('Assets/Audio/SFX/Player/low_hp_alert.wav')

    level_up = pygame.mixer.Sound('Assets/Audio/SFX/Player/level_up.wav')

    game_begin = pygame.mixer.Sound('Assets/Audio/SFX/Ambience/game_begin.wav')
    wind = pygame.mixer.Sound('Assets/Audio/SFX/Ambience/wind.wav')

    ui_select = pygame.mixer.Sound('Assets/Audio/SFX/UI/ui_select.wav')
    ui_confirm = pygame.mixer.Sound('Assets/Audio/SFX/UI/ui_confirm.wav')

pygame.mixer_music.set_volume(0)
