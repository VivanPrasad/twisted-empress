import pygame

pygame.mixer.init()

class Music:
    title_music = pygame.mixer.Sound("Assets/Audio/Music/menu.mp3"); title_music.set_volume(2)
    
    the_plains = pygame.mixer.Sound("Assets/Audio/Music/Areas/the_plains.mp3"); the_plains.set_volume(0.5)
    the_desert = pygame.mixer.Sound("Assets/Audio/Music/Areas/the_desert.mp3"); the_desert.set_volume(0.5)
    the_enchanted_forest = pygame.mixer.Sound("Assets/Audio/Music/Areas/the_enchanted_forest.mp3") ; the_enchanted_forest.set_volume(0.9)
    the_castle = pygame.mixer.Sound("Assets/Audio/Music/Areas/the_castle.mp3"); the_castle.set_volume(0.8)
    
    area_music = [the_plains,the_desert,the_enchanted_forest,the_castle,title_music] #make sure to have it minus of the other area due to the index!

    the_rogue = pygame.mixer.Sound("Assets/Audio/Music/Bosses/the_rogue.mp3"); the_rogue.set_volume(0.9)
    the_guardian = pygame.mixer.Sound("Assets/Audio/Music/Bosses/the_guardian.mp3"); the_guardian.set_volume(0.9)
    the_wizard = pygame.mixer.Sound("Assets/Audio/Music/Bosses/the_sorcerer.mp3"); the_wizard.set_volume(0.9)
    the_prince = pygame.mixer.Sound("Assets/Audio/Music/Bosses/the_prince.mp3"); the_prince.set_volume(0.9)
    the_empress = pygame.mixer.Sound("Assets/Audio/Music/Bosses/the_empress.mp3"); the_empress.set_volume(0.9)
    boss_music = [the_rogue,the_guardian,the_wizard,the_prince,the_empress]

    the_haunter = pygame.mixer.Sound("Assets/Audio/Music/Bosses/the_haunter.mp3"); the_haunter.set_volume(0.9) #miniboss
    #the angel miniboss does not have a soundtrack

class SFX: #All the SFX are stored as variables in a class to be played at anytime!
    health_orb = pygame.mixer.Sound('Assets/Audio/SFX/Objects/health_orb.wav'); health_orb.set_volume(1.5)
    mana_orb = pygame.mixer.Sound('Assets/Audio/SFX/Objects/mana_orb.wav'); mana_orb.set_volume(0.9)
    
    throw_one = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/throw_one.wav'); throw_one.set_volume(0.8)
    throw_two = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/throw_two.wav'); throw_two.set_volume(0.8)
    throw_circle = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/throw_circle.wav'); throw_circle.set_volume(0.9)
    
    shield = pygame.mixer.Sound('Assets/Audio/SFX/Player/shield.wav'); shield.set_volume(0.8)
    dash = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/dash.wav'); dash.set_volume(1.5)

    arrow_hit = pygame.mixer.Sound('Assets/Audio/SFX/Player/Odyssey/arrow_hit.wav'); arrow_hit.set_volume(0.8)
    arrow_special_hit = pygame.mixer.Sound('Assets/Audio/SFX/Player/Odyssey/arrow_special_hit.wav'); arrow_special_hit.set_volume(0.5)

    sword_hit = pygame.mixer.Sound('Assets/Audio/SFX/Player/Lionheart/sword_hit.wav'); sword_hit.set_volume(0.5)
    sword_hit2 = pygame.mixer.Sound('Assets/Audio/SFX/Player/Lionheart/sword_hit2.wav'); sword_hit2.set_volume(0.6)
    sword_hit3 = pygame.mixer.Sound('Assets/Audio/SFX/Player/Lionheart/sword_hit3.wav'); sword_hit3.set_volume(0.5)
    sword_special_hit = pygame.mixer.Sound('Assets/Audio/SFX/Player/Lionheart/sword_special_hit.wav'); sword_special_hit.set_volume(0.5)
    
    orb_throw = pygame.mixer.Sound('Assets/Audio/SFX/Player/Acuity/orb_throw.wav'); orb_throw.set_volume(0.9)
    orb_hit = pygame.mixer.Sound('Assets/Audio/SFX/Player/Acuity/orb_hit.wav'); orb_hit.set_volume(0.9)
    orb_special = pygame.mixer.Sound('Assets/Audio/SFX/Player/Acuity/orb_special.wav'); orb_special.set_volume(0.9)
    
    laser = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/laser.wav'); laser.set_volume(1.2)
    charge = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/charge.wav'); charge.set_volume(0.9)
    player_hurt = pygame.mixer.Sound('Assets/Audio/SFX/Player/player_hurt.wav'); player_hurt.set_volume(1.2)
    death = pygame.mixer.Sound('Assets/Audio/SFX/Player/death.wav'); death.set_volume(1.5)
    
    sword_shing = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/sword_shing.wav'); sword_shing.set_volume(0.3)
    ice_attack = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/ice.wav'); ice_attack.set_volume(0.5)
    lightning_attack = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/lightning.wav'); lightning_attack.set_volume(0.5)
    low_hp_alert = pygame.mixer.Sound('Assets/Audio/SFX/Player/low_hp_alert.wav'); low_hp_alert.set_volume(1.3)

    level_up = pygame.mixer.Sound('Assets/Audio/SFX/Player/level_up.wav'); level_up.set_volume(3)

    disappear = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/disappear.wav'); disappear.set_volume(0.5)
    enemy_death = pygame.mixer.Sound('Assets/Audio/SFX/Enemies/enemy_death.wav'); level_up.set_volume(1.2)

    game_begin = pygame.mixer.Sound('Assets/Audio/SFX/Ambience/game_begin.wav')
    wind = pygame.mixer.Sound('Assets/Audio/SFX/Ambience/wind.wav')

    ui_select = pygame.mixer.Sound('Assets/Audio/SFX/UI/ui_select.wav')
    ui_confirm = pygame.mixer.Sound('Assets/Audio/SFX/UI/ui_confirm.wav')
