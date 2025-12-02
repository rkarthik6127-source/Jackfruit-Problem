import random

# ============================================================================
# CLASSES - OOP for organizing game entities
# ============================================================================


class Item:
    def __init__(self, name, value, bonus=0):
        self.name = name
        self.value = value
        self.bonus = bonus


class Player:
    CLASSES = {
        "Oracle": (80, 12, 8, 18),
        "Swordsman": (100, 18, 12, 10),
        "Cavalier": (120, 15, 16, 8),
        "SharpShooter": (85, 20, 6, 14)
    }

    def __init__(self, name, pclass):
        self.name = name
        self.pclass = pclass
        hp, atk, df, spd = self.CLASSES[pclass]
        self.max_hp = self.hp = hp
        self.atk = atk
        self.defense = df
        self.speed = spd
        self.gold = 50
        self.level = 1
        self.exp = 0
        self.items = []
        self.weapon = None
        self.armor = None

    def get_atk(self):
        return self.atk + (self.weapon.bonus if self.weapon else 0)

    def get_def(self):
        return self.defense + (self.armor.bonus if self.armor else 0)

    def heal(self, amt):
        self.hp = min(self.hp + amt, self.max_hp)

    def add_exp(self, amt):
        self.exp += amt
        if self.exp >= self.level * 100:
            self.level += 1
            self.max_hp += 10
            self.hp = self.max_hp
            self.atk += 2
            self.defense += 2
            print(f"\n🎉 Level {self.level}! HP+10, ATK+2, DEF+2")


class Monster:
    TYPES = {
        "Goblin": (30, 8, 4, 12, 15, 20),
        "Wolf": (40, 12, 5, 16, 20, 30),
        "Orc": (60, 15, 8, 8, 35, 50),
        "Troll": (80, 18, 12, 6, 50, 70)
    }

    def __init__(self, mtype):
        self.name = mtype
        hp, atk, df, spd, gold, exp = self.TYPES[mtype]
        self.hp = hp
        self.atk = atk
        self.defense = df
        self.speed = spd
        self.gold = gold
        self.exp = exp

# ============================================================================
# FUNCTIONAL HELPERS - Small, reusable functions
# ============================================================================


def calc_damage(atk, defense):
    return max(1, atk - defense + random.randint(-2, 2))


def get_input(prompt, options):
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print(f"Invalid. Choose: {', '.join(options)}")


def try_flee(p_spd, m_spd):
    chance = 0.5 + (p_spd - m_spd) * 0.05
    return random.random() < max(0.3, min(0.9, chance))

# ============================================================================
# GAME - Main controller
# ============================================================================


