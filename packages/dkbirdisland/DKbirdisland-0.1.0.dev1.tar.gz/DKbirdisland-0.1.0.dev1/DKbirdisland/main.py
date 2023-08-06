import pygame
import os
import sys
import random

main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_img(name):
    path = os.path.join(main_dir, "images", name)
    return pygame.image.load(path)


def game():
    pygame.display.set_caption("Donkey Kong: Bird Island")


    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 350
    GAME_SPEED = 20
    GROUND_WIDTH = 2 * SCREEN_WIDTH
    GROUND_HEIGHT = 35
    MIN_HEIGHT = 228
    SPEED_JUMP = 50
    GRAVITY = 9

    class Donkey(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)

            self.images_walk = [load_img('animations/Andar (1).png').convert_alpha(),
                                load_img('animations/Andar (2).png').convert_alpha(),
                                load_img('animations/Andar (3).png').convert_alpha(),
                                load_img('animations/Andar (4).png').convert_alpha(),
                                load_img('animations/Andar (5).png').convert_alpha(),
                                load_img('animations/Andar (6).png').convert_alpha()]

            self.images_jump = [load_img('animations/Jump (1).png').convert_alpha(),
                                load_img('animations/Jump (2).png').convert_alpha(),
                                load_img('animations/Jump (3).png').convert_alpha(),
                                load_img('animations/Jump (4).png').convert_alpha(),
                                load_img('animations/Jump (5).png').convert_alpha()]

            self.speed = SPEED_JUMP

            self.current_image = 0
            self.image = load_img('original.png').convert_alpha()
            self.rect = self.image.get_rect()
            self.rect[0] = 20
            self.rect[1] = 228

            

        def update(self):
            self.current_image = (self.current_image + 1) % 6
            self.image = self.images_walk[self.current_image]
            

            self.speed += GRAVITY
            self.rect[1] += self.speed

            if self.rect[1] > MIN_HEIGHT:
                self.rect[1] = MIN_HEIGHT
                self.speed = 0

        def jump(self):
            if self.rect[1] == MIN_HEIGHT:
                self.speed = -SPEED_JUMP

    class Ground(pygame.sprite.Sprite):
        def __init__(self, xpos):
            pygame.sprite.Sprite.__init__(self)

            self.image = load_img('ground.fw.png')
            self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

        def update(self):
            self.rect[0] -= GAME_SPEED

    class Obstacles(pygame.sprite.Sprite):
        def __init__(self, xpos):
            pygame.sprite.Sprite.__init__(self)

            self.images = [load_img('snake1.png').convert_alpha(),
                           load_img('barris.png').convert_alpha()]

            

            range = random.randrange(0, 2)

            self.image = self.images[range]

            if range == 0:
                self.image = pygame.transform.scale(self.image,(40, 70))
            elif range == 1:
                self.image = pygame.transform.scale(self.image, (73, 70))
            #else:
                #self.image = pygame.transform.scale(self.image, (73, 60))
                #obstacle_y = 60

            self.rect = self.image.get_rect()
            self.rect[0] = xpos
            self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT - 70


        def update(self):
            self.rect[0] -= GAME_SPEED

    def is_off_screen(sprite):
        return sprite.rect[0] < -(sprite.rect[2])

    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    BACKGROUND = load_img("background.png")

    donkey_group = pygame.sprite.Group()
    donkey = Donkey()
    donkey_group.add(donkey)

    ground_group = pygame.sprite.Group()

    for i in range(2):
        ground = Ground(GROUND_WIDTH * i)
        ground_group.add(ground)

    obstacle_group = pygame.sprite.Group()
    obstacle = Obstacles(800)
    obstacle_group.add(obstacle)

    clock = pygame.time.Clock()

    # Principal
    running = True
    while running:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    donkey.jump()

        screen.blit(BACKGROUND, (0, 0))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDTH - 50)
            ground_group.add(new_ground)

        if is_off_screen(obstacle_group.sprites()[0]):
            obstacle_group.remove(obstacle_group.sprites()[0])
            new_obstacle = Obstacles(random.randint(800, 1000))
            obstacle_group.add(new_obstacle)


        donkey_group.update()
        obstacle_group.update()
        ground_group.update()

        donkey_group.draw(screen)
        obstacle_group.draw(screen)
        ground_group.draw(screen)

        pygame.display.update()

        if pygame.sprite.groupcollide(donkey_group, obstacle_group, False, False, pygame.sprite.collide_mask):
            break


if __name__ == '__main__':
    game()
