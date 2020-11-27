
class user_powerups:
    def __init__(self):
        self.freeze_powerup = False
        self.freeze_cooldown = 0
        self.speed_powerup = False
        self.speed_cooldown = 0

    def check_freeze_cooldown(self, enemies):
        if self.freeze_cooldown >= 650: self.freeze_cooldown = 0
        elif self.freeze_cooldown >= 1:
            self.freeze_cooldown += 1
            if self.freeze_cooldown >= 250:
                for enemy in enemies:
                    if enemy.velocity == 0: enemy.velocity += 1.5

    def check_speed_cooldown(self, user):
        if self.speed_cooldown >= 950: self.speed_cooldown = 0
        elif self.speed_cooldown >= 1:
            self.speed_cooldown += 1
            if self.speed_cooldown >= 500:
                if user.velocity != 3: user.velocity -= 4

    def start_freeze_powerup(self, enemies):
        for enemy in enemies:
            if enemy.velocity != 0: enemy.velocity -= 1.5
        self.freeze_cooldown = 1
        self.freeze_powerup = False

    def start_speed_powerup(self, user):
        if user.velocity != 7: user.velocity += 4
        self.speed_cooldown = 1
        self.speed_powerup = False

