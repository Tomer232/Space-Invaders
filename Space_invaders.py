import pygame
import random
import math

# Initializing the pygame.
pygame.init()

# Creating the screen.
screen = pygame.display.set_mode((800, 600))

# Title nd icon.
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('enemy.png')
pygame.display.set_icon(icon)

# Player.
user_space_ship = pygame.image.load('space_ship.png')
player_x = 370
player_y = 550
player_moves = 0

# Enemy.
enemy_image = []
enemy_x = []
enemy_y = []
enemy_moves_x = []
enemy_moves_y = []
num_of_enemy = 6
enemy_killed = 0

for i in range(num_of_enemy):
    enemy_image.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 768))  # random spawn points.
    enemy_y.append(random.randint(30, 120))  # ^.
    enemy_moves_x.append(0.25)
    enemy_moves_y.append(25)

# new Enemy.
new_enemy_image = []
new_enemy_x = []
new_enemy_y = []
new_enemy_moves_x = []
new_enemy_moves_y = []
num_of_new_enemy = 2
new_enemy_killed = 0

for q in range(num_of_new_enemy):
    new_enemy_image.append(pygame.image.load('enemy2.png'))
    new_enemy_x.append(random.randint(0, 768))  # random spawn points.
    new_enemy_y.append(random.randint(30, 100))  # ^.
    new_enemy_moves_x.append(0.2)
    new_enemy_moves_y.append(20)

# Bullet.
# ready - you cant see the bullet on the screen.
# fire - the bullet is currently moving.
bullet_image = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 555
bullet_moves_x = 0
bullet_moves_y = 0.7
bullet_state = "ready"
bullet_shoot = 0
hit_rate = 0
trigger_pulled = 0
total_hits = 0

# Score.
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
text_x = 10
text_y = 6
hit1 = 0
hit2 = 0

# Game over text.
over_font = pygame.font.Font('freesansbold.ttf', 32)
end_stats_font = pygame.font.Font('freesansbold.ttf', 8)

# instruction.
instruction_font = pygame.font.Font('freesansbold.ttf', 20)
left_key = pygame.image.load('left.png')
right_key = pygame.image.load('right.png')
spacebar = pygame.image.load('spacebar.png')
enter_key = pygame.image.load('enter.png')

# time related things.
flag = False
new_start_time = 0
time_text = 0
game_length = 0
final_game_length = 0


# Game over function.
def game_over_text():
    accuracy_to_display = hit_rate_calc()
    over_text = font.render("- GAME OVER -", True, (0, 0, 0))
    final_score_text = font.render("Final Score : " + str(score_value), True, (0, 0, 0))
    play_again_text = font.render("Press 'R' to Play Again or 'E' to Exit.", True, (0, 0, 0))
    kills = font.render("KILLS           " + ":  " + "easy alien " + str(enemy_killed) + " | " + "hard alien " +
                        str(new_enemy_killed),
                        True, (0, 0, 0))
    time = font.render("TIME             " + ":                 "
                                             " " + str(final_game_length) + " sec", True, (0, 0, 0))
    accuracy = font.render("ACCURACY  " + ":                  "
                                          "  {:.2f} %".format(accuracy_to_display), True, (0, 0, 0))
    pygame.draw.rect(screen, (0, 0, 0), (170, 150, 460, 220), 3)  # game over rect
    pygame.draw.rect(screen, (0, 0, 0), (220, 393, 360, 30), 2)  # play again rect
    pygame.draw.line(screen, (0, 0, 0), (326, 192), (475, 192), 2)  # under game over
    pygame.draw.line(screen, (0, 0, 0), (196, 293), (600, 293), 2)  # kills/ acc divider
    pygame.draw.line(screen, (0, 0, 0), (196, 323), (600, 323), 2)  # acc/ time divider
    screen.blit(over_text, (327, 175))
    screen.blit(final_score_text, (332, 210))
    screen.blit(play_again_text, (225, 400))
    screen.blit(kills, (196, 270))
    screen.blit(accuracy, (196, 300))
    screen.blit(time, (196, 330))


