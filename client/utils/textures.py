import pygame
from resources import resources

screen = pygame.display.set_mode((1920, 1080))

block_images = {
            "Dirt": pygame.transform.scale(pygame.image.load(resources("assets/graphics/dirt.png")), (40, 40)).convert(),
            "Stone": pygame.transform.scale(pygame.image.load(resources("assets/graphics/stone.png")), (40, 40)).convert(),
            "Obsidian": pygame.transform.scale(pygame.image.load(resources("assets/graphics/obsidian.png")), (40, 40)).convert(),
            "Bedrock": pygame.transform.scale(pygame.image.load(resources("assets/graphics/bedrock.png")), (40, 40)).convert()
        }

PlayerSkin = {
    "Standing Right" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/standing_right.png")), (40, 80)).convert_alpha(),
    "Walking Right" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/walking_right.png")), (40, 80)).convert_alpha(),
    "Standing Left" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/standing_left.png")), (40, 80)).convert_alpha(),
    "Walking Left" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/walking_left.png")), (40, 80)).convert_alpha(),
    "Jumping Right" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/jumping_right.png")), (40, 80)).convert_alpha(),
    "Jumping Left" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/jumping_left.png")), (40, 80)).convert_alpha(),
    "Mining Right" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/mining_right.png")), (40, 80)).convert_alpha(),
    "Mining Right Gold" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/mining_right_gold.png")), (40, 80)).convert_alpha(),
    "Mining Right Grey" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/mining_right_grey.png")), (40, 80)).convert_alpha(),
    "Mining Right Purple" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/mining_right_purple.png")), (40, 80)).convert_alpha(),
    "Mining Left" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/mining_left.png")), (40, 80)).convert_alpha(),
    "Mining Left Gold" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/mining_left_gold.png")), (40, 80)).convert_alpha(),
    "Mining Left Grey" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/mining_left_grey.png")), (40, 80)).convert_alpha(),
    "Mining Left Purple" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/mining_left_purple.png")), (40, 80)).convert_alpha()
}

ZombieSkin = {
    "Standing Right" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/standing_right.png")), (40, 80)).convert_alpha(),
    "Walking Right" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/walking_right.png")), (40, 80)).convert_alpha(),
    "Standing Left" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/standing_left.png")), (40, 80)).convert_alpha(),
    "Walking Left" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/walking_left.png")), (40, 80)).convert_alpha(),
    "Jumping Right" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/jumping_right.png")), (40, 80)).convert_alpha(),
    "Jumping Left" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/skins/jumping_left.png")), (40, 80)).convert_alpha()
}

textures_dict = {
    "Dirt" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/dirt.png")), (40 , 40)).convert(),
    "Stone" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/stone.png")), (40 , 40)).convert(),
    "Obsidian" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/obsidian.png")), (40 , 40)).convert(),
    "Wood" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/dirt.png")), (40 , 40)).convert(),
    "Bedrock" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/bedrock.png")), (40 , 40)).convert(),
    "Wood1" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/wood1.png")), (40 , 40)).convert(),
    "Wood2" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/wood2.png")), (40 , 40)).convert(),
    "Doorup" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/porteup.png")), (40 , 40)).convert(),
    "Doordown" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/portedown.png")), (40 , 40)).convert(),
    "Game" : pygame.transform.scale(pygame.image.load(resources("assets/graphics/bloc_2048.png")), (40 , 40)).convert(),
    "Tuile" : {
        2 : pygame.transform.scale(pygame.image.load(resources("assets/graphics/tuile_2.png")), (40 , 40)).convert(),
        4 : pygame.transform.scale(pygame.image.load(resources("assets/graphics/tuile_4.png")), (40 , 40)).convert(),
        8 : pygame.transform.scale(pygame.image.load(resources("assets/graphics/tuile_8.png")), (40 , 40)).convert(),
        16 : pygame.transform.scale(pygame.image.load(resources("assets/graphics/tuile_16.png")), (40 , 40)).convert(),
        32 : pygame.transform.scale(pygame.image.load(resources("assets/graphics/tuile_32.png")), (40 , 40)).convert(),
        64 : pygame.transform.scale(pygame.image.load(resources("assets/graphics/tuile_64.png")), (40 , 40)).convert(),
        128 : pygame.transform.scale(pygame.image.load(resources("assets/graphics/tuile_128.png")), (40 , 40)).convert(),
        256 : pygame.transform.scale(pygame.image.load(resources("assets/graphics/tuile_256.png")), (40 , 40)).convert(),
        512 : pygame.transform.scale(pygame.image.load(resources("assets/graphics/tuile_512.png")), (40 , 40)).convert()
    }
}

texture_background = pygame.transform.scale(pygame.image.load(resources("assets/graphics/background/background.png")), (9360 , 3240)).convert_alpha()

del screen