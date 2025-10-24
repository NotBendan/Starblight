Starblight v1.2

A side-scrolling shoot-'em-up made using Python Arcade.

Use the arrow keys to move your spaceship and the space bar to fire lasers.

In your fight to defend the city, you'll be up against a variety of enemy ships.

Pods only move straight forward and don't fire any lasers. They award 100 points for destroying.
Turrets don't move at all, and fire lasers at a moderate pace. They also give 100 points.
Shuttles follow less straightforward paths and fire lasers at a quicker pace. They give 200 points.
Starfighters move in a zig-zag pattern and fire lasers at a quick pace. They give 300 points.

The boss is at the end of the stage. If you shoot him one hundred times, you'll destroy him, and earn 5000 points.
After that, the game restarts, but everything now moves slightly faster. If you earn 20000 points, you get an extra life.



Credits

Stage Design, Programming, and Testing by ga13xy (notbendan)

Art, Sprites, Sound, and Music by kenney.nl

Python Arcade by Paul Vincent Craven

Changelog:

v1.2 (10/23/2025)
- Revamped title screen
- Player position bound to screen
- Capped on-screen player laser count to 4
- Explosion animation on player death
- Added sound effect for earning a 1-up

- Fixed boss firing patterns not randomizing properly
- Multiplied scores by 100 because number go up

- Removed more redundant lines of code
- Code modified to prepare for potential future levels [hehe]

Dev Note: Since the next version will likely contain a new level, it might take more time before it releases.
Don't expect an immediate next-day patch like the one before.

v1.1 (10/22/2025)
- Level data reworked to no longer be a massive if statement
- Level data moved from maingame.py to own file (levelData.py)

- Enemy firing timers are now called on initialization, and are no longer sectioned into quarter-seconds
- Enemy spawning system no longer skips spawning enemies at higher game speeds

- Removed various redundant lines of code
- Developer credits updated

v1.01 (2/12/2024)
- Fixed error in credits
- Modified pod code slightly (did not affect gameplay)

v1.0 (12/14/2022)
- Initial release version