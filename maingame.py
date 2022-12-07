from enemyLogic import *

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
GAME_RUNNING = 2
GAME_OVER = 3


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
        self.player_lives = None
        self.score = 0
        self.background = None
        self.background_start_x = None
        self.background_start_y = None

        self.enemy_explosion = None
        self.enemy_laser_sound = None
        self.background_music = None

        self.set_mouse_visible(True)
        self.current_state = None

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        self.laser_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.enemy_laser_list = arcade.SpriteList()
        self.spawner_list = arcade.SpriteList()
        self.score = 0

        img = ":resources:images/space_shooter/playerShip3_orange.png"
        self.player_sprite = arcade.Sprite(img, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 300
        self.player_sprite.angle = -90
        self.player_laser_sound = arcade.load_sound(":resources:sounds/fall3.wav")
        self.player_explosion = arcade.load_sound(":resources:sounds/explosion1.wav")
        self.player_lives = 3

        self.enemy_explosion = arcade.load_sound(":resources:sounds/explosion2.wav")
        self.enemy_laser_sound = arcade.load_sound(":resources:sounds/laser2.wav")
        self.background_music = arcade.load_sound(":resources:music/funkyrobot.mp3")

        self.background = arcade.load_texture("./images/far-buildings-long.png")
        self.background_start_x = 2000
        self.current_state = GAME_INTRO
        arcade.play_sound(self.background_music, .8, 0, True)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(self.background_start_x, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH * 5, SCREEN_HEIGHT, self.background)
        if self.current_state == GAME_INTRO:
            arcade.draw_text("Welcome to Starblight.", SCREEN_WIDTH // 4 + 20, SCREEN_HEIGHT // 2 + 90,
                             arcade.color.WHITE, 25)
            arcade.draw_text("Use the arrow keys to move your spaceship.", SCREEN_WIDTH // 10 - 15,
                             SCREEN_HEIGHT // 2 + 30, arcade.color.WHITE, 25)
            arcade.draw_text("Press the space bar to fire the lasers.", SCREEN_WIDTH // 6 - 10, SCREEN_HEIGHT // 2,
                             arcade.color.WHITE, 25)
            arcade.draw_text("Press Enter to continue.", SCREEN_WIDTH // 4 + 10, (SCREEN_HEIGHT // 2 - 60),
                             arcade.color.WHITE, 25)
        if self.current_state == GAME_RUNNING:
            self.player_sprite.draw()
            self.laser_list.draw()
            self.enemy_laser_list.draw()
            self.enemy_list.draw()
            arcade.draw_text(f"Score: {self.score}", 10, 575, arcade.color.WHITE, 14)
            life_sprite = arcade.Sprite(":resources:images/space_shooter/playerShip3_orange.png", .4)
            life_sprite.center_x, life_sprite.center_y = 25, 25
            life_sprite.draw()
            arcade.draw_text(f"x {self.player_lives}", 55, 18, arcade.color.WHITE, 20)
        if self.current_state == GAME_OVER:
            arcade.draw_text("Game Over", 225, 300, arcade.color.WHITE, 50)

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """
        if self.current_state == GAME_INTRO:
            if key == arcade.key.ENTER:
                self.current_state = GAME_RUNNING
        if self.current_state == GAME_RUNNING:
            if key == arcade.key.UP:
                self.player_sprite.change_y = MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.player_sprite.change_y = -MOVEMENT_SPEED
            elif key == arcade.key.LEFT:
                self.player_sprite.change_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.player_sprite.change_x = MOVEMENT_SPEED
            elif key == arcade.key.SPACE:
                laser = Laser(":resources:images/space_shooter/laserBlue01.png",
                              self.player_sprite.center_x, self.player_sprite.center_y, 0)
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
        arcade.play_sound(self.player_explosion)
        self.laser_list = arcade.SpriteList()
        self.enemy_laser_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.spawner_list = arcade.SpriteList()
        if self.player_lives < 1:
            self.current_state = GAME_OVER
            return None
        self.background_start_x = 2000
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 300
    
    def add_spawner(self, y_position: float, enemy_type: str, enemy_count: int = 1, distance_multiplier: float = 1):
        temp_spawner = EnemySpawner(y_position, enemy_type, enemy_count, distance_multiplier)
        for spawner in self.spawner_list:
            if temp_spawner == spawner:
                return None
        self.spawner_list.append(temp_spawner)

    def add_enemies(self):
        # Adds enemies when the screen scrolls to them
        if self.background_start_x == 1900:
            self.add_spawner(500, "pod", 4)
        if self.background_start_x == 1800:
            self.add_spawner(100, "pod", 4)
        if self.background_start_x == 1750:
            self.add_spawner(25, "turret", 2, 2)
        if self.background_start_x == 1600:
            self.add_spawner(300, "pod", 2)

        if self.background_start_x == 1450:
            self.add_spawner(575, "turret-r")
        if self.background_start_x == 1350:
            self.add_spawner(450, "shuttle1", 3)
        if self.background_start_x == 1200:
            self.add_spawner(250, "pod", 5)
        if self.background_start_x == 1150:
            self.add_spawner(100, "shuttle1-r", 2)
        if self.background_start_x == 1050:
            self.add_spawner(575, "turret-r", 3, 1.5)
        if self.background_start_x == 950:
            self.add_spawner(500, "shuttle2", 3)
        if self.background_start_x == 850:
            self.add_spawner(350, "starfighter")
        if self.background_start_x == 750:
            self.add_spawner(25, "turret", 2, 3)
        if self.background_start_x == 700:
            self.add_spawner(100, "shuttle2-r", 2)
        if self.background_start_x == 600:
            self.add_spawner(200, "pod", 3)
            self.add_spawner(400, "pod", 3)

        if self.background_start_x == 400:
            self.add_spawner(350, "starfighter", 3)

    def on_update(self, delta_time):

        if self.current_state == GAME_RUNNING:
            # Scrolling Background
            if self.background_start_x > -1200:
                self.background_start_x -= BACKGROUND_SPEED * speed_scale
            elif self.background_start_x < -1200:
                self.background_start_x = 1200
            self.add_enemies()

        self.player_sprite.update()
        self.enemy_list.update()
        self.laser_list.update()
        self.enemy_laser_list.update()
        self.spawner_list.update()

        for spawner in self.spawner_list:
            for enemy in spawner.temp_list:
                if enemy not in self.enemy_list:
                    self.enemy_list.append(enemy)

        for laser in self.laser_list:
            laser.change_x = LASER_SPEED
            if laser.center_x >= 900:
                self.laser_list.remove(laser)

        for laser in self.enemy_laser_list:
            if laser.angle == 45:
                laser.change_x = -ENEMY_LASER_SPEED // 2 - 1
                laser.change_y = ENEMY_LASER_SPEED // 2
            if laser.angle == 135:
                laser.change_x = -ENEMY_LASER_SPEED // 2 - 1
                laser.change_y = -ENEMY_LASER_SPEED // 2
            if laser.angle == 90:
                laser.change_x = -ENEMY_LASER_SPEED
            if laser.center_x >= 900 or laser.center_y >= 900:
                self.enemy_laser_list.remove(laser)
            if laser.collides_with_sprite(self.player_sprite):
                self.kill_player()

        for enemy in self.enemy_list:
            if enemy.counter == enemy.pause_time:
                enemy_laser = enemy.fire_laser()
                self.enemy_laser_list.append(enemy_laser)

            if enemy.collides_with_sprite(self.player_sprite):
                self.kill_player()

            for laser in self.laser_list:
                if laser.collides_with_sprite(enemy):
                    if enemy.enemy_type == "starfighter":
                        self.score += 3
                    elif enemy.enemy_type == "shuttle1" or enemy.enemy_type == "shuttle1-r" or \
                            enemy.enemy_type == "shuttle2" or enemy.enemy_type == "shuttle2-r":
                        self.score += 2
                    else:
                        self.score += 1
                    self.laser_list.remove(laser)
                    enemy.kill()
                    arcade.play_sound(self.enemy_explosion)


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


main()
