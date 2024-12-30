# Andrew Nguyen, Computing ID: fru4yr
# Derek Song, Computing ID: xrr4td

# CS 1110 with Raymond Pettit, final project final game

# Three Basic Features
# Game Input: user will either choose the keys "a" and "d" or the right or left arrow to move the player at the bottom. Player will also use the space bar to shoot at enemies, and the "r" key to restart.
# Game Over: if the player gets hit by an enemy projectile 10 times, the health will deplete to 0 and the game will be over.
# Graphics/Images: For the enemies, the player, and projectiles we will use correlating images to represent each

# Four Additional Features
# Restart when game is over: When player runs out of lives, or destroys all enemies, the game end screen will display and the player will be given the option to restart the game by pressing "r"
# Enemies: The game will follow the same premise as space invaders where at the start of the game, there are numerous "invaders" that the player must destroy that also randomly shoot projectiles at the player
# Sprite Animation: As enemies move across the screen, with each tick they will move a certain distance across the screen and change their poses.
# Object Oriented Code: We would have classes for the enemies, which would be called multiple times, the player

# Changes from Checkpoint 1 to checkpoint 2: instead of having object oriented code, we would instead have a healthbar that tracks the players health and is shown up on screen for the player to see. When the health is 0, the health bar will be empty and the game will be over, the player will lose.