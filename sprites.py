# sprites.py
import os

import pygame
import random
import math
from settings import *
class Saw(pygame.sprite.Sprite):
    def __init__(self, walls):
        super().__init__()
        self.walls = walls
        self.retention = 1.34
        self.gravity = GRAVITY
        self.damping = 0.99
        self.radius = 50
        self.image = pygame.transform.scale(pygame.image.load('assets/Circular_tipped_saw_blade_sketch1.svg'), (self.radius, self.radius)).convert_alpha()
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.speed_x = 0
        self.speed_y = 0
        self.dragging = False
        self.start_pos = None
        self.MAX_SPEED_X = 20
        self.MAX_SPEED_Y = 20
    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self.start_pos = pygame.Vector2(event.pos)
                self.speed_x = 0
                self.speed_y = 0
        elif event.type == pygame.MOUSEBUTTONUP and self.dragging:
            self.dragging = False
            end_pos = pygame.Vector2(event.pos)
            drag_vector = (self.start_pos - end_pos) * 0.1
            self.speed_x, self.speed_y = drag_vector.x, drag_vector.y
            self.constrain_speed()
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.rect.center = event.pos

    def update(self):
        if not self.dragging:
            self.apply_gravity()
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            self.walls.check_collision_with_line(self)
            self.apply_damping()
            self.check_bounds()

    def constrain_speed(self):
        """ Ensure the speed does not exceed maximum limits. """
        if abs(self.speed_x) > self.MAX_SPEED_X:
            self.speed_x = self.MAX_SPEED_X if self.speed_x > 0 else -self.MAX_SPEED_X
        if abs(self.speed_y) > self.MAX_SPEED_Y:
            self.speed_y = self.MAX_SPEED_Y if self.speed_y > 0 else -self.MAX_SPEED_Y

    def apply_gravity(self):
        if self.rect.bottom < SCREEN_HEIGHT - self.walls.wall_thickness:
            self.speed_y += self.gravity

    def apply_damping(self):
        self.speed_x *= self.damping
        self.speed_y *= self.damping
        self.constrain_speed()

    def check_bounds(self):
        if self.rect.left < self.walls.wall_thickness:
            self.rect.left = self.walls.wall_thickness
            self.speed_x = -self.speed_x * self.retention
        elif self.rect.right > SCREEN_WIDTH - self.walls.wall_thickness:
            self.rect.right = SCREEN_WIDTH - self.walls.wall_thickness
            self.speed_x = -self.speed_x * self.retention
        if self.rect.top < self.walls.wall_thickness:
            self.rect.top = self.walls.wall_thickness
            self.speed_y = -self.speed_y * self.retention
        elif self.rect.bottom > SCREEN_HEIGHT - self.walls.wall_thickness:
            self.rect.bottom = SCREEN_HEIGHT - self.walls.wall_thickness
            self.speed_y = -self.speed_y * self.retention


class Balloon(pygame.sprite.Sprite):
    def __init__(self, x, y, radius=25, walls=''):
        super().__init__()
        self.walls = walls
        self.radius = radius
        self.gravity = GRAVITY  # Gravity effect
        self.speed_y = 0
        self.speed_x = 0  # Add horizontal speed
        self.wall_thickness = WALL_THICKNESS
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        self.image = pygame.transform.scale(pygame.image.load('assets/ballons/' + random.choice(os.listdir('assets/ballons'))), (self.radius * 2, self.radius * 2)).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.pos = pygame.Vector2(self.rect.center)


    def apply_gravity(self):
        if self.rect.bottom < SCREEN_HEIGHT - self.wall_thickness:
            self.speed_y += self.gravity
        else:
            self.rect.bottom = SCREEN_HEIGHT - self.wall_thickness
            self.speed_y = -self.speed_y * 0.8  # bounce effect with retention

        if self.rect.left < self.wall_thickness:
            self.rect.left = self.wall_thickness
            self.speed_x = -self.speed_x * 0.8
        elif self.rect.right > SCREEN_WIDTH - self.wall_thickness:
            self.rect.right = SCREEN_WIDTH - self.wall_thickness
            self.speed_x = -self.speed_x * 0.8

    def update(self):
        self.apply_gravity()
        self.pos.x += self.speed_x
        self.pos.y += self.speed_y
        self.rect.center = self.pos
        self.walls.check_collision_with_line(self)


def handle_balloon_collisions(balloons):
    for balloon in balloons:
        for other_balloon in balloons:
            if balloon != other_balloon and balloon.pos.distance_to(other_balloon.pos) < balloon.radius + other_balloon.radius:
                resolve_collision(balloon, other_balloon)

def resolve_collision(balloon1, balloon2):
    # Calculate the vector between the balloons
    collision_vector = balloon1.pos - balloon2.pos
    distance = collision_vector.length()

    if distance == 0:
        distance = 1  # Prevent division by zero

    overlap = 0.5 * (balloon1.radius + balloon2.radius - distance)

    # Normalize the collision vector
    collision_vector.normalize_ip()

    # Displace the balloons based on the overlap
    balloon1.pos += collision_vector * overlap
    balloon2.pos -= collision_vector * overlap

    # Update the rect positions
    balloon1.rect.center = balloon1.pos
    balloon2.rect.center = balloon2.pos

    # Calculate velocities along the collision vector
    velocity1 = pygame.Vector2(balloon1.speed_x, balloon1.speed_y)
    velocity2 = pygame.Vector2(balloon2.speed_x, balloon2.speed_y)
    velocity1_along_collision = velocity1.dot(collision_vector)
    velocity2_along_collision = velocity2.dot(collision_vector)

    # Swap the velocities along the collision vector
    new_velocity1 = velocity1 - collision_vector * velocity1_along_collision + collision_vector * velocity2_along_collision
    new_velocity2 = velocity2 - collision_vector * velocity2_along_collision + collision_vector * velocity1_along_collision

    balloon1.speed_x, balloon1.speed_y = new_velocity1
    balloon2.speed_x, balloon2.speed_y = new_velocity2

class Walls:
    def __init__(self):
        self.wall_thickness = WALL_THICKNESS

        self.lines = [
            ((0, 0), (SCREEN_WIDTH // 2.4, SCREEN_HEIGHT // 3)),
            ((SCREEN_WIDTH, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        ]

    def check_collision_with_line(self, sprite):
        for line_start, line_end in self.lines:
            if sprite.rect.clipline(line_start, line_end):
                normal = self.calculate_normal(line_start, line_end)
                sprite.speed = reflect(pygame.Vector2(sprite.speed_x, sprite.speed_y), normal)
                sprite.speed_x, sprite.speed_y = sprite.speed.x, sprite.speed.y

    def calculate_normal(self, start, end):
        """ Calculate the normal vector perpendicular to the line. """
        dx, dy = pygame.Vector2(end) - pygame.Vector2(start)
        normal = pygame.Vector2(-dy, dx)
        normal.normalize_ip()
        return normal

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), self.wall_thickness)
        for line in self.lines:
            pygame.draw.line(screen, WHITE, line[0], line[1], self.wall_thickness)

def reflect(velocity, normal):
    """ Reflects a velocity vector off a surface with a given normal vector. """
    normal = pygame.Vector2(normal)
    normal.normalize_ip()
    return velocity - 2 * velocity.dot(normal) * normal