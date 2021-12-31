import pygame
from random import randint

pygame.init()

screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("pooFromTheSky")

clock = pygame.time.Clock()

background = pygame.image.load("C:\\python\\game-pangpang\\poo_from_the_sky\\background.png")

character = pygame.image.load("C:\\python\\game-pangpang\\poo_from_the_sky\\character.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_position = (screen_width / 2) - (character_width / 2)
character_y_position = screen_height - character_height
to_x = 0
character_speed = 0.2

enemy = pygame.image.load("C:\\python\\game-pangpang\\poo_from_the_sky\\enemy2.png")
enemy_size = enemy.get_rect().size
enemy_width = enemy_size[0]
enemy_height = enemy_size[1]
enemy_x_position = randint(0, (screen_width - enemy_width))
enemy_y_position = 0
enemy_speed = 0.9

start_ticks = pygame.time.get_ticks()

game_font = pygame.font.Font(None, 40)
score = 0

running = True

while running:
    dt = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            to_x -= character_speed
        elif event.key == pygame.K_RIGHT:
            to_x += character_speed

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            to_x = 0

    character_x_position += to_x * dt

    if character_x_position < 0:
        character_x_position = 0
    elif character_x_position > screen_width - character_width:
        character_x_position = screen_width - character_width

    enemy_y_position += enemy_speed * dt

    if enemy_y_position > screen_height:
        enemy_y_position = 0
        enemy_x_position = randint(0, (screen_width - enemy_width))
        score += 1

    character_rect = character.get_rect()
    character_rect.left = character_x_position
    character_rect.top = character_y_position

    enemy_rect = enemy.get_rect()
    enemy_rect.left = enemy_x_position
    enemy_rect.top = enemy_y_position

    if character_rect.colliderect(enemy_rect):
        print("충돌했어요")
        running = False

    screen.blit(background, (0, 0))
    screen.blit(character, (character_x_position, character_y_position))
    screen.blit(enemy, (enemy_x_position, enemy_y_position))

    score_text = game_font.render(str(int(score)), True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    pygame.display.update()

pygame.time.delay(1000)

pygame.quit()
