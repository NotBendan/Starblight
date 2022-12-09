import random
import arcade

speed_scale = 1


class Laser(arcade.Sprite):
    def __init__(self, sprite, center_x, center_y, angle):
        super().__init__(sprite)
        self.center_x = center_x
        self.center_y = center_y
        self.angle = angle


class Enemy(arcade.Sprite):
    def __init__(self, center_x, center_y, enemy_type):
        if enemy_type == "pod":
            super().__init__(":resources:images/topdown_tanks/tankBody_green.png", 1.25)
            self.angle = -90
            self.pause_time = None
        elif enemy_type == "turret":
            super().__init__(":resources:images/tiles/leverLeft.png", 0.5)
            self.pause_time = round(60 / speed_scale)
        elif enemy_type == "turret-r":  # "-r" stands for reverse
            super().__init__(":resources:images/tiles/leverRight.png", 0.5)
            self.angle = 180
            self.pause_time = round(60 / speed_scale)
        elif enemy_type == "shuttle1" or enemy_type == "shuttle1-r":  # "-r" stands for reverse
            super().__init__(":resources:images/space_shooter/playerShip1_blue.png", 0.65)
            self.angle = 90
            self.pause_time = round(40 / speed_scale)
        elif enemy_type == "shuttle2" or enemy_type == "shuttle2-r":  # "-r" stands for reverse
            super().__init__(":resources:images/space_shooter/playerShip1_green.png", 0.65)
            self.angle = 90
            self.pause_time = round(40 / speed_scale)
        elif enemy_type == "starfighter":
            super().__init__(":resources:images/space_shooter/playerShip2_orange.png", 0.65)
            self.angle = 90
            self.pause_time = round(30 / speed_scale)

        self.center_x = center_x
        self.center_y = center_y
        self.enemy_type = enemy_type
        self.counter = 0
        self.laser_sound = arcade.load_sound(":resources:sounds/laser2.wav")

    def fire_laser(self):
        laser = None
        if self.enemy_type == "turret":
            laser = Laser(":resources:images/space_shooter/laserRed01.png",
                          self.center_x - 15, self.center_y, 45)
            # Calculates the time between laser shots
            if 10 // speed_scale < 2:
                self.pause_time = round((2 // 4 * 60) + self.counter)
            else:
                self.pause_time = round((random.randrange(2, round(10 / speed_scale)) / 4) * 60 + self.counter)

        elif self.enemy_type == "turret-r":
            laser = Laser(":resources:images/space_shooter/laserRed01.png",
                          self.center_x - 15, self.center_y, 135)
            if 10 // speed_scale < 2:
                self.pause_time = round((2 // 4 * 60) + self.counter)
            else:
                self.pause_time = round(((random.randrange(2, round(10 / speed_scale)) / 4) * 60) + self.counter)

        elif self.enemy_type == "shuttle1" or self.enemy_type == "shuttle1-r" or \
                self.enemy_type == "shuttle2" or self.enemy_type == "shuttle2-r":
            laser = Laser(":resources:images/space_shooter/laserRed01.png",
                          self.center_x, self.center_y, 90)
            if 8 // speed_scale < 3:
                self.pause_time = round((2 // 4 * 60) + self.counter)
            else:
                self.pause_time = round(((random.randrange(3, round(8 / speed_scale)) / 4) * 60) + self.counter)

        elif self.enemy_type == "starfighter":
            laser = Laser(":resources:images/space_shooter/laserRed01.png",
                          self.center_x, self.center_y, 90)
            if 6 // speed_scale < 2:
                self.pause_time = round((2 // 4 * 60) + self.counter)
            else:
                self.pause_time = round(((random.randrange(2, round(6 / speed_scale)) / 4) * 60) + self.counter)
        arcade.play_sound(self.laser_sound, 0.5)
        return laser

    def update(self):
        self.center_x += -1 * speed_scale
        self.counter += 1 * speed_scale
        if self.center_x < -100:
            self.kill()
        if self.enemy_type == "pod":
            if -1 < self.counter % 100 < 20:
                self.center_x += -3 * speed_scale
        elif self.enemy_type == "shuttle1" or self.enemy_type == "shuttle1-r":
            if -1 < self.counter % 120 < 30 or 59 < self.counter % 120 < 90:
                self.center_x += -3 * speed_scale
            elif 29 < self.counter % 120 < 60:
                if self.enemy_type == "shuttle1-r":
                    self.center_y += 4 * speed_scale
                else:
                    self.center_y += -4 * speed_scale
            elif 89 < self.counter % 120 < 120:
                if self.enemy_type == "shuttle1-r":
                    self.center_y += -4 * speed_scale
                else:
                    self.center_y += 4 * speed_scale
        elif self.enemy_type == "shuttle2" or self.enemy_type == "shuttle2-r":
            if -1 < self.counter % 100 < 40:
                self.center_x += -5 * speed_scale
            elif 39 < self.counter % 100 < 100:
                if self.enemy_type == "shuttle2-r":
                    self.center_y += 1.5 * speed_scale
                else:
                    self.center_y += -1.5 * speed_scale
                self.center_x += 2 * speed_scale
        elif self.enemy_type == "starfighter":
            self.center_x += -3 * speed_scale
            if -1 < self.counter % 60 < 30:
                self.center_y += -3 * speed_scale
            if 29 < self.counter % 60 < 60:
                self.center_y += 3 * speed_scale


class EnemySpawner(arcade.Sprite):
    def __init__(self, center_y, enemy_type, enemy_count, distance_multiplier):
        super().__init__(":resources:images/items/coinGold.png")
        self.center_x = 850
        self.center_y = center_y
        self.enemy_type = enemy_type
        self.enemy_count = enemy_count
        self.counter = 0
        self.temp_list = arcade.SpriteList()
        self.multiplier = distance_multiplier

    def update(self):
        self.counter += 1
        if self.counter == (50 * self.multiplier // speed_scale) * self.enemy_count + 1:
            self.kill()
        if self.counter % ((50 * self.multiplier) // speed_scale) == 0:
            self.temp_list.append(Enemy(self.center_x, self.center_y, self.enemy_type))
