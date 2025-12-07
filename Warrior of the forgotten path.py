import time
import math
import random

# ---- Data / globals ----
classTypes = ["Mage", "Rogue", "Archer", "General"]
statNames = ["Attack", "Speed", "Defence", "SPower", "Health"]
classStats = [[3, 5, 5, 10, 100], [10, 7, 3, 3, 100],
              [7, 10, 5, 1, 100], [8, 8, 8, 8, 100]]
pName = ""
pStats = [0, 0, 0, 0, 0]
statAdjustment = [0, 0, 0, 0, 0]
pClass = -1
pMoney = 500
pStatus = "Fine"
pLevel = 0
pExp = 0
currentLocation = "Home"
placesToTravel = [["Oodragoth", "CastleVania",
                   "Land of the fallen", "Home"], [200, 300, 75, 0]]
distanceFromHome = 0
activityMenu = ["View Stats", "Travel", "Shop", "Inventory"]
itemsToBuy = [["potion", "burnHeal", "iceHeal",
               "statBoost"], [100, 50, 50, 200]]
itemsToFind = [["potion", "burnHeal", "iceHeal", "statBoost", "cheapVase", "expensiveVase", "garbage"],
               [100, 50, 50, 200, 25, 300, 0]]
monsterTypes = [
    ["Fire Demon", "Ice Bandit", "Paul the Monkey",
        "Weak Enemy", "KING OF HELL-RASHOMON"],
    [10, 8, 5, 1, 30],   # attack
    [8, 5, 7, 3, 11],    # speed
    [5, 7, 3, 1, 15],    # special attack power
    [10, 10, 5, 2, 15],  # defence
    [100, 100, 75, 30, 300]  # health
]
inventory = ["potion"]
escapeAttempt = [False, False]
monsterStats = None
monsterChoice = None

# ---- Utilities ----


def safe_int_input(prompt: str, allow_negative_one: bool = False) -> int:
    while True:
        try:
            val = int(input(prompt))
            if not allow_negative_one and val < 0:
                print("Please enter a non-negative number.")
                continue
            return val
        except ValueError:
            print("Invalid input. Please enter an integer.")


def indexInList(item, myList):
    for i, v in enumerate(myList):
        if item == v:
            return i
    return -1


def listToText(myList):
    s = "\n"
    for i, item in enumerate(myList):
        s += f"{i}) {item}\n"
    return s + "\n"


def checkMenuRange(question, listName, isCanceable=False):
    prompt = question + listToText(listName)
    while True:
        index = safe_int_input(prompt, allow_negative_one=isCanceable)
        if isCanceable and index == -1:
            return -1
        if 0 <= index < len(listName):
            return index
        print("Invalid choice, please try again.\n")


def starLine(numRows, numSleep):
    sLine = "*" * 10
    for _ in range(numRows):
        print(sLine)
    time.sleep(numSleep)


def showInventory(inv):
    if len(inv) < 1:
        print("Inventory is EMPTY!")
        return
    uniq = list(dict.fromkeys(inv))
    for i, item in enumerate(uniq):
        print(f"{i}) {item} ({inv.count(item)})")

# ---- Items / Inventory ----


def useItemMenu():
    global pStatus, pStats, statAdjustment
    if len(inventory) < 1:
        print("Inventory is EMPTY!")
        return
    uniq = list(dict.fromkeys(inventory))
    showInventory(inventory)
    chosenItem = checkMenuRange("What item will you use? ", uniq, True)
    if chosenItem == -1:
        return
    itemName = uniq[chosenItem]
    itemToUse = indexInList(itemName, itemsToFind[0])
    if itemToUse == 0:  # potion
        pStats[4] += 10
        print("You've been healed 10 HP!")
    elif itemToUse == 1:  # burnHeal
        if pStatus in ("Fine", "Ice"):
            print("Burn Heal had no effect.")
        else:
            pStatus = "Fine"
            print(pName + " was Burn Healed!")
    elif itemToUse == 2:  # iceHeal
        if pStatus in ("Fine", "Burn"):
            print("Ice Heal had no effect.")
        else:
            pStatus = "Fine"
            print(pName + " was Ice Healed!")
    elif itemToUse == 3:  # statBoost
        checkStatBoost = checkMenuRange("What stat would you like to temporarily boost?", [
                                        "Attack", "Speed", "Defence", "SPower"])
        numBoost = math.ceil(pStats[checkStatBoost] * 0.1) or 1
        pStats[checkStatBoost] += numBoost
        statAdjustment[checkStatBoost] += numBoost
        print("Stat Boosted!")
    else:
        print("That item can't be used right now.")
    if itemToUse != -1 and itemToUse < len(itemsToFind[0]):
        inventory.remove(itemsToFind[0][itemToUse])
    print("Current Stats:")
    for i in range(len(statNames)):
        print(statNames[i], pStats[i])

