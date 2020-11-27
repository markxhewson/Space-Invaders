import pygame, os, json
from shipClass import Ship
from laserClass import laserClass as Laser

red_enemy = pygame.image.load(os.path.join("graphics", "red_enemy.png"))
green_enemy = pygame.image.load(os.path.join("graphics", "green_enemy.png"))
pink_enemy = pygame.image.load(os.path.join("graphics", "pink_enemy.png"))
laser = pygame.image.load(os.path.join("graphics", "pixel_laser_yellow.png"))

with open("settings.json") as configuration:
    config = json.load(configuration)

class enemyShip(Ship):
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.enemy_colors = { "red": red_enemy, "green": green_enemy, "pink": pink_enemy }
        self.ship = self.enemy_colors[color]
        self.velocity = config["entityValues"]["enemySpeed"]
        self.mask = pygame.mask.from_surface(self.ship)
        self.laser_img = laser

    def move(self, velocity):
        self.y += velocity

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser); self.cooldown_counter = 1