class Game:
    LOCATIONS = ["town", "forest", "cave", "mountain"]
    SHOP = [
        ("Iron Sword", 30, 5, "weapon"),
        ("Steel Axe", 50, 8, "weapon"),
        ("Leather Armor", 25, 4, "armor"),
        ("Chain Mail", 45, 7, "armor"),
        ("Health Potion", 15, 30, "potion"),
        ("Greater Potion", 30, 60, "potion")
    ]

    def __init__(self):
        self.player = None
        self.location = "town"

    def start(self):
        print("\n" + "="*50)
        print("⚔️  TEXT RPG ADVENTURE  ⚔️")
        print("="*50 + "\n")

        name = input("Character name: ").strip()
        print("\nClasses:")
        classes = list(Player.CLASSES.keys())
        for i, c in enumerate(classes, 1):
            print(f"{i}. {c}")

        choice = get_input("Choose (1-4): ", ["1", "2", "3", "4"])
        self.player = Player(name, classes[int(choice)-1])
        print(f"\nWelcome, {name} the {self.player.pclass}!\n")

        self.main_loop()

    def main_loop(self):
        while True:
            print(f"\n{'='*50}")
            print(
                f"📍 {self.location.upper()} | HP: {self.player.hp}/{self.player.max_hp} | Gold: {self.player.gold}")
            print(f"{'='*50}")
            print("1. Stats  2. Inventory  3. Travel  4. Rest  5. Quit")

            choice = get_input("Choice: ", ["1", "2", "3", "4", "5"])

            if choice == "1":
                self.show_stats()
            elif choice == "2":
                self.show_inventory()
            elif choice == "3":
                self.travel()
            elif choice == "4":
                amt = self.player.max_hp // 2
                self.player.heal(amt)
                print(f"\n😴 Rested. +{amt} HP")
            elif choice == "5":
                print("\nThanks for playing!")
                break

    def show_stats(self):
        p = self.player
        print(f"\n📊 {p.name} | Lv.{p.level} {p.pclass}")
        print(f"HP: {p.hp}/{p.max_hp} | EXP: {p.exp}/{p.level*100}")
        print(f"ATK: {p.get_atk()} | DEF: {p.get_def()} | SPD: {p.speed}")
        print(f"Gold: {p.gold}")

    def show_inventory(self):
        p = self.player
        print("\n🎒 INVENTORY")
        if not p.items:
            print("Empty")
        else:
            for i, item in enumerate(p.items, 1):
                eq = " [E]" if item == p.weapon or item == p.armor else ""
                print(f"{i}. {item.name}{eq}")

        print(f"\nWeapon: {p.weapon.name if p.weapon else 'None'}")
        print(f"Armor: {p.armor.name if p.armor else 'None'}")

        if p.items:
            choice = input("\nUse item # (or Enter): ").strip()
            if choice.isdigit() and 1 <= int(choice) <= len(p.items):
                self.use_item(p.items[int(choice)-1])

    def use_item(self, item):
        if "Sword" in item.name or "Axe" in item.name:
            self.player.weapon = item
            print(f"⚔️ Equipped {item.name}")
        elif "Armor" in item.name or "Mail" in item.name:
            self.player.armor = item
            print(f"🛡️ Equipped {item.name}")
        elif "Potion" in item.name:
            self.player.heal(item.bonus)
            self.player.items.remove(item)
            print(f"💚 Used {item.name}. +{item.bonus} HP")

    def travel(self):
        print("\n🗺️ TRAVEL")
        for i, loc in enumerate(self.LOCATIONS, 1):
            curr = " [HERE]" if loc == self.location else ""
            print(f"{i}. {loc.capitalize()}{curr}")

        choice = get_input(f"Go (1-{len(self.LOCATIONS)}): ",
                           [str(i) for i in range(1, len(self.LOCATIONS)+1)])
        new_loc = self.LOCATIONS[int(choice)-1]

        if new_loc == self.location:
            print("\nAlready here!")
            return

        self.location = new_loc
        print(f"\n→ Traveling to {new_loc}...")

        if new_loc == "town":
            self.visit_shop()
        else:
            self.explore()

    def visit_shop(self):
        print("\n🏪 SHOP")
        choice = get_input("Enter shop? (y/n): ", ["y", "n"])
        if choice == "n":
            return

        while True:
            print(f"\nGold: {self.player.gold}")
            for i, (name, cost, _, _) in enumerate(self.SHOP, 1):
                print(f"{i}. {name} - {cost}g")

            choice = input("\nBuy # (or 0 to leave): ").strip()
            if choice == "0":
                break

            if choice.isdigit() and 1 <= int(choice) <= len(self.SHOP):
                name, cost, bonus, itype = self.SHOP[int(choice)-1]
                if self.player.gold >= cost:
                    self.player.gold -= cost
                    self.player.items.append(Item(name, cost, bonus))
                    print(f"✅ Bought {name}")
                else:
                    print(f"❌ Need {cost}g, have {self.player.gold}g")

    def explore(self):
        chances = {"forest": 0.6, "cave": 0.7, "mountain": 0.8}
        monsters = {"forest": ["Goblin", "Wolf"], "cave": [
            "Goblin", "Orc"], "mountain": ["Orc", "Troll"]}

        if random.random() < chances.get(self.location, 0.5):
            mtype = random.choice(monsters.get(self.location, ["Goblin"]))
            self.combat(Monster(mtype))
        else:
            if random.random() < 0.5:
                gold = random.randint(10, 30)
                self.player.gold += gold
                print(f"\n💰 Found {gold} gold!")
            else:
                loot = random.choice(self.SHOP)
                item = Item(loot[0], loot[1], loot[2])
                self.player.items.append(item)
                print(f"\n📦 Found {item.name}!")

    def combat(self, monster):
        print(f"\n⚔️ {monster.name} appears! HP:{monster.hp} ATK:{monster.atk}")

        while self.player.hp > 0 and monster.hp > 0:
            print(f"\n{'='*40}")
            print(
                f"You: {self.player.hp}/{self.player.max_hp} | {monster.name}: {monster.hp}")
            print(f"{'='*40}")

            if self.player.speed >= monster.speed:
                if not self.player_turn(monster):
                    return
                if monster.hp > 0:
                    self.monster_turn(monster)
            else:
                self.monster_turn(monster)
                if self.player.hp > 0 and not self.player_turn(monster):
                    return

            if monster.hp <= 0:
                print(f"\n🎉 Victory! +{monster.gold}g +{monster.exp}exp")
                self.player.gold += monster.gold
                self.player.add_exp(monster.exp)
                if random.random() < 0.3:
                    loot = random.choice(self.SHOP)
                    self.player.items.append(Item(loot[0], loot[1], loot[2]))
                    print(f"Dropped {loot[0]}!")
                return

            if self.player.hp <= 0:
                self.game_over()
                return

    def player_turn(self, monster):
        print("\n1. Attack  2. Item  3. Flee")
        choice = get_input("Action: ", ["1", "2", "3"])

        if choice == "1":
            dmg = calc_damage(self.player.get_atk(), monster.defense)
            monster.hp -= dmg
            print(f"⚔️ Deal {dmg} damage!")
        elif choice == "2":
            potions = [it for it in self.player.items if "Potion" in it.name]
            if potions:
                self.use_item(potions[0])
            else:
                print("No potions!")
        elif choice == "3":
            if try_flee(self.player.speed, monster.speed):
                print(f"🏃 Fled!")
                return False
            print("❌ Can't escape!")
        return True

    def monster_turn(self, monster):
        dmg = calc_damage(monster.atk, self.player.get_def())
        self.player.hp -= dmg
        print(f"💥 {monster.name} deals {dmg} damage!")

    def game_over(self):
        print("\n" + "="*50)
        print("💀 GAME OVER 💀")
        print("="*50)
        print(f"Level {self.player.level} | {self.player.gold} gold")

        if get_input("\nPlay again? (y/n): ", ["y", "n"]) == "y":
            self.__init__()
            self.start()

# ============================================================================
# ENTRY POINT
# ============================================================================


def main():
    Game().start()


if __name__ == "__main__":
    main()
