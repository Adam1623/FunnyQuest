#########################################################################
# Author : Adam Fast
# Description: Funny Quest, a Turn-based rpg. Buy upgrades and fight monsters until taking down the bees!
# Date Created : December 20, 2022
#########################################################################
import turtle
import random
import time
import winsound
import ast
# CHANGE THE DEBUG VALUE TO SKIP INTRO
# Can also cheat by editing values in save file, for any experimentation you may want to do.
# Save files may not always work properly
debug = False

global charshape1, charshape2, char1Stats, char2Stats, char1Name, char2Name, curplace, allfighters, \
    gold, bagitems, difficulty, savefile, allvars, whichloop, firstload, shopitems
savefile = ""
loadfile = ""
char1Name = ""
char2Name = ""
char1Stats = []
char2Stats = []
char1Upgrades = 0
char2Upgrades = 0
curplace = 0
allfighters = []
gold = 0
bagitems = []
difficulty = 0
whichloop = ""
charshape1 = ""
charshape2 = ""
shopitems = []
firstload = False
allvars = [char1Name, char2Name, char1Stats, char2Stats, char1Upgrades, char2Upgrades, curplace, allfighters,
           gold, bagitems, difficulty, whichloop, charshape1, charshape2]
savedvars = []


def stopmusic(track):
    winsound.PlaySound(None, winsound.SND_PURGE)
    if track is not None:
        winsound.PlaySound(track, winsound.SND_ASYNC)


def startmusic(track):
    winsound.PlaySound(track, winsound.SND_ASYNC | winsound.SND_NOSTOP | winsound.SND_LOOP)


# Lets player choose to load a save file or not.
while loadfile not in ["y", "n"]:
    loadfile = input("Would you like to load your save file (y/n)? ")
    if loadfile == "y":
        try:
            savefile = open("FunnyQuestSavefile.txt", "r")
        except FileNotFoundError:
            print("No save file found. Exiting program.")
            quit()
        else:
            firstload = True
            savedvars = []
            for i in savefile.readlines():
                i = i.rstrip()
                try:
                    int(i)
                except ValueError:
                    pass
                else:
                    i = int(i)
                savedvars.append(i)
            char1Name = list(savedvars)[0]
            char2Name = list(savedvars)[1]

            aaa = ast.literal_eval(list(savedvars)[2])
            aaa[1] = aaa[2]
            char1Stats = aaa

            aaa = ast.literal_eval(list(savedvars)[3])
            aaa[1] = aaa[2]
            char2Stats = aaa

            aaa = ast.literal_eval(list(savedvars)[4])
            char1Upgrades = aaa

            aaa = ast.literal_eval(list(savedvars)[5])
            char2Upgrades = aaa

            curplace = list(savedvars)[6]

            aaa = ast.literal_eval(list(savedvars)[7])
            allfighters = aaa

            gold = list(savedvars)[8]

            aaa = ast.literal_eval(list(savedvars)[9])
            bagitems = aaa

            difficulty = list(savedvars)[10]
            whichloop = list(savedvars)[11]
            charshape1 = list(savedvars)[12]
            charshape2 = list(savedvars)[13]
        savefile.close()
        break
    elif loadfile == "n":
        print("Making new save file, starting game.")
        break
    print("Invalid input.")


def savegame():
    global savefile, allvars
    allvars = allvars
    savefile = open("FunnyQuestSavefile.txt", "w")
    allvars[0] = char1Name
    allvars[1] = char2Name
    aaa = char1Stats
    if len(aaa) > 2:
        aaa[1] = aaa[2]
        aaa[-1] = allfighters[0][-1]
    allvars[2] = aaa

    aaa = char2Stats
    if len(aaa) > 2:
        aaa[1] = aaa[2]
        aaa[-1] = allfighters[1][-1]
    allvars[3] = aaa

    allvars[4] = char1Upgrades
    allvars[5] = char2Upgrades
    allvars[6] = curplace
    if len(savedvars) > 6:
        savedvars[7] = allfighters
    allvars[7] = allfighters
    allvars[8] = gold
    allvars[9] = bagitems
    allvars[10] = difficulty
    allvars[11] = whichloop
    wlist = savedvars
    if not savedvars:
        wlist = allvars
    for v in range(len(allvars)):
        savefile.write(f"{wlist[v]}\n")

    savefile.close()


#####
# Default setup stuff
#####
win = turtle.Screen()
win.setup(800, 800)
rootwindow = turtle.getcanvas().winfo_toplevel()
rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
win.bgcolor("black")


def restartloop():
    win.onclick(whichloop)


curtrack = "track1"


def sound(s):
    try:
        winsound.PlaySound(s, winsound.SND_ASYNC | winsound.SND_NOSTOP)
    except RuntimeError:
        pass
    else:
        winsound.PlaySound(s, winsound.SND_ASYNC | winsound.SND_NOSTOP)

#####
# Saves all sprites to the turtle window, and adds some into sublists for easier distinction
#####
allSprites = ["Warrior", "Archer", "King", "Doctor",
              "Slime", "Ant", "Bat", "Bandit", "Rat", "Bee", "Big Bee",
              "Bag", "RedPotion", "GoldenArrow", "CoinPouch", "Bandages",
              "AttackButton", "ItemButton", "RevengeButtonOff", "RevengeButtonOn", "UseButton", "ButtonBg",
              "BuyButton", "CoinIcon", "LeaveButton",
              "WarriorUpgrade1", "WarriorUpgrade2", "WarriorUpgrade3",
              "ArcherUpgrade1", "ArcherUpgrade2", "ArcherUpgrade3",
              "KingUpgrade1", "KingUpgrade2", "KingUpgrade3",
              "DocUpgrade1", "DocUpgrade2", "DocUpgrade3",
              "RockBag", "ThrowingStar", "Apple", "Bomb", "Goop",
              "ShopBg", "GrassBg", "EndCredits"]
for i in allSprites:
    win.addshape(f"{i}" + ".gif")
allGameClasses = allSprites[:4]
#####
# Creates turtles, name variables and stat variables for the characters
#####
c1 = turtle.Turtle()
c1.speed(0)
c1.ht()
c1.up()
c2 = turtle.Turtle()
c2.speed(0)
c2.ht()
c2.up()
char1Stats = []
char2Stats = []
allStats = [[], []]

#####
# Creates turtles for any potential enemies
#####
e1 = turtle.Turtle()
e1.speed(0)
e1.ht()
e1.up()
e2 = turtle.Turtle()
e2.speed(0)
e2.ht()
e2.up()
e3 = turtle.Turtle()
e3.speed(0)
e3.ht()
e3.up()
e4 = turtle.Turtle()
e4.speed(0)
e4.ht()
e4.up()
enemySprites = [e1, e2, e3, e4]
enemyStats = []