# Score function.
def show_score(x, y):
    global time_text, final_game_length
    if not enemy_y[0] > 525 and not new_enemy_y[0] > 525:
        score = font.render("Score : " + str(score_value), True, (0, 0, 0))
        time_text = font.render("Time : " + str(elapsed_time), True, (0, 0, 0))
        final_game_length = elapsed_time
        screen.blit(score, (x, y))
        screen.blit(time_text, (x + 660, y))
        pygame.draw.rect(screen, (0, 0, 0), (0, 25, 800, 2), 2)  # the line below score while the game runs.


def instructions():
    global i
    pygame.draw.rect(screen, (0, 0, 0), (260, 85, 280, 430), 3)
    pygame.draw.line(screen, (0, 0, 0), (310, 135), (490, 135), 2)
    pygame.draw.circle(screen, (0, 0, 0), (285, 180), 3, 0)
    pygame.draw.circle(screen, (0, 0, 0), (285, 250), 3, 0)
    pygame.draw.circle(screen, (0, 0, 0), (285, 320), 3, 0)
    pygame.draw.circle(screen, (0, 0, 0), (285, 390), 3, 0)
    pygame.draw.circle(screen, (0, 0, 0), (285, 460), 3, 0)
    instruction_text = font.render("- INSTRUCTIONS -", True, (0, 0, 0))
    screen.blit(instruction_text, (310, 115))

    instructions_font = pygame.font.Font('freesansbold.ttf', 15)
    instruction_text = [
        "Press            to shoot the enemy.",
        "Press            to move left.",
        "Press            to move right.",
        "Press            to start the game.",
        "Press 'E' to exit."
    ]
    for i, instruction_text in enumerate(instruction_text):
        screen.blit(instructions_font.render(instruction_text, True, (0, 0, 0)), (295, 173 + (i * 70)))

    screen.blit(spacebar, (343, 165))
    screen.blit(left_key, (343, 235))
    screen.blit(right_key, (343, 305))
    screen.blit(enter_key, (343, 375))


# Player function to display the player image.
def player(x, y):
    screen.blit(user_space_ship, (x, y))


# player settings including movement & boundaries
def player_settings():
    global player_x
    player_x += player_moves

    # Boundaries of the spaceship user.
    if player_x <= 0:
        player_x = 0
    elif player_x >= 768:
        player_x = 768


# which enemy to show on screen.
def enemy(x, y, t, num):
    if num == 6:
        screen.blit(enemy_image[t], (x, y))
    else:
        screen.blit(new_enemy_image[t], (x, y))


# enemy respawn
def enemy_respawn(num, contact, enemy_val_x, enemy_val_y):
    global score_value, bullet_y, bullet_state, hit1, hit2, enemy_killed, new_enemy_killed
    if contact and num == 6:
        bullet_y = 555
        bullet_state = "ready"
        hit1 += 1
        print("hit1")
        if hit1 == 2:
            enemy_val_x[i] = random.randint(0, 768)  # random x spawn points.
            enemy_val_y[i] = random.randint(50, 150)  # random y spawn points.
            enemy_killed += 1
            score_value += 1
            hit1 = 0
    elif contact and num == 2:
        bullet_y = 555
        bullet_state = "ready"
        hit2 += 1
        print("hit2")
        if hit2 == 3:
            enemy_val_x[i] = random.randint(0, 768)  # random x spawn points.
            enemy_val_y[i] = random.randint(50, 150)  # random y spawn points.
            new_enemy_killed += 1
            score_value += 2
            hit2 = 0


# Firing bullet function.
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x, y))


# bullet movement.
def bullet_movement():
    global bullet_y, bullet_state
    if bullet_y <= 20:
        bullet_y = 555
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_moves_y


# Detecting collision function.
def collision(enemy_point_x, enemy_point_y, bullet_point_x, bullet_point_y):
    global total_hits
    distance = math.sqrt((math.pow(enemy_point_x - bullet_point_x, 2)) + (math.pow(enemy_point_y - bullet_point_y, 2)))
    if distance < 20:
        total_hits += 1
        return True
    else:
        return False


