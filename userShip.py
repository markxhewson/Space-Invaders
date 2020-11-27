import pygame, os, json
from shipClass import Ship

user_ship = pygame.image.load(os.path.join("graphics", "pixel_ship_yellow.png"))
user_laser = pygame.image.load(os.path.join("graphics", "pixel_laser_yellow.png"))

with open("settings.json") as configuration:
    config = json.load(configuration)

class userShip(Ship):

    def __init__(self, x, y, health=100):
        super().__init__(x, y)
        self.ship = user_ship
        self.health = health
        self.laser_img = user_laser
        self.velocity = config["entityValues"]["userSpeed"]
        self.mask = pygame.mask.from_surface(self.ship)
        self.max_health = health; self.shooting = False

    def move_lasers(self, vel, objs, instance):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(750): self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        if obj in objs: objs.remove(obj)
                        if laser in self.lasers: self.lasers.remove(laser)
                        if not self.health >= 95: self.health += 2
                        instance.points += 1

    def draw(self, screen):
        super().draw(screen); self.healthbar(screen)

    def healthbar(self, screen):
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y + self.ship.get_height() + 10, self.ship.get_width(), 10))
        pygame.draw.rect(screen, (0,255,0), (self.x, self.y + self.ship.get_height() + 10, self.ship.get_width() * (self.health/self.max_health), 10))
