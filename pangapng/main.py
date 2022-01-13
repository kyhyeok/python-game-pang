import pygame
import os

pygame.init()

screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("PangPang")

clock = pygame.time.Clock()

current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, "images")

background = pygame.image.load(os.path.join(image_path, "background.png"))

stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_position = (screen_width / 2) - (character_width / 2)
character_y_position = screen_height - character_height - stage_height

character_to_x = 0
character_speed = 5

weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []

weapon_speed = 10

ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png"))
]

ball_speed_y = [-18, -15, -12, -9]

balls = []

balls.append({
    "position_x": 50,
    "position_y": 50,
    "image_index": 0,
    "to_x": 3,
    "to_y": -6,
    "init_speed_y": ball_speed_y[0]
})

weapon_to_remove = -1
ball_to_remove = -1

running = True
while running:
    dt = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_position = character_x_position + (character_width / 2) - (weapon_width / 2)
                weapon_y_position = character_y_position
                weapons.append([weapon_x_position, weapon_y_position])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0

    character_x_position += character_to_x

    if character_x_position < 0:
        character_to_x = 0
    elif character_x_position > screen_width - character_width:
        character_x_position = screen_width - character_width

    weapons = [[weapon[0], weapon[1] - weapon_speed] for weapon in weapons]
    weapons = [[weapon[0], weapon[1]] for weapon in weapons if weapon[1] > 0]

    for ball_index, ball_value in enumerate(balls):
        ball_position_x = ball_value["position_x"]
        ball_position_y = ball_value["position_y"]
        ball_image_index = ball_value['image_index']

        ball_size = ball_images[ball_image_index].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_position_x <= 0 or ball_position_x > screen_width - ball_width:
            ball_value["to_x"] = ball_value["to_x"] * -1

        if ball_position_y >= screen_height - stage_height - ball_height:
            ball_value["to_y"] = ball_value["init_speed_y"]
        else:
            ball_value["to_y"] += 0.5

        ball_value["position_x"] += ball_value["to_x"]
        ball_value["position_y"] += ball_value["to_y"]

    character_rect = character.get_rect()
    character_rect.left = character_x_position
    character_rect.top = character_y_position

    for ball_index, ball_value in enumerate(balls):
        ball_position_x = ball_value["position_x"]
        ball_position_y = ball_value["position_y"]
        ball_image_index = ball_value['image_index']

        ball_rect = ball_images[ball_image_index].get_rect()
        ball_rect.left = ball_position_x
        ball_rect.top = ball_position_y

        if character_rect.colliderect(ball_rect):
            running = False
            break

        for weapon_index, weapon_value in enumerate(weapons):
            weapon_position_x = weapon_value[0]
            weapon_position_y = weapon_value[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_position_x
            weapon_rect.top = weapon_position_y

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_index
                ball_to_remove = ball_index

                if ball_image_index < 3:
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    small_ball_rect = ball_images[ball_image_index + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    balls.append({
                        "position_x": ball_position_x + ((ball_width / 2) - (small_ball_width / 2)),
                        "position_y": ball_position_y + ((ball_height / 2) - (small_ball_height / 2)),
                        "image_index": ball_image_index + 1,
                        "to_x": -3,
                        "to_y": -6,
                        "init_speed_y": ball_speed_y[ball_image_index + 1]
                    })

                    balls.append({
                        "position_x": ball_position_x + ((ball_width / 2) - (small_ball_width / 2)),
                        "position_y": ball_position_y + ((ball_height / 2) - (small_ball_height / 2)),
                        "image_index": ball_image_index + 1,
                        "to_x": 3,
                        "to_y": -6,
                        "init_speed_y": ball_speed_y[ball_image_index + 1]
                    })
                    break

    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    screen.blit(background, (0, 0))

    for weapon_x_position, weapon_y_position in weapons:
        screen.blit(weapon, (weapon_x_position, weapon_y_position))

    for index, value in enumerate(balls):
        ball_position_x = value['position_x']
        ball_position_y = value['position_y']
        ball_image_index = value["image_index"]
        screen.blit(ball_images[ball_image_index], (ball_position_x, ball_position_y))

    screen.blit(stage, (0, screen_height - stage_height))
    screen.blit(character, (character_x_position, character_y_position))

    pygame.display.update()

pygame.time.delay(1000)

pygame.quit()