#####
# Creates turtles for each button
#####
battlebg = turtle.Turtle()
battlebg.speed(0)
battlebg.ht()
battlebg.up()
attackb = turtle.Turtle()
attackb.speed(0)
attackb.ht()
attackb.up()
revengeb = turtle.Turtle()
revengeb.speed(0)
revengeb.ht()
revengeb.up()
hb1 = turtle.Turtle()
hb1.speed(0)
hb1.ht()
hb1.width(5)
hb1.color("#9b1212")
hb1.up()
hb2 = turtle.Turtle()
hb2.speed(0)
hb2.ht()
hb2.width(5)
hb2.color("#9b1212")
hb2.up()
rb = turtle.Turtle()
rb.speed(0)
rb.ht()
rb.width(5)
rb.color("#9b1212")
rb.up()
itemb = turtle.Turtle()
itemb.speed(0)
itemb.ht()
itemb.up()
itembuse = turtle.Turtle()
itembuse.speed(0)
itembuse.ht()
itembuse.up()
itemb1 = turtle.Turtle()
itemb1.speed(0)
itemb1.ht()
itemb1.up()
itemb2 = turtle.Turtle()
itemb2.speed(0)
itemb2.ht()
itemb2.up()
itemb3 = turtle.Turtle()
itemb3.speed(0)
itemb3.ht()
itemb3.up()
itemb4 = turtle.Turtle()
itemb4.speed(0)
itemb4.ht()
itemb4.up()
itembuttons = [itemb1, itemb2, itemb3, itemb4]
sitem4 = turtle.Turtle()
sitem4.speed(0)
sitem4.ht()
sitem4.up()
sitem5 = turtle.Turtle()
sitem5.speed(0)
sitem5.ht()
sitem5.up()
sitem6 = turtle.Turtle()
sitem6.speed(0)
sitem6.ht()
sitem6.up()
buyitemb = turtle.Turtle()
buyitemb.speed(0)
buyitemb.ht()
buyitemb.up()
shopleaveb = turtle.Turtle()
shopleaveb.speed(0)
shopleaveb.ht()
shopleaveb.up()
coinb = turtle.Turtle()
coinb.speed(0)
coinb.ht()
coinb.up()
coinb2 = turtle.Turtle()
coinb2.speed(0)
coinb2.ht()
coinb2.up()

#####
# Randomly selects a class for both characters
#####
# Order: name, (hp), max hp, revenge, strength, defense, luck, current revenge
# Revenge charges based on the amount of damage you take, and lets you unleash a special attack when at max
gameClasses = [
    # name,     mhp, r, s, d, l,  cr
    ("warrior", 15, 13, 4, 1, 8, 0),
    ("archer", 13, 7, 5, 0, 20, 0),
    ("king", 12, 9, 3, 2, 15, 0),
    ("doctor", 10, 7, 2, 1, 18, 0)]
allitems = [
    "RedPotion",
    "GoldenArrow",
    "CoinPouch",
    "Bandages",

    "WarriorUpgrade1",
    "WarriorUpgrade2",
    "WarriorUpgrade3",
    "ArcherUpgrade1",
    "ArcherUpgrade2",
    "ArcherUpgrade3",
    "KingUpgrade1",
    "KingUpgrade2",
    "KingUpgrade3",
    "DocUpgrade1",
    "DocUpgrade2",
    "DocUpgrade3",

    "RockBag",
    "ThrowingStar",
    "Apple",
    "Bomb",
    "Goop"

]
itemdesc = [
    [
        "Health potion",
        "Golden arrow",
        "Coin pouch",
        "Bandages",

        "Sharper sword (Warrior)",
        "Shield (Warrior)",
        "Gold sword (Warrior)",
        "Bronze arrows (Archer)",
        "Iron arrows (Archer)",
        "Diamond arrows (Archer)",
        "Shinier chalice (King)",
        "Shinier crown (King)",
        "Platinum crown (King)",
        "Acidic potions (Doctor)",
        "Stronger potions (Doctor)",
        "Strongest potions (Doctor)",

        "Bag of rocks",
        "Throwing star",
        "Apple",
        "Bomb",
        "Goop"
    ],
    [
        "Heals this character by 15 hp.",
        "Deals 15 damage to one enemy, ignoring defense.",
        "Deals 6 damage to all enemies.",
        "Heals both characters by 7 hp.",

        " +1 attack \n +5 luck",
        " +1 defense \n +5 max hp",
        " +2 attack \n +10 luck",
        " +1 attack \n +2 max hp",
        " +1 attack \n +3 max hp",
        " +1 attack \n +1 defense \n +5 luck",
        " +2 attack \n +4 max hp",
        " +1 defense \n +7 max hp",
        " +1 attack \n +2 defense \n +5 luck",
        " +3 attack",
        " +2 attack \n +1 defense",
        " +2 attack \n +3 max hp",

        "Deals 4 damage to all enemies.",
        "Hits three enemies for 5 damage, ignoring defense.",
        "+1 defense to both characters for this battle.",
        "Deals 14 damage to one enemy.",
        "+4 defense to this character for one battle"
    ]
]
# List of all enemies
# Order: name, hp, max hp, gold, strength, defense, lethality , difficulty(MUST BE AT END)
# lethality is the odds the enemy will attack the character with less health
enemyTypes = [
    # name,  hp, mhp, g, s, d, l , di
    ("ant", 4, 4, 1, 3, 1, 20, 1),
    ("slime", 10, 10, 2, 3, 0, 50, 2),
    ("rat", 8, 8, 2, 4, 0, 0, 4),
    ("bandit", 10, 10, 5, 5, 1, 60, 7),
    ("bat", 15, 15, 4, 4, 1, 70, 8),
    ("bee", 20, 20, 8, 5, 2, 0, 100),
    ("big bee", 42, 42, 100, 8, 1, 80, 200)
]
# Positions for the enemy on the screen
enemyPositions = [(250, 0), (150, 60), (150, -90), (250, 120)]
allpos = [(-250, 110), (-250, -50), (250, 0), (150, 60), (150, -90), (250, 120)]
#####
# Sets up text drawer
#####
curText = turtle.Turtle()
curText.speed(0)
curText.ht()
curText.up()
turnText = turtle.Turtle()
turnText.speed(0)
turnText.ht()
turnText.up()
itemdescText = turtle.Turtle()
itemdescText.speed(0)
itemdescText.ht()
itemdescText.up()


#####
# Used for writing text, with parameters to customize the text


