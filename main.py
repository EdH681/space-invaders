import pygame
from keyboard import is_pressed
import time

pygame.init()
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

clock = pygame.time.Clock()
counter, text = 300, '10'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
tfont = pygame.font.SysFont('arial', 30)

# ====================window setup====================
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Space Invaders target practice')

icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

# images
body = pygame.image.load('assets/Black.png')
body = pygame.transform.scale(body, (1, 10))

projectile = pygame.image.load('assets/laser.png')

PLAYER = pygame.image.load('assets/player_ship.png')

enemy1 = pygame.image.load('assets/enemy.png')

shot = pygame.mixer.Sound('assets/laser_sound.mp3')

bang = pygame.mixer.Sound('assets/boom.wav')
bang.set_volume(0.1)

bang2 = pygame.mixer.Sound('assets/boom.mp3')

clear = pygame.mixer.Sound('assets/levelup.mp3')

# text
score = 0
font = pygame.font.SysFont('Helvetica', 20)

# ====================================================

print(bang.get_volume())

# ==========constants / defaults==========
x = 231
y = 450
projectile_x = 1000
projectile_y = 0
enemy_y = 50
enemy_x = 244
width = 25
height = 10
speed = 2
projectile_speed = 10
pause = 15
fireable = True
count = 0
enemy_speed = 0.5
instruction_comm = 0
enemy_offset = 50
enemy_instructions = ['right', 'down', 'left', 'down']
enemy_position = 'right'
timer_coords = (235, 20)
timer_colour = (255, 255, 255)

# ========================================
for a in range(1000000):
    globals()['state_%s' % a] = True


# functions


# left side
def enemy_follow_R(num, x, y):
    global enemy1, i, projectile_y, score
    x -= i * 50

    if globals()['state_%s' % num]:
        globals()['%s' % str(num)] = win.blit(enemy1, (x, y))
        globals()['hitbox_%s' % num] = (x, y, 22, 16)
        # pygame.draw.rect(win, (0, 255, 0), globals()['hitbox_%s' % num], 2)

    else:
        globals()['%s' % str(num)] = win.blit(body, (x, y))

    if x < projectile_x < x + 22 and y < projectile_y < y + 16 and globals()['state_%s' % num]:
        # print('hit left ' + str(globals()['%s' % str(num)]))
        projectile_y = -100
        bang.play()
        globals()['state_%s' % str(num)] = False
        score += 1
        print(score)


# right side
def enemy_follow_L(num, x, y):
    global enemy1, i, projectile_y, score
    if globals()['state_%s' % num] and i > 0:
        hit_box = (x, y, 22, 16)
        globals()['%s' % str(num)] = win.blit(enemy1, (x, y))
        #pygame.draw.rect(win, (255, 0, 0), hit_box, 2)
    else:
        globals()['%s' % str(num)] = win.blit(body, (x, y))

    if x < projectile_x < x + 22 and y < projectile_y < y + 16 and i > 0 and globals()['state_%s' % num]:
        # print('hit right ' + str(globals()['%s' % str(num)]))
        projectile_y = -100
        bang.play()
        globals()['state_%s' % str(num)] = False
        score += 1
        print(score)


def enemy_movement():
    global enemy_speed, enemy_x, enemy_position, enemy_y
    # print(enemy_position)
    # print(enemy_x)

    if enemy_position == 'right':
        enemy_x -= enemy_speed
        if enemy_x <= 170:
            enemy_position = 'left'

    if enemy_position == 'left':
        enemy_x += enemy_speed
        if enemy_x >= 300:
            enemy_position = 'right'

    if enemy_x >= 419 or enemy_x <= 71:
        enemy_y += 5


def shoot():
    global projectile_x, projectile_y, x, y, fireable, score, event

    if is_pressed('up') and fireable:
        fireable = False
        projectile_x = x + 19
        projectile_y = y + 30
        shot.play()
    if projectile_y < 0:
        fireable = True
    if projectile_y == 0:
        score -= 1
        bang.play()


def ship():
    global x, y
    win.blit(PLAYER, (x, y))


def user_input():
    global x, key_press, event
    if is_pressed('right') or event == pygame.JOYAXISMOTION:
        x += speed
    if is_pressed('left'):
        x -= speed


# ===game mainloop===

running = True

before = time.time()
while running:

    # moving the projectile
    projectile_y -= projectile_speed
    projectile_hit_box = (projectile_x, projectile_y, 3, 11)
    # pygame.draw.rect(win, (0, 0, 255), projectile_hit_box, 2)
    # adding items and updating window
    ship()

    text = font.render(('Score: ' + str(score)), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (250, 60)
    win.blit(text, textRect)

    if score % 35 == 0 and score != 0:
        clear.play()
        score += 1
        for a in range(1000000):
            globals()['state_%s' % a] = True

    for r in range(5):
        # print('r=', r)
        for i in range(4):
            enemy_multiplier = i + r
            # print((r*3)+enemy_multiplier)
            enemy_num = (r * 3) + enemy_multiplier
            enemy_follow_R(enemy_num, enemy_x, 50 + (enemy_y + (r * 50)))
            enemy_follow_L(enemy_num * 20, (enemy_x + (i * 50)), 50 + (enemy_y + (r * 50)))

    win.blit(projectile, (projectile_x, projectile_y))
    pygame.display.update()

    win.fill('black')

    # slowing down each iteration
    pygame.time.delay(pause)

    # checking for close button
    for event in pygame.event.get():


        if event.type == pygame.QUIT:
            running = False
        if counter > 0:
            timer_text = str(str((int(counter) // 60)) + ':' + str(int(counter) % 60)).rjust(3)

            if len(timer_text) == 3 and (int(counter) % 60) < 10:
                timer_text = (str((int(counter) // 60)) + ':0' + str(int(counter) % 60))
            elif len(timer_text) == 3 and (int(counter) % 60) > 10:
                timer_text += '0'
            if int(counter) % 60 < 10 and int(counter) // 60 == 0:
                timer_colour = (255, 0, 0)
        else:
            timer_text = "Time's up!"
            for a in range(1000000):
                globals()['state_%s' % a] = False
        if event.type == pygame.USEREVENT:
            counter -= 1
    win.blit(font.render(timer_text, True, timer_colour), timer_coords)
    # movement
    shoot()
    user_input()
    enemy_movement()
    clock.tick(144)
after = time.time()

print(-(before - after))
