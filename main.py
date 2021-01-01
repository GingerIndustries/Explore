print("Becoming self-aware...")
from colorama import Fore, Back
import enemy
import term
import colorama
from time import sleep
import sys
import os
print("Starting Skynet")
from readchar import readchar, readkey
import json
colorama.init()
print(Fore.RESET)

cur_room = "start"
inventory = []
monies = 0
max_health = 30
health = max_health
game_running = True
player_damage = 5
enemies_list = []
achievements_list = []
puzzle_tries_remaining = 3

BLINKING_TEXT = '\x1b[5m'
RESET_FANCY_TEXT = '\x1b[m'
print("Created memory boxes")
try:
    with open("json/rooms.json", "r") as read_file:
        room_data = json.load(read_file)
    with open("json/items.json", "r") as read_file:
        item_data = json.load(read_file)
    with open("json/enemies.json", "r") as read_file:
        enemy_data = json.load(read_file)
    with open("json/boss_levels.json", "r") as read_file:
        boss_level_data = json.load(read_file)
    with open("json/ascii.json", "r") as read_file:
        ascii_data = json.load(read_file)
    with open("json/achievements.json", "r") as read_file:
        achievments_data = json.load(read_file)
except Exception as e:
    print("shite, crusty screwed up")
    raise e


def typewriter(text, isFast=False):
    for x in text:
        print(x, end='')
        sys.stdout.flush()
        if isFast:
            sleep(0.04)
        else:
            sleep(0.1)


def getRoomData(roomID):
    return room_data.get("rooms").get(roomID)


def loadEnemies(roomID):
    enemies_objects = []
    for item in roomID.get("enemies"):
        enemies_objects.append(enemy.Enemy(enemy_data.get(item)))
    return enemies_objects


def enemiesAttack(enemies_objects):
    global health
    for item in enemies_objects:
        damageTaken = item.attack()
        if item.getCurHealth() <= 0:
            item.die()
            enemies_objects.delete(item)
        if damageTaken:
            takeDamage(damageTaken)


def getStructNameFromValue(key, value):
    for name, content in item_data.items():
        if key in content.keys() and content[key] == value:
            return name


def getAchievementData(ach_name):
    return achievments_data.get(ach_name)


def achievementGet(ach_name):
    if ach_name not in achievements_list:
        print(ascii_data.get("achievement_get"))
        sleep(0.5)
        typewriter(getAchievementData(ach_name).get("name"))
        sleep(0.5)
        typewriter(
            "\nType " + Fore.GREEN + "achievements" + Fore.RESET +
            " to see more info!\n\n",
            isFast=True)
        achievements_list.append(ach_name)


def listAchievements():
    typewriter("Your achievements:\n")
    if len(achievements_list) != 0:
        for item in achievements_list:
            itemData = getAchievementData(item)
            print(Fore.GREEN + itemData.get("name") + Fore.RESET + " | " +
                  itemData.get("description") + "\n")
    else:
        print(Fore.RED + "You don't have any achievements!" + Fore.RESET +
              "\n")


def makeChoice(options):
    print(Fore.GREEN)
    counter = 0
    for item in options:
        counter += 1
        print("[" + str(counter) + "] " + item)
    num_list = list(range(1, (counter + 1)))
    num_list = map(str, num_list)
    num_list = list(num_list)
    while True:
        rc = readchar()
        if rc in num_list:
            break
        else:
            print(Fore.YELLOW + "Invalid choice!")
    print(Fore.RESET)
    return int(rc)


def confirmPurchase(item_name, price):
    global monies
    if monies >= price:
        typewriter(
            "Buy " + Fore.GREEN + item_name + Fore.RESET + " for " +
            Fore.YELLOW + str(price) + Fore.RESET + " coins?\n",
            isFast=True)
        choice = makeChoice(["Yes!", "Nope."])
        if choice == 1:
            monies -= price
            return True
        else:
            return False
    else:
        typewriter(Fore.RED + "Not enough monies!" + Fore.RESET, isFast=True)
        return False


def triggerEvents(roomID):
    room = getRoomData(roomID)
    if len(room.get("entry_trigger")) != 0:
        globals()[room.get("entry_trigger")]()  #what the hell is this


