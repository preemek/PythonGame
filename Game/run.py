import pygame

#uruchamianie okna
pygame.init()
screen = pygame.display.set_mode((1300,800))

#wczytywanie grafik
bg = pygame.image.load("img/background.png")
robo_walking = [pygame.image.load("img/Robot/character_robot_walk0.png"),pygame.image.load("img/Robot/character_robot_walk1.png"),pygame.image.load("img/Robot/character_robot_walk2.png"),
                pygame.image.load("img/Robot/character_robot_walk3.png"),pygame.image.load("img/Robot/character_robot_walk4.png"),pygame.image.load("img/Robot/character_robot_walk5.png"),
                pygame.image.load("img/Robot/character_robot_walk6.png"),pygame.image.load("img/Robot/character_robot_walk7.png")]
ladder_img = pygame.image.load("img/Tiles/fenceLow.png")

#gracz
class Player:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.left = False
        self.right = False
        self.standing = True
        self.walk_position = 0
        self.velocity = 20
        self.hitbox = (self.x + 10, self.y +70 , 160, 180)

    def draw(self, screen):
        if self.standing:
            screen.blit(robo_walking[0], (self.x, self.y))
        else:
            if self.walk_position < len(robo_walking):
                    screen.blit(robo_walking[self.walk_position], (self.x, self.y))
                    self.walk_position += 1
            else:
                screen.blit(robo_walking[0], (self.x, self.y))
                self.walk_position = 1

            # if self.walkCount == 0:
            #     screen.blit(robo_walking[0], (self.x, self.y))
            #     self.walkCount += 1
            # elif self.walkCount == 1:
            #     screen.blit(robo_walking[1], (self.x, self.y))
            #     self.walkCount += 1
            # elif self.walkCount == 2:
            #     screen.blit(robo_walking[2], (self.x, self.y))
            #     self.walkCount +=1
            # elif self.walkCount == 3:
            #     screen.blit(robo_walking[3], (self.x, self.y))
            #     self.walkCount +=1
            # elif self.walkCount == 4:
            #     screen.blit(robo_walking[4], (self.x, self.y))
            #     self.walkCount +=1
            # elif self.walkCount == 5:
            #     screen.blit(robo_walking[5], (self.x, self.y))
            #     self.walkCount =0
        self.hitbox = (self.x + 10, self.y + 70, 160, 180)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)


class Object:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.hitbox = (self.x + 5, self.y +40 , 160, 180)

    def draw(self, screen):

        screen.blit(ladder_img, (self.x, self.y))
        screen.blit(ladder_img, (self.x, self.y+50))
        screen.blit(ladder_img, (self.x, self.y + 100))

        self.hitbox = (self.x + 5, self.y +40 , 160, 180)
        pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 1)



def update_all():
    screen.blit(bg, (0,0))
    ladder.draw(screen)
    robot.draw(screen)
    pygame.display.update()



#loop

running = True

robot = Player(600,550,2,2)
ladder = Object(100,550,2,2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and robot.x + 170 < 1300:
        robot.x += robot.velocity
        robot.standing = False
    elif keys[pygame.K_LEFT] and robot.x - 10 > 0:
        robot.x -= robot.velocity
        robot.standing = False
    else:
        robot.standing = True

    update_all()
    print("taktowanie")


