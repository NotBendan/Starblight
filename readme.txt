Starblight v1.1

A side-scrolling shoot-'em-up made using Python Arcade.

Use the arrow keys to move your spaceship and the space bar to fire lasers.

In your fight to defend the city, you'll be up against a variety of enemy ships.

Pods only move straight forward and don't fire any lasers. They award one point for destroying.
Turrets don't move at all, and fire lasers at a moderate pace. They also give one point.
Shuttles follow less straightforward paths and fire lasers at a quicker pace. They give two points.
Starfighters move in a zig-zag pattern and fire lasers at a quick pace. They give three points.

The boss is at the end of the stage. If you shoot him one hundred times, you'll destroy him, and earn fifty points.
After that, the game restarts, but everything now moves slightly faster. If you earn 250 points, you get an extra life.



Credits

Stage Design, Programming, and Testing by ga13xy (notbendan)

Art, Sprites, and Music by kenney.nl

Python Arcade by Paul Vincent Craven

Changelog:

v1.1 (10/22/2025)
- Level data reworked to no longer be a massive if statement
- Level data moved to separate file from maingame

- Enemy firing timers are now called on initialization, and are no longer sectioned into quarter-seconds
- Enemy spawning system no longer skips spawning enemies at higher game speeds

- Removed various redundant/repetitive lines of code
- Developer credits updated

v1.01 (2/12/2024)
- Fixed error in credits
- Modified pod code slightly (did not affect gameplay)

v1.0 (12/14/2022)
- Initial release version