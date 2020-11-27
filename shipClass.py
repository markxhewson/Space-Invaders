import pygame, sys
from laserClass import laserClass as Laser

class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship = None
        self.laser_img = None
        self.lasers = []
        self.cooldown_counter = 0

    def draw(self, screen):
        screen.blit(self.ship.convert_alpha(), (self.x, self.y))
        for laser in self.lasers: laser.draw(screen)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(750): self.lasers.remove(laser)
            if laser.collision(obj):
                self.lasers.remove(laser); obj.health -= 15

    def cooldown(self):
        if self.cooldown_counter >= 20: self.cooldown_counter = 0
        elif self.cooldown_counter > 0: self.cooldown_counter += 1

    def shoot(self):
        if self.cooldown_counter == 0:
            laser = Laser(self.x-25, self.y, self.laser_img)
            self.lasers.append(laser); self.cooldown_counter = 1

    def get_height(self):
        return self.ship.get_height()

    def get_width(self):
        return self.ship.get_width()