# ---- Combat ----


def playerAttack():
    global pStatus, pStats, inventory, statAdjustment, monsterStats
    runStat = random.randint(0, 100)
    fightChoice = checkMenuRange("What are you gonna do? ", [
                                 "Fight", "Item", "Run"])
    if fightChoice == 0:  # Fight
        attackType = checkMenuRange(
            "Choose an attack!", ["Weapon", "Magic", "Dodge"])
        monDefPercentage = 1 - (monsterStats[2] / 12)
        if attackType == 0:
            print("BOOM BOOM")
            damage = pStats[0] * monDefPercentage
            print("Damage " + str(round(damage, 2)))
            monsterStats[4] -= damage
        elif attackType == 1:
            print("Woosh WOOOOSHHhhhhh WOOOSH")
            critChance = random.randint(0, 100)
            critBonus = 1
            if critChance > 70:
                print("CRITICAL HIT!")
                critBonus = 1.4
            damage = (pStats[3] * monDefPercentage) * critBonus
            print("Damage " + str(round(damage, 2)))
            monsterStats[4] -= damage
        else:
            escapeAttempt[0] = True
        print("Monster Health " + str(max(0, round(monsterStats[4], 2))))
        starLine(1, 1.2)
    elif fightChoice == 1:
        useItemMenu()
    else:
        chance_to_run = (pStats[1] / 20) * 100
        if chance_to_run >= runStat:
            print("Got away safely!")
            for i in range(len(statAdjustment)):
                pStats[i] -= statAdjustment[i]
                statAdjustment[i] = 0
            escapeAttempt[1] = True
            starLine(2, 0.8)
        else:
            print("Could not escape!")
    return escapeAttempt


def monsterAttack():
    global pStatus, pStats, monsterChoice, monsterStats
    if pStatus != "Fine":
        if pStatus == "Burn":
            pStats[4] -= 5
            print(pName + " was hurt by burn (-5 HP).")
        elif pStatus == "Ice":
            pStats[4] -= 3
            print(pName + " was hurt by ice (-3 HP).")
        print(pName + " health is now " + str(max(0, pStats[4])))
    print("Monster turn")
    starLine(1, 0.8)
    attackOptionChance = random.randint(0, 100)
    pDefPercentage = 1 - (pStats[2] / 20)
    if monsterChoice == 0:  # Fire Demon
        if attackOptionChance < 45:
            print("FIRE BREATH!")
            pStats[4] -= monsterStats[3] * pDefPercentage
            if random.randint(0, 100) < 30:
                pStatus = "Burn"
                print(pName + " was burned from attack!")
        elif attackOptionChance < 90:
            print("HEAD BUTT!")
            pStats[4] -= monsterStats[0] * pDefPercentage
        else:
            if random.randint(0, 100) < 10:
                print("SELF HEAL!")
                monsterStats[4] *= 1.1
            else:
                print("YOU ABSOLUTE FOOL!")
    elif monsterChoice == 1:  # Ice Bandit
        if attackOptionChance < 45:
            print("ICE TEETH!")
            pStats[4] -= monsterStats[3] * pDefPercentage
            if random.randint(0, 100) < 30:
                pStatus = "Ice"
                print(pName + " received frost bite from attack!")
        elif attackOptionChance < 90:
            print("HIGH KICK!")
            pStats[4] -= monsterStats[0] * pDefPercentage
        else:
            if random.randint(0, 100) < 10:
                print("SELF HEAL!")
                monsterStats[4] *= 1.1
            else:
                print("LOL U THOUGHT U COULD DEFEAT ME?")
    elif monsterChoice == 2:  # Paul the Monkey
        if attackOptionChance < 50:
            print("Hi I'm Paul")
        else:
            print("Monke C Monke 2 fingers in the eye!")
            pStats[4] -= (monsterStats[0] * pDefPercentage)
    elif monsterChoice == 3:
        print("Boop on your nose!")
        pStats[4] -= (monsterStats[0] * pDefPercentage)
    else:  # KING
        kingofHellYells = ["WELCOME TO THE HELL DIMENSION", "THE HEAT IS ETERNAL",
                           "WORORORORORAH you think you can escape this HELL DIMENSION?"]
        print(random.choice(kingofHellYells))
        if attackOptionChance < 45:
            print("BLACK FLAMES OF HELL!")
            pStats[4] -= monsterStats[3] * pDefPercentage
        elif attackOptionChance < 90:
            print("SLAP, CRACKLE, POP")
            pStats[4] -= monsterStats[0] * pDefPercentage
        else:
            if random.randint(0, 100) < 10:
                print("DOUBLE SELF HEAL!!!!!")
                monsterStats[4] *= 1.2
            else:
                print("YOU ARE NOTHING BUT AN INSECT TO A GOD!")
    print(pName + " Health: " + str(max(0, round(pStats[4], 2))))

