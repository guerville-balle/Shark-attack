import pygame
import sys
import numpy as np
import random
import time
import math


## Define the technical functions

# Return a normal vector with random direction
def random_normal_vector():
    v = np.array([2*random.random()-1,2*random.random()-1])
    d = (v[0]**2+v[1]**2)**(1/2)
    return v/d
    
# Return the norm of a vector
def normalize(v):
    d = (v[0]**2+v[1]**2)**(1/2)
    return v/d

# Compute the distance between two points
def distance(p,q):
    return ((p[0]-q[0])**2+(p[1]-q[1])**2)**(1/2)

# Drawing level bar
def draw_level_bar(surface, x, y, width, height, ratio):
    pygame.draw.rect(surface, (0, 255, 0), (x, y, width * ratio, height))
    pygame.draw.rect(screen, Black, pygame.Rect(x, y, width, height),2)


# Define the class Predator
class Predator:
    """The Predator class determines the shark and how to control it."""
    # Initialize the shark with a random position and direction
    def __init__(self, width, height):
        self.position = np.array([width*random.random(),height*random.random()])
        self.dimension = [7,10,10,10,9,9,7,5,5,4,4,4,3]
        self.direction = random_normal_vector()
        self.skeleton = np.array([self.position-i*5*self.direction for i in range(len(self.dimension))])
        self.tail_size = 4
        self.tail = np.array([self.skeleton[-1]-i*4*self.direction for i in range(self.tail_size)])
        self.speed = 1.2
        self.boost_level = 100
    
    def update_position(self,x,y,boost):
    # Handle key presses
        if boost and Shark.boost_level > 0:
            Shark.speed = 2
            Shark.boost_level -= 1
        else:
            Shark.speed = 1.2
            if Shark.boost_level < 100:
                Shark.boost_level += 0.1
        if not (x,y)==(0,0):
            Shark.direction = speed_scale*normalize(np.array([x,y]))
            Shark.position += Shark.speed*Shark.direction
        else:
            Shark.direction = 0.999*self.direction
            Shark.position += Shark.direction

        # Keep the point within the screen boundaries
        Shark.position[0] = max(5, min(width - 5, Shark.position[0]))
        Shark.position[1] = max(5, min(height - 5, Shark.position[1]))
        
    def animate(self, x, y, boost=False, loading=False):
        if not loading:
            self.update_position(x, y, boost)
        self.skeleton[0]=self.position
        pygame.draw.circle(screen, Grey, self.skeleton[0], self.dimension[0])
        for i in range(len(self.skeleton)-1):
            direction = normalize(self.skeleton[i+1] - self.skeleton[i])
            self.skeleton[i+1] = self.skeleton[i] + 5*direction
            pygame.draw.circle(screen, Grey, self.skeleton[i+1], self.dimension[i+1])
        normal=self.skeleton[2]-self.skeleton[3]
        pygame.draw.polygon(screen,Grey,[self.skeleton[0],self.skeleton[3]+4*np.array((normal[1],-normal[0])),self.skeleton[3]-4*np.array((normal[1],-normal[0]))])
        normal=self.skeleton[9]-self.skeleton[10]
        pygame.draw.polygon(screen,Grey,[self.skeleton[8],self.skeleton[10]+2*np.array((normal[1],-normal[0])),self.skeleton[10]-2*np.array((normal[1],-normal[0]))])
        self.tail[0]=self.skeleton[-1]
        for i in range(self.tail_size-1):
            direction = normalize(self.tail[i+1] - self.tail[i])
            self.tail[i+1] = self.tail[i] + 4*direction
            pygame.draw.line(screen, Grey, self.tail[i], self.tail[i+1],width=3)



## Main program

# Initialize Pygame
pygame.init()
clock = pygame.time.Clock()
FPS=60
pygame.mixer.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height + 100))
pygame.display.set_caption("Shark attack")

# Definition of the colors
White = (255, 255, 255)
Black = (0, 0, 0)
Grey = (100, 100, 100)
Red = (255, 0, 0)
Blue = (0, 0, 255)

# Creation of the Shark
Shark = Predator(width, height)
speed_scale = 2.5

# Beginning of the game
running = True
while running:

    # Handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    x,y = 0,0        
    if keys[pygame.K_LEFT]:
        x = -1
    if keys[pygame.K_RIGHT]:
        x = 1
    if keys[pygame.K_UP]:
        y = -1
    if keys[pygame.K_DOWN]:
        y = 1
    boost = keys[pygame.K_SPACE]

    # Update the display
    screen.fill(White)
    Shark.animate(x,y,boost)
    pygame.display.flip()
    clock.tick(FPS)