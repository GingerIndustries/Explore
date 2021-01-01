from colorama import Fore
import random
print("Loaded spoopy codes")

class Enemy():
    def __init__(self, enemy_data):
        self.enemy_data = enemy_data
        self.max_health = enemy_data.get("health")
        self.cur_health = self.max_health
        self.name = enemy_data.get("name")

    def attack(self):
        monster = self.enemy_data
        if random.choice(range((monster.get("difficulty") + 1))) != 0:
            damageTaken = random.randint(1, (
            1 + (round(random.random() * 10 * monster.get("difficulty")))))
            print(Fore.RED + self.name + " attacks for " + str(damageTaken) +
            " damage!" + Fore.RESET + "\n")
            return damageTaken
        else:
            print(Fore.RED + self.name + " swings but misses!\n" + Fore.RESET)
            return False


    def getCurHealth(self):
        return self.cur_health
    def _setHealth(self, value):
      self.cur_health = value
    def getName(self):
      return self.name
    def getMaxHealth(self):
        return self.max_health

    def takeDamage(self, newHealthValue):
        self._setHealth(newHealthValue)
        #print(Fore.RED + self.name + " Health: [" + Fore.RESET + str(self.cur_health) + Fore.RED + "]" + Fore.RESET)

    def die(self):
        print(Fore.RED + self.name + " has died!" + Fore.RESET)
        xp = random.randint(1, (self.enemy_data.get("difficulty") * 2))
        if len(self.enemy_data.get("loot")) != 0:
            return self.enemy_data.get("loot"), xp
        else:
            return False, xp
