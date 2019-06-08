import random
import re

from termcolor import colored

from app.common_functions import the_name, comma_separated, formatted_items, odds, remove_little_words


class Battle:
    def __init__(self, adventure, list_of_attackers, list_of_defenders, contested_item=None):
        self.adventure = adventure
        self.attackers = list_of_attackers
        self.defenders = list_of_defenders
        self.contested_item = contested_item or None
        self.coward = False

    def battle_help(self):
        """ List of commands available during battle """
        command_list = {"attack": True,
                        "throw": bool(self.adventure.player.equipped_weapon),
                        "eat <something>": bool([x for x in self.adventure.player.inventory if x.category == "food"]),
                        "run away": bool(self.adventure.player not in self.attackers),
                        "inventory": True,
                        "equip": bool(self.adventure.player.inventory),
                        "status": True}
        for command, status in command_list.items():
            if status:
                print(command)

    def sort_the_dead(self, list_of_mobs):
        alive_mobs = []
        for mob in list_of_mobs:
            if mob.health > 0:
                alive_mobs.append(mob)
            else:
                mob_id = the_name(mob.name).capitalize()
                if mob.equipped_weapon:
                    mob.inventory.append(mob.equipped_weapon)
                stuff = mob.inventory
                self.adventure.player.body_count += 1
                s = f" You add {comma_separated(formatted_items(stuff))} to your " \
                    f"inventory." if stuff else ''
                print(f"You killed {mob_id}.{s}")
                for i in stuff:
                    self.adventure.add_item_to_inventory(i, i.quantity)

                if odds(3):
                    self.adventure.player.increase_skill('strength', 2)

                if mob.name in self.adventure.player.hit_list:
                    reward = random.randint(100, 500)
                    self.adventure.player.money += reward
                    self.adventure.player.hit_list.remove(mob.name)
                    self.adventure.player.assassination_count += 1
                    print(f"You have eliminated the pesky {remove_little_words(mob.name)}. For your troubles, you earn {reward}.")
                if self.adventure.player.body_count % 5 == 0:
                    print("You've really been racking up the body count.")
                    self.adventure.player.increase_skill('self loathing', random.randint(2, 8))

                if self.adventure.player.building_local:
                    self.adventure.player.building_local.mobs.remove(mob)
                else:
                    self.adventure.player.square.mobs.remove(mob)
        return alive_mobs

    @staticmethod
    def attack(attackers, defenders):

        usefulness = [(0, 10), (10, 15), (15, 25), (25, 32), (32, 50), (50, 60)]

        for attacker in attackers:
            for defender in defenders:
                w = attacker.equipped_weapon
                try:
                    damage = random.randint(usefulness[w.weapon_rating][0], usefulness[w.weapon_rating][1])
                except (AttributeError, TypeError):
                    damage = random.randint(usefulness[0][0], usefulness[0][1])

                major = defender.major_armor.defense if defender.major_armor else 0
                minor = defender.minor_armor.defense if defender.minor_armor else 0
                armor_defense = ((major + minor) * 5) / 100
                if armor_defense > 0:
                    damage -= round(damage * armor_defense)

                defender.health -= damage
                print(f"{attacker.name.capitalize()} inflicted {damage} damage to {defender.name}. "
                      f"{defender.name.capitalize()} has {defender.health} health left.")

    def throw(self, attackers, defenders):
        usefulness = [(0, 20), (10, 30), (20, 40), (10, 25), (5, 15), (0, 10)]

        for attacker in attackers:
            for defender in defenders:
                if not attacker.equipped_weapon:
                    return
                w = attacker.equipped_weapon
                try:
                    damage = random.randint(usefulness[w.weapon_rating][0], usefulness[w.weapon_rating][1])
                except AttributeError:
                    damage = random.randint(usefulness[0][0], usefulness[0][1])

                major = defender.major_armor.defense if defender.major_armor else 0
                minor = defender.minor_armor.defense if defender.minor_armor else 0
                armor_defense = ((major + minor) * 5) / 100
                if armor_defense > 0:
                    damage -= round(damage * armor_defense)

                defender.health -= damage
                w.quantity -= 1
                self.adventure.add_item_to_inventory(w, 1, self.adventure.map)

                print(f"{attacker.name.capitalize()} inflicted {damage} damage to {defender.name}. "
                      f"{defender.name.capitalize()} has {defender.health} health left.")
                if w.quantity == 0:
                    print(f"You are out of {w.plural}.")
                    attacker.equipped_weapon = None

    def run_away(self):
        if self.adventure.player in self.attackers:
            print("You can't leave the battle. You must fight!")
        else:
            self.coward = True
            self.attackers = []
            self.adventure.player.run_away_count += 1
            print("You run away in a cowardly panic.")
            dirs = ["north", "south", "east", "west"]
            random_dir = dirs[random.randint(0, len(dirs) - 1)]
            self.adventure.change_direction(random_dir)

    def battle_loop(self):
        while self.adventure.player.health > 0 and self.attackers:
            if self.adventure.player in self.attackers:
                self.battle_commands_manager()
                self.defenders = self.sort_the_dead(self.defenders)
                if not self.defenders:
                    print("Everyone you were attacking is now dead. Carry on.")
                    break
            else:
                self.attack(self.attackers, self.defenders)
                if not self.attackers:
                    print("Everyone attacking you is now dead. Carry on.")
                    break

            if self.adventure.player.health <= 0:
                break

            if self.adventure.player in self.defenders:
                self.battle_commands_manager()
                self.attackers = self.sort_the_dead(self.attackers)
                for attacker in self.attackers:
                    if attacker.health <= 50:
                        print(f"{the_name(attacker.name).capitalize()} decided the fight is not worth it and has bowed out.")
                self.attackers = [mob for mob in self.attackers if mob.health > 50]
                if not self.attackers and not self.coward:
                    print("Nobody is attacking you anymore.")
                    if self.contested_item:
                        self.adventure.add_item_to_inventory(self.contested_item, self.contested_item.quantity)
                        print(f"Added {self.contested_item.name if self.contested_item.quantity == 1 else self.contested_item.plural} to your inventory.")
                        self.contested_item.quantity = 0
                        self.adventure.player.square.clean_up_map()

            else:
                self.attack(self.defenders, self.attackers)
                # TODO mobs can eat food if they have it to regain health maybe?
        if self.adventure.player.health <= 0:
            self.death()

    def death(self):
        if not self.adventure.player.job:
            print(f"{colored('You died.', 'magenta')} The end.")
            return
        else:
            print(f"{colored('You died,', 'magenta')} but luckily your job provides you health insurance.")
            cost_to_live = random.randint(200, 500)
            if self.adventure.player.money >= cost_to_live:
                print(f"You shell out {cost_to_live} to the insurance guys and rejoin the living at 50% health!")
                self.adventure.player.health = 50
                self.adventure.player.money -= cost_to_live
                self.battle_loop()
            else:
                print(f"However, it costs {cost_to_live} to save you, and you only have {self.adventure.player.money} in your account.")
                print("The end.")

    def battle_commands_manager(self):
        while True and self.attackers:
            words = input()
            words.strip()
            words = words.lower().split(" ")
            battle_paused_commands = {
                "help": (self.battle_help, []),
                "^eat.*": (self.adventure.eat_food, [" ".join(words[1:])]),
                "status": (print, [self.adventure.player.status()]),
                "inventory": (print, [self.adventure.player.pretty_inventory()]),
                "run away": (self.run_away, []),
                "equip": (self.adventure.equip, [" ".join(words[1:])])
            }

            paused = False
            for k, v in battle_paused_commands.items():
                if re.match(k, " ".join(words)):
                    v[0](*v[1])
                    paused = True
                    break
            if paused:
                continue

            if self.adventure.player in self.attackers:
                attacking_actions = {
                    "^attack": (self.attack, [self.attackers, self.defenders]),
                    "^throw.*": (self.throw, [self.attackers, self.defenders])
                }
            else:
                attacking_actions = {
                    "^attack": (self.attack, [self.defenders, self.attackers]),
                    "^throw.*": (self.throw, [self.defenders, self.attackers])
                }

            for k, v in attacking_actions.items():
                if re.match(k, " ".join(words)):
                    v[0](*v[1])
                    break
            else:
                paused = True
                print("I don't know that command.")

            if paused:
                continue
            else:
                break
