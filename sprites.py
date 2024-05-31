# sprites.py
import pygame
import random
from settings import *


class Saw(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.mass = mass
        self.retention = 2
        self.bounce_stop = 50
        self.gravity = 10

        self.wall_thickness = WALL_THICKNESS
        self.radius = 50
        self.image = pygame.transform.scale(pygame.image.load('assets/Circular_tipped_saw_blade_sketch1.svg'),
                                            (self.radius, self.radius)).convert_alpha()

        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed_x = SAW_SPEED
        self.speed_y = SAW_SPEED

    def check_gravity(self):
        if self.rect.y < SCREEN_HEIGHT - self.radius - (self.wall_thickness):
            self.speed_y += self.gravity
        else:
            if self.speed_y > self.bounce_stop:
                self.speed_y = self.speed_y * -1 * self.retention


    def update(self):
        self.check_gravity()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        print("x: ", self.rect.x)
        print("y: ", self.rect.y)
        if self.rect.left < self.wall_thickness / 2 or self.rect.right > SCREEN_WIDTH - (self.wall_thickness / 2):
            self.speed_x = -self.speed_x
        if self.rect.top < self.wall_thickness / 2 or self.rect.bottom > SCREEN_HEIGHT - (self.wall_thickness / 2):
            self.speed_y = -self.speed_y


class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, (255, 0, 0), [0, 0, 30, 50])
        self.rect = self.image.get_rect(center=(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)))


class Walls:
    def __init__(self):
        self.wall_thickness = WALL_THICKNESS

    def draw(self, screen):
        left = pygame.draw.line(screen, 'white', (0, 0), (0, SCREEN_HEIGHT), self.wall_thickness)
        right = pygame.draw.line(screen, 'white', (SCREEN_WIDTH, 0), (SCREEN_WIDTH, SCREEN_HEIGHT), self.wall_thickness)
        top = pygame.draw.line(screen, 'white', (0, 0), (SCREEN_WIDTH, 0), self.wall_thickness)
        bottom = pygame.draw.line(screen, 'white', (0, SCREEN_HEIGHT), (SCREEN_WIDTH, SCREEN_HEIGHT),
                                  self.wall_thickness)
        return [left, right, top, bottom]
