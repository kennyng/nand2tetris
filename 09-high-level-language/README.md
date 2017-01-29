[Project 09: High-Level Programming](http://www.nand2tetris.org/09.php)


## GAME: Alien Invasion
A shooter game sort of like Space Invaders but simpler)


## PREMISE/GAMEPLAY:
An army of aliens is invading the base. The player controls a laser cannon by
moving it horizontally across the bottom of the screen and fires lasers at the
descending aliens. The player must destroy all aliens before they reach the
base (indicated by boundary lines in the implementation).

Whenever an alien is hit by the laser, the player earns points.
The laser cannon that the player uses is very powerful and is the only weapon
that can destroy the aliens. However, the laser cannon is very slow and can
only fire a single shot at a time. Also, the ammunition that the laser cannon
uses is very expensive, very difficult to obtain, and very armful to the
environment. The player is ordered to not waste ammunition and only fire the
laser cannon only as much as needed. That's why whenever the laser cannon is
shot, the player loses points.


## SCORING & RULES
    (1) Laser cannon can only be fired a single shot at a time
        (only one laser beam can be on the screen). It is important to time the shots.
    (2) 250 points earned for every alien destroyed.
    (3) 50 points deducted for every laser shot.
    (4) The player must destroy all aliens before the aliens reach the base.
    (5) Perfect Score: 50 shots taken and a score of 10000.


## INSTRUCTIONS:
    - LEFT ARROW: Moves the player (laser cannon) to the left
    - RIGHT ARROW: Moves the player (laser cannon) to the right
    - SPACE BAR: Shoot laser from laser cannon (only one shot can be fired at a time)
    - ESC: quit the game


## TO RUN GAME:
    (1) Compile program using supplied Jack Compiler.
    (2) Load all .vm files into VMEmulator.
    (3) Run the program.


## FILES:
Alien.jack, AlienInvasion.jack, GameBoard.jack, Laser.jack, Main.jack, Player.jack