def writetext(colour, speed, font, section, trail, textobj, text):
    if debug:
        speed = 0
        trail = 0
    temptext = ""
    if font == 0:
        font = ("Courier", 25, "")
    if textobj == 0:
        textobj = curText
    textobj.color(colour)
    # Bottom left
    if type(section) == tuple:
        textobj.goto(section[0], section[1])
    elif section == 1:
        textobj.goto(-200, -200)
    # Centered, middle
    elif section == 2:
        textobj.goto(-250, 0)
    # Top left
    elif section == 3:
        textobj.goto(-320, 200)
    # Bottom right
    elif section == 4:
        textobj.goto(350 - len(text) * font[1], -200)
    # Middle left, textbox height
    elif section == 5:
        textobj.goto(-370, -200)
    # Top middle
    elif section == 6:
        textobj.goto(-200, 350)
    if speed == 0:
        temptext = text
        textobj.write(temptext, font=font)
    else:
        for i in range(len(text)):
            temptext += text[i]
            textobj.write(len(temptext) * " " + temptext[i], font=font)
            time.sleep(1 / speed)

    if trail != 0:
        for i in range(trail + 1):
            textobj.write(len(temptext) * " " + " " + "." * i, font=font)
            time.sleep(0.4)


#####
# Determines which class the two characters will be and sets their stats
#####
if loadfile == "n":
    while allStats[0] == allStats[1] or allStats[0] == [] or allStats[1] == []:
        try:
            allStats[allStats.index([])] = random.choice(gameClasses)
        except ValueError:
            char1Stats = []
            char2Stats = []
            allStats = [[], []]
    char1Stats = list(allStats[1])
    char2Stats = list(allStats[0])
    c1.shape(allGameClasses[gameClasses.index(tuple(char1Stats))] + ".gif")
    c2.shape(allGameClasses[gameClasses.index(tuple(char2Stats))] + ".gif")
    charshape1 = c1.shape()
    charshape2 = c2.shape()
    char1Stats.insert(1, char1Stats[1])
    char2Stats.insert(1, char2Stats[1])


#####
# Opening scene, Asks for both character names to be inputted, writes some text revealing
# what class both characters are, fades in and starts the tutorial battle.
#####


def intro():
    if loadfile == "y":
        startmusic("GRASSY MOUNTAIN.wav")
        return
    global char1Name, char2Name
    if not debug:
        char1Name = win.textinput("Name selection", "What is your first character's name? ")[0:15].capitalize()
        char2Name = win.textinput("Name selection", "What is your second character's name? ")[0:15].capitalize()
    else:
        char1Name = "Char 1"
        char2Name = "Char 2"
    win.bgcolor("black")
    writetext("white", 50, 0, 2, 3, 0, "Your adventure begins")
    curText.clear()
    writetext("white", 50, 0, 3, 1, 0, f"{char1Name}, the {char1Stats[0].title()}")
    writetext("white", 50, 0, 4, 1, 0, f"{char2Name}, the {char2Stats[0].title()}")

    if debug:
        win.bgcolor("gray100")
        curText.clear()
    else:
        startmusic("GRASSY MOUNTAIN.wav")
        time.sleep(1)
        curText.clear()
        for i in range(10):
            time.sleep(0.1)
            win.bgcolor(f"gray{(i + 1) * 10}")
        time.sleep(0.1)


#####
# Start of battle code
#####


global battleover, turnnum, nextturn, target, targetpos, menuact, itempos, inhandle, \
    itemcho, crit, eselected, multiattack

if loadfile == "n":
    # An integer used to determine how many enemies and their stats, the higher number the harder the difficulty
    difficulty = 0
    bagitems = []
    gold = 0
    # Add two items to bag at start of the game based on the classes of hero
    # (only called at start of game, not each battle)
    for i in gameClasses:
        if char1Stats[0] == i[0] or char2Stats[0] == i[0]:
            bagitems.append(allitems[gameClasses.index(i)])


def startbattle():
    global difficulty, enemyStats, firstload, allvars, allfighters, char1Stats, char2Stats
    # All possibles types of enemies
    tempenemytypes = enemyTypes
    # Changeable difficulty to count each enemy being chosen
    tempdif = difficulty
    # Used for generating a group of enemies
    tempenemies = []
    # List storing all enemy stats
    enemyStats = []
    # Sets sprites of player characters
    c1.shape(charshape1)
    c2.shape(charshape2)
    if not firstload:
        if tempdif == 0:
            tempenemies.append(enemyTypes[1])
        # While loop used to calculate and randomly generate which enemies to spawn, always hits difficulty value
        while tempdif != 0:
            tempdif = difficulty
            tempenemies = []
            totalvalue = 0
            for e in range(4):
                tempenemy = list(random.choice(tempenemytypes))
                tempenemies.append(tempenemy)
                totalvalue += tempenemy[-1]
                if tempdif == totalvalue:
                    break
            tempdif -= totalvalue
        thisbattle = tempenemies
    else:
        for i in range(len(allfighters[2:len(allfighters)])):
            allfighters[i + 2][1] = allfighters[i + 2][2]
        thisbattle = list(allfighters[2:len(allfighters)])
    if firstload:
        char1Stats = allfighters[0]
        char2Stats = allfighters[1]
    else:
        firstload = False
    # This is the boss fight
    if difficulty >= 30:
        stopmusic(None)
        startmusic("QUESTING.wav")
        thisbattle = [enemyTypes[-1], enemyTypes[-2], enemyTypes[-2], enemyTypes[-2]]
    for a in range(len(thisbattle)):
        enemyStats.append(thisbattle[a])
        enemySprites[a].shape(f"{enemyStats[a][0].title()}" + ".gif")
        enemySprites[a].goto(enemyPositions[a])
    # Draws all enemies and characters on screen, {sets background}
    c1.goto(allpos[0])
    c2.goto(allpos[1])
    c1.st()
    c2.st()
    for conenemies in range(len(enemyStats)):
        enemySprites[conenemies].st()

    #####
    # Point where battle loop begins
    #####
    global battleover, turnnum, nextturn, whichloop, menuact, itempos, inhandle, eselected, multiattack
    battleover = 0
    turnnum = 0
    allfighters = []
    nextturn = False
    eselected = 0
    menuact = 0
    itempos = [(-30, 70), (-30, -10), (-30, -90)]
    multiattack = True
    # Sets up sprites for bag items
    itemb1.shape("Bag.gif")
    itembuse.shape("UseButton.gif")
    while char1Stats == [] or char2Stats == []:
        aaa = ast.literal_eval(list(savedvars)[2])
        char1Stats = aaa
        aaa = ast.literal_eval(list(savedvars)[3])
        char2Stats = aaa
    allfighters.append(char1Stats)
    allfighters.append(char2Stats)
    for i in thisbattle:
        allfighters.append(list(i))
    allvars[7] = allfighters
    if allfighters.index(allfighters[turnnum]) < 2:
        battlebg.shape("ButtonBg.gif")
        battlebg.goto(0, -250)
        attackb.shape("AttackButton.gif")
        attackb.goto(-250, -280)
        itemb.shape("ItemButton.gif")
        itemb.goto(0, -280)
        revengeb.shape("RevengeButtonOff.gif")
        revengeb.goto(230, -280)
        if allfighters[0][7] >= allfighters[0][3]:
            revengeb.shape("RevengeButtonOn.gif")
        hb1start = allpos[0][0] - 50, allpos[0][1] - 60
        hb1end = allpos[0][0] + 40, allpos[0][1] - 60
        hb2start = allpos[1][0] - 50, allpos[1][1] - 60
        hb2end = allpos[1][0] + 40, allpos[1][1] - 60
        hb1.goto(hb1start)
        hb1.down()
        hb1.goto(hb1end)

        hb2.goto(hb2start)
        hb2.down()
        hb2.goto(hb2end)

        writetext("black", 0, ("Courier", 20), 5, 0, turnText, f"{[char1Name, char2Name][turnnum]}'s turn.")
        updatehealthbar(3)
        battlebg.st()
        attackb.st()
        itemb.st()
        revengeb.st()
        # Sets what loop the game loop starts with
        inhandle = True
        whichloop = battleloop
        restartloop()
        attackb.onclick(attacking)
        itemb.onclick(openitems)
        itembuse.onclick(useitemb)
        revengeb.onclick(userevenge)


