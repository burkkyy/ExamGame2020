import pygame
import math
import random

# <editor-fold desc="Game init stuff">
pygame.init()
size = (700, 500)
clock = pygame.time.Clock()
run = True
win = pygame.display.set_mode(size)
win_rect = win.get_rect()
pygame.display.set_caption("Caleb's Space Game")
# </editor-fold>

# <editor-fold desc="Colors">
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# </editor-fold>

# <editor-fold desc="Game vars">
give_info = False
end_game = False
game_width = 2000
game_height = 2000
number_of_stars = 500
number_of_enemies = 6
enemy_health = 2
enemy_speed_multi = 4
player_life = 20
bullet_speed = 5
# </editor-fold>

# <editor-fold desc="Pictures and Sounds">
player_img = pygame.image.load("player_space_ship.png")
player_img = pygame.transform.scale(player_img, (50, 50))

enemy_img = pygame.image.load("enemy_space_ship.png")
enemy_img = pygame.transform.scale(enemy_img, (120, 60))

enemy_boss_img = pygame.image.load("enemy_boss_space_ship.png")
enemy_boss_img = pygame.transform.scale(enemy_boss_img, (100, 40))

Explosion = [
    pygame.image.load("Explosion1.png"),
    pygame.image.load("Explosion2.png"),
    pygame.image.load("Explosion3.png"),
    pygame.image.load("Explosion4.png"),
    pygame.image.load("Explosion5.png"),
    pygame.image.load("Explosion6.png"),
    pygame.image.load("Explosion7.png"),
    pygame.image.load("Explosion8.png"),
    pygame.image.load("Explosion9.png"),
    pygame.image.load("Explosion10.png"),
    pygame.image.load("Explosion11.png"),
    pygame.image.load("Explosion12.png"),
]

bullet_sound = pygame.mixer.Sound("shooting_sound.wav")
explosion_sound = pygame.mixer.Sound("SFX_Explosion_02.wav")
pygame.mixer.music.load("halo_theme.wav")
pygame.mixer.music.play(-1)
# </editor-fold>

# <editor-fold desc="Math formulas">