def trigger_gate():
    global cur_room
    choice = makeChoice(["Talk to the ogre", "Leave"])
    os.system("clear")
    if choice == 1:
        typewriter(
            Fore.RED + "Ogre: " + Fore.RESET +
            "STOP! If you want to get through this gate, your going to have to pay! And if you think you can fight me, well, "
            + Fore.GREEN + "*the ogre grabs a club leaning against the wall*" +
            Fore.RESET + " you're wrong!\n",
            isFast=True)
        ogre_choice_1 = makeChoice(["Fight the ogre", "Pay the ogre", "Leave"])
        if ogre_choice_1 == 1:
            typewriter(
                Fore.RED + "Ogre: " + Fore.RESET +
                "Well little man, get ready to get MASHED!",
                isFast=True)
            #fighting code goes here
        elif ogre_choice_1 == 2:
            typewriter(
                Fore.RED + "Ogre: " + Fore.RESET +
                "Hand over the cash puny human!\n\n",
                isFast=True)
            if confirmPurchase("access to the room behind the gate", 10):
                sleep(1)
                os.system("clear")
                typewriter(
                    Fore.RED + "Ogre: " + Fore.RESET +
                    "Ok, fine, you can go...",
                    isFast=True)
            else:
                sleep(1)
                os.system("clear")
                typewriter(
                    Fore.RED + "Ogre: " + Fore.RESET +
                    "Hah! Of course you don't have enough monies. Now, BEGONE!\n",
                    isFast=True)
                sleep(1)
                cur_room = move(cur_room, 1)
                printRoom(cur_room)
        elif ogre_choice_1 == 3:
            typewriter(
                Fore.RED + "Ogre: " + Fore.RESET +
                "Of course you'd run away. Puny humans...",
                isFast=True)
            cur_room = move(cur_room, 1)
            printRoom(cur_room)
    elif choice == 2:
        cur_room = move(cur_room, 1)
        printRoom(cur_room)


def secretPitRoomPuzzleTrigger():
    global puzzle_tries_remaining
    start_choice = makeChoice(
        ["Look at the inscriptions", "Look at the buttons", "Leave"])
    if start_choice == 1:
        typewriter(
            "You stare at the inscriptions, brushing away the centuries of dust and grime that coat them. The runes appear to read, '3 chances you have, no more no less. What happens if you are wrong? That you should be able to guess.' The floor creaks ominously beneath you. Nervously, you continue to read. 'Here's a puzzle, just for you. If it's too hard, take the exit behind you. The more you take, the more you leave behind. What am I?'",
            isFast=True)
        secretPitRoomPuzzleTrigger()
    elif start_choice == 2:
        typewriter(
            " There are 26 square buttons, each with a rune on them. There is also a 27th button, much longer than the rest, and a 28th, with a set of runes that translate into 'Go'. It's like a keyboard...",
            isFast=True)
        keyboard_choice = makeChoice(["Enter some text", "Go back"])
        if keyboard_choice == 1:
            answer = input("What do you type? >")
            if answer.lower() == "footsteps":
              typewriter("You push the GO button and hear the distinctive sound of a spring retracting, followed by  the grinding of ancient gears rotating. The sound of metal scraping past metal fills your ears. Suddenly, it stops. After a few seconds, you hear a clunk and the sound of water rusintg into a bucket. Slowly, a section of wall slides away, as the hundred-year-old machinery strains to move its immense weight. Lying in an alcove behind it is a shiny key.\n", isFast=True)
              getLoot
            else:
              puzzle_tries_remaining -= 1
              if puzzle_tries_remaining <= 0:
                typewriter("The click comes one more time, and then silence. Suddenly the floor tiles under you fall away, and you drop screaming into the void.", isFast=True)
                sleep(1)
                die()
              else:
                typewriter("Suddenly,you hear something sliding down the wall behind the keyboard. It travels lower and lower, but suddenly rams into something. As it grinds back up, there is a click from something under the floor. You remember what the inscription said. 'Three tries you have, no more no less.'")
                secretPitRoomPuzzleTrigger()
        else:
            secretPitRoomPuzzleTrigger()
    elif start_choice == 3:
      pass


def printHealth():
    healthData = ""
    healthData += (Fore.RESET + "Health: [")
    if health <= round(max_health / 3):
        healthData += (Fore.RED)
    elif health <= round(max_health / 2):
        healthData += (Fore.YELLOW)
    else:
        healthData += (Fore.GREEN)
    healthData += (str(health) + Fore.RESET + "/" + str(max_health) + "]")
    print(healthData)


