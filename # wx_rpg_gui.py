import random
import wx

# ============================================================================
# GAME CLASSES - Same OOP structure as before
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
            return True
        return False


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
        self.hp = self.max_hp = hp
        self.atk = atk
        self.defense = df
        self.speed = spd
        self.gold = gold
        self.exp = exp

# ============================================================================
# FUNCTIONAL HELPERS
# ============================================================================


def calc_damage(atk, defense):
    return max(1, atk - defense + random.randint(-2, 2))


def try_flee(p_spd, m_spd):
    chance = 0.5 + (p_spd - m_spd) * 0.05
    return random.random() < max(0.3, min(0.9, chance))

# ============================================================================
# GAME LOGIC
# ============================================================================


class GameLogic:
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
        self.monster = None
        self.in_combat = False

    def explore(self):
        chances = {"forest": 0.6, "cave": 0.7, "mountain": 0.8}
        monsters = {"forest": ["Goblin", "Wolf"], "cave": [
            "Goblin", "Orc"], "mountain": ["Orc", "Troll"]}

        if random.random() < chances.get(self.location, 0.5):
            mtype = random.choice(monsters.get(self.location, ["Goblin"]))
            self.monster = Monster(mtype)
            self.in_combat = True
            return f"⚔️ {self.monster.name} appears! HP: {self.monster.hp}"
        else:
            if random.random() < 0.5:
                gold = random.randint(10, 30)
                self.player.gold += gold
                return f"💰 Found {gold} gold!"
            else:
                loot = random.choice(self.SHOP)
                item = Item(loot[0], loot[1], loot[2])
                self.player.items.append(item)
                return f"📦 Found {item.name}!"

# ============================================================================
# WX PYTHON UI
# ============================================================================


class RPGFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Text RPG Adventure", size=(700, 600))
        self.game = GameLogic()

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Title
        title = wx.StaticText(panel, label="⚔️ TEXT RPG ADVENTURE ⚔️")
        title_font = wx.Font(16, wx.FONTFAMILY_DEFAULT,
                             wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        main_sizer.Add(title, 0, wx.ALL | wx.CENTER, 10)

        # Status Panel
        status_box = wx.StaticBox(panel, label="Status")
        status_sizer = wx.StaticBoxSizer(status_box, wx.VERTICAL)

        self.status_text = wx.StaticText(
            panel, label="Click 'New Game' to start")
        status_sizer.Add(self.status_text, 0, wx.ALL, 5)

        # Health Bar
        health_sizer = wx.BoxSizer(wx.HORIZONTAL)
        health_sizer.Add(wx.StaticText(panel, label="HP:"), 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.health_bar = wx.Gauge(panel, range=100, size=(200, 20))
        self.health_bar.SetValue(100)
        health_sizer.Add(self.health_bar, 1, wx.EXPAND)
        self.health_label = wx.StaticText(panel, label="100/100")
        health_sizer.Add(self.health_label, 0,
                         wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        status_sizer.Add(health_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # Monster Health Bar (hidden initially)
        monster_sizer = wx.BoxSizer(wx.HORIZONTAL)
        monster_sizer.Add(wx.StaticText(panel, label="Enemy:"),
                          0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.monster_bar = wx.Gauge(panel, range=100, size=(200, 20))
        self.monster_bar.SetValue(0)
        monster_sizer.Add(self.monster_bar, 1, wx.EXPAND)
        self.monster_label = wx.StaticText(panel, label="")
        monster_sizer.Add(self.monster_label, 0,
                          wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        status_sizer.Add(monster_sizer, 0, wx.EXPAND | wx.ALL, 5)

        main_sizer.Add(status_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Game Log
        log_box = wx.StaticBox(panel, label="Game Log")
        log_sizer = wx.StaticBoxSizer(log_box, wx.VERTICAL)
        self.log = wx.TextCtrl(panel, style=wx.TE_MULTILINE |
                               wx.TE_READONLY, size=(-1, 200))
        log_sizer.Add(self.log, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(log_sizer, 1, wx.EXPAND | wx.ALL, 10)

        # Command Buttons
        btn_sizer = wx.GridSizer(3, 3, 5, 5)

        self.btn_new = wx.Button(panel, label="New Game")
        self.btn_stats = wx.Button(panel, label="View Stats")
        self.btn_inventory = wx.Button(panel, label="Inventory")
        self.btn_travel = wx.Button(panel, label="Travel")
        self.btn_rest = wx.Button(panel, label="Rest")
        self.btn_attack = wx.Button(panel, label="⚔️ Attack")
        self.btn_use_potion = wx.Button(panel, label="💚 Use Potion")
        self.btn_flee = wx.Button(panel, label="🏃 Flee")
        self.btn_shop = wx.Button(panel, label="🏪 Shop")

        btn_sizer.Add(self.btn_new, 0, wx.EXPAND)
        btn_sizer.Add(self.btn_stats, 0, wx.EXPAND)
        btn_sizer.Add(self.btn_inventory, 0, wx.EXPAND)
        btn_sizer.Add(self.btn_travel, 0, wx.EXPAND)
        btn_sizer.Add(self.btn_rest, 0, wx.EXPAND)
        btn_sizer.Add(self.btn_attack, 0, wx.EXPAND)
        btn_sizer.Add(self.btn_use_potion, 0, wx.EXPAND)
        btn_sizer.Add(self.btn_flee, 0, wx.EXPAND)
        btn_sizer.Add(self.btn_shop, 0, wx.EXPAND)

        main_sizer.Add(btn_sizer, 0, wx.EXPAND | wx.ALL, 10)

        # Bind events
        self.btn_new.Bind(wx.EVT_BUTTON, self.on_new_game)
        self.btn_stats.Bind(wx.EVT_BUTTON, self.on_stats)
        self.btn_inventory.Bind(wx.EVT_BUTTON, self.on_inventory)
        self.btn_travel.Bind(wx.EVT_BUTTON, self.on_travel)
        self.btn_rest.Bind(wx.EVT_BUTTON, self.on_rest)
        self.btn_attack.Bind(wx.EVT_BUTTON, self.on_attack)
        self.btn_use_potion.Bind(wx.EVT_BUTTON, self.on_use_potion)
        self.btn_flee.Bind(wx.EVT_BUTTON, self.on_flee)
        self.btn_shop.Bind(wx.EVT_BUTTON, self.on_shop)

        panel.SetSizer(main_sizer)
        self.update_buttons()
        self.Centre()

    def log_message(self, msg):
        self.log.AppendText(msg + "\n")

    def update_health_bar(self):
        if self.game.player:
            percent = int(
                (self.game.player.hp / self.game.player.max_hp) * 100)
            self.health_bar.SetValue(percent)
            self.health_label.SetLabel(
                f"{self.game.player.hp}/{self.game.player.max_hp}")

    def update_monster_bar(self):
        if self.game.monster:
            percent = int(
                (self.game.monster.hp / self.game.monster.max_hp) * 100)
            self.monster_bar.SetValue(percent)
            self.monster_label.SetLabel(
                f"{self.game.monster.name}: {self.game.monster.hp}/{self.game.monster.max_hp}")
        else:
            self.monster_bar.SetValue(0)
            self.monster_label.SetLabel("")

    def update_status(self):
        if self.game.player:
            status = f"{self.game.player.name} | Lv.{self.game.player.level} {self.game.player.pclass} | "
            status += f"📍 {self.game.location.upper()} | 💰 {self.game.player.gold}g"
            self.status_text.SetLabel(status)

    def update_buttons(self):
        has_player = self.game.player is not None
        in_combat = self.game.in_combat

        self.btn_stats.Enable(has_player)
        self.btn_inventory.Enable(has_player)
        self.btn_travel.Enable(has_player and not in_combat)
        self.btn_rest.Enable(has_player and not in_combat)
        self.btn_shop.Enable(
            has_player and self.game.location == "town" and not in_combat)

        self.btn_attack.Enable(has_player and in_combat)
        self.btn_use_potion.Enable(has_player and in_combat)
        self.btn_flee.Enable(has_player and in_combat)

    def on_new_game(self, event):
        dlg = wx.TextEntryDialog(
            self, "Enter your character name:", "Character Creation")
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue() or "Hero"

            classes = list(Player.CLASSES.keys())
            class_dlg = wx.SingleChoiceDialog(
                self, "Choose your class:", "Class Selection", classes)
            if class_dlg.ShowModal() == wx.ID_OK:
                pclass = class_dlg.GetStringSelection()
                self.game.player = Player(name, pclass)
                self.game.location = "town"
                self.game.in_combat = False
                self.game.monster = None

                self.log.Clear()
                self.log_message(f"Welcome, {name} the {pclass}!")
                self.log_message("Your adventure begins in the town.")

                self.update_health_bar()
                self.update_monster_bar()
                self.update_status()
                self.update_buttons()

    def on_stats(self, event):
        p = self.game.player
        msg = f"Name: {p.name}\nClass: {p.pclass}\nLevel: {p.level}\n"
        msg += f"HP: {p.hp}/{p.max_hp}\nATK: {p.get_atk()} | DEF: {p.get_def()} | SPD: {p.speed}\n"
        msg += f"Gold: {p.gold}\nEXP: {p.exp}/{p.level*100}"
        wx.MessageBox(msg, "Character Stats", wx.OK | wx.ICON_INFORMATION)

    def on_inventory(self, event):
        p = self.game.player
        if not p.items:
            wx.MessageBox("Your inventory is empty.",
                          "Inventory", wx.OK | wx.ICON_INFORMATION)
            return

        items = [f"{i.name} (+{i.bonus})" for i in p.items]
        dlg = wx.SingleChoiceDialog(
            self, "Select item to use/equip:", "Inventory", items)
        if dlg.ShowModal() == wx.ID_OK:
            idx = dlg.GetSelection()
            item = p.items[idx]

            if "Sword" in item.name or "Axe" in item.name:
                p.weapon = item
                self.log_message(f"⚔️ Equipped {item.name}")
            elif "Armor" in item.name or "Mail" in item.name:
                p.armor = item
                self.log_message(f"🛡️ Equipped {item.name}")
            elif "Potion" in item.name:
                p.heal(item.bonus)
                p.items.remove(item)
                self.log_message(f"💚 Used {item.name}. +{item.bonus} HP")
                self.update_health_bar()

    def on_travel(self, event):
        dlg = wx.SingleChoiceDialog(
            self, "Where do you want to go?", "Travel", GameLogic.LOCATIONS)
        dlg.SetSelection(GameLogic.LOCATIONS.index(self.game.location))

        if dlg.ShowModal() == wx.ID_OK:
            new_loc = dlg.GetStringSelection()
            if new_loc == self.game.location:
                self.log_message("You're already here!")
                return

            self.game.location = new_loc
            self.log_message(f"→ Traveling to {new_loc}...")
            self.update_status()

            if new_loc != "town":
                msg = self.game.explore()
                self.log_message(msg)
                if self.game.in_combat:
                    self.update_monster_bar()

            self.update_buttons()

    def on_rest(self, event):
        amt = self.game.player.max_hp // 2
        self.game.player.heal(amt)
        self.log_message(f"😴 You rest and recover {amt} HP")
        self.update_health_bar()

    def on_attack(self, event):
        if not self.game.in_combat:
            return

        p = self.game.player
        m = self.game.monster

        # Player attacks first if faster
        if p.speed >= m.speed:
            dmg = calc_damage(p.get_atk(), m.defense)
            m.hp -= dmg
            self.log_message(f"⚔️ You deal {dmg} damage to {m.name}!")

            if m.hp <= 0:
                self.win_combat()
                return

            # Monster counterattacks
            dmg = calc_damage(m.atk, p.get_def())
            p.hp -= dmg
            self.log_message(f"💥 {m.name} deals {dmg} damage!")
        else:
            # Monster attacks first
            dmg = calc_damage(m.atk, p.get_def())
            p.hp -= dmg
            self.log_message(f"💥 {m.name} deals {dmg} damage!")

            if p.hp <= 0:
                self.game_over()
                return

            # Player counterattacks
            dmg = calc_damage(p.get_atk(), m.defense)
            m.hp -= dmg
            self.log_message(f"⚔️ You deal {dmg} damage to {m.name}!")

            if m.hp <= 0:
                self.win_combat()
                return

        self.update_health_bar()
        self.update_monster_bar()

        if p.hp <= 0:
            self.game_over()

    def on_use_potion(self, event):
        potions = [i for i in self.game.player.items if "Potion" in i.name]
        if not potions:
            wx.MessageBox("No potions available!",
                          "Error", wx.OK | wx.ICON_WARNING)
            return

        potion = potions[0]
        self.game.player.heal(potion.bonus)
        self.game.player.items.remove(potion)
        self.log_message(f"💚 Used {potion.name}. +{potion.bonus} HP")
        self.update_health_bar()

        # Monster attacks
        m = self.game.monster
        p = self.game.player
        dmg = calc_damage(m.atk, p.get_def())
        p.hp -= dmg
        self.log_message(f"💥 {m.name} deals {dmg} damage!")
        self.update_health_bar()

        if p.hp <= 0:
            self.game_over()

    def on_flee(self, event):
        if try_flee(self.game.player.speed, self.game.monster.speed):
            self.log_message("🏃 You successfully fled!")
            self.end_combat()
        else:
            self.log_message("❌ Failed to flee!")
            # Monster gets free attack
            dmg = calc_damage(self.game.monster.atk,
                              self.game.player.get_def())
            self.game.player.hp -= dmg
            self.log_message(f"💥 {self.game.monster.name} deals {dmg} damage!")
            self.update_health_bar()

            if self.game.player.hp <= 0:
                self.game_over()

    def on_shop(self, event):
        shop_items = [
            f"{name} - {cost}g (+{bonus})" for name, cost, bonus, _ in GameLogic.SHOP]

        dlg = wx.SingleChoiceDialog(self, f"Your Gold: {self.game.player.gold}g\n\nSelect item to buy:",
                                    "Shop", shop_items)
        if dlg.ShowModal() == wx.ID_OK:
            idx = dlg.GetSelection()
            name, cost, bonus, itype = GameLogic.SHOP[idx]

            if self.game.player.gold >= cost:
                self.game.player.gold -= cost
                self.game.player.items.append(Item(name, cost, bonus))
                self.log_message(f"✅ Bought {name} for {cost}g")
                self.update_status()
            else:
                wx.MessageBox(f"Not enough gold! Need {cost}g, have {self.game.player.gold}g",
                              "Error", wx.OK | wx.ICON_WARNING)

    def win_combat(self):
        m = self.game.monster
        self.log_message(f"🎉 Victory! Defeated {m.name}!")
        self.game.player.gold += m.gold
        self.log_message(f"Gained {m.gold} gold and {m.exp} EXP!")

        if self.game.player.add_exp(m.exp):
            self.log_message(
                f"🎉 Level up! Now level {self.game.player.level}!")

        if random.random() < 0.3:
            loot = random.choice(GameLogic.SHOP)
            item = Item(loot[0], loot[1], loot[2])
            self.game.player.items.append(item)
            self.log_message(f"Dropped {item.name}!")

        self.end_combat()
        self.update_status()

    def end_combat(self):
        self.game.in_combat = False
        self.game.monster = None
        self.update_monster_bar()
        self.update_buttons()

    def game_over(self):
        self.log_message("💀 GAME OVER!")
        wx.MessageBox(f"You have fallen at level {self.game.player.level}.\n"
                      f"Final stats: {self.game.player.gold} gold, {self.game.player.exp} EXP",
                      "Game Over", wx.OK | wx.ICON_INFORMATION)
        self.game.player = None
        self.game.in_combat = False
        self.game.monster = None
        self.update_buttons()
        self.update_monster_bar()

# ============================================================================
# MAIN
# ============================================================================


def main():
    app = wx.App()
    frame = RPGFrame()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
