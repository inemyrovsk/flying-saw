# game.py
import pygame
from settings import *
from sprites import Saw, Walls, Balloon, handle_balloon_collisions
import random

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.walls = Walls()
        self.saw = Saw(self.walls)
        self.all_sprites.add(self.saw)
        self.running = True
        self.score = 0
        self.balloons = pygame.sprite.Group()
        while len(self.balloons) < NUM_BALLOONS:
            new_balloon = Balloon(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50),
                                  walls=self.walls)
            self.balloons.add(new_balloon)
        self.all_sprites.add(self.balloons)
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.all_sprites.update()
        handle_balloon_collisions(self.balloons)
        hits = pygame.sprite.spritecollide(self.saw, self.balloons, True)
        self.score += len(hits)

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.walls.draw(self.screen)
        pygame.display.flip()
