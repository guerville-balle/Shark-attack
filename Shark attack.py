"""
    Shark Attack!!!
    It's a game where the player controls a shark and tries to eat as fish.
"""

# Third-party imports
import pygame
import sys
import numpy as np
import random
import time


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
    

## Define the classes

# Define the class Fish
class Fish:
    """The Fish class determine the basic behavior of the fish in the aquarium"""
    # Initialize the fish with a random position and direction
    def __init__(self, width, height):
        self.position = np.array([width*random.random(),height*random.random()])
        self.direction = random_normal_vector()
    
    # Define the representation of the fish
    def __repr__(self):
    	return "><(((°>"
    
    # Animation of the fish
    def animate(self, school, Shark, width, height):
        # Avoid the border of the aquiarium
        avoid_border = np.array([0.,0.])
        border_visibility = ((width+height)/2)/20
        if np.abs(self.position[0]-width/2)>width/2-border_visibility:
            avoid_border[0] += -np.sign(self.position[0]-width/2)*(np.abs(self.position[0]-width/2)-border_visibility)**(1)
        if np.abs(self.position[1]-height/2)>height/2-border_visibility:
            avoid_border[1] += -np.sign(self.position[1]-height/2)*(np.abs(self.position[1]-height/2)-border_visibility)**(1)
    
        # Adapt the direction in function of the 6 closest fish
        surrounding = [(distance(self.position,fish.position),fish) for fish in school]
        surrounding.sort()
        adapt_direction = np.array([0.,0.])
        for dist, neighbor in surrounding[1:7]:
            # Synchronize the direction
            adapt_direction += neighbor.direction
        
            # Cohesion and repulsion according to the distance with the other fish
            if dist < 10:
                adapt_direction += (1-dist/10)*(self.position - neighbor.position)*10
            else:
                adapt_direction += -normalize(self.position - neighbor.position)*0.01

        # Avoid the predators when they are close    
        avoid_predator = np.array([0.,0.])
        d = distance(Shark.position,self.position)
        if d<5:
            School.school.remove(self)
        elif d<30:
            avoid_predator += ((1-d/30))*(self.position - Shark.position)

        # Update the direction and the position of the fish
        self.direction = normalize( (18*self.direction + adapt_direction/6 + avoid_border/10 + avoid_predator) )
        self.position += self.direction + random_normal_vector()/10

# Define the class School_of_fish
class School_of_fish:
    """The School_of_fish class constrcut a school of fish in the aquarium and animate them."""
    # Initialize the school with a given size, in a aquarium of given width and height
    def __init__(self, size, width, height):
        self.school = [Fish(width, height) for i in range(size)]
        self.width = width
        self.height = height

    # Return the size of the school
    def size(self):
        return len(self.school)
        
    # Animation of the school
    def animate(self, shark):
        for fish in self.school:
            fish.animate(self.school, shark, self.width, self.height)
            pygame.draw.circle(screen, Blue, fish.position, 3)
    
# Define the class Predator
class Predator:
    """The Predator class determines the shark and how to control it."""
    def __init__(self, width, height):
        self.position = np.array([width*random.random(),height*random.random()])
        self.speed = 1.2
        self.boost_level = 100

    def loading_animate(self):
        pygame.draw.circle(screen, Red, self.position, 5)
    
    def animate(self):
    # Handle key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and Shark.boost_level > 0:
            Shark.speed = 2
            Shark.boost_level -= 1
        else:
            Shark.speed = 1.2
            if Shark.boost_level < 100:
                Shark.boost_level += 0.1
        if keys[pygame.K_LEFT]:
            Shark.position[0] -= Shark.speed
        if keys[pygame.K_RIGHT]:
            Shark.position[0] += Shark.speed
        if keys[pygame.K_UP]:
            Shark.position[1] -= Shark.speed
        if keys[pygame.K_DOWN]:
            Shark.position[1] += Shark.speed

        # Keep the point within the screen boundaries
        Shark.position[0] = max(5, min(width - 5, Shark.position[0]))
        Shark.position[1] = max(5, min(height - 5, Shark.position[1]))
        
        pygame.draw.circle(screen, Red, self.position, 5)


## Main program

# Initialize Pygame
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Shark_music.mp3")
pygame.mixer.music.play(loops=-1)

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height + 100))
pygame.display.set_caption("Shark attack")

# Definition of the colors
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Blue = (0, 0, 255)


