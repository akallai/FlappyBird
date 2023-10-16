#!/usr/bin/env python
import pygame
from pygame.locals import *
import sys
import random
from typing import List
import yaml # <-- config einlesen

#TODO: 

# - funktionen ggf. splitten ()
# - nichts hardcoden sondern entweder konstanten oder config
# - collider unten weniger aggresiv machen
# - Effizienzrefactoring


class FlappyBird:
    """
    A FlappyBird game class.
    
    Attributes:
        screen: The main display screen.
        bird: Rectangular shape representing the bird.
        background: The background image.
        birdSprites: List containing images for bird animation.
        wallUp: Image for the upper wall.
        wallDown: Image for the lower wall.
        gap: Gap between the walls.
        wallx: X-coordinate of the wall.
        birdY: Y-coordinate of the bird.
        jump: Indicates the state of the jump.
        jumpSpeed: Speed of the jump.
        gravity: Gravity affecting the bird.
        dead: Indicates whether the bird is dead or not.
        sprite: Index of the current bird sprite.
        counter: A counter keeping track of walls crossed.
        offset: A random offset for the wall position.
    """
    
    def __init__(self):
        """
        Initializes the FlappyBird game with default settings.
        """
        self.screen = pygame.display.set_mode((400, 708))
        self.bird = pygame.Rect(5, 5, 50, 50)
        self.background = pygame.image.load("assets/background.png").convert()
        self.birdSprites: List[pygame.Surface] = [
            pygame.image.load("assets/1.png").convert_alpha(),
            pygame.image.load("assets/2.png").convert_alpha(),
            pygame.image.load("assets/dead.png")
        ]
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.birdY = 350
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 5
        self.dead = False
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        
    def updateWalls(self):
        """
        Updates the wall positions and resets them when they go off-screen.
        Also updates the counter and random offset for wall positions.
        """
        self.wallx -= 2  # Move walls leftwards
        if self.wallx < -80:
            self.wallx = 400  # Reset wall position
            self.counter += 1  # Increment counter
            self.offset = random.randint(-110, 110)  # Update random offset
            
    # birdgravitation, springen, collisiondetection
    def birdUpdate(self):
        """
        Updates the bird position based on gravity and jump state.
        Checks for collision with walls and screen boundaries.
        """
        if self.jump:
            self.jumpSpeed -= 1
            self.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.birdY += self.gravity
            self.gravity += 0.2

        self.bird[1] = self.birdY
        
        # Define wall rectangles for collision detection
        upRect = pygame.Rect(self.wallx, 360 + self.gap - self.offset + 10, self.wallUp.get_width() - 10, self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx, 0 - self.gap - self.offset - 10, self.wallDown.get_width() - 10, self.wallDown.get_height())
        
        # Check for collisions
        if upRect.colliderect(self.bird) or downRect.colliderect(self.bird):
            self.dead = True

        # Check for screen boundary collision
        if not 0 < self.bird[1] < 720:
            self.reset_game()
            
    def reset_game(self):
        """Resets the game to initial state."""
        self.bird[1] = 50
        self.birdY = 50
        self.dead = False
        self.counter = 0
        self.wallx = 400
        self.offset = random.randint(-110, 110)
        self.gravity = 5

    def run(self):
        """
        Main game loop.
        """
        
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        game_started = False
        # Menü
        while not game_started:
            clock.tick(1)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            print(event.type)
            if event.type == pygame.KEYUP:
                game_started = True
            self.screen.fill((255, 0, 0))
            pygame.display.update()
        # Start des Spiels

        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (
                    event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]
                    and not self.dead
                ):
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp, (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown, (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter), -1, (255, 255, 255)), (200, 50))

            if self.dead:
                self.sprite = 2
            elif self.jump:
                self.sprite = 1

            self.screen.blit(self.birdSprites[self.sprite], (70, self.birdY))

            if not self.dead:
                self.sprite = 0

            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