# hit rate calculation.
def hit_rate_calc():
    global hit_rate
    if trigger_pulled == 0:
        return 0
    else:
        hit_rate = (total_hits / trigger_pulled) * 100
        return hit_rate


# funtion to start over the game and resetting the values.
def start_over():
    global enemy_x, enemy_y, new_enemy_x, new_enemy_y, player_x, player_y, bullet_state, score_value, hit1, hit2, \
        elapsed_time, flag, trigger_pulled, total_hits, hit_rate
    for k in range(num_of_enemy):
        enemy_x[k] = random.randint(0, 768)
        enemy_y[k] = random.randint(50, 150)
    for k in range(num_of_new_enemy):
        new_enemy_x[k] = random.randint(0, 768)
        new_enemy_y[k] = random.randint(30, 120)

    player_x = 370
    player_y = 550
    bullet_state = "ready"
    score_value = 0
    hit1 = 0
    hit2 = 0
    elapsed_time = 0
    flag = True
    trigger_pulled = 0
    total_hits = 0
    hit_rate = 0


# enemy setting function, including movement & collision & endgame.
def enemy_settings(num, new_num, enemy_val_x, enemy_moves_val_x, enemy_val_y, enemy_moves_val_y, new_enemy_val_y):
    global i, bullet_y, bullet_state, hit1, hit2, score_value
    for i in range(num):

        # Game over.
        if enemy_val_y[i] > 525:
            for j in range(num):
                enemy_val_y[j] = 2000
            for j in range(new_num):
                new_enemy_val_y[j] = 2000
            game_over_text()
            break

        # enemy movement settings.
        enemy_val_x[i] += enemy_moves_val_x[i]
        if enemy_val_x[i] <= 0:
            enemy_moves_val_x[i] = 0.35
            enemy_val_y[i] += enemy_moves_val_y[i]
        elif enemy_val_x[i] >= 768:
            enemy_moves_val_x[i] = -0.35
            enemy_val_y[i] += enemy_moves_val_y[i]

        # Collision
        contact = collision(enemy_val_x[i], enemy_val_y[i], bullet_x, bullet_y)
        enemy_respawn(num, contact, enemy_val_x, enemy_val_y)
        enemy(enemy_val_x[i], enemy_val_y[i], i, num)


running = False
displaying_instructions = True
# instructions loop.
while displaying_instructions:
    screen.fill((120, 200, 150))
    instructions()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            displaying_instructions = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                displaying_instructions = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # ENTER key
                displaying_instructions = False
                running = True
    pygame.display.update()

start_time = pygame.time.get_ticks()

# Game Loop.
while running:

    # Background screen color.
    screen.fill((120, 200, 150))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                # press 'e' to exit the game.
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # Left arrow is pressed.
                player_moves = -0.15
            if event.key == pygame.K_RIGHT:
                # Right arrow is pressed.
                player_moves = 0.15
            if event.key == pygame.K_SPACE:
                # Bullet is being fired.
                if bullet_state == "ready":
                    if enemy_y[0] < 2000:
                        trigger_pulled += 1
                    bullet_x = player_x
                    fire_bullet(player_x, bullet_y)
            if event.key == pygame.K_r:
                # restart the game.
                print("r is pressed")
                start_over()
                new_start_time = pygame.time.get_ticks()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # Keystroke has been release.
                player_moves = 0

    player_settings()

    # enemy 1
    enemy_settings(num_of_enemy, num_of_new_enemy, enemy_x, enemy_moves_x, enemy_y, enemy_moves_y, new_enemy_y)

    if flag:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - new_start_time) / 1000
    else:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000

    if elapsed_time >= 20:
        # enemy 2
        enemy_settings(num_of_new_enemy, num_of_enemy, new_enemy_x, new_enemy_moves_x, new_enemy_y, new_enemy_moves_y,
                       enemy_y)

    # Bullet movement.
    bullet_movement()
    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