## Opening screen

# Definition of the Title and the menu
title = pygame.font.Font(None, 75)
Title = title.render("Shark attack!!!", True, (255, 255, 255))
background = Title.get_rect(center=(400, 300))

menu = pygame.font.Font(None, 25)
text_1 = menu.render("- Press 's' to start", True, (255, 255, 255))
text_2 = menu.render("- Press 'exc' to quit", True, (255, 255, 255))
text_3 = menu.render("- Press 'space' to use the speed booster", True, (255, 255, 255))

# Opening loop
running = True
end_of_game = False
while running:
    # Handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            end_of_game = True

    # Handle the choice of the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_s]:
        running = False
    
    # Display the opening screen
    screen.fill((0, 0, 0))
    screen.blit(Title, background)
    screen.blit(text_1, (250,400))
    screen.blit(text_2, (250,433))
    screen.blit(text_3, (250,466))
    pygame.display.flip()

# Loop for several game
while not end_of_game:

    # Definition of the level bars texts
    info = pygame.font.Font(None, 30)
    Boost = info.render("Booster", True,Black)
    Boost_bg = Boost.get_rect(center=(530, 660))
    Hunting = info.render("Hunting", True,Black)
    Hunting_bg = Hunting.get_rect(center=(280, 660))


    # Construction of the school and the predator
    nbr_of_fish = 50
    School=School_of_fish(nbr_of_fish, width, height)
    Shark=Predator(width, height)

    # Prepare the countdown
    load_counter = 150
    Count_down = 3
    Count = title.render(f"{Count_down}", True, Black)
    Count_bg = Count.get_rect(center=(400, 300))

    # Loading loop
    running = True
    while running and load_counter > 0 and not end_of_game:
        # Decrease the counter
        load_counter -= 1

        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                end_of_game = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        # Update the display the loading screen
        screen.fill(White) 
        screen.blit(Boost, Boost_bg) 
        screen.blit(Hunting, Hunting_bg)
        draw_level_bar(screen, 580, 650, 200, 20, Shark.boost_level/100 )
        draw_level_bar(screen, 20, 650, 200, 20, ((nbr_of_fish - School.size()))/10 )
        Shark.loading_animate()
        School.animate(Shark)
        screen.blit(Count, Count_bg)

        # Update the countdown
        pygame.display.flip()
        if load_counter % 50 == 0:
            Count_down -= 1
            Count = title.render(f"{Count_down}", True, Black)
            Count_bg = Count.get_rect(center=(400, 300))


    ## Main game loop

    # Initialization of the timer
    elapsed_time = 100000
    start = time.time()

    # Beginning of the game
    while running and not end_of_game:

        # Handle quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                end_of_game = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        # Update the display
        screen.fill(White)
        screen.blit(Boost, Boost_bg)
        screen.blit(Hunting, Hunting_bg)
        draw_level_bar(screen, 580, 650, 200, 20, Shark.boost_level/100 )
        draw_level_bar(screen, 20, 650, 200, 20, ((nbr_of_fish - School.size()))/10 )
        Shark.animate()
        School.animate(Shark)
        pygame.display.flip()

        # Check if the game is over
        if nbr_of_fish - School.size() == 10:
            running = False
            end = time.time()
            elapsed_time = end - start

    time.sleep(0.25)

    ## End of the game

    # Prepare the texts
    Score_text = pygame.font.Font(None, 40)
    Score = Score_text.render("Your score is:", True, (255, 255, 255))
    Score_background = Score.get_rect(center=(400, 300))

    Score_value = Score_text.render(f"{elapsed_time:.3f} seconds", True, (255, 255, 255))
    Value_background = Score_value.get_rect(center=(400, 350))

    menu = pygame.font.Font(None, 25)
    menu_1 = menu.render("- Press 'r' to play again", True, (255, 255, 255))
    menu_2 = menu.render("- Press 'exc' to quit", True, (255, 255, 255))

    # End of the game loop
    running = True
    while running and not end_of_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                end_of_game = True
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False
            end_of_game = True
        if keys[pygame.K_r]:    
            running = False
        
        # Update the display
        screen.fill((0, 0, 0))  
        screen.blit(Score, Score_background)
        screen.blit(Score_value, Value_background)
        screen.blit(menu_1, (30,600))
        screen.blit(menu_2, (30,625))
        pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()
