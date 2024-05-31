# game.py
import pygame
from settings import *
from sprites import Saw, Balloon, Walls


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.Group()
        self.balloons = pygame.sprite.Group()
        self.saw = Saw()
        self.all_sprites.add(self.saw)
        for _ in range(NUM_BALLOONS):
            balloon = Balloon()
            self.all_sprites.add(balloon)
            self.balloons.add(balloon)
        self.walls = Walls()
        self.running = True
        self.score = 0

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
        hits = pygame.sprite.spritecollide(self.saw, self.balloons, True)
        self.score += len(hits)

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.walls.draw(self.screen)
        pygame.display.flip()
