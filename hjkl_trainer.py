import time
import sched
import os
import keyboard
import random
import re


array = [[' ' for _ in range(10)] for _ in range(10)]
highscores = []
most_recent_nickname = "VIM"





class Player:
    player_y = 4
    player_x = 5
    prev_inputs = []
    quit_triggered = False

    @staticmethod
    def trigger_quit():
        Player.quit_triggered = True
    @staticmethod
    def reset_quit():
        Player.quit_triggered = False
    @staticmethod
    def has_quit():
        return Player.quit_triggered 
    
    @staticmethod
    def reset():
        Player.player_y = 4
        Player.player_x = 5


def clear_console():
    if os.name == 'nt':  # For Windows
        os.system('cls')
    else:  # For macOS and Linux
        os.system('clear')

def process_input(keyboard_event):

    # print(keyboard_event.scan_code)

    if keyboard_event.event_type == keyboard.KEY_UP:
        return

    if keyboard_event.scan_code == 4: # 4
        if Player.player_x > 0:
            Player.player_x -= 1 
    elif keyboard_event.scan_code == 38: # J
        if Player.player_y < 9:
            Player.player_y += 1
     
    elif keyboard_event.scan_code == 40: # k
        if Player.player_y > 0:
            Player.player_y -= 1   
    elif keyboard_event.scan_code == 37: # l
        if Player.player_x < 9:
            Player.player_x += 1

    elif keyboard_event.scan_code == 12: # q
 
        Player.trigger_quit()

def display():
    print("+-H-<--J-!--K-^--L->-+")
    for y, row in enumerate(array):
        display_line = ["|"]
        for x, cell in enumerate(row):
            if y == Player.player_y and x == Player.player_x:
                display_line.append("x")

            elif y == Gem.gem_y and x == Gem.gem_x:
                display_line.append("$")

            else:
                enemy_flag = False
                for tuple in Enemy.locations:
                    if y == tuple[0] and x == tuple[1]:
                        display_line.append("O") 
                        enemy_flag = True
                        break

                if not enemy_flag:               
                    display_line.append(" ")

        display_line.append("|")

        print(' '.join(display_line))
    print("+---------------------+")

class Enemy:

    test_property = False
    @classmethod
    def change_test_property(cls):
        Enemy.test_property = True

    @classmethod
    def print_locations(cls):
        print(Enemy.locations)

    instances = []

    locations = []

    @classmethod
    def log_locations(cls):
        Enemy.locations = []
        for instance in Enemy.instances:
            Enemy.locations.append((instance.enemy_y, instance.enemy_x))

    @classmethod
    def move_all(cls):
        for instance in Enemy.instances:
            instance.move_self()



    def __init__(self):
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

        self.enemy_y = self.determine_y()
        self.enemy_x = self.determine_x()

        Enemy.instances.append(self)

    def determine_y(self):
        if self.direction == "UP":
            return - 1
        elif self.direction == "DOWN":
            return 10
        else:
            return random.randint(0,9)
        
    def determine_x(self):
        if self.direction == "RIGHT":
            return - 1
        elif self.direction == "LEFT":
            return 10
        else:
            return random.randint(0,9)
        
    def move_self(self):
        if self.direction == "UP":
            self.enemy_y += 1
        elif self.direction == "DOWN":
            self.enemy_y -= 1
        elif self.direction == "RIGHT":
            self.enemy_x += 1
        elif self.direction == "LEFT":
            self.enemy_x -= 1

      
        if self.check_if_oob():
            self.self_destruct()

    def check_if_oob(self):
        if (self.direction == "UP" and self.enemy_y >= 10) or (self.direction == "DOWN" and self.enemy_y <= -1) or (self.direction == "RIGHT" and self.enemy_x >= 10) or (self.direction == "LEFT" and self.enemy_x <= -1):
            return True
        else:
            return False
        
    def self_destruct(self):

        Enemy.instances.remove(self)
        del self

    @classmethod
    def kill_all(cls):
        Enemy.locations = []
        for instance in Enemy.instances:
            instance.self_destruct()