def battleendcheck():
    global allfighters, battleover, inhandle
    count = 0
    for c in allfighters[0:2]:
        if c[1] <= 0:
            count += 1
    if count == len(allfighters[0:2]):
        battleover = 2
    else:
        count = 0
        for e in allfighters[2:len(allfighters)]:
            if e[1] <= 0:
                count += 1
        if count == len(allfighters[2:len(allfighters)]):
            battleover = 1
    return battleover


def endcredits():
    win.clear()
    battlebg = turtle.Turtle()
    battlebg.speed(0)
    battlebg.ht()
    battlebg.up()
    stopmusic("ROLL THE CREDITS.wav")
    for i in range(10):
        time.sleep(0.05 * i)
        win.bgcolor(f"gray{100 - i * 10}")
    time.sleep(0.2)
    win.bgcolor("black")
    battlebg.shape("EndCredits.gif")
    battlebg.goto(0, -1400)
    battlebg.st()
    while battlebg.pos()[1] < 720:
        battlebg.goto(0, battlebg.pos()[1] + 1)
        time.sleep(0.01)
    win.exitonclick()


def endbattle(didwin):
    global allfighters, gold, difficulty, inhandle
    for t in [c1, c2, e1, e2, e3, e4]:
        t.ht()
    closemenu(1)
    closemenu(2)
    closemenu(3)
    closemenu(4)
    if didwin:
        if difficulty >= 30:
            endcredits()
            return
        char1Stats[7] = allfighters[0][7]
        char2Stats[7] = allfighters[1][7]
        for i in allfighters[2: len(allfighters)]:
            gold += i[3]
        difficulty += 2
        whichplace(2)
    else:
        quit()


def enemyselection(x, y):
    global target, allfighters, whichloop, targetpos, inhandle
    if whichloop != enemyselection:
        return
    target = []
    for i in enemyPositions:
        if i[0] - 40 <= x <= i[0] + 40 and i[1] - 40 <= y <= i[1] + 40:
            try:
                target = allfighters[enemyPositions.index(i) + 2]
            except IndexError:
                pass
            else:
                if target[1] > 0:
                    targetpos = i
                    whichloop = battleloop
                    damagecalc(0.25, 0.5)
    if not target:
        restartloop()


def battleloop(x, y):
    global battleover, turnnum, allfighters, nextturn, target, menuact, inhandle, crit
    if battleover == -1:
        return
    battleover = battleendcheck()
    if battleover == 0:
        if nextturn:
            turnnum += 1
            nextturn = False
            menuact = 0
            if turnnum == len(allfighters):
                turnnum = 0
            # Skips turn if person has no health left
            if allfighters[turnnum][1] <= 0:
                nextturn = True
                battleloop(0, 0)
                return
            # If player's turn
            if allfighters.index(allfighters[turnnum]) < 2:
                turnText.clear()
                writetext("black", 0, ("Courier", 20), 5, 0, turnText, f"{[char1Name, char2Name][turnnum]}'s turn.")
                battlebg.st()
                attackb.st()
                itemb.st()
                if allfighters[turnnum][7] >= allfighters[turnnum][3]:
                    revengeb.shape("RevengeButtonOn.gif")
                else:
                    revengeb.shape("RevengeButtonOff.gif")
                updatehealthbar(3)
                revengeb.st()
                inhandle = True
                restartloop()
            else:
                curText.clear()
                turnText.clear()
                attackb.ht()
                itemb.ht()
                revengeb.ht()
                rb.clear()
                inhandle = True
                attacking(0, 0)
    if battleover == 1:
        battleover = -1
        inhandle = False
        turnText.clear()
        curText.clear()
        writetext("black", 0, ("Courier", 25, "bold"), 6, 0, 0, "      You won!")
        time.sleep(1)
        endbattle(True)
    elif battleover == 2:
        battleover = -1
        inhandle = False
        turnText.clear()
        curText.clear()
        writetext("black", 0, 0, 6, 0, 0, "You lost...")
        time.sleep(1)
        endbattle(False)


def closemenu(which):
    global whichloop, nextturn, turnnum
    # Attack menu
    if which == 1:
        curText.clear()
        whichloop = battleloop
        restartloop()
    # Item menu
    elif which == 2:
        curText.clear()
        itemdescText.clear()
        itembuse.ht()
        for b in itembuttons:
            b.ht()
        whichloop = battleloop
        restartloop()
    # Health bars
    elif which == 3:
        hb1.clear()
        hb2.clear()
    # Buttons
    elif which == 4:
        turnText.clear()
        attackb.ht()
        itemb.ht()
        revengeb.ht()
        battlebg.ht()
        rb.clear()


