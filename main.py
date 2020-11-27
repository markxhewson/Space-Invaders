import pygame, sys, json, utils, os
from userShip import userShip
from enemyShip import enemyShip
from abilities import user_powerups
from random import randrange, choice

with open("settings.json") as configuration:
    config = json.load(configuration)

pygame.init()

background_location = pygame.transform.scale(pygame.image.load(os.path.join("graphics", "background.jpg")), (config["gameSettings"]["borderWidth"], config["gameSettings"]["borderHeight"]))
freeze_powerup = pygame.image.load(os.path.join("graphics", "slow_boost.png"))
speed_powerup = pygame.image.load(os.path.join("graphics", "speed_boost.png"))

class SpaceInvaders:
    def __init__(self, width, height):
        self.width = width; self.height = height
        self.background_name = config["graphicsSettings"]["backgroundLocation"]
        self.caption = pygame.display.set_caption(config["gameName"])
        self.screen = pygame.display.set_mode([self.width, self.height])
        self.clock = pygame.time.Clock()
        self.display = pygame.display
        self.font = pygame.font.Font(None, 26)
        self.font_color = (241, 12, 39)
        self.lives = config["gameSettings"]["defaultLives"]; self.points = 0; self.level = 0
        self.fps = config["gameSettings"]["maxFramerate"]
        self.enemies = []; self.active = True; self.lost = False
        self.wave = 0; self.wave_increase = config["gameSettings"]["waveIncrease"]
        
    def start_game(self, instance):
        print("Loading game functions..")
        self.run(instance)

    def update_screen(self, powerup):
        self.screen.blit(pygame.image.load(self.background_name), (0, 0))
        self.screen.blit(freeze_powerup, (650, 25))
        self.screen.blit(speed_powerup, (635, 140))
        self.screen.blit(self.font.render(f"• Lives: {self.lives}", 1, self.font_color), (24, 35))
        self.screen.blit(self.font.render(f"• Points: {self.points}", 1, self.font_color), (24, 75))
        self.screen.blit(self.font.render(f"• Level: {self.level}", 1, self.font_color), (24, 115))
        self.screen.blit(self.font.render(f"Cooldown: {int(powerup.freeze_cooldown / 60)}", 1, self.font_color), (630, 105))
        self.screen.blit(self.font.render(f"Cooldown: {int(powerup.speed_cooldown / 60)}", 1, self.font_color), (630, 235))

        for enemies in self.enemies: enemies.draw(self.screen)

        if self.lost:
            lost_label = self.font.render(config["screenMessages"]["gameEndMessage"], 1, self.font_color)
            self.screen.blit(lost_label, (int(self.width / 2) - int(lost_label.get_width() / 2), 350))

    def create_enemies(self, user, instance, powerup):
        for enemies in self.enemies:
            enemies.move(enemies.velocity)
            enemies.move_lasers(config["entityValues"]["laserSpeed"], user)

            if randrange(1, 150) == 1:
                if enemies.velocity != 0: enemies.shoot()
                
            if utils.collide(enemies, user):
                self.enemies.remove(enemies)
                self.points += 1; user.health -= 15
                
            if enemies.y >= 735:
                self.lives -= 1; self.enemies.remove(enemies)

        if powerup.freeze_powerup: powerup.start_freeze_powerup(self.enemies)
        if powerup.speed_powerup: powerup.start_speed_powerup(user)
        powerup.check_freeze_cooldown(self.enemies)
        powerup.check_speed_cooldown(user)
                
        user.move_lasers(-config["entityValues"]["laserSpeed"], self.enemies, instance)

    def check_enemies(self):
        if len(self.enemies) <= 0:
            self.wave += self.wave_increase; self.level += 1

            for i in range(self.wave):
                enemy_object = enemyShip(randrange(50, self.width - 100), randrange(-3000, -25), choice(["red", "green", "pink"]))
                self.enemies.append(enemy_object)

    def send_text(self, message, x, y):
        lost_message = self.font.render(message, 1, self.font_color)
        self.screen.blit(lost_message, (x, y))

    def run(self, instance):
        user = userShip(345, 650)
        powerup = user_powerups()

        while self.active:
            if self.lost: end_menu()
            if self.lives <= 0 or user.health <= 0: self.lost = True
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: self.close_program()

            # UPDATING FUNCTIONS
            self.update_screen(powerup); self.create_enemies(user, instance, powerup)
            # CREATE USER & ENEMIES
            user.draw(self.screen); self.check_enemies()

            if self.lives <= 0: self.lost = True
            keys = pygame.key.get_pressed()

            # LEFT
            if keys[pygame.K_LEFT] and user.x - user.velocity > 0:
                if keys[pygame.K_SPACE]: user.x -= user.velocity - 1
                else: user.x -= user.velocity
            # RIGHT
            if keys[pygame.K_RIGHT] and user.x + user.velocity + user.get_width() < self.width:
                if keys[pygame.K_SPACE]: user.x += user.velocity - 1
                else: user.x += user.velocity
            # UP
            if keys[pygame.K_UP] and user.y - user.velocity > 0:
                if keys[pygame.K_SPACE]: user.y -= user.velocity - 1
                else: user.y -= user.velocity
            # DOWN
            if keys[pygame.K_DOWN] and user.y + user.velocity + user.get_height() + 5 < self.height:
                if keys[pygame.K_SPACE]: user.y += user.velocity - 1
                else: user.y += user.velocity
                
            #SHOOT
            if keys[pygame.K_SPACE]: user.shoot()

            #FREEZE POWERUP ACTIVATOR
            if keys[pygame.K_x]:
                if powerup.freeze_cooldown == 0: powerup.freeze_powerup = True
                else:
                    if powerup.freeze_cooldown <= 400 and powerup.freeze_cooldown != 0: pass
            #SPEED POWERUP ACTIVATOR
            if keys[pygame.K_c]:
                if powerup.speed_cooldown == 0: powerup.speed_powerup = True
                else:
                    if powerup.speed_cooldown <= 400 and powerup.speed_cooldown != 0: pass
                    
            self.clock.tick(self.fps)
            self.display.update()

    def close_program(self):
        self.active = False
        pygame.quit()
        sys.exit()

