from enemyLogic import *
from levelData import *

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
MOVEMENT_SPEED = 5
BACKGROUND_SPEED = 1
LASER_SPEED = 12
ENEMY_LASER_SPEED = 6

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Starblight"

GAME_INTRO = 1
GAME_STAGE_1 = 2
GAME_BOSS_1 = 3
GAME_STAGE_2 = 4
GAME_BOSS_2 = 5
GAME_OVER = 6


class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.laser_list = None
        self.enemy_list = None
        self.enemy_laser_list = None
        self.spawner_list = None

        self.player_sprite = None
        self.player_laser_sound = None
        self.player_explosion = None
        self.player_1up = None
        self.player_lives = None
        self.death_timer = -1
        self.score = 0
        self.background = None
        self.background_x = None
        self.background_start_y = None
        self.explosion_sprite = None
        self.explosion_sprite_index = 0
        self.explosion_sprite_list = None

        self.boss_sprite = None
        self.boss_health = None
        self.boss_timer = None
        self.level_enemy_index = 0

        self.enemy_explosion = None
        self.enemy_laser_sound = None
        self.background_music = None
        self.music_player = None

        self.set_mouse_visible(True)
        self.current_state = None

        # Speed scale made an attribute to fix bugs related to increasing the value of the variable
        self.speed_scale = None

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.laser_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_laser_list = arcade.SpriteList()
        self.spawner_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite(":resources:images/space_shooter/playerShip3_orange.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 300
        self.player_sprite.angle = -90
        self.player_laser_sound = arcade.load_sound(":resources:sounds/fall3.wav")
        self.player_explosion = arcade.load_sound(":resources:sounds/explosion1.wav")
        self.player_1up = arcade.load_sound(":resources:sounds/upgrade4.wav")
        self.player_lives = 3
        self.explosion_sprite = arcade.Sprite()
        self.explosion_sprite_list = ["./images/explosion1.png", "./images/explosion2.png", "./images/explosion3.png",
                                      "./images/explosion4.png", "./images/explosion5.png", "./images/explosion6.png",
                                      "./images/explosion7.png", "./images/explosion8.png", ]

        self.boss_sprite = arcade.Sprite(":resources:images/topdown_tanks/tankBody_darkLarge.png", 3)
        self.boss_sprite.center_y = 300
        self.boss_sprite.center_x = 900
        self.boss_sprite.angle = 90
        self.boss_timer = 0

        self.enemy_explosion = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.enemy_laser_sound = arcade.load_sound(":resources:sounds/laser2.wav")
        self.background_music = arcade.load_sound(":resources:music/funkyrobot.mp3")

        self.background = arcade.load_texture("./images/far-buildings-long.png")
        self.background_x = 2000
        self.current_state = GAME_INTRO
        self.speed_scale = INITIAL_SPEED_SCALE

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.background_x, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH * 5, SCREEN_HEIGHT, self.background)
        if self.current_state == GAME_INTRO:
            arcade.draw_text("Starblight", 0, 475,
                             arcade.color.WHITE, 50, 800, "center")
            arcade.draw_text("Arrow keys: Move", 0,300,
                             arcade.color.WHITE, 25, 800, "center")
            arcade.draw_text("Space: Fire lasers", 0, 260,
                             arcade.color.WHITE, 25, 800, "center")
            arcade.draw_text("Press Enter", 0, 50,
                             arcade.color.WHITE, 25, 800, "center")
        if self.current_state == GAME_STAGE_1 or self.current_state == GAME_BOSS_1:

            self.laser_list.draw()
            self.enemy_laser_list.draw()
            self.enemy_list.draw()
            arcade.draw_text(f"Score: {self.score}", 10, 575, arcade.color.WHITE, 14)
            # Drawing the life counter
            life_sprite = arcade.Sprite(":resources:images/space_shooter/playerShip3_orange.png", .4)
            life_sprite.center_x, life_sprite.center_y = 25, 25
            life_sprite.draw()
            arcade.draw_text(f"x {self.player_lives}", 55, 18, arcade.color.WHITE, 20)
            if self.death_timer > 0:
                self.explosion_sprite.draw()
            else:
                self.player_sprite.draw()
            if self.current_state == GAME_BOSS_1:
                self.boss_sprite.draw()
        if self.current_state == GAME_OVER:
            arcade.draw_text("Game Over", 225, 300, arcade.color.WHITE, 50)
            arcade.draw_text(f"Score: {self.score}", 0, 200, arcade.color.WHITE, 30, 800, "center")

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if self.current_state == GAME_INTRO:
            if key == arcade.key.ENTER:
                self.current_state = GAME_STAGE_1
                self.music_player = arcade.play_sound(self.background_music, .8, 0, True)
        if self.current_state == GAME_STAGE_1 or self.current_state == GAME_BOSS_1:
            if key == arcade.key.UP:
                self.player_sprite.change_y = MOVEMENT_SPEED * self.speed_scale
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -MOVEMENT_SPEED * self.speed_scale
            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -MOVEMENT_SPEED * self.speed_scale
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = MOVEMENT_SPEED * self.speed_scale
            elif (key == arcade.key.SPACE) and (len(self.laser_list) < 4):
                laser = Laser(self.player_sprite.center_x, self.player_sprite.center_y, 0, ":resources:images/space_shooter/laserBlue01.png")
                arcade.play_sound(self.player_laser_sound)
                self.laser_list.append(laser)

    def on_key_release(self, key, modifiers):
        """
        Called when the user releases a key.
        """
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def kill_player(self):
        self.player_lives -= 1

        # Resetting the game after the player dies
        self.laser_list = arcade.SpriteList()
        self.enemy_laser_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.spawner_list = arcade.SpriteList()
        self.level_enemy_index = 0
        if self.player_lives < 1:
            self.current_state = GAME_OVER
            self.music_player.pause()
            return None

        # Checking to see if the player has passed a check point
        if self.background_x <= 0:
            self.background_x = 0
        elif self.background_x <= 1100:
            self.background_x = 1100
        else:
            self.background_x = 2000

        if self.current_state == GAME_BOSS_1:
            self.current_state = GAME_STAGE_1
        while (LEVEL1[self.level_enemy_index][0] >= self.background_x) and (self.current_state == GAME_STAGE_1):
            self.level_enemy_index += 1

        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 300
        return None

    def add_spawner(self, y_position: float, enemy_type: str, enemy_count: int = 1, distance_multiplier: float = 1):
        temp_spawner = EnemySpawner(y_position, enemy_type, enemy_count, distance_multiplier, self.speed_scale)
        # Removing duplicate spawners by checking every attribute that can be manually set
        for spawner in self.spawner_list:
            if temp_spawner.center_y == spawner.center_y and temp_spawner.enemy_type == spawner.enemy_type and \
                    temp_spawner.enemy_count == spawner.enemy_count and temp_spawner.multiplier == spawner.multiplier:
                return None
        self.spawner_list.append(temp_spawner)
        return None

    def add_enemies(self):
        while (self.current_state == GAME_STAGE_1) and (LEVEL1[self.level_enemy_index][0] >= self.background_x):
            self.add_spawner(LEVEL1[self.level_enemy_index][1], LEVEL1[self.level_enemy_index][2],
                             LEVEL1[self.level_enemy_index][3], LEVEL1[self.level_enemy_index][4])
            self.level_enemy_index += 1

    def increase_score(self, amount: int):
        old_score = self.score % 20000
        self.score += amount * 100
        # Every 20000 points, the player will earn an extra life
        if old_score > self.score % 20000:
            self.player_lives += 1
            arcade.play_sound(self.player_1up, 1.5)

    def on_update(self, delta_time):
        if self.current_state == GAME_STAGE_1:
            # Scrolling Background
            if self.background_x > -1200:
                self.background_x -= BACKGROUND_SPEED * self.speed_scale
            elif self.background_x < -1200:
                self.background_x = -1200
            elif self.background_x == -1200:
                # Initializing boss fight
                self.boss_health = 100
                self.boss_timer = 100
                self.boss_sprite.center_x = 900
                self.boss_sprite.center_y = 300
                self.boss_sprite.fire_timer = 120
                self.current_state = GAME_BOSS_1
        # Enemy spawning
        self.add_enemies()

        # player position bounding
        if ((self.player_sprite.change_x < 0) and (self.player_sprite.center_x <= 25)) or \
                ((self.player_sprite.change_x > 0) and (self.player_sprite.center_x >= 775)):
            self.player_sprite.change_x = 0
        if ((self.player_sprite.change_y < 0) and (self.player_sprite.center_y <= 25)) or \
                ((self.player_sprite.change_y > 0) and (self.player_sprite.center_y >= 575)):
            self.player_sprite.change_y = 0

        self.player_sprite.update()
        self.enemy_list.update()
        self.laser_list.update()
        self.enemy_laser_list.update()
        self.spawner_list.update()

        # Boss fight logic
        if self.current_state == GAME_BOSS_1:
            self.boss_sprite.update()
            if self.boss_sprite.center_x > 700:
                self.boss_sprite.center_x -= 1 * self.speed_scale
            else:
                self.boss_sprite.center_x = 700
                self.boss_timer += 1 * self.speed_scale
                if self.boss_timer % 400 < 200:
                    self.boss_sprite.center_y += 2
                else:
                    self.boss_sprite.center_y -= 2
                if self.boss_timer >= self.boss_sprite.fire_timer:
                    for position in range(1, 4):
                        temp_y_position = self.boss_sprite.center_y + (50 * position - 100)
                        self.enemy_laser_list.append(Laser(self.boss_sprite.center_x - 15, temp_y_position, 90))
                        arcade.play_sound(self.enemy_laser_sound, 0.5)
                    self.boss_sprite.fire_timer = round(
                        random.randrange(45, round(90 / self.speed_scale)) + self.boss_timer)
                for laser in self.laser_list:
                    if laser.collides_with_sprite(self.boss_sprite):
                        self.boss_health -= 1
                        laser.kill()
                        arcade.play_sound(self.enemy_explosion)
                        # Boss death / game repeat
                        if self.boss_health <= 0:
                            self.increase_score(50)
                            self.current_state = GAME_STAGE_1
                            self.background_x = 2000
                            self.speed_scale += .1
                            self.level_enemy_index = 0

        # Adding enemies from spawners
        for spawner in self.spawner_list:
            for enemy in spawner.temp_list:
                if enemy not in self.enemy_list:
                    self.enemy_list.append(enemy)

        # Moving lasers / removing them when they move off-screen
        for laser in self.laser_list:
            laser.change_x = LASER_SPEED * self.speed_scale
            if laser.center_x >= 900:
                self.laser_list.remove(laser)

        # Moving enemy lasers / removing them when they move off-screen
        for laser in self.enemy_laser_list:
            if laser.angle == 45:
                laser.change_x = (-ENEMY_LASER_SPEED // 2 - 1) * self.speed_scale
                laser.change_y = (ENEMY_LASER_SPEED // 2) * self.speed_scale
            if laser.angle == 135:
                laser.change_x = (-ENEMY_LASER_SPEED // 2 - 1) * self.speed_scale
                laser.change_y = (-ENEMY_LASER_SPEED // 2) * self.speed_scale
            if laser.angle == 90:
                laser.change_x = -ENEMY_LASER_SPEED * self.speed_scale
            if laser.center_x >= 900 or laser.center_y >= 700 or laser.center_y <= -100:
                self.enemy_laser_list.remove(laser)
            if laser.collides_with_sprite(self.player_sprite) and (self.death_timer == -1):
                arcade.play_sound(self.player_explosion)
                self.death_timer = 40

        if self.death_timer > 0:
            self.explosion_sprite = arcade.Sprite(self.explosion_sprite_list[self.explosion_sprite_index])
            self.explosion_sprite.center_y = self.player_sprite.center_y
            self.explosion_sprite.center_x = self.player_sprite.center_x
            if (self.death_timer % 5 == 0) and (self.death_timer != 40):
                self.explosion_sprite_index += 1
            self.death_timer -= 1
        elif self.death_timer == 0:
            self.death_timer = -1
            self.explosion_sprite_index = 0
            self.kill_player()

        for enemy in self.enemy_list:
            # Enemies firing lasers
            if enemy.pause_time >= 0:
                if enemy.frame_counter >= enemy.pause_time:
                    self.enemy_laser_list.append(enemy.fire_laser())

            # Checking for player collision with enemies
            if enemy.collides_with_sprite(self.player_sprite) and (self.death_timer == -1):
                arcade.play_sound(self.player_explosion)
                self.death_timer = 40

            # Checking for laser collision with enemies
            for laser in self.laser_list:
                if laser.collides_with_sprite(enemy):
                    # Scoring system
                    if enemy.enemy_type == "starfighter":
                        self.increase_score(3)
                    elif enemy.enemy_type == "shuttle1" or enemy.enemy_type == "shuttle1-r" or \
                            enemy.enemy_type == "shuttle2" or enemy.enemy_type == "shuttle2-r":
                        self.increase_score(2)
                    else:
                        self.increase_score(1)
                    self.laser_list.remove(laser)
                    enemy.kill()
                    arcade.play_sound(self.enemy_explosion)


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


main()
