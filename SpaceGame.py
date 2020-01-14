import pygame
import math
import random

pygame.init()

size = (700, 500)
clock = pygame.time.Clock()
run = True

win = pygame.display.set_mode(size)
pygame.display.set_caption("Caleb's Space Game")

### Colors ###
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

player_width = 50
player_height = 50
game_width = 2000
game_height = 2000
number_of_stars = 1000

### Pictures ###
player_img = pygame.image.load("C:/Users/Caleb/Documents/Python/FinalGame/Pictures/Player_space_ship.png")
player_img = pygame.transform.scale(player_img, (50, 50))

enemy_img = pygame.image.load("C:/Users/Caleb/Documents/Python/FinalGame/Pictures/Enemy_space_ship.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 30))

enemyboss_img = pygame.image.load("C:/Users/Caleb/Documents/Python/FinalGame/Pictures/enemy_boss_space_ship.png")
enemyboss_img = pygame.transform.scale(enemyboss_img, (100, 40))

defalt = pygame.image.load("C:/Users/Caleb/Documents/Python/FinalGame/Pictures/red_box.png")
defalt = pygame.transform.scale(defalt, (player_width, player_height))


class Object():
    def __init__(self, x=None, y=None, width=None, height=None, img=defalt):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if width and height:
            self.rect = pygame.Rect(x, y, width, height)

        self.img = img


class Player(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class Block(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)


class Enemy(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)


class Enemy_Boss(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)


class GameBoard():
    def __init__(self, r, s, speed, player=None, star_list=None, enemy=None):  # r is rect, s is size
        ### Border rectangles ###
        self.top_rect = pygame.Rect(r[0] - r[2] / 2, r[1] - r[3] / 2 - s, r[2] + s, s)
        self.right_rect = pygame.Rect(r[0] + r[2] / 2, r[1] - r[3] / 2, s, r[3] + s)
        self.bottom_rect = pygame.Rect(r[0] - r[2] / 2 - s, r[1] + r[3] / 2, r[2] + s, s)
        self.left_rect = pygame.Rect(r[0] - r[2] / 2 - s, r[1] - r[3] / 2 - s, s, r[3] + s)

        ### Player rect ###
        self.player_rect = player

        ### Draw objects ###
        self.star_list = star_list
        self.enemey = enemy

        ### All object lists ###
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

        if keys[pygame.K_a]:
            for i in range(len(self.move_objects)):
                for k in range(len(self.move_objects[i])):
                    self.move_objects[i][k][0] += self.left_vel

        if keys[pygame.K_s]:
            for i in range(len(self.move_objects)):
                for k in range(len(self.move_objects[i])):
                    self.move_objects[i][k][1] += self.down_vel

        if keys[pygame.K_d]:
            for i in range(len(self.move_objects)):
                for k in range(len(self.move_objects[i])):
                    self.move_objects[i][k][0] += self.right_vel


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
)

game = GameBoard(
    (o[0], o[1], game_width, game_height),  # origin, width, height
    50,  # border rect size
    5,  # Speed
    player.rect,  # Player rectangle
    star_list,
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
    print("Working")
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
