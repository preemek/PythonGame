import pygame
from abc import ABC, abstractmethod

#uruchamianie okna
pygame.init()
screen = pygame.display.set_mode((1300,800))

#wczytywanie grafik
bg = pygame.image.load("img/background.png")
robo_walking = [pygame.image.load("img/Robot/character_robot_walk0.png"),pygame.image.load("img/Robot/character_robot_walk1.png"),pygame.image.load("img/Robot/character_robot_walk2.png"),
                pygame.image.load("img/Robot/character_robot_walk3.png"),pygame.image.load("img/Robot/character_robot_walk4.png"),pygame.image.load("img/Robot/character_robot_walk5.png"),
                pygame.image.load("img/Robot/character_robot_walk6.png"),pygame.image.load("img/Robot/character_robot_walk7.png")]
ladder_img = pygame.image.load("img/Tiles/fenceLow.png")
ground = pygame.image.load("img/groundIce.png")
climbing = [pygame.image.load("img/Robot/character_robot_climb0.png"), pygame.image.load("img/Robot/character_robot_climb1.png")]
bulletimg = pygame.image.load("img/number1.png")

#gracz
class Player:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.height = 180
        self.width = 160
        self.left = False
        self.right = False
        self.standing = True
        self.climbing = False
        self.shotting = False
        self.walk_position = 0
        self.climb_position = 0
        self.amo = 10
        self.__velocity = 15
        self.hitbox = (self.x + 10, self.y +70 , 160, 180)

    @property
    def velocity(self):
        return self.__velocity

    @velocity.setter
    def velocity(self, velocity):
        self.__velocity = velocity

    def draw(self, screen):
        if self.standing:
            screen.blit(robo_walking[0], (self.x, self.y))
        elif self.climbing:
            screen.blit(climbing[self.climb_position], (self.x, self.y))
            self.climb_position += 1
            if self.climb_position == 2:
                self.climb_position =0
        else:
            if self.walk_position < len(robo_walking):
                screen.blit(robo_walking[self.walk_position], (self.x, self.y))
                self.walk_position += 1
            else:
                screen.blit(robo_walking[0], (self.x, self.y))
                self.walk_position = 1

        self.hitbox = (self.x + 10, self.y + 70, 160, 180)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)



class Object(ABC):
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image

    @abstractmethod
    def draw(self, screen):
        pass

class Ladders(Object):
    def __init__(self,x,y,image):
        super().__init__(x, y, image)
        self.hitbox = (self.x + 5, self.y +40 , 70, 70)
        self.height = 70
        self.width = 70

    def draw(self,screen):
        screen.blit(self.image, (self.x, self.y))
        self.hitbox = (self.x, self.y, 70, 70)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

        screen.blit(self.image, (self.x, self.y + 50))
        self.hitbox = (self.x, self.y + 50, 70, 70)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

        screen.blit(self.image, (self.x, self.y + 100))
        self.hitbox = (self.x, self.y + 100, 70, 70)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)

        screen.blit(self.image, (self.x, self.y + 150))
        self.hitbox = (self.x, self.y + 150, 70, 70)
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

    def draw(self, screen):
        # if robot.right:
        screen.blit(self.image, (self.x + 50, self.y))
        print("hmm")
                # self.hitbox = (self.x, self.y, 70, 70)
                # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)
        # if robot.left:



def update_all():
    screen.blit(bg, (0,0))
    platform1.draw(screen)
    ladder.draw(screen)
    if robot.shotting and bullets[0].x < 1300:
        bullets[0].x += bullets[0].bull_velocity
        bullets[0].draw(screen)
    else:
        bullets[0].x = robot.x
        robot.shotting = False
    robot.draw(screen)
    pygame.display.update()



#loop
running = True

#instances
robot = Player(600,550,robo_walking[0])
ladder = Ladders(100, 580, ladder_img)
platform1 = Platform(0, ladder.y +10, ground)
bullet = Projectile(robot.x, robot.y+130, bulletimg)
bullets = list()
while robot.amo:
    bullets.append(bullet)
    robot.amo -= 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    def is_climbing():
        if robot.x + 40 <= ladder.x <= robot.x + 80  and robot.y < 340:
            robot.climbing = True
        else:
            robot.climbing = False

    is_climbing()

    if keys[pygame.K_RIGHT] and robot.x + 170 < 1300 and robot.climbing is False:
        robot.x += robot.velocity
        robot.standing = False
        robot.right = True
        if keys[pygame.K_SPACE]:
            robot.shotting = True
        # robot.shotting = True
        print("Pozycja robota x :{}".format(robot.x))
        print("Pozycja drabiny x :{}".format(ladder.x))

    elif keys[pygame.K_LEFT] and robot.x - 10 > 0 and robot.climbing is False:
        robot.x -= robot.velocity
        robot.standing = False
        if keys[pygame.K_SPACE]:
            robot.shotting = True
        print("Pozycja robota x :{}".format(robot.x))
        print("Pozycja drabiny x :{}".format(ladder.x))
        print("Pozycja robota y :{}".format(robot.y))

    elif keys[pygame.K_UP] and robot.x + 40 <= ladder.x <= robot.x + 80 and robot.y + 240 > ladder.y:
        robot.y -= robot.velocity
        robot.climbing = True
        robot.standing = False
        print("Pozycja robota y :{}".format(robot.y))
        print("Pozycja drabiny y :{}".format(ladder.y))
    elif keys[pygame.K_SPACE] and robot.climbing is False:
        robot.shotting = True
        # robot.shotting = True
        print("spacepressed")
    else:
        robot.standing = True
        robot.right = False

    update_all()