# ---- Main ----


def main():
    global pName, pClass, pStats, pLevel, pExp, pMoney, distanceFromHome
    global monsterStats, monsterChoice, escapeAttempt
    pName = input("What is your name\n").strip() or "Hero"
    print("Welcome to the wonderful world of Magic Land, " + pName + "!")
    starLine(2, 0.6)
    for i, ct in enumerate(classTypes):
        print(f"{ct}:")
        for j in range(len(classStats[i])):
            print(statNames[j], classStats[i][j])
        starLine(1, 0.6)
    pClass = checkMenuRange("Choose your Class: ", classTypes)
    print("You have chosen " + classTypes[pClass] + "!")
    pStats = classStats[pClass].copy()
    starLine(1, 1)
    print("From henceforth you shall be known as " +
          pName + " the " + classTypes[pClass])
    starLine(1, 1)
    print("Long ago in a time when anything was possible there was a land called NEBYULYN\nthat was ironically home to a great warrior\nbut spooky things happen in the middle of home and it's up to courage....I mean " + pName + " to save the day!")
    starLine(1, 1.5)

    inGameLoop = True
    while inGameLoop and pStats[4] > 0:
        actChoice = checkMenuRange(
            "My Noble warrior what would you like to do? ", activityMenu)
        if actChoice == 0:
            print("Your Stats:")
            for i in range(len(statNames)):
                print(statNames[i], pStats[i])

            # travel
        elif actChoice == 1:
            print("Travel")
            travelChoice = checkMenuRange(
                "Where would you like to travel to? ", placesToTravel[0], True)
            if travelChoice == -1:
                print("Travel cancelled.")
                continue
            if placesToTravel[1][travelChoice] == distanceFromHome:
                print("Well that was fast! You're already there!")
                continue
            print("And so " + pName + " set off on their journey to " +
                  placesToTravel[0][travelChoice])
            distanceDivider = random.randint(3, 6)
            distanceTraveled = math.ceil(
                placesToTravel[1][travelChoice] / distanceDivider)
            isTravelNeg = placesToTravel[1][travelChoice] < distanceFromHome
            inTravel = True
            while inTravel and pStats[4] > 0:
                if not isTravelNeg:
                    distanceFromHome += distanceTraveled
                    if distanceFromHome >= placesToTravel[1][travelChoice]:
                        print("You have reached " +
                              placesToTravel[0][travelChoice])
                        inTravel = False
                else:
                    distanceFromHome -= distanceTraveled
                    if distanceFromHome <= placesToTravel[1][travelChoice]:
                        print("You have reached " +
                              placesToTravel[0][travelChoice])
                        inTravel = False
                if not inTravel:
                    distanceFromHome = placesToTravel[1][travelChoice]
                    break

                if random.randint(0, 100) < 60:
                    inFight = True
                    monsterPercentage = random.randint(0, 100)
                    if monsterPercentage <= 25:
                        monsterChoice = 3
                    elif monsterPercentage <= 55:
                        monsterChoice = 0
                    elif monsterPercentage <= 85:
                        monsterChoice = 1
                    elif monsterPercentage < 99:
                        monsterChoice = 2
                    else:
                        monsterChoice = 4
                    starLine(1, 0.8)
                    print("You have been challenged to fight by " +
                          monsterTypes[0][monsterChoice])
                    starLine(1, 0.6)
                    monsterStats = [
                        monsterTypes[1][monsterChoice],  # attack
                        monsterTypes[2][monsterChoice],  # speed
                        monsterTypes[4][monsterChoice],  # defence
                        monsterTypes[3][monsterChoice],  # special power
                        monsterTypes[5][monsterChoice]   # health
                    ]
                    chanceAdditional = 0
                    if pStats[1] > monsterStats[1]:
                        chanceAdditional = random.randint(25, 50)
                    turnChance = 50 + chanceAdditional
                    currentTurn = 1 if random.randint(
                        0, 100) < turnChance else -1
                    escapeAttempt = [False, False]
                    while inFight and pStats[4] > 0:
                        if currentTurn == 1:
                            escapeAttempt = playerAttack()
                            if escapeAttempt[1]:
                                escapeAttempt[1] = False
                                inFight = False
                                break
                        else:
                            incChance = 0
                            if pStats[1] > monsterStats[1]:
                                incChance = random.randint(25, 50)
                            dChance = 25 + incChance
                            failChance = random.randint(0, 100)
                            if escapeAttempt[0]:
                                if failChance < dChance:
                                    print(pName + " HAS NARROWLY AVOIDED ATTACK!")
                                else:
                                    print("DODGE FAILED")
                                    monsterAttack()
                                escapeAttempt[0] = False
                            else:
                                monsterAttack()
                        starLine(1, 0.6)
                        currentTurn *= -1
                        if pStats[4] <= 0:
                            print("The mighty " + pName +
                                  " has fallen... may they rest in pieces.")
                            break
                        if monsterStats[4] <= 0:
                            print(pName + " has defeated the monster!")
                            for i in range(len(statAdjustment)):
                                pStats[i] -= statAdjustment[i]
                                statAdjustment[i] = 0
                            pExp += 10
                            print(pName + " has gained 10 exp!")
                            starLine(1, 0.6)
                            if pExp % ((pLevel + 1) * 10) == 0:
                                pExp = 0
                                if pLevel < 20:
                                    pLevel += 1
                                    print(pName + " is now level " + str(pLevel))
                                    starLine(1, 0.6)
                                    print("You earned one stat point!")
                                    print("Current Stats:")
                                    for i in range(len(statNames)):
                                        print(statNames[i], pStats[i])
                                    statIncreaseChoice = checkMenuRange(
                                        "", statNames)
                                    pStats[statIncreaseChoice] += 1
                                    print(
                                        statNames[statIncreaseChoice] + " is now " + str(pStats[statIncreaseChoice]))
                            inFight = False
                            break
                else:
                    starLine(1, 0.6)
                    print("Traveling......")
                    starLine(1, 0.6)
                    pickUpChance = random.randint(0, 100)
                    if pickUpChance < 20:
                        itemFound = itemsToFind[0][0]
                    elif pickUpChance < 30:
                        itemFound = itemsToFind[0][1]
                    elif pickUpChance < 40:
                        itemFound = itemsToFind[0][2]
                    elif pickUpChance < 45:
                        itemFound = itemsToFind[0][3]
                    elif pickUpChance < 65:
                        itemFound = itemsToFind[0][4]
                    elif pickUpChance < 69:
                        itemFound = itemsToFind[0][5]
                    else:
                        itemFound = itemsToFind[0][6]
                    print(pName + " has found " + itemFound)
                    addItemCheck = checkMenuRange(
                        "Add this item to your inventory?", ["Yes", "No"])
                    if addItemCheck == 0:
                        print(itemFound + " was added to your inventory")
                        inventory.append(itemFound)
                    else:
                        print(itemFound + " was discarded")
                    starLine(1, 0.6)
                    print(pName + " continues journey!")
                    starLine(1, 0.6)

        elif actChoice == 2:  # Shop
            while True:
                print("Current balance is $" + str(pMoney))
                shopChoice = checkMenuRange("Welcome to my Shop! My Name is Ezro, how may I help you?", [
                                            "Buy", "Sell", "Show Inventory", "Exit"], True)
                if shopChoice == -1:
                    break
                if shopChoice == 3:
                    print("Thank you! Come again!")
                    break
                if shopChoice == 0:
                    buyChoice = checkMenuRange(
                        "What would you like to buy?", itemsToBuy[0])
                    price = itemsToBuy[1][buyChoice]
                    if pMoney - price >= 0:
                        inventory.append(itemsToBuy[0][buyChoice])
                        pMoney -= price
                        print(
                            f"Bought {itemsToBuy[0][buyChoice]} for ${price}.")
                    else:
                        print("You can't afford that item!")
                elif shopChoice == 1:
                    if len(inventory) > 0:
                        itemList = list(dict.fromkeys(inventory))
                        showInventory(inventory)
                        sellChoice = checkMenuRange(
                            "What would you like to sell?", itemList)
                        if sellChoice != -1:
                            itemIndex = indexInList(
                                itemList[sellChoice], itemsToFind[0])
                            if itemIndex != -1:
                                sellPrice = math.floor(
                                    itemsToFind[1][itemIndex] * 0.9)
                                confirmChoice = checkMenuRange(
                                    "Sell for " + str(sellPrice) + "?", ["Yes", "No"])
                                if confirmChoice == 0:
                                    pMoney += sellPrice
                                    inventory.remove(itemsToFind[0][itemIndex])
                                    print(
                                        "Item Sold! New balance: $" + str(pMoney))
                                else:
                                    print("Sale cancelled.")
                            else:
                                print("This item cannot be sold here.")
                    else:
                        print("You have nothing to sell!")
                elif shopChoice == 2:
                    showInventory(inventory)

        elif actChoice == 3:
            showInventory(inventory)

    if pStats[4] <= 0:
        print("Game Over. You have perished.")
    else:
        print("Goodbye, traveler.")


if __name__ == "__main__":
    main()