def attacking(x, y):
    global turnnum, nextturn, target, targetpos, whichloop, allfighters, menuact, inhandle, crit
    crit = False
    if not inhandle:
        sound("off.wav")
        return
    inhandle = False
    # Called if it's a player's attack
    if allfighters.index(allfighters[turnnum]) < 2:
        sound("on.wav")
        # Determines if attack is a crit
        if random.randint(1, 100) <= allfighters[turnnum][6]:
            crit = True
        if menuact == 1:
            closemenu(1)
            menuact = 0
        else:
            closemenu(2)
            menuact = 1
            writetext("black", 0, 0, 6, 0, 0, "Choose who to attack:")
            whichloop = enemyselection
            restartloop()
    # else called if it's an enemy's turn
    else:
        writetext("black", 0, 0, 6, 0, 0, f"{allfighters[turnnum][0].title()} Attacking!")
        whichtarget = [allfighters[0], allfighters[1]]
        weakcalc1 = allfighters[0][1] + int(allfighters[0][2] / 2)
        weakcalc2 = allfighters[1][1] + int(allfighters[1][2] / 2)
        if whichtarget[0][1] <= 0 or whichtarget[1][1] <= 0:
            if whichtarget[0][1] <= 0:
                target = allfighters[1]
                targetpos = (-250, -50)
            else:
                target = allfighters[0]
                targetpos = (-250, 150)
        elif random.randint(1, 100) > allfighters[turnnum][6]:
            # Chooses stronger character
            if weakcalc1 > weakcalc2:
                target = allfighters[0]
                targetpos = (-250, 150)
            else:
                target = allfighters[1]
                targetpos = (-250, -50)
        # Chooses weaker character
        elif weakcalc1 > weakcalc2:
            target = allfighters[1]
            targetpos = (-250, -50)
            if weakcalc1 == weakcalc2:
                if allfighters[0][2] >= allfighters[1][2]:
                    target = allfighters[0]
                    targetpos = (-250, 150)
                else:
                    target = allfighters[1]
                    targetpos = (-250, -50)
        else:
            target = allfighters[0]
            targetpos = (-250, 150)
        whichloop = battleloop
        inhandle = True
        damagecalc(0.25, 0.4)
    restartloop()
    inhandle = True


def updatehealthbar(which):
    global allfighters
    if which == 1:
        hb1start = allpos[0][0] - 50, allpos[0][1] - 60
        hb1end = allpos[0][0] + 40, allpos[0][1] - 60
        hb1calc = allfighters[0][1] / allfighters[0][2] * 90 + hb1start[0]
        if hb1calc <= hb1start[0]:
            hb1.clear()
        else:
            hb1.up()
            hb1.goto(hb1start)
            hb1.down()
            hb1.clear()
            hb1.goto(hb1calc, hb1end[1])
    elif which == 2:
        hb2start = allpos[1][0] - 50, allpos[1][1] - 60
        hb2end = allpos[1][0] + 40, allpos[1][1] - 60
        hb2calc = allfighters[1][1] / allfighters[1][2] * 90 + hb2start[0]
        if hb2calc <= hb2start[0]:
            hb2.clear()
        else:
            hb2.up()
            hb2.goto(hb2start)
            hb2.down()
            hb2.clear()
            hb2.goto(hb2calc, hb2end[1])
    elif which == 3:
        # revenge button start pos: (230, -280)
        rbstart = (170, -320)
        rbcalc = allfighters[turnnum][7] / allfighters[turnnum][3] * 120 + rbstart[0]
        if rbcalc <= rbstart[0]:
            rb.clear()
        else:
            rb.up()
            rb.goto(rbstart)
            rb.down()
            rb.clear()
            rb.goto(rbcalc, -320)


def damagecalc(delay1, delay2):
    # Order: name, (hp), max hp, revenge, strength, defense, luck, revenge level
    # Revenge charges based on the amount of damage you take, and lets you unleash a special attack when at max
    # name, hp, mhp, r, s, d, l,  cr
    global turnnum, target, targetpos, nextturn, whichloop, inhandle, crit
    if not inhandle:
        return
    inhandle = False
    attacker = allfighters[turnnum]
    tempattack = attacker[4]
    if crit:
        tempattack *= 2
    damagedealt = tempattack - target[5]
    if damagedealt <= 0:
        damagedealt = 1
    target[1] -= damagedealt
    allturts = [c1, c2, e1, e2, e3, e4]
    attacker = [c1, c2, e1, e2, e3, e4][turnnum]
    # Special things only when player is being targeted
    if allfighters.index(target) < 2:
        updatehealthbar(allfighters.index(target) + 1)
        if target[7] + damagedealt >= target[3]:
            target[7] = target[3]
        else:
            target[7] += damagedealt

    prevpos = attacker.pos()
    attacker.goto(0, 50)
    time.sleep(delay1)
    critclr = "black"
    if crit:
        writetext("red", 0, ("Courier", 10), (targetpos[0] - 15, targetpos[1] + 65), 0, 0, "Crit!")
        critclr = "red"
        sound("crit.wav")
    elif allfighters.index(target) < 2:
        sound("playerattack.wav")
    else:
        sound("enemyattack.wav")
    writetext(critclr, 0, 0, (targetpos[0] - 10, targetpos[1] + 30), 0, 0, f"{damagedealt}")
    if target[1] <= 0:
        if allfighters.index(target) < 2:
            allturts[allfighters.index(target)].ht()
        target[1] = 0
        for a in range(len(allfighters)):
            if allturts[a].pos() == targetpos:
                while allturts[a].isvisible():
                    allturts[a].ht()
                break
    time.sleep(delay2)
    attacker.goto(prevpos)
    curText.clear()
    nextturn = True
    battleloop(0, 0)


def openitems(x, y):
    global nextturn, menuact, whichloop, bagitems, itembuttons, inhandle
    if not inhandle:
        sound("off.wav")
        return
    inhandle = False
    sound("on.wav")
    if menuact == 2:
        menuact = 0
        closemenu(2)
    else:
        menuact = 2
        closemenu(1)
        writetext("black", 0, 0, 6, 0, 0, "Click item for info:")
        itemb1.goto(-30, 0)
        itemb1.st()
        for item in range(len(bagitems)):
            itembuttons[item + 1].shape(str(bagitems[item]) + ".gif")
            itembuttons[item + 1].goto(itempos[item])
        for item in range(len(bagitems)):
            itembuttons[item + 1].st()
    whichloop = itemchoice
    restartloop()
    inhandle = True


def itemchoice(x, y):
    global itempos, itemcho, inhandle, whichloop
    if not inhandle:
        return
    inhandle = False
    for i in itempos:
        if i[0] - 40 <= x <= i[0] + 40 and i[1] - 40 <= y <= i[1] + 40:
            try:
                itemcho = bagitems[itempos.index(i)]
            except IndexError:
                pass
            else:
                # If statement makes sure items can only be selected when visible on screen
                if itembuttons[bagitems.index(itemcho) + 1].isvisible():
                    itemchoidx = allitems.index(itemcho)
                    itemdescText.clear()
                    writetext("black", 0, ("Courier", 15, "bold"), (-100, 280), 0, itemdescText,
                              f"{itemdesc[0][itemchoidx]}")
                    writetext("black", 0, ("Courier", 15), (-100 - len(itemdesc[1][itemchoidx]) * 3, 250), 0,
                              itemdescText, f"{itemdesc[1][itemchoidx]}")
                    itembuse.goto(-30, 190)
                    itembuse.st()
    inhandle = True


