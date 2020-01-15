import pygame
import math
import random

pygame.init()

size = (700, 500)
clock = pygame.time.Clock()
run = True

win = pygame.display.set_mode(size)
win_rect = win.get_rect()
pygame.display.set_caption("Caleb's Space Game")

### Colors ###
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

### Game info vars ###
player_width = 50
player_height = 50
game_width = 2000
game_height = 2000
number_of_stars = 1000
number_of_enemies = 10

### Pictures ###
player_img = pygame.image.load("C:/Users/Caleb/Documents/Python/FinalGame/Pictures/Player_space_ship.png")
player_img = pygame.transform.scale(player_img, (50, 50))

enemy_img = pygame.image.load("C:/Users/Caleb/Documents/Python/FinalGame/Pictures/Enemy_space_ship.png")
enemy_img = pygame.transform.scale(enemy_img, (120, 60))

enemyboss_img = pygame.image.load("C:/Users/Caleb/Documents/Python/FinalGame/Pictures/enemy_boss_space_ship.png")
enemyboss_img = pygame.transform.scale(enemyboss_img, (100, 40))

defalt = pygame.image.load("C:/Users/Caleb/Documents/Python/FinalGame/Pictures/red_box.png")
defalt = pygame.transform.scale(defalt, (player_width, player_height))

def ds(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

class Object():
    def __init__(self, x=None, y=None, width=None, height=None, image=defalt):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if width and height:
            self.rect = pygame.Rect(x, y, width, height)

        self.image = image


class Player(Object):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.original_image = image
        self.image = self.original_image.copy()
        self.image_rect = self.original_image.get_rect(center=win_rect.center)
        self.angle = 0

    def draw(self, win):
        win.blit(self.image, self.image_rect)
        pos = pygame.mouse.get_pos()
        self.angle = 360 - 90 - math.atan2(pos[1] - size[1]/2, pos[0] - size[0]/2)*180/math.pi
        self.rotate()

    def rotate(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.image_rect = self.image.get_rect(center=self.image_rect.center)
        self.angle += 1


class Block(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)


class Enemy(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image=image)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))


class Enemy_Boss(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)


class GameBoard():
    def __init__(self, r, s, speed, player, star_list, enemy_list, enemy_boss):  # r is rect, s is size
        ### Border rectangles ###
        self.top_rect = pygame.Rect(r[0] - r[2] / 2, r[1] - r[3] / 2 - s, r[2] + s, s)
        self.right_rect = pygame.Rect(r[0] + r[2] / 2, r[1] - r[3] / 2, s, r[3] + s)
        self.bottom_rect = pygame.Rect(r[0] - r[2] / 2 - s, r[1] + r[3] / 2, r[2] + s, s)
        self.left_rect = pygame.Rect(r[0] - r[2] / 2 - s, r[1] - r[3] / 2 - s, s, r[3] + s)

        ### Images ###
        self.player_rect = player
        self.enemy_list = enemy_list
        self.enemy_boss = enemy_boss

        ### Circle objects ###
        self.star_list = star_list

        ### Rectangle objects ###
        self.border = [
            self.top_rect,
            self.right_rect,
            self.bottom_rect,
            self.left_rect,
        ]

        self.move_objects = [
            self.border,
            self.star_list,
        ]

        self.move_images = [
            self.enemy_list,
            #self.enemy_boss,
        ]

        ### Velocitys ###
        self.up_vel = speed
        self.down_vel = -speed
        self.right_vel = -speed
        self.left_vel = speed

    def draw(self, win):
        for i in self.border:
            pygame.draw.rect(win, RED, i)

        for i in self.star_list:
            pygame.draw.circle(win, WHITE, (i[0], i[1]), i[2])

        for i in self.enemy_list:
            i.draw(win)

        self.move()

    def move(self):
        keys = pygame.key.get_pressed()
        '''
        for i in range(len(self.border_list)):
            self.border_list[i][0,1] += self._vel
        '''
        if keys[pygame.K_w]:
            for i in range(len(self.move_objects)):
                for k in range(len(self.move_objects[i])):
                    self.move_objects[i][k][1] += self.up_vel

            for i in self.move_images:
                for k in i:
                    k.y += self.up_vel

        if keys[pygame.K_a]:
            for i in range(len(self.move_objects)):
                for k in range(len(self.move_objects[i])):
                    self.move_objects[i][k][0] += self.left_vel

            for i in self.move_images:
                for k in i:
                    k.x += self.left_vel

        if keys[pygame.K_s]:
            for i in range(len(self.move_objects)):
                for k in range(len(self.move_objects[i])):
                    self.move_objects[i][k][1] += self.down_vel

            for i in self.move_images:
                for k in i:
                    k.y += self.down_vel

        if keys[pygame.K_d]:
            for i in range(len(self.move_objects)):
                for k in range(len(self.move_objects[i])):
                    self.move_objects[i][k][0] += self.right_vel

            for i in self.move_images:
                for k in i:
                    k.x += self.right_vel


### Defining vars ###
o = (size[0] / 2, size[1] / 2)  # Center of screen

star_list = []
star_radius = 2
for i in range(number_of_stars):
    x = random.randrange(o[0] - game_width / 2, o[0] + game_width / 2)
    y = random.randrange(o[1] - game_height / 2, o[1] + game_height / 2)
    star_list.append([x, y, star_radius])

player = Player(
    o[0] - player_width / 2,
    o[1] - player_height / 2,
    player_width,
    player_height,
    player_img,
)

enemy_list = []
for i in range(number_of_enemies):
    x = random.randrange(o[0] - game_width / 2, o[0] + game_width / 2)
    y = random.randrange(o[1] - game_height / 2, o[1] + game_height / 2)
    enemy_list.append(Enemy(x, y, enemy_img))

enemy_boss = Enemy_Boss(0, 0, 0, 0)

game = GameBoard(
    (o[0], o[1], game_width, game_height),  # origin, width, height
    50,  # border rect size
    5,  # Speed
    player.rect,  # Player rectangle
    star_list,  # List of stars
    enemy_list,  # List of all the enemies
    enemy_boss,  # Just the boss
)

### Main Game Loop ###
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.fill(BLACK)

    ### Draw Stuff ###
    player.draw(win)
    game.draw(win)
    ### End Draw   ###
    
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