def ds(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def findrise(y1, y2):
    return y2 - y1


def findrun(x1, x2):
    return x2 - x1


def normalize(origin, mouse_pos):
    dis = ds(origin, mouse_pos)
    return findrise(origin[0], mouse_pos[0]) / dis, findrun(origin[1], mouse_pos[1]) / dis


def enemy_new_pos(top_rect_pos):
    global size, game_width, game_height, end_game
    enemy_w = enemy_boss_img.get_rect()[2]  # Enemy width
    enemy_h = enemy_boss_img.get_rect()[3]  # Enemy height
    origin = top_rect_pos  # Top left pos of game border

    x_side = random.randrange(0, 2)
    y_side = random.randrange(0, 2)

    if x_side:
        try:
            new_x = random.randrange(origin[0] + 50, 0 - enemy_w - 50)
        except:
            new_x = random.randrange(size[1] + enemy_w, origin[0] + game_width - enemy_w - 50)
    else:
        try:
            new_x = random.randrange(size[1] + enemy_w, origin[0] + game_width - enemy_w - 50)
        except:
            new_x = random.randrange(origin[0] + 50, 0 - enemy_w - 50)

    if y_side:
        try:
            new_y = random.randrange(origin[1] + 50, 0 - enemy_h - 50)
        except:
            new_y = random.randrange(size[1] + enemy_h, origin[1] + game_height - enemy_h - 50)
    else:
        try:
            new_y = random.randrange(size[1] + enemy_h, origin[1] + game_height - enemy_h - 50)
        except:
            new_y = random.randrange(origin[1] + 50, 0 - enemy_h - 50)

    print(new_x, new_y)
    return new_x, new_y
# </editor-fold>

# <editor-fold desc="Player Class">


class Player:
    def __init__(self, x, y, width, height, image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.original_image = image
        self.image = self.original_image.copy()
        self.image_rect = self.original_image.get_rect(center=win_rect.center)
        self.angle = 0

    def draw(self, window):
        window.blit(self.image, self.image_rect)
        pos = pygame.mouse.get_pos()
        self.angle = 360 - 90 - math.atan2(pos[1] - size[1]/2, pos[0] - size[0]/2)*180/math.pi
        self.rotate()

    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image_rect = self.image.get_rect(center=self.image_rect.center)
        self.angle += 1
# </editor-fold>

# <editor-fold desc="Game board class">


class GameBoard:
    def __init__(self, r, s, speed, player_rect):  # r is rect, s is size
        # <editor-fold desc="Velocities">
        self.up_vel = speed
        self.down_vel = -speed
        self.right_vel = -speed
        self.left_vel = speed
        # </editor-fold>

        # <editor-fold desc="Player info">
        self.player_rect = player_rect
        self.player_center = [int(player_rect[0] + player_rect[2]/2), int(player_rect[1] + player_rect[3]/2)]
        self.player_life = player_life
        self.health_bar = (3, size[1] - 13, self.player_life*10, 10)
        self.anti_health_bar = (3 + self.player_life * 10, size[0], 1, 10)
        self.score = 0
        # </editor-fold>

        # <editor-fold desc="Border rectangles">
        self.top_rect = pygame.Rect(r[0] - r[2] / 2, r[1] - r[3] / 2 - s, r[2] + s, s)
        self.right_rect = pygame.Rect(r[0] + r[2] / 2, r[1] - r[3] / 2, s, r[3] + s)
        self.bottom_rect = pygame.Rect(r[0] - r[2] / 2 - s, r[1] + r[3] / 2, r[2] + s, s)
        self.left_rect = pygame.Rect(r[0] - r[2] / 2 - s, r[1] - r[3] / 2 - s, s, r[3] + s)
        self.border_size = s
        self.top_rect_pos = (self.top_rect[0] + self.border_size, self.top_rect[1] + self.border_size)
        self.border = [
            self.top_rect,
            self.right_rect,
            self.bottom_rect,
            self.left_rect,
        ]
        # </editor-fold>

        # <editor-fold desc="Stars">
        self.star_list = []
        for i in range(number_of_stars):
            x = random.randrange(o[0] - game_width / 2, o[0] + game_width / 2)
            y = random.randrange(o[1] - game_height / 2, o[1] + game_height / 2)
            self.star_list.append([x, y, 2])
        # </editor-fold>

        # <editor-fold desc="Enemies">
        self.enemy_list = []
        self.enemy_health_list = []
        self.enemy_vel_x_list = []
        self.enemy_vel_y_list = []
        for i in range(number_of_enemies):
            x, y = enemy_new_pos(self.top_rect_pos)  # random pos
            self.enemy_list.append(pygame.Rect(x, y, enemy_img.get_rect()[2], enemy_img.get_rect()[3]))
            self.enemy_health_list.append(enemy_health)
            self.enemy_vel_x_list.append(0)
            self.enemy_vel_y_list.append(0)

        self.enemy_bounce_list = []
        self.enemy_bounce_health_list = []
        self.enemy_bounce_vel_x_list = []
        self.enemy_bounce_vel_y_list = []
        for i in range(number_of_enemies*2):
            x, y = enemy_new_pos(self.top_rect_pos)  # random pos
            self.enemy_bounce_list.append(pygame.Rect(x, y, enemy_img.get_rect()[2], enemy_img.get_rect()[3]))
            self.enemy_bounce_vel_x_list.append(random.randrange(-10, 10))  # Random speed x
            self.enemy_bounce_vel_y_list.append(random.randrange(-10, 10))  # Random speed y
            self.enemy_bounce_health_list.append(enemy_health)

        self.enemy_boss_list = []
        self.boss_score = 0
        # </editor-fold>

        self.bullets = []
        self.explosions = []  # x, y, timer, count
        self.move_objects = [
            self.border,
            self.star_list,
            self.enemy_list,
            self.enemy_bounce_list,
            self.enemy_boss_list,
            self.bullets,
            self.explosions,
        ]  # All non-player objects to do base move

    def update(self, window):
        # <editor-fold desc="Object draw">
        for border in self.border:
            pygame.draw.rect(window, RED, border)

        for star in self.star_list:
            pygame.draw.circle(window, WHITE, (star[0], star[1]), star[2])

        for enemy in self.enemy_list:
            window.blit(enemy_img, (enemy[0], enemy[1]))

        for enemy_bounce in self.enemy_bounce_list:
            window.blit(enemy_img, (enemy_bounce[0], enemy_bounce[1]))

        for bullet in self.bullets:
            pygame.draw.circle(window, RED, (int(bullet[0]), int(bullet[1])), 5)

        for explosion in self.explosions:
            explosion[2] += 1
            if explosion[2] >= 5:
                explosion[2] = 0
                explosion[3] += 1
                if explosion[3] >= 11:
                    self.explosions.remove(explosion)
            window.blit(Explosion[explosion[3]], (explosion[0], explosion[1]))
        # </editor-fold>

        # <editor-fold desc="Health bar draw">
        self.health_bar = (3, size[1] - 13, self.player_life * 10, 10)
        self.anti_health_bar = (3 + self.player_life*10, size[1] - 13, player_life*10 - self.player_life*10, 10)
        pygame.draw.rect(window, GREEN, self.health_bar)
        pygame.draw.rect(window, RED, self.anti_health_bar)
        # </editor-fold>

        # <editor-fold desc="Score board draw">
        font1 = pygame.font.Font("freesansbold.ttf", 16)
        text1 = font1.render(str("Score: " + str(self.score)), True, RED, BLACK)
        win.blit(text1, (3, 450))
        # </editor-fold>

        # Check if boss should spawn
        if self.boss_score // 10:
            self.boss_score = 0
            print("Spawn new boss")

        # Update self.top_rect_pos and move objects
        self.top_rect_pos = (self.top_rect[0] + self.border_size, self.top_rect[1] + self.border_size)
        self.move()

    def move(self):
        # <editor-fold desc="Enemies">
        for i in range(len(self.enemy_list)):
            # Set the speed
            self.enemy_vel_x_list[i], self.enemy_vel_y_list[i] = normalize(
                (self.enemy_list[i][0], self.enemy_list[i][1]), self.player_center
            )

            # Check for player collision
            if self.enemy_list[i].move(
                    self.enemy_vel_x_list[i], self.enemy_vel_y_list[i]
            ).colliderect(self.player_rect):
                # Add new explosion and play sound
                self.explosions.append([self.enemy_list[i][0], self.enemy_list[i][1], 0, 0])
                pygame.mixer.Sound.play(explosion_sound)

                # Decrease player life
                self.player_life -= 1

                # Set new random enemy pos
                self.enemy_list[i][0] = enemy_new_pos(self.top_rect_pos)[0]
                self.enemy_list[i][1] = enemy_new_pos(self.top_rect_pos)[1]

            # Check for wall collision
            collide_index = self.enemy_list[i].move(
                self.enemy_vel_x_list[i],
                self.enemy_vel_y_list[i],
            ).collidelist(self.border)

            # if no collision find path and move
            if collide_index == -1:
                self.enemy_list[i][0] += self.enemy_vel_x_list[i]*enemy_speed_multi
                self.enemy_list[i][1] += self.enemy_vel_y_list[i]*enemy_speed_multi

            else:
                # checks if enemy hit wall
                if collide_index == 0:
                    self.enemy_list[i][1] -= self.enemy_vel_y_list[i] * enemy_speed_multi
                if collide_index == 1:
                    self.enemy_list[i][0] -= self.enemy_vel_x_list[i] * enemy_speed_multi
                if collide_index == 2:
                    self.enemy_list[i][1] -= self.enemy_vel_y_list[i] * enemy_speed_multi
                if collide_index == 3:
                    self.enemy_list[i][0] -= self.enemy_vel_x_list[i] * enemy_speed_multi

        # Bouncing enemies
        for i in range(len(self.enemy_bounce_list)):
            # Check for player collision
            if self.enemy_bounce_list[i].move(
                    self.enemy_bounce_vel_x_list[i], self.enemy_bounce_vel_y_list[i]
            ).colliderect(self.player_rect):
                # Add new explosion and play sound
                self.explosions.append([self.enemy_bounce_list[i][0], self.enemy_bounce_list[i][1], 0, 0])
                pygame.mixer.Sound.play(explosion_sound)

                # Decrease player life
                self.player_life -= 1

                # Set new random enemy pos
                self.enemy_bounce_list[i][0] = enemy_new_pos(self.top_rect_pos)[0]
                self.enemy_bounce_list[i][1] = enemy_new_pos(self.top_rect_pos)[1]

            # Check for wall collision
            collide_index = self.enemy_bounce_list[i].move(
                self.enemy_bounce_vel_x_list[i],
                self.enemy_bounce_vel_y_list[i],
            ).collidelist(self.border)

            # if no collision find path and move
            if collide_index == -1:
                self.enemy_bounce_list[i][0] += self.enemy_bounce_vel_x_list[i]
                self.enemy_bounce_list[i][1] += self.enemy_bounce_vel_y_list[i]

            else:
                # checks if enemy hit wall
                if collide_index == 0:
                    self.enemy_bounce_vel_y_list[i] *= -1
                if collide_index == 1:
                    self.enemy_bounce_vel_x_list[i] *= -1
                if collide_index == 2:
                    self.enemy_bounce_vel_y_list[i] *= -1
                if collide_index == 3:
                    self.enemy_bounce_vel_x_list[i] *= -1
        # </editor-fold>

        # <editor-fold desc="Bullets">
        for bullet in self.bullets:
            bullet[0] += bullet[2]*50
            bullet[1] += bullet[3]*50

            # Checks to see if bullet collides with game border, not perfect detection
            for i in range(len(self.border)):
                if self.border[i].collidepoint((bullet[0], bullet[1])):
                    self.bullets.remove(bullet)

            # fixes first check by seeing if bullet is out of game range
            if bullet[0] < -100000 or bullet[0] > 100000 or bullet[1] < -100000 or bullet[1] > 100000:
                self.bullets.remove(bullet)

        for i in range(len(self.enemy_list)):
            for bullet in self.bullets:
                # Checks if bullet hits enemy
                if self.enemy_list[i].collidepoint((bullet[0], bullet[1])):
                    self.enemy_health_list[i] -= 1
                    self.bullets.remove(bullet)

            # checks if enemy[?] should be dead or not
            if self.enemy_health_list[i] <= 0:
                pygame.mixer.Sound.play(explosion_sound)
                self.score += 1
                self.boss_score += 1
                self.explosions.append([self.enemy_list[i][0], self.enemy_list[i][1], 0, 0])
                self.enemy_health_list[i] = enemy_health

                # Sets random new pos of dead enemy for revival
                self.enemy_list[i][0] = enemy_new_pos(self.top_rect_pos)[0]
                self.enemy_list[i][1] = enemy_new_pos(self.top_rect_pos)[1]

        for i in range(len(self.enemy_bounce_list)):
            for bullet in self.bullets:
                # Checks if bullet hits enemy
                if self.enemy_bounce_list[i].collidepoint((bullet[0], bullet[1])):
                    self.enemy_bounce_health_list[i] -= 1
                    self.bullets.remove(bullet)

            # checks if enemy[?] should be dead or not
            if self.enemy_bounce_health_list[i] <= 0:
                pygame.mixer.Sound.play(explosion_sound)
                self.score += 1
                self.boss_score += 1
                self.explosions.append([self.enemy_bounce_list[i][0], self.enemy_bounce_list[i][1], 0, 0])
                self.enemy_bounce_health_list[i] = enemy_health

                # Sets random new pos of dead enemy for revival
                self.enemy_bounce_list[i][0] = enemy_new_pos(self.top_rect_pos)[0]
                self.enemy_bounce_list[i][1] = enemy_new_pos(self.top_rect_pos)[1]
        # </editor-fold>

        # <editor-fold desc="Key events">
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if not self.top_rect.move(0, self.up_vel).colliderect(self.player_rect):
                for i in range(len(self.move_objects)):
                    for k in range(len(self.move_objects[i])):
                        self.move_objects[i][k][1] += self.up_vel
        if keys[pygame.K_a]:
            if not self.left_rect.move(self.left_vel, 0).colliderect(self.player_rect):
                for i in range(len(self.move_objects)):
                    for k in range(len(self.move_objects[i])):
                        self.move_objects[i][k][0] += self.left_vel
        if keys[pygame.K_s]:
            if not self.bottom_rect.move(0, self.down_vel).colliderect(self.player_rect):
                for i in range(len(self.move_objects)):
                    for k in range(len(self.move_objects[i])):
                        self.move_objects[i][k][1] += self.down_vel
        if keys[pygame.K_d]:
            if not self.right_rect.move(self.right_vel, 0).colliderect(self.player_rect):
                for i in range(len(self.move_objects)):
                    for k in range(len(self.move_objects[i])):
                        self.move_objects[i][k][0] += self.right_vel
        # </editor-fold>

    def shoot(self):
        pygame.mixer.Sound.play(bullet_sound)
        rise, run = normalize(self.player_center, pygame.mouse.get_pos())
        self.bullets.append(
            [self.player_center[0], self.player_center[1], rise, run]
        )
# </editor-fold>

# <editor-fold desc="Objects">


o = (size[0] / 2, size[1] / 2)  # Center of screen
player = Player(
    o[0] - 50 / 2,
    o[1] - 50 / 2,
    50,
    50,
    player_img,
)
game = GameBoard(
    (o[0], o[1], game_width, game_height),  # origin, width, height
    50,  # border rect size
    5,  # Speed of background
    player.rect,  # Player rectangle
)


def game_info():
    print("============================================================")
    print("Enemies: ", len(game.enemy_list))
    print("Bullets: ", len(game.bullets))
    print("Explosions: ", len(game.explosions))
# </editor-fold>

# <editor-fold desc="Main game loop">


while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                game.shoot()

    win.fill(BLACK)

    if game.player_life <=0:
        end_game = True

    if end_game:
        font = pygame.font.Font("freesansbold.ttf", 32)
        text = font.render("YOU DIED, GAME OVER", True, RED, BLACK)
        win.blit(text, (size[0] / 2 - 200, size[1] / 2))
    else:
        player.draw(win)
        game.update(win)

    # Game info print
    if give_info:
        game_info()

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
# </editor-fold>
