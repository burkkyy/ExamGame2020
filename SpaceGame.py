import pygame
import math
import random

# init stuff
pygame.init()
size = (700, 500)
clock = pygame.time.Clock()
run = True
win = pygame.display.set_mode(size)
win_rect = win.get_rect()
pygame.display.set_caption("Caleb's Space Game")

# Colors ###
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Game info vars ###
game_width = 2000
game_height = 2000
number_of_stars = 1000
number_of_enemies = 10

# picture
player_img = pygame.image.load("C:/Users/Caleb/Documents/Python/FinalGame/Pictures/Player_space_ship.png")
player_img = pygame.transform.scale(player_img, (50, 50))

enemy_img = pygame.image.load("C:/Users/Caleb/Documents/Python/FinalGame/Pictures/Enemy_space_ship.png")
enemy_img = pygame.transform.scale(enemy_img, (120, 60))

enemy_boss_img = pygame.image.load("C:/Users/Caleb/Documents/Python/FinalGame/Pictures/enemy_boss_space_ship.png")
enemy_boss_img = pygame.transform.scale(enemy_boss_img, (100, 40))

# Formulas
def ds(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


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


class GameBoard:
    def __init__(self, r, s, speed, player_rect):  # r is rect, s is size
        # Player rect ###
        self.player_rect = player_rect

        # Border rectangles ###
        self.top_rect = pygame.Rect(r[0] - r[2] / 2, r[1] - r[3] / 2 - s, r[2] + s, s)
        self.right_rect = pygame.Rect(r[0] + r[2] / 2, r[1] - r[3] / 2, s, r[3] + s)
        self.bottom_rect = pygame.Rect(r[0] - r[2] / 2 - s, r[1] + r[3] / 2, r[2] + s, s)
        self.left_rect = pygame.Rect(r[0] - r[2] / 2 - s, r[1] - r[3] / 2 - s, s, r[3] + s)
        self.border = [
            self.top_rect,
            self.right_rect,
            self.bottom_rect,
            self.left_rect,
        ]

        # Stars and enemies ###
        self.star_list = []
        for i in range(number_of_stars):
            star_radius = 2
            x = random.randrange(o[0] - game_width / 2, o[0] + game_width / 2)
            y = random.randrange(o[1] - game_height / 2, o[1] + game_height / 2)
            self.star_list.append([x, y, star_radius])
        self.enemy_list = []
        for i in range(number_of_enemies):
            x = random.randrange(o[0] - game_width / 2, o[0] + game_width / 2)
            y = random.randrange(o[1] - game_height / 2, o[1] + game_height / 2)
            self.enemy_list.append(pygame.Rect(x, y, enemy_img.get_rect()[2], enemy_img.get_rect()[3]))

        # All objects to move ###
        self.move_objects = [
            self.border,
            self.star_list,
            self.enemy_list,
        ]

        # Velocities ###
        self.up_vel = speed
        self.down_vel = -speed
        self.right_vel = -speed
        self.left_vel = speed

    def draw(self, window):
        for i in self.border:
            pygame.draw.rect(win, RED, i)
        for i in self.star_list:
            pygame.draw.circle(win, WHITE, (i[0], i[1]), i[2])
        for i in self.enemy_list:
            window.blit(enemy_img, (i[0], i[1]))
        self.move()

    def move(self):
        # Enemy ui movement
        for enemy in self.enemy_list:
            if enemy.move(1, 0).collidelist(self.border) == -1:
                enemy[0] += 1

        # Base movement for everything
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


# Defining vars ###
o = (size[0] / 2, size[1] / 2)  # Center of screen

player = Player(
    o[0] - player_img.get_rect()[2] / 2,
    o[1] - player_img.get_rect()[3] / 2,
    player_img.get_rect()[2],
    player_img.get_rect()[3],
    player_img,
)

game = GameBoard(
    (o[0], o[1], game_width, game_height),  # origin, width, height
    50,  # border rect size
    5,  # Speed
    player.rect,  # Player rectangle
)

# Main Game Loop ###
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.fill(BLACK)
    player.draw(win)  # Player draw
    game.draw(win)  # Everything but player draw
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