def load_game():
    if __name__ == "__main__":
        game = SpaceInvaders(config["gameSettings"]["borderWidth"], config["gameSettings"]["borderHeight"])
        game.start_game(game)

def start_menu():
    title_font = pygame.font.SysFont("comicsans", 25); gameContinue = True
    start_screen = pygame.display.set_mode((config["gameSettings"]["borderWidth"], config["gameSettings"]["borderHeight"]))
    game_info = config["screenMessages"]["gameInformation"]
    count = 200
    linesCount = 0
    
    while gameContinue:
        start_screen.blit(background_location, (0,0))
        
        title_label = title_font.render(config["screenMessages"]["startMenu"], 1, (255,255,255))
        start_screen.blit(title_label, (15, 175))

        for lines in game_info:
            text = lines.split(";")
            font_text = title_font.render(text[1], 1, (255, 255, 255))
            start_screen.blit(font_text, (15, int(text[0])))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: gameContinue = False; exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN: load_game()

        pygame.display.update()

def end_menu():
    title_font = pygame.font.SysFont("comicsans", 25); gameContinue = True
    end_screen = pygame.display.set_mode((config["gameSettings"]["borderWidth"], config["gameSettings"]["borderHeight"]))
    game_end_info = config["screenMessages"]["gameEndInformation"]
    
    while gameContinue:
        end_screen.blit(background_location, (0,0))
        
        title_label = title_font.render(config["screenMessages"]["gameEndMessage"], 1, (255,255,255))
        end_screen.blit(title_label, (15, 175))

        for lines in game_end_info:
            text = lines.split(";")
            font_text = title_font.render(text[1], 1, (255, 255, 255))
            end_screen.blit(font_text, (15, int(text[0])))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: gameContinue = False; exit()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_x]: gameContinue = False; exit()
                else: load_game()

        pygame.display.update()

start_menu()