def move_enemies():
    for instance in Enemy.instances:
        instance.move_self()
    
def check_collision():
    for tuple in Enemy.locations:
        if Player.player_y == tuple[0] and Player.player_x == tuple[1]:
            return True
    return False
        
def spawn_enemy():
    Enemy()

class Gem:

    @staticmethod
    def determine_coord():
        return random.randint(1, 8)

    gem_y = determine_coord()
    gem_x = determine_coord()

    @classmethod
    def collect(cls):
        cls.gem_y = cls.determine_coord()
        cls.gem_x = cls.determine_coord()

def gem_collision():
    if Player.player_y == Gem.gem_y and Player.player_x == Gem.gem_x:
        Gem.collect()
        return True
    return False

def reset_game():
    Gem.collect()
    Player.reset()
    Enemy.kill_all()

def read_highscores():
    filename = "highscores.txt"
    if os.path.isfile(filename):
        with open(filename, 'r') as file:
            content = file.read().splitlines()
            global highscores
            highscores = []
            for i, line in enumerate(content):
                parts = line.strip().split()
                # print(parts)
                highscores.append((parts[0], parts[2]))
                if i == len(content) - 1:
                    global most_recent_nickname
                    most_recent_nickname = parts[0]
    
def write_highscores():
    filename = "highscores.txt"
    with open(filename, 'w') as file:
        for score in highscores:
            file.write(f"{score[0]} : {str(score[1])}\n")

def add_score(new_score):
    user_input = input(f"Enter a 3 letter name for your score of {new_score}!!(default is '{most_recent_nickname}'): ")
    name_slug = ""
    if len(user_input) < 3 or re.search(r'[^a-zA-Z]', user_input):
        name_slug = most_recent_nickname
    else:
        name_slug = "".join([user_input[0],user_input[1],user_input[2]]).upper()

    highscores.append((name_slug, new_score))

def print_highscores():
    sorted_highscores = sorted(highscores, key=lambda x: int(x[1]), reverse=True)
    print("HIGHSCORES")
    if len(sorted_highscores) == 0:
        print(" - no highscores yet - ")
    for i, score in enumerate(sorted_highscores):
        if i < 10:
            print(f"{str(i + 1)}: {score[0]} : {str(score[1])}")

def main():
    read_highscores()
    try:
        keyboard.hook(process_input)

    except KeyboardInterrupt:

        print("get me outa heeeerrreee")

    frames = 0
    levels = 1
    gems = 0
    current_score = 0

    done = False

    while not done:
        time.sleep(0.025)
        
        frames += 1

        if frames % (12 - min([(levels // 3), 7]))== 0:
            move_enemies()
            Enemy.log_locations()

        if frames % 200 < 175:
            if frames % (65 - levels) == 1:
                spawn_enemy()
            if levels > 5 and frames % 50 == 1:
                spawn_enemy()
            if levels > 10 and frames % 75 == 1:
                spawn_enemy()
            if levels > 15 and frames % 100 == 1:
                spawn_enemy()
            if levels > 20 and frames % 110 == 1:
                current_score += 5
                spawn_enemy()
                spawn_enemy()
            if levels > 25 and frames % 170 == 1:
                current_score += 10
                spawn_enemy()
                spawn_enemy()
                spawn_enemy()
   
        
        if gem_collision():
            gems += 1
            if gems % 4 == 0:
                levels += 1
                current_score += 50
            else:
                current_score += 20

        if check_collision():
            done = True

        if Player.has_quit():
            done = True

        clear_console()
        print("LEVEL: ", levels, " SCORE: ", current_score)
        display()

    done = False

    keyboard.unhook_all()
    clear_console()

    print("Game Over!")
    player_continue = input("\n")
    clear_console()

    print_highscores()
    add_score(current_score)
    write_highscores()
    clear_console()
    print_highscores()
    replay = input("Enter q to quit or anything else to replay!")
    keyboard.unhook_all()

    if replay != "q":
        Player.reset_quit()
        reset_game()
        done = False
        main()

if __name__ == "__main__":
    main()  # Initial call to main()



