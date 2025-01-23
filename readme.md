# Shark Attack Game 🦈

A simple arcade-style game where you control a shark and try to eat as many fish as possible in the shortest time. Navigate through a school of fish while managing your speed boost to catch your prey!

## Features

- Control a shark predator in an aquarium environment
- Dynamic school of fish with realistic flocking behavior
- Speed boost mechanic with regenerating boost meter
- Background music
- Multiple rounds of play
- Best score memory

## Requirements

- Python 3.x
- Pygame
- NumPy

## Installation

1. Ensure you have Python installed on your system
2. Install the required packages:
```bash
pip install pygame numpy
```
3. Place the `Shark_music.mp3` file in the same directory as the game script

## How to Play

1. Run the game:
```bash
python shark_attack.py
```

2. Controls:
   - Arrow keys: Move the shark
   - Spacebar: Activate speed boost
   - 'S': Start the game
   - 'R': Restart after completing a round
   - 'ESC': Quit the current game
   
3. Game Objective:
   - Catch 10 fish as quickly as possible
   - Use your boost meter strategically to catch fish
   - The boost meter regenerates when not in use

## Game Elements

- Green bars:
  - Left bar: Progress toward catching 10 fish
  - Right bar: Boost meter level

## Scoring

Your score is based on the time taken to catch 10 fish. The faster you complete the objective, the better your score!

## Notes

- The fish exhibit flocking behavior and will try to avoid your shark
- Fish will automatically be removed when they are eaten
- The boost meter depletes while holding spacebar and regenerates when not in use
