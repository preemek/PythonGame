import pygame, time, random
from abc import ABC, abstractmethod

#uruchamianie okna
pygame.init()
screen = pygame.display.set_mode((1300,800))

#wczytywanie grafik
bg = pygame.image.load("img/background.png")
robo_stay = pygame.image.load("img/Robot/character_robot_wide.png")
robo_walking_right= [pygame.image.load("img/Robot/right/character_robot_walk0.png"),pygame.image.load("img/Robot/right/character_robot_walk1.png"),pygame.image.load("img/Robot/right/character_robot_walk2.png"),
                pygame.image.load("img/Robot/right/character_robot_walk3.png"),pygame.image.load("img/Robot/right/character_robot_walk4.png"),pygame.image.load("img/Robot/right/character_robot_walk5.png"),
                pygame.image.load("img/Robot/right/character_robot_walk6.png"),pygame.image.load("img/Robot/right/character_robot_walk7.png")]
robo_walking_left= [pygame.image.load("img/Robot/left/character_robot_walk0.png"),pygame.image.load("img/Robot/left/character_robot_walk1.png"),pygame.image.load("img/Robot/left/character_robot_walk2.png"),
                pygame.image.load("img/Robot/left/character_robot_walk3.png"),pygame.image.load("img/Robot/left/character_robot_walk4.png"),pygame.image.load("img/Robot/left/character_robot_walk5.png"),
                pygame.image.load("img/Robot/left/character_robot_walk6.png"),pygame.image.load("img/Robot/left/character_robot_walk7.png")]
ladder_img = pygame.image.load("img/Tiles/fenceLow.png")
ground = pygame.image.load("img/groundIce.png")
climbing = [pygame.image.load("img/Robot/character_robot_climb0.png"), pygame.image.load("img/Robot/character_robot_climb1.png")]
bulletimg = [pygame.image.load("img/number1.png"), pygame.image.load("img/number2.png")]
attack_img = pygame.image.load("img/Robot/character_robot_attackKick.png")

#music
pygame.mixer.music.load("mp3/kungfu.mp3")
pygame.mixer.music.play()

#pozycje grafik
bg_x = 0
bg_y = 0
bg_x2 = 1300
bg_y2 = 0
start_scroll_when_right = 950
start_scroll_when_left = 350

#graczz
class Player:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.height = self.image.get_height()
        self.width = self.image.get_width()
        self.left = False
        self.right = False
        self.standing = True
        self.climbing = False
        self.shotting = False
        self.stand_walk = False
        self.on_ladder = False #stoi na drabinie bez ruchu
        self.walk_position = 0
        self.climb_position = 0
        self.amo = 10
        self.__velocity = 15
        self.hitbox = (self.x + 10, self.y + 70 , self.width, self.height)

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity):
        self.__velocity = velocity

    def draw(self, screen):
        if self.standing and self.shotting is False:
            screen.blit(robo_stay, (self.x, self.y))
        elif self.climbing and self.on_ladder is False:
            screen.blit(climbing[self.climb_position], (self.x, self.y))
            self.climb_position += 1
            if self.climb_position == 2:
                self.climb_position = 0
        elif self.shotting:
            screen.blit(attack_img, (self.x, self.y))
        elif self.climbing and self.on_ladder is True:
            screen.blit(climbing[0], (self.x, self.y))
        else:
            if robot.right:
                if self.walk_position < len(robo_walking_right):
                    screen.blit(robo_walking_right[self.walk_position], (self.x, self.y))
                    self.walk_position += 1
                else:
                    screen.blit(robo_walking_right[0], (self.x, self.y))
                    self.walk_position = 1
            if robot.left:
                if self.walk_position < len(robo_walking_right):
                    screen.blit(robo_walking_left[self.walk_position], (self.x, self.y))
                    self.walk_position += 1
                else:
                    screen.blit(robo_walking_left[0], (self.x, self.y))
                    self.walk_position = 1

        self.hitbox = (self.x + 10, self.y + 70, 160, 180)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)



class Object(ABC):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.height = self.image.get_height()
        self.width = self.image.get_width()

    @abstractmethod
    def draw(self, screen):
        pass