def die():
    global game_running
    os.system("clear")
    sleep(1)
    typewriter(Fore.RED + "You have died.")
    game_running = False


def takeDamage(damage):
    global health
    health -= damage
    if health <= 0:
        die()
    else:
        printHealth()


def attackMonster(enemy_data):
    if len(enemy_data) == 0:
        print(Fore.RED + "You can't do that!" + Fore.RESET)
    else:
        print("You attack " + enemy_data[0].getName() + " for " +
              str(player_damage) + " damage!")
        enemy_health = (enemy_data[0].getCurHealth() - player_damage)
        enemy_data[0].takeDamage((enemy_health))


def printRoom(roomID):
    global enemies_list
    room = getRoomData(roomID)
    loot = room.get("loot")
    if len(room.get("enemies")) == 0:
        pass
    typewriter(room.get("roomDesc"), isFast=True)
    print("\n")
    if len(loot):
        _loot_names = []
        for item in loot:
            _loot_names.append(getItemName(item))
        print(Fore.CYAN + "You see: ", end="")
        print(*_loot_names)
        print(Fore.RESET)
    exits = room.get("exits")
    print("Exits: " + Fore.GREEN, end="")
    if len(exits):
      print(*exits)
    else:
      print("None")
    print(Fore.RESET)
    triggerEvents(roomID)
    enemies_list = loadEnemies(room)
    if len(enemies_list) != 0:
        enemiesAttack(enemies_list)


def credits():
    os.system("clear")
    typewriter(Fore.GREEN + "Credits:\n")
    typewriter(
        Fore.CYAN + "CrustyFriends" + Fore.RESET + ": Game Design/Ideas\n",
        isFast=True)
    typewriter(
        Fore.CYAN + "tehgingergod/Blue" + Fore.RESET + ": Programming\n",
        isFast=True)
    print("(Enter to continue)")
    while readkey() != "\r":
        pass


def getItemName(itemID):
    item = item_data.get(itemID)
    return item.get("name")


def move(roomID, direction):
    room = getRoomData(roomID)
    if direction == 1:
        print("You move north.")
        return room.get("neighboring_rooms").get("north")
    elif direction == 2:
        print("You move east.")
        return room.get("neighboring_rooms").get("east")
    elif direction == 3:
        print("You move south.")
        return room.get("neighboring_rooms").get("south")
    elif direction == 4:
        print("You move west.")
        return room.get("neighboring_rooms").get("west")
    elif direction == 5:
        print("You jump down into the hole.")
        return room.get("neighboring_rooms").get("down")


def getLoot(roomID, itemName):
    global monies, inventory
    room = getRoomData(roomID)
    if not len(room.get("loot")) == 0:
        _loot = room.get("loot")
        itemID = getStructNameFromValue("name", itemName.title())
        item = item_data.get(itemID)
        if itemID in _loot:
            if itemID not in inventory:
                print("You pick up: " + Fore.GREEN, end="")
                if item.get("rarity") == "common":
                    print(Fore.GREEN, end="")
                elif item.get("rarity") == "uncommon":
                    print(Fore.YELLOW, end="")
                elif item.get("rarity") == "rare":
                    print(Fore.CYAN, end="")
                elif item.get("rarity") == "key":
                  print(Fore.PURPLE)
                print(item.get("name"))
                if item.get("name") == "Gold Coins":
                    monies += 10
                    print("+10 monies!" + Fore.RESET)
                    _loot.pop("Gold Coins")
                inventory.append(itemID)
            else:
                print(Fore.RED + "You already have that!")
        else:
            print(Fore.RED + "You don't see that!")
        print(Fore.RESET)
    else:
        print(Fore.YELLOW + "No items in this room..." + Fore.RESET)


def displayInventory():
    print("Items in your inventory:")
    for item_name in inventory:
        item = item_data.get(item_name)
        if item.get("rarity") == "common":
            print(Fore.GREEN, end="")
        elif item.get("rarity") == "uncommon":
            print(Fore.YELLOW, end="")
        elif item.get("rarity") == "rare":
            print(Fore.CYAN, end="")
        print(item.get("name"))
        print(Fore.RESET + Back.RESET)


print("Done")

