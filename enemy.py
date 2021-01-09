from colorama import Fore
import random


class Enemy():
    def __init__(self, enemy_data):
        #print("init")
        self.enemy_data = enemy_data
        self.max_health = enemy_data.get("health")
        self.cur_health = self.max_health
        self.name = enemy_data.get("name")
        self.is_dead = False

    def attack(self):
      if not self.is_dead:
        monster = self.enemy_data
        if random.choice(range((monster.get("difficulty") + 1))) != 0:
            damageTaken = random.randint(((monster.get("difficulty") ^ 2 ) + 1), (
            1 + (round(random.random() * 10 * monster.get("difficulty")))))
            
            print(Fore.RED + self.name + " attacks for " + str(damageTaken) +
            " damage!" + Fore.RESET + "\n")
            return damageTaken
        else:
            print(Fore.RED + self.name + " swings but misses!\n" + Fore.RESET)
            return False
      else:
        return False


    def getCurHealth(self):
        return self.cur_health
    def getName(self):
      return self.name
    def getMaxHealth(self):
        return self.max_health
    def getIsDead(self):
      return self.is_dead
    def takeDamage(self, amount):
      if not self.is_dead:
        self.cur_health -= amount
        print(Fore.RED + self.name + " Health: [" + Fore.RESET + str(self.cur_health) + Fore.RED + "]" + Fore.RESET)
        return True
      else:
        return False

    def die(self):
        self.is_dead = True
        print(Fore.RED + self.name + " has died!" + Fore.RESET)
        xp = random.randint(1, (self.enemy_data.get("difficulty") * 2))
        if len(self.enemy_data.get("loot")) != 0:
            return self.enemy_data.get("loot"), xp
        else:
            return False, xp
print("Loaded spoopy codes")