class Ladders(Object):
    def __init__(self,x,y,image):
        super().__init__(x, y, image)
        self.part1_reach = self.y
        self.part2_reach = self.y + 50
        self.part3_reach = self.y + 100
        self.part4_reach = self.y + 150
        self.hitbox = (self.x, self.y, self.width, self.height)

    def draw(self,screen):
        screen.blit(self.image, (self.x, self.part1_reach))
        self.hitbox = (self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

        screen.blit(self.image, (self.x, self.part2_reach))
        self.hitbox = (self.x, self.y + 50, self.width, self.height)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

        screen.blit(self.image, (self.x, self.part3_reach))
        self.hitbox = (self.x, self.y + 100, self.width, self.height)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

        screen.blit(self.image, (self.x, self.part4_reach))
        self.hitbox = (self.x, self.y + 150, self.width, self.height)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

class Platform(Object):
    def __init__(self, x, y, image):
        super().__init__(x,y,image)
        self.hitbox = (self.x, self.y, 1300, 10)

    def draw(self,screen):
        pygame.draw.rect(screen, (0, 0, 0), self.hitbox, 10)

class Projectile(Object):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        # self.hitbox = (self.x, self.y, image.get_width(), image.get_height())
        self.bull_velocity = 30
        self.on_way = False

    def draw(self, screen):
        # if robot.right:
        screen.blit(self.image, (self.x + 50, self.y))
                # self.hitbox = (self.x, self.y, 70, 70)
                # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)
        # if robot.left:



def update_all():
    screen.blit(bg, (bg_x, bg_y))
    screen.blit(bg, (bg_x2, bg_y2))
    platform1.draw(screen)
    ladder.draw(screen)
    for m in range(len(bullets)):
        if bullets[m].on_way is True and bullets[m].x < 1300:
            bullets[m].x += bullets[m].bull_velocity
            bullets[m].draw(screen)
        else:
            bullets[m].on_way = False
            bullets[m].x = robot.x
            bullets[m].y = robot.y +130


    robot.draw(screen)
    pygame.display.update()

def coming_bullets():
    for i in range(len(bullets)):
        if bullets[i].on_way is True:
            if i == 9 and bullets[0].on_way is False:
                bullets[0].on_way = True
                # print("w drodze {}".format(i))
                break
            elif i == 9 and bullets[0].on_way is True:
                # print("cos")
                break
            elif bullets[i + 1].on_way is False:
                bullets[i + 1].on_way = True
                # print("w drodze {}".format(i + 1))
                break
            else:
                continue
        else:
            bullets[0].on_way = True
            # for m in range(len(bullets)):
            #     print("{}".format(bullets[m].on_way))
            # print("w drodze {}".format(i))
            break

def is_climbing():
    if robot.x + 40 <= ladder.x <= robot.x + 80 and ladder.part4_reach + 70 > robot.y + 250 > ladder.part1_reach:
        robot.climbing = True
    else:
        robot.climbing = False
        robot.on_ladder = False

def is_shooting():
    if keys[pygame.K_SPACE] and robot.climbing is False:
        robot.shotting = True
    else:
        robot.shotting = False




#loop
running = True

#instances
robot = Player(550,550,robo_walking_right[0])
platform1 = Platform(0, 580, ground)
ladder = Ladders(100, platform1.y, ladder_img)
bullets = list()

for i in range(robot.amo):
    bullet = Projectile(robot.x, robot.y + 130, random.choice(bulletimg))
    bullets.append(bullet)
    robot.amo -= 1


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    is_climbing()
    is_shooting()

    if keys[pygame.K_RIGHT] and bg_x2 >= -5 and robot.climbing is False and robot.x + 170 < 1300:
        if robot.climbing is False:
            if robot.x > start_scroll_when_right and bg_x2 > 0:
                bg_x -= robot.velocity
                bg_x2 -= robot.velocity
            else:
                robot.x += robot.velocity
                robot.standing = False
                robot.right = True
                if keys[pygame.K_SPACE]:
                    coming_bullets()
        robot.right = True
        robot.left = False
        print("Pozycja BG x :{}".format(bg_x2))
        print("Pozycja robota x :{}".format(robot.x))
        print("Pozycja drabiny x :{}".format(ladder.x))

    elif keys[pygame.K_LEFT] and bg_x <= 0 and robot.x - 10 > 0 and robot.climbing is False:
        if robot.climbing is False:
            if robot.x < start_scroll_when_left and bg_x < 0:
                bg_x += robot.velocity
                bg_x2 += robot.velocity
            else:
                robot.x -= robot.velocity
                robot.standing = False
                robot.right = True
                if keys[pygame.K_SPACE]:
                    coming_bullets()
        robot.right = True
        robot.left = False
        # if robot.climbing is False:
        #     robot.x -= robot.velocity
        #     robot.standing = False
        #     if keys[pygame.K_SPACE]:
        #         coming_bullets()
        robot.right = False
        robot.left = True
        print("Scroll left{}".format(start_scroll_when_left))
        print("Pozycja robota x :{}".format(robot.x))
        print("Pozycja BG x :{}".format(bg_x))
        print("Pozycja robota y :{}".format(robot.y))
    elif keys[pygame.K_DOWN] and robot.x + 40 <= ladder.x <= robot.x + 80 and ladder.part4_reach + 70 > robot.y + 250 >= ladder.part1_reach - 10:
        robot.y += robot.velocity
        robot.climbing = True
        robot.standing = False
        robot.on_ladder = False
        print("Pozycja robota y :{}".format(robot.y))
        print("Pozycja drabiny y :{}".format(ladder.y))

    elif keys[pygame.K_UP] and robot.x + 40 <= ladder.x <= robot.x + 80 and ladder.part4_reach + 70 >= robot.y + 250 > ladder.part1_reach:
        robot.y -= robot.velocity
        robot.climbing = True
        robot.standing = False
        robot.on_ladder = False
        print("Pozycja robota y :{}".format(robot.y))
        print("Pozycja drabiny y :{}".format(ladder.y))

    elif keys[pygame.K_SPACE] and robot.climbing is False:
        # robot.shotting = True
        coming_bullets()
    else:
        if robot.climbing is True:
            robot.on_ladder = True
        else:
            robot.standing = True




    update_all()