def miscselection(x, y):
    global target, allfighters, whichloop, targetpos, inhandle, eselected, multiattack
    if not multiattack:
        return
    multiattack = False
    target = []
    for i in enemyPositions:
        if i[0] - 40 <= x <= i[0] + 40 and i[1] - 40 <= y <= i[1] + 40:
            try:
                target = allfighters[enemyPositions.index(i) + 2]
            except IndexError:
                pass
            else:
                if target[1] > 0:
                    targetpos = i
                    eselected += 1
                    inhandle = True
                    useitemb(0, 0)
                    return
    multiattack = True
    restartloop()


def miscattack(delay1, delay2, targets, damage, ignoredef):
    global whichloop, eselected, allpos
    allturts = [c1, c2, e1, e2, e3, e4]
    curText.clear()
    if len(targets) > 6:
        targets = [targets]
    attacker = allturts[turnnum]
    prevpos = attacker.pos()
    tempalltargets = list(targets)
    attacker = [c1, c2, e1, e2, e3, e4][turnnum]
    attacker.goto(0, 50)
    writetext("black", 0, 0, 6, 0, 0, f"     Attacking!")
    time.sleep(delay1)
    sound("crit.wav")
    for t in range(len(targets)):
        if targets[t][1] > 0:
            temptargetpos = allpos[t + 2]
            tempalltargets.remove(targets[t])
            tempdamage = damage
            if not ignoredef:
                tempdamage -= targets[t][5]
                if tempdamage < 0:
                    tempdamage = 0
            targets[t][1] -= tempdamage
            if eselected:
                temptargetpos = targetpos
            writetext("red", 0, 0, (temptargetpos[0] - 10, temptargetpos[1] + 30), 0, 0, f"{tempdamage}")
            if targets[t][1] <= 0:
                targets[t][1] = 0
                for a in range(len(allfighters)):
                    if allturts[a].pos() == temptargetpos:
                        while allturts[a].isvisible():
                            allturts[a].ht()
                        break
    time.sleep(delay2)
    attacker.goto(prevpos)


def mischeal(targets, power, delay, move):
    global allfighters
    charpos = [c1, c2]
    if move:
        char = charpos[turnnum]
        prevpos = char.pos()
        char.goto(0, 50)
    writetext("black", 0, 0, 6, 0, 0, f"      Healing!")
    if len(targets) > 6:
        targets = [targets]
    sound("heal.wav")
    for t in targets:
        if t[1] > 0:
            t[1] += power
            if t[1] > t[2]:
                t[1] = t[2]
            writetext("green", 0, 0, (charpos[allfighters.index(t)].pos()[0] - 10,
                                      charpos[allfighters.index(t)].pos()[1] + 30), 0, 0, f"{power}")
            updatehealthbar(allfighters.index(t) + 1)
    time.sleep(delay)
    if move:
        char.goto(prevpos)


def miscbuff(targets, stat, power, delay):
    possiblestats = ["maxhp", "revenge", "strength", "defense", "luck", "currevenge"]
    statindex = possiblestats.index(stat) + 2
    charpos = [c1, c2]
    writetext("black", 0, 0, 6, 0, 0, f"{stat.title()} buffed!")
    if len(targets) > 6:
        targets = [targets]
    sound("buff.wav")
    for t in targets:
        if t[1] > 0:
            t[statindex] += power
            writetext("green", 0, 0, (charpos[allfighters.index(t)].pos()[0] - 10,
                                      charpos[allfighters.index(t)].pos()[1] + 30), 0, 0, f"{power}")
    time.sleep(delay)


def useitemb(x, y):
    global inhandle, itemcho, bagitems, nextturn, whichloop, target, eselected, multiattack
    if not inhandle:
        sound("off.wav")
        return
    inhandle = False
    sound("on.wav")
    if itemcho in allitems:
        closemenu(2)
        if itemcho == "RedPotion":
            mischeal(allfighters[turnnum], 15, 0.75, False)
        elif itemcho == "GoldenArrow":
            writetext("black", 0, 0, (-280, 350), 0, 0, "Choose who to attack with item:")
            whichloop = miscselection
            restartloop()
            if eselected == 0:
                return
            curText.clear()
            miscattack(0.25, 0.5, target, 15, True)
            eselected = 0
        elif itemcho == "CoinPouch":
            miscattack(0.25, 0.75, allfighters[2:len(allfighters)], 6, False)
        elif itemcho == "Bandages":
            mischeal(allfighters[0:2], 7, 0.75, False)
        elif itemcho == "RockBag":
            miscattack(0.25, 0.5, allfighters[2: len(allfighters)], 4, False)
        elif itemcho == "ThrowingStar":
            writetext("black", 0, 0, (-340, 350), 0, 0, f"Choose who to attack with item (x{3 - eselected}):")
            whichloop = miscselection
            restartloop()
            if eselected == 0:
                return
            curText.clear()
            miscattack(0.2, 0.3, target, 5, True)
            curText.clear()
            if battleendcheck() == 0:
                writetext("black", 0, 0, (-340, 350), 0, 0, f"Choose who to attack with item (x{3 - eselected}):")
                if eselected <= 2:
                    multiattack = True
                    return
            eselected = 0
        elif itemcho == "Apple":
            miscbuff(allfighters[0:2], "defense", 1, 0.8)
        elif itemcho == "Bomb":
            writetext("black", 0, 0, (-280, 350), 0, 0, "Choose who to attack with item:")
            whichloop = miscselection
            restartloop()
            if not eselected:
                return
            miscattack(0.3, 0.6, target, 14, False)
        elif itemcho == "Goop":
            miscbuff(allfighters[turnnum], "defense", 4, 0.4)
        bagitems.remove(itemcho)
    closemenu(2)
    eselected = False
    curText.clear()
    nextturn = True
    multiattack = True
    whichloop = battleloop
    battleloop(0, 0)