sleep(0.3)
try:
    while True:
        os.system("clear")
        typewriter("Welcome to ")
        for x in (Fore.BLUE + '''
  ___________              .__                        
  \_   _____/__  _________ |  |   ___________   ____  
  |    __)_\  \/  /\____ \|  |  /  _ \_  __ \_/ __ \ 
  |        \>    < |  |_> >  |_(  <_> )  | \/\  ___/ 
  /_______  /__/\_ \|   __/|____/\____/|__|    \___  >
        \/      \/|__|                           \/ ''' + Fore.RESET):
            print(x, end='')
            sys.stdout.flush()
            sleep(0.005)
        typewriter(
            Fore.GREEN + "\n\n[1] PLAY" + Fore.RESET + "\n", isFast=True)
        typewriter(
            Fore.YELLOW + "[2] CREDITS" + Fore.RESET + "\n", isFast=True)
        typewriter(
            Fore.RED +
            "\n\nWARNING: DEMO BUILD\nGAME IS UNSTABLE AND MAY CRASH AT ANY TIME\n"
            + Fore.RESET,
            isFast=True)
        rc = readchar()
        if rc == '1':
            os.system("clear")
            break
        elif rc == "2":
            credits()

    typewriter(
        "You are a young explorer looking to rid the world of evil, conquer the darkness! You have arrived at the entrence of a dungeon notorious for all the adventurers that have gone missing within. But you know that you can defeat whatever is lurking in the depths of the dungeon. And so you decend into the darkness below...\n",
        isFast=True)
    sleep(1.5)
    print(BLINKING_TEXT, end="")
    typewriter(Fore.GREEN + "\n(Enter to continue)")
    print(RESET_FANCY_TEXT)
    while readkey() != "\r":
        pass
    os.system("clear")
    typewriter(
        Fore.YELLOW + "Monies: " + str(monies) + Fore.RESET + "\n" + Fore.GREEN
        + "Type 'help' for the command list!\n" + Fore.RESET,
        isFast=True)
    while game_running:
        sleep(1)
        printRoom(cur_room)
        command = input("> ")
        os.system("clear")
        print(Fore.YELLOW + "Monies: " + str(monies) + Fore.RESET + "\n")
        if command == "go north" and "north" in getRoomData(cur_room).get(
                "exits"):
            cur_room = move(cur_room, 1)
        elif command == "go east" and "east" in getRoomData(cur_room).get(
                "exits"):
            cur_room = move(cur_room, 2)
        elif command == "go south" and "south" in getRoomData(cur_room).get(
                "exits"):
            cur_room = move(cur_room, 3)
        elif command == "go west" and "west" in getRoomData(cur_room).get(
                "exits"):
            cur_room = move(cur_room, 4)
        elif command == "go down" and "down" in getRoomData(cur_room).get(
                "exits"):
            cur_room = move(cur_room, 5)
        elif command == "debug":
            achievementGet("curiosity")
        elif "pick" in command:
            _pick_args = command.split()
            _pick_args.pop(0)
            _pick_name = " ".join(_pick_args)
            try:
                getLoot(cur_room, _pick_name)
            except TypeError:
                pass
            sleep(1.5)
            os.system("clear")
            print(Fore.YELLOW + "Monies: " + str(monies) + Fore.RESET)
        elif command == "inventory":
            displayInventory()
        elif command == "attack" or command == "a":
            attackMonster(enemies_list)
        elif command == "achievements":
            listAchievements()
        elif command == "help":
            typewriter(Fore.GREEN + "Help:" + Fore.RESET + "\n")
            print("go" + Fore.GREEN + " [north|east|south|west]" + Fore.RESET +
                  ": Change the room you're in\n")
            print("pick: Pick up any items in the room you're in.\n")
            print("inventory: List the items in your inventory.\n")
            print("-----------------\n")
        else:
            print(Fore.RED + "Invalid command." + Fore.RESET)
    for x in (Fore.GREEN + '''\n\n 
    ____  ____ ____   ____     ___ _   _ ____  ____ 
  / _  |/ _  |    \ / _  )   / _ \ | | / _  )/ ___)
  ( ( | ( ( | | | | ( (/ /   | |_| \ V ( (/ /| |    
  \_|| |\_||_|_|_|_|\____)   \___/ \_/ \____)_|    
  (_____|                                                  
  ''' + Fore.RESET):
        print(x, end='')
        sys.stdout.flush()
        sleep(0.005)
except Exception as e:
    print("oh shite, blue screwed up")
    raise e
finally:
    pass