def userevenge(x, y):
    global inhandle, turnnum, allfighters, nextturn, whichloop
    if not inhandle or revengeb.shape() == "RevengeButtonOff.gif":
        sound("off.wav")
        return
    inhandle = False
    closemenu(1)
    closemenu(2)
    allfighters[turnnum][7] = 0
    # Warrior revenge
    if allfighters[turnnum][0] == gameClasses[0][0]:
        miscbuff(allfighters[0:2], "strength", allfighters[turnnum][4] // 2, 1)
    # Archer revenge
    if allfighters[turnnum][0] == gameClasses[1][0]:
        miscattack(0.25, 0.75, allfighters[2:len(allfighters)], allfighters[turnnum][4] * 2 - 3, False)
    # King revenge
    if allfighters[turnnum][0] == gameClasses[2][0]:
        miscbuff(allfighters[turnnum % 1], "defense", (difficulty // 7) + 1, 1)
    # Doctor revenge
    if allfighters[turnnum][0] == gameClasses[3][0]:
        mischeal(allfighters[0:2], allfighters[turnnum][4] * 3 + 4, 0.75, True)
    nextturn = True
    curText.clear()
    whichloop = battleloop
    restartloop()


#####
#####
#   END OF COMBAT, SHOP BEGINS ###
#####
#####
if loadfile == "n":
    whichupgrades = allGameClasses.index(str(char1Stats[0]).title()) * 3
    char1Upgrades = allitems[whichupgrades + 4: whichupgrades + 7]
    whichupgrades = allGameClasses.index(str(char2Stats[0]).title()) * 3
    char2Upgrades = allitems[whichupgrades + 4: whichupgrades + 7]
curshopitems = []

# "RockBag",
# "ThrowingStar",
# "Apple",
# "Bomb",
# "Goop"
goldcosts = [
    10, 15, 25,
    8, 14, 20,
    9, 18, 20,
    10, 18, 22,
    5, 12, 8, 18, 25

]

global shoppos, shopitembuttons
orgshoppos = [(-220, 280), (10, 280), (240, 280), (-120, -300), (70, -300), (270, -300)]
orgshopitembuttons = [itemb1, itemb2, itemb3, sitem4, sitem5, sitem6]


def openshop():
    global whichloop, shoppos, shopitembuttons, inhandle, shopitems, char1Stats, char2Stats, firstload
    firstload = False
    shoppos = [(-220, 280), (10, 280), (240, 280), (-120, -280), (70, -280), (270, -280)]
    shopitembuttons = [itemb1, itemb2, itemb3, sitem4, sitem5, sitem6]
    shopitems = []
    curText.clear()
    turnText.clear()
    itemdescText.clear()
    # Sets top three items to upgrade for first hero, random choice of both heroes, and upgrade for second hero
    if len(char1Upgrades) > 0:
        itemb1.shape(char1Upgrades[- len(char1Upgrades)] + ".gif")
    else:
        shoppos.remove(orgshoppos[0])
        shopitembuttons.remove(orgshopitembuttons[0])
    if len(char2Upgrades) > 0:
        itemb3.shape(char2Upgrades[- len(char2Upgrades)] + ".gif")
    else:
        shoppos.remove(orgshoppos[2])
        shopitembuttons.remove(orgshopitembuttons[2])
    if random.randint(1, 2) == 1:
        if len(char1Upgrades) > 1:
            itemb2.shape(char1Upgrades[1 - len(char1Upgrades)] + ".gif")
        elif len(char2Upgrades) > 1:
            itemb2.shape(char2Upgrades[1 - len(char2Upgrades)] + ".gif")
        else:
            shoppos.remove(orgshoppos[1])
            shopitembuttons.remove(orgshopitembuttons[1])
    else:
        if len(char2Upgrades) > 1:
            itemb2.shape(char2Upgrades[1 - len(char2Upgrades)] + ".gif")
        elif len(char1Upgrades) > 1:
            itemb2.shape(char1Upgrades[1 - len(char1Upgrades)] + ".gif")
        else:
            shoppos.remove(orgshoppos[1])
            shopitembuttons.remove(orgshopitembuttons[1])
    tempitems = list(allitems[16:len(allitems)])
    for a in shopitembuttons[3: len(shopitembuttons)]:
        item = str(random.choice(tempitems))
        a.shape(item + ".gif")
        tempitems.remove(item)
    for b in range(len(shopitembuttons)):
        it = shopitembuttons[b]
        it.goto(shoppos[b])
        it.st()
        shopitems.append(it.shape()[0:len(it.shape()) - 4])
    coinb.shape("CoinIcon.gif")
    coinb.goto(-75, -100)
    coinb2.shape("CoinIcon.gif")
    coinb2.goto(-350, -340)
    buyitemb.shape("BuyButton.gif")
    buyitemb.goto(50, -100)
    shopleaveb.shape("LeaveButton.gif")
    shopleaveb.goto(320, -360)
    shopleaveb.st()
    coinb2.st()
    writetext("black", 0, ("Courier", 15, "bold"), (-350 - (len(str(gold) * 7)), -350), 0, turnText, f"{gold}")
    writetext("black", 0, ("Courier", 25), 6, 0, turnText, f"Click item for info.")
    whichloop = shopchoice
    inhandle = True
    restartloop()


def shopchoice(x, y):
    global inhandle, shoppos, itemcho, shopitembuttons, shopitems
    if not inhandle:
        return
    inhandle = False
    for i in shoppos:
        if i[0] - 40 <= x <= i[0] + 40 and i[1] - 40 <= y <= i[1] + 40:
            try:
                itemcho = shoppos.index(i)
            except IndexError:
                pass
            else:
                # If statement makes sure items can only be selected when visible on screen
                if shopitembuttons[itemcho].isvisible():
                    itemchoidx = allitems.index(shopitems[itemcho])
                    itemdescText.clear()
                    curText.clear()
                    writetext("white", 0, ("Courier", 18, "bold"), (-370, 100), 0, itemdescText,
                              f"{itemdesc[0][itemchoidx]}")
                    writetext("white", 0, ("Courier", 18), (-370, 20), 0,
                              itemdescText, f"{itemdesc[1][itemchoidx]}")
                    itemcho = shopitems[itemcho]
                    writetext("black", 0, ("Courier", 15, "bold"), (-80, -110), 0, itemdescText,
                              str(goldcosts[allitems.index(itemcho) - 4]))
                    writetext("white", 0, ("Courier", 12, "bold"), (-95, -70), 0, itemdescText, f"Cost")

                    buyitemb.st()
                    coinb.st()

    inhandle = True
    buyitemb.onclick(checkgold)
    shopleaveb.onclick(closeshop)


def checkgold(x, y):
    global itemcho, inhandle, bagitems, shopitems, shopitembuttons, gold, char1Stats, char2Stats
    if not inhandle:
        return
    inhandle = False
    turnText.clear()
    curText.clear()
    itemx = allitems.index(itemcho)
    if len(bagitems) == 3 and itemx > 15:
        writetext("white", 0, ("Courier", 18, "bold"), (-100, -50), 0, 0, "Bag is full")
        sound("off.wav")
    elif gold - goldcosts[itemx - 4] < 0:
        writetext("white", 0, ("Courier", 18, "bold"), (-100, -50), 0, 0, "Not enough gold")
        sound("off.wav")
    elif itemcho in allitems:
        itemdescText.clear()
        # name, hp, mhp, r, s, d, l, cr

        if itemx == 4:
            if char1Stats[0] == "warrior":
                char1Stats[4] += 1
                char1Stats[6] += 5
            else:
                char2Stats[4] += 1
                char2Stats[6] += 5
            try:
                char1Upgrades.remove("WarriorUpgrade1")
            except ValueError:
                char2Upgrades.remove("WarriorUpgrade1")
        elif itemx == 5:
            if char1Stats[0] == "warrior":
                char1Stats[5] += 1
                char1Stats[2] += 5
            else:
                char2Stats[5] += 1
                char2Stats[2] += 5
            try:
                char1Upgrades.remove("WarriorUpgrade2")
            except ValueError:
                char2Upgrades.remove("WarriorUpgrade2")
        elif itemx == 6:
            if char1Stats[0] == "warrior":
                char1Stats[4] += 2
                char1Stats[6] += 10
            else:
                char2Stats[4] += 2
                char2Stats[6] += 10
            try:
                char1Upgrades.remove("WarriorUpgrade3")
            except ValueError:
                char2Upgrades.remove("WarriorUpgrade3")
        elif itemx == 7:
            if char1Stats[0] == "archer":
                char1Stats[4] += 1
                char1Stats[2] += 2
            else:
                char2Stats[4] += 1
                char2Stats[2] += 2
            try:
                char1Upgrades.remove("ArcherUpgrade1")
            except ValueError:
                char2Upgrades.remove("ArcherUpgrade1")
        elif itemx == 8:
            if char1Stats[0] == "archer":
                char1Stats[4] += 1
                char1Stats[2] += 3
            else:
                char2Stats[4] += 1
                char2Stats[2] += 3
            try:
                char1Upgrades.remove("ArcherUpgrade2")
            except ValueError:
                char2Upgrades.remove("ArcherUpgrade2")
        elif itemx == 9:
            if char1Stats[0] == "archer":
                char1Stats[4] += 1
                char1Stats[5] += 1
                char1Stats[6] += 10
            else:
                char2Stats[4] += 1
                char2Stats[5] += 1
                char2Stats[6] += 10
            try:
                char1Upgrades.remove("ArcherUpgrade3")
            except ValueError:
                char2Upgrades.remove("ArcherUpgrade3")
        elif itemx == 10:
            if char1Stats[0] == "king":
                char1Stats[4] += 2
                char1Stats[2] += 4
            else:
                char2Stats[4] += 2
                char2Stats[2] += 4
            try:
                char1Upgrades.remove("KingUpgrade1")
            except ValueError:
                char2Upgrades.remove("KingUpgrade1")
        elif itemx == 11:
            if char1Stats[0] == "king":
                char1Stats[5] += 1
                char1Stats[2] += 7
            else:
                char2Stats[5] += 1
                char2Stats[2] += 7
            try:
                char1Upgrades.remove("KingUpgrade2")
            except ValueError:
                char2Upgrades.remove("KingUpgrade2")
        elif itemx == 12:
            if char1Stats[0] == "king":
                char1Stats[4] += 1
                char1Stats[5] += 2
                char1Stats[6] += 5
            else:
                char2Stats[4] += 1
                char2Stats[5] += 2
                char2Stats[6] += 5
            try:
                char1Upgrades.remove("KingUpgrade3")
            except ValueError:
                char2Upgrades.remove("KingUpgrade3")
        elif itemx == 13:
            if char1Stats[0] == "doctor":
                char1Stats[4] += 3
            else:
                char2Stats[4] += 3
            try:
                char1Upgrades.remove("DocUpgrade1")
            except ValueError:
                char2Upgrades.remove("DocUpgrade1")
        elif itemx == 14:
            if char1Stats[0] == "doctor":
                char1Stats[4] += 2
                char1Stats[5] += 1
            else:
                char2Stats[4] += 2
                char2Stats[5] += 1
            try:
                char1Upgrades.remove("DocUpgrade2")
            except ValueError:
                char2Upgrades.remove("DocUpgrade2")
        elif itemx == 15:
            if char1Stats[0] == "doctor":
                char1Stats[4] += 2
                char1Stats[2] += 5
            else:
                char2Stats[4] += 2
                char2Stats[2] += 5
            try:
                char1Upgrades.remove("DocUpgrade3")
            except ValueError:
                char2Upgrades.remove("DocUpgrade3")
        else:
            bagitems.append(itemcho)
        buyitemb.ht()
        coinb.ht()
        gold -= goldcosts[itemx - 4]
        sound("shop.wav")
        shopitembuttons[shopitems.index(itemcho)].ht()
        turnText.clear()
    writetext("black", 0, ("Courier", 15, "bold"), (-350 - (len(str(gold) * 7)), -350), 0, turnText, f"{gold}")
    inhandle = True


def closeshop(x, y):
    global inhandle
    if not inhandle:
        return
    inhandle = False
    for a in [curText, turnText, itemdescText]:
        a.clear()
    for a in shopitembuttons:
        a.ht()
    for a in [coinb, coinb2, buyitemb, shopleaveb, itembuse]:
        a.ht()
    whichplace(1)


def whichplace(which):
    global curplace, allvars, savedvars
    curplace = which
    allvars[6] = curplace
    if len(savedvars) > 4:
        savedvars[6] = curplace
        savedvars[7] = allfighters
        allvars[7] = allfighters
        savedvars[8] = gold
        savedvars[9] = bagitems
        savedvars[10] = difficulty
    if which == 1:
        win.bgpic("GrassBg.gif")
        startbattle()
    elif which == 2:
        win.bgpic("ShopBg.gif")
        openshop()
    savegame()


allvars = [char1Name, char2Name, char1Stats, char2Stats, char1Upgrades, char2Upgrades, curplace, allfighters,
            gold, bagitems, difficulty, whichloop, charshape1, charshape2]


if loadfile == "n":
    curplace = 1

# Starts intro
intro()

# Starts first battle
whichplace(curplace)

# Starts loop allowing buttons to be clicked
restartloop()

# Loops for any potential buttons on the screen
# Combat:
attackb.onclick(attacking)
itemb.onclick(openitems)
itembuse.onclick(useitemb)
revengeb.onclick(userevenge)

# Shop:
buyitemb.onclick(checkgold)
shopleaveb.onclick(closeshop)

win.mainloop()
