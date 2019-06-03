import random
import re
import sys
import time

from reusables.string_manipulation import int_to_words

from app.common_functions import formatted_items, comma_separated, parse_inventory_action, odds, remove_little_words, \
    are_is, find_specifics
from app.main_classes import MapSquare, Player
from app.battle import Battle


class Adventure:
    def __init__(self, name):
        self.player = Player(name=name, location=(0, 0))
        self.map = {(0, 0): MapSquare(name="spawn")}
        self.player.square = self.map[(0, 0)]
        self.map[(0, 0)].generate_items()
        self.map[(0, 0)].generate_buildings(self.player)
        self.map[(0, 0)].generate_mobs(self.player)

    def help_me(self):
        """ List of commands based on situation """
        command_list = {"look around": True,
                        "go <southwest>": True,
                        "inventory": True,
                        "status": True,
                        "pick up <something>": bool(self.player.square.items and self.player.building_local is None),
                        "eat <something>": bool([x for x in self.player.inventory if x.category == "food"]),
                        "visit <a building>": bool(self.player.square.buildings),
                        "leave <the building>": bool(self.player.building_local),
                        "buy <something>": bool(self.player.building_local and self.player.building_local.wares),
                        "apply <for a job>": bool(self.player.building_local and self.player.building_local.jobs),
                        "battle <a mob>": bool(self.player.square.mobs or self.player.building_local.mobs),
                        "equip <something>": bool(self.player.inventory),
                        "ask <a mob> for a quest": bool(self.player.square.mobs or self.player.building_local.mobs),
                        "say hi to <a mob>": bool(self.player.square.mobs or self.player.building_local.mobs),
                        "turn in quest": bool(self.player.quest),
                        "go to work": bool(self.player.job),
                        "map": True,
                        "exit": True}

        for command, status in command_list.items():
            if status:
                print(command)

    def commands_manager(self, words):
        """ Command handler. """
        words = words.lower().split(" ")
        commands = {
            "^visit.*": (self.interact_with_building, [" ".join(words[1:])]),
            "^take.*": (self.pick_up, [" ".join(words[1:])]),
            "^eat.*": (self.eat_food, [" ".join(words[1:])]),
            "^buy.*": (self.buy, [" ".join(words[1:])]),
            "^equip.*": (self.equip, [" ".join(words[1:])]),
            "help": (self.help_me, []),
            "^go (?!to work).*": (self.change_direction, [' '.join(words[1:]).strip()]),
            "map": (self.player.square.map_picture, [self.map, self.player]),
            ".*turn in.*": (self.turn_in_quest, []),
            "complete quest": (self.turn_in_quest, []),
            "look around": (self.look_around, []),
            ".*look.*": (self.look_around, []),
            "^work.*": (self.go_to_work, []),
            "go to work": (self.go_to_work, []),
            "leave": (self.leave_building, []),
            "inventory": (print, [self.player.pretty_inventory()]),
            "status": (print, [self.player.status(self.player)]),
            "ls": (print, ["What, you think this is Linux?"]),
            "^attack": (self.battle_kickoff, [" ".join(words[1:])]),
            "^fight": (self.battle_kickoff, [" ".join(words[1:])]),
            "^battle": (self.battle_kickoff, [" ".join(words[1:])]),
            ".*say.*": (self.talk, [words]),
            ".*talk.*": (self.talk, [words]),
            ".*ask.*": (self.talk, [words]),
            "^pick up.*": (self.pick_up, [" ".join(words[2:])]),
            "^apply.*": (self.apply_for_job, [" ".join(words[1:])])
        }

        for k, v in commands.items():
            if re.match(k, " ".join(words)):
                v[0](*v[1])
                return

        if words[0] == "exit" and self.player.building_local:
            self.leave_building()

        elif words[0] == "exit" and self.player.building_local is None:
            self.player.health = 0
            print("Goodbye!")
            # TODO save game before exiting?
            # TODO shouldn't be able to work back to back
            # TODO add inventory limit
        else:
            print("I don't know that command.")

    def change_direction(self, direction):
        """ Change direction """

        if not direction or direction not in ["n", "ne", "nw", "s", "se", "sw", "e", "w", "north",
                                              "northeast", "northwest", "south", "southeast", "southwest",
                                              "east", "west", "up", "down", "left", "right"]:
            print("Looks like you're headed nowhere fast!")
            return

        # TODO travel to distant squares
        sys.stdout.write("Traveling . . .")
        sys.stdout.flush()
        count = 5
        vehicles = [x.rarity for x in self.player.inventory if x.category == 'vehicle']
        travel_time = 1
        if 'super rare' in vehicles:
            travel_time = 0
        elif 'rare' in vehicles:
            travel_time = .1
        elif 'common' in vehicles:
            travel_time = .2
        elif vehicles:
            travel_time = .5

        while count > 0:
            time.sleep(travel_time)
            sys.stdout.write(" .")
            sys.stdout.flush()
            count -= 1
        print()

        self.leave_building()
        x, y = self.player.location
        if direction.lower() in ("n", "ne", "nw", "north", "northeast", "northwest", "up"):
            y += 1
        if direction.lower() in ("e", "ne", "se", "east", "northeast", "southeast", "right"):
            x += 1
        if direction.lower() in ("s", "se", "sw", "south", "southeast", "southwest", "down"):
            y -= 1
        if direction.lower() in ("w", "nw", "sw", "west", "northwest", "southwest", "left"):
            x -= 1

        new_coordinates = (x, y)
        self.player.location = new_coordinates

        if new_coordinates not in self.map.keys():
            self.map[new_coordinates] = MapSquare()
            self.map[new_coordinates].generate_buildings(self.player)
            self.map[new_coordinates].generate_mobs(self.player)
            self.map[new_coordinates].generate_items()
        self.player.square = self.map[new_coordinates]
        print(f"You are now located on map coordinates {new_coordinates}, which is {self.player.square.square_type}.")

        # TODO add limits for items generated
        self.look_around()

    def look_around(self):
        """ Describe the player's surroundings """
        if self.player.building_local is None:
            if self.player.square.items:
                print(f"You can see {comma_separated(formatted_items(self.player.square.items))} near you.")
            if self.player.square.buildings:
                q = len(self.player.square.buildings)
                if q == 1:
                    q = self.player.square.buildings[0].quantity
                print(f"The building{'s' if q > 1 else ''} here {are_is(self.player.square.buildings)}.")
            if self.player.square.mobs:
                print(f"There {are_is(self.player.square.mobs)} here.")
            if self.player.square.items == [] and self.player.square.buildings == [] and self.player.square.mobs == []:
                print("Nothing seems to be nearby.")

        else:
            if self.player.building_local.wares:
                wares = [f"{int_to_words(x.quantity)} {x.plural}" if x.quantity > 1 else x.name for x in self.player.building_local.wares]
                print(f"This {self.player.building_local.name} has these items for sale: {comma_separated(wares)}")

            if self.player.building_local.mobs:
                print(f"There {are_is(self.player.building_local.mobs)} here.")
            if self.player.building_local.jobs:
                print(f"You can apply for the following open positions here: "
                      f"{comma_separated([x.name for x in self.player.building_local.jobs])}")
            if (self.player.building_local.mobs is None or self.player.building_local.mobs == []) and \
                    (self.player.building_local.wares is None or self.player.building_local.wares == []):
                print("There isn't anything here.")

    def irritate_the_locals(self, item):
        """ Decide whether or not to agro mobs if the player tries to pick up a rare item.
        Returns list of mobs or False
        """
        if item.rarity in ('rare', 'super rare') and odds(2) and self.player.square.mobs:
            angry_mob = [x for x in self.player.square.mobs if odds(2) and x.health > 50]
            angry_mob = angry_mob if len(angry_mob) >= 1 else [self.player.square.mobs[0]]
            return angry_mob
        return False

    def pick_up(self, words):
        """ Add items from surroundings to player inventory """
        if not self.player.square.items:
            print("Nothing to pick up.")
            return
        words = words.replace(',', '')
        quantity, item_text = parse_inventory_action(words)
        item_text = 'all' if item_text is None else item_text

        specific_items = find_specifics(item_text, self.player.square.items)
        if not specific_items:
            print("Sorry, I can't find that.")
            return

        items_added = []
        for item in specific_items:
            angry_mob = self.irritate_the_locals(item)
            if angry_mob is False:
                q = item.quantity if quantity == "all" or quantity is None else quantity
                if q > item.quantity:
                    print("Can't pick up that many.")
                    break
                self.add_item_to_inventory(item, q)
                items_added.append((item, q))
                item.quantity -= q
            else:
                self.player.square.clean_up_map()
                if items_added:
                    print(f"Added {comma_separated([x[0].name if x[1] == 1 else x[0].plural for x in items_added])} "
                          f"to your inventory.")
                print(f"""Uh oh, {"the locals don't" if len(angry_mob) > 1 else "someone doesn't"} like you """
                      f"""trying to take """
                      f"""their {remove_little_words(item.name) if item.quantity == 1 else item.plural}!""")
                battle = Battle(self, angry_mob, [self.player], contested_item=item)
                battle.battle_loop()
                break
        else:
            self.player.square.clean_up_map()
            if items_added:
                print(f"Added {comma_separated([x[0].name if x[1] == 1 else x[0].plural for x in items_added])} "
                      f"to your inventory.")

    def add_item_to_inventory(self, item_to_add, quantity, mob=None):
        mob = mob or self.player
        mob_inventory = mob.inventory if mob is not self.map else self.player.square.items

        if mob != self.map and mob.equipped_weapon is not None and item_to_add.name == mob.equipped_weapon.name:
            mob.equipped_weapon.quantity += quantity

        elif item_to_add.name in [x.name for x in mob_inventory]:
            for item in mob_inventory:
                if item_to_add.name == item.name:
                    item.quantity += int(quantity)
        else:
            new_item = item_to_add.copy()
            new_item.quantity = quantity
            mob_inventory.append(new_item)

    def eat_food(self, words):
        """ Eat food in your inventory to gain health """
        # TODO add drinking for coffee and whiskey shots
        # TODO only eat one bagel not all bagels
        quantity, item_text = parse_inventory_action(words)

        if quantity is None and item_text is None:
            print("I can't figure out what you want to eat!")
            return

        def eat(item_eaten, q):
            if q > item_eaten.quantity:
                print("Cant eat that many")
                return

            item_eaten.quantity -= q

            if item_eaten.quantity == 0:
                self.player.inventory.remove(item_eaten)
            # TODO chance to loose health eating mysterious berries?
            # TODO stop eating when health is 100
            # TODO eat bagel ate all bagels not singular bagel
            for x in range(0, q):
                if self.player.health < 100:
                    if item_eaten.name == "a magic pill":
                        regenerate = 100 - self.player.health
                    else:
                        regenerate = random.randint(0, 100 - self.player.health)
                    self.player.health += regenerate
                    print(f"Regenerated {regenerate} health by eating {item_eaten.name}.")

        food = [x for x in self.player.inventory if x.category == "food"]
        if item_text and "perishable" in item_text:
            food = [x for x in self.player.inventory if x.category == "food" and x.perishable]

        if item_text is None and quantity is "all":
            for i in food:
                eat(i, i.quantity)

        elif "food" in item_text:
            for i in food:
                if isinstance(quantity, int):
                    if i.quantity <= quantity:
                        i.quantity = 0
                        quantity -= i.quantity
                        eat(i, quantity)
                    elif quantity < i.quantity:
                        i.quantity -= quantity
                        quantity = 0
                    else:
                        break
                else:
                    eat(i, i.quantity)

        else:
            for i in food:
                if item_text in i.name or item_text in i.plural:
                    if quantity == "all":
                        quantity = i.quantity
                    eat(i, quantity)
                    return
            else:
                print(f"Couldn't eat {item_text}")

    def go_to_work(self):
        """ Spend time at work to earn money and experience """
        if not self.player.job:
            print("Sorry, you don't have a job. Try applying for one.")
            return

        if self.player.phase != "day" and "night" not in self.player.job.name:
            print("You can only work in the daytime.")
            return
        elif self.player.phase != "night" and "night" in self.player.job.name:
            print("You can only work in the nighttime.")
            return

        if self.player.job.location != self.player.location:
            print(f"Your job is not here. You need to go here: {self.player.job.location}")
            return

        sys.stdout.write("Working . . .")
        sys.stdout.flush()
        count = 8
        while count > 0:
            time.sleep(1.5)
            sys.stdout.write(" .")
            sys.stdout.flush()
            count -= 1
        print()
        print(f"You earned ${self.player.job.salary}.")
        self.player.money += self.player.job.salary
        if self.player.job.skills_learned:
            for skill in self.player.job.skills_learned:
                percentage = random.randint(0, 20)
                try:
                    self.player.skills[skill] += percentage
                except KeyError:
                    self.player.skills[skill] = percentage

            mastery = [f"{s} - {m}" for s, m in self.player.skills.items()]
            if mastery:
                print(f"You gained some skill mastery at work! {comma_separated(mastery)}%")

    @staticmethod
    def find_specific_job(words, list_of_jobs):
        for job in list_of_jobs:
            for word in remove_little_words(words).split(' '):
                if word.lower() in job.name.lower() or word.lower() == job.name.lower():
                    return job

    def apply_for_job(self, words):
        """ Player skills determine chances of getting a job """
        if not self.player.building_local or not self.player.building_local.jobs:
            print("No jobs to apply for here.")
            return
        if not words:
            if len(self.player.building_local.jobs) == 1:
                job = self.player.building_local.jobs[0]
            else:
                print("What job are you applying for?")
                return
        else:
            job = self.find_specific_job(words, self.player.building_local.jobs)
        if job:
            if job == self.player.job:
                print("You already have this job.")
                return

            if job.inventory_needed and job.inventory_needed not in self.player.inventory:
                print(f"You need {job.inventory_needed} for this job.")
                return

            match_score = 0

            for skill in job.skills_needed:
                if skill in self.player.skills.keys():
                    if self.player.skills[skill] > 90:
                        print(f"Wow, it says here you are really good at {skill}.")
                    match_score += (self.player.skills[skill] / len(job.skills_needed))

            match_score = 1 if match_score >= 100 else 100 - match_score

            if odds(match_score):
                print(f"Congratulations {self.player.name}, you got the job!")
                self.player.job = job
                # TODO clean-up job so it doesn't show on job listing?

            else:
                bad_news = [f"I'm sorry, we're looking for candidates with more "
                            f"{comma_separated(job.skills_needed)} skills right now.",
                            "We'll let you know."]
                print(bad_news[random.randint(0, len(bad_news) - 1)])
        else:
            print("That's not a job we are hiring for currently.")

    def interact_with_building(self, words):
        """ Try entering a building """
        building = find_specifics(words, self.player.square.buildings)
        building = building[0] if building else None
        if building is not None:
            if building.category == 'building':
                if odds(8) is True:
                    print(f"Too bad, {building.name} is closed right now. Try again later.")
                else:
                    self.player.building_local = building
                    print(f"You are now inside {building.name}.")
                    self.look_around()

            else:
                if odds(10) is False or self.player.phase == 'night':
                    print("The occupants of this residence have kicked you out.")
                else:
                    self.player.building_local = building
                    print("You are now inside a house.")
                    self.look_around()

        else:
            print("That's not a place you can visit.")

    def leave_building(self):
        """ Exit the building the player is inside """
        if self.player.building_local is not None:
            print(f"Leaving {self.player.building_local.name}")
            self.player.building_local = None

    def buy(self, words):
        """ Establish a transaction to purchase wares """
        wares = []
        haggle_for = True
        quantity, item_text = parse_inventory_action(words)

        if quantity == 'all' and item_text is None:
            wares = [x for x in self.player.building_local.wares]
            ware_list = [f"{ware.plural} x {ware.quantity}" for ware in self.player.building_local.wares]
            price_total = sum([ware.price * ware.quantity for ware in self.player.building_local.wares])
            print(f"For {comma_separated(ware_list)}, that comes to ${price_total}.")

        else:
            for ware in self.player.building_local.wares:

                if remove_little_words(item_text) in ware.name or remove_little_words(item_text) in ware.plural:
                    wares = [ware]
                    if quantity == "all":
                        quantity = ware.quantity

                    if quantity > ware.quantity:
                        print(f"Sorry, we only have {ware.quantity} for sale.")
                        haggle_for = False
                    else:
                        print(f"For {ware.plural} x {quantity}, that comes to ${ware.price * quantity}.")
                    break
            else:
                print("I can't figure out what you want.")
                haggle_for = False

        if haggle_for is True:
            price_offered = input("Make me an offer:")
            try:
                price_offered = int(price_offered.strip(" "))
                self.haggle(wares, quantity, price_offered)
            except ValueError:
                print("I was hoping for a number, sorry.")
            except TypeError:
                print("I was hoping for a number, sorry.")

    def haggle(self, items, quantity, price_offered):
        """ Negotiate the price on items for sale """
        if price_offered > self.player.money:
            print("Sorry you don't have enough cash to make that offer. Try getting a job.")
            return

        if quantity == 'all':
            price = sum([item.price * item.quantity for item in items])
        else:
            price = sum([item.price for item in items]) * quantity

        if price <= price_offered <= self.player.money:
            self.buy_items(items, quantity, price_offered)
            print("Purchase complete")

        elif price > price_offered > 0:
            if odds(price - price_offered) is True:
                print("Ok, sounds like a deal.")
                self.buy_items(items, quantity, price_offered)
            else:
                print("Sorry, I can't sell for that price.")
        else:
            print("Sorry, I can't sell for that price")

    def buy_items(self, items, quantity, cost):
        """ Add bought items to player inventory and subtract cost from player's cash """
        for item in items:
            q = item.quantity if quantity == 'all' else quantity
            self.add_item_to_inventory(item, q)
            if q == item.quantity:
                self.player.building_local.wares.remove(item)
            else:
                item.quantity -= q
        self.player.money -= cost

    def talk(self, words):
        """ Say hello to mobs and ask for quests """

        mobs = self.player.square.mobs if self.player.building_local is None else self.player.building_local.mobs

        if mobs and len(mobs) == 1:
            specific_mob = mobs
        else:
            specific_mob = find_specifics(words, mobs)
        if not specific_mob:
            print("Don't know who to talk to.")
        else:
            specific_mob = specific_mob[0]
            single_mob = remove_little_words(specific_mob.name)
            non_responses = [f"The {single_mob} just looks at you.",
                             f"The {single_mob} doesn't respond.",
                             f"The {single_mob} is pretending not to speak english.",
                             f"The {single_mob} lets out a high pitched and unintelligible shriek.",
                             f"The {single_mob} ignores you completely."]

            no_quest_responses = [f"The {single_mob} shakes his head gravely.",
                                  # TODO add mob gender
                                  f"The {single_mob} says 'No quests today.'",
                                  f"The {single_mob} says 'I don't feel like it right now'.",
                                  f"The {single_mob} laughs maniacally. 'A quest? For you? Yeah right.'"]

            yes_quest_responses = [f"The ground shakes as the {single_mob} roars 'YES, I HAVE A QUEST FOR YOU!'",
                                   f"The {single_mob} says 'Yup, I've got a quest for you.'",
                                   f"The {single_mob} says 'Fiiiineeee, I'll give you a quest'.",
                                   f"The {single_mob} scratches his head thoughtfully."]

            greeting_responses = [f"The {single_mob} nods.",
                                  f"The {single_mob} smiles and waves at you.",
                                  f"The {single_mob} sneers at your impertinence.",
                                  f"The {single_mob} gives you a cheerful 'Hello!'"]
            fighting_responses = [f"The {single_mob} is very annoyed by your nagging.",
                                  "Those are fighting words.",
                                  f"The {single_mob} takes great offence to you.",
                                  f"The {single_mob}'s patience has snapped."]
            if specific_mob.irritation_level < 10:
                specific_mob.irritation_level += 1
            if odds(11 - specific_mob.irritation_level):
                print(fighting_responses[random.randint(0, len(no_quest_responses) - 1)])
                battle = Battle(self, [specific_mob], [self.player])
                battle.battle_loop()
                return

            if "quest" in words:
                specific_mob.generate_quest()
                if specific_mob.quest is None:
                    print(no_quest_responses[random.randint(0, len(no_quest_responses) - 1)])
                elif specific_mob.quest is not False:
                    print(yes_quest_responses[random.randint(0, len(yes_quest_responses) - 1)])
                    print(specific_mob.quest[2])
                    if input("Do you accept the quest?{} yes/no:".format(
                            ' This will replace your current quest.' if self.player.quest else '')).lower() == "yes":
                        self.player.quest = (specific_mob, self.player.location)
            elif any(word in ("hi", "hello", "greet", "greetings", "howdy") for word in words):
                print(greeting_responses[random.randint(0, len(greeting_responses) - 1)])
            else:
                print(non_responses[random.randint(0, len(non_responses) - 1)])

            self.player.greeting_count += 1
            if self.player.greeting_count % 15 == 0:
                print(f"By the way, you have been really outgoing lately!")
                self.player.increase_skill('communication', random.randint(1, 5))

    def turn_in_quest(self):
        """ Complete the quest if criteria is met, otherwise help player remember quest details """
        if self.player.quest is None:
            print("You don't have a quest.")
            return

        mob_name = remove_little_words(self.player.quest[0].name)
        mob = self.player.quest[0]

        if self.player.quest[1] != self.player.location:
            print(f"The {mob_name} who gave you your quest is not here. You need to go to {self.player.quest[1]}.")
            return

        if mob not in self.player.square.mobs:
            print(f"Looks like the {mob_name} who gave you the quest is dead. That's too bad.")
            self.player.quest = None
            return

        quest_item = mob.quest[0]
        quantity = mob.quest[1]
        for item in self.player.inventory:
            if item.name == quest_item.name:
                if item.quantity >= quantity:
                    print(f"You have enough {quest_item.plural} the {mob_name} requested.")
                    item.quantity -= quantity

                    self.add_item_to_inventory(item, quantity, mob)

                    skill = mob.skills[random.randint(0, len(mob.skills) - 1)]
                    percentage = random.randint(1, 100)
                    print(f"In exchange, the {mob_name} teaches you some {skill}.")
                    self.player.increase_skill(skill, percentage)
                    self.player.quest = None
                    mob.quest = None
                else:
                    # TODO you have to un-equip the thing to turn in if you are wielding it
                    # TODO turning in the same quest twice doesn't seem to work if you have the item
                    print(f"You don't have enough {quest_item.plural}. The {mob_name} requested {quantity}, "
                          f"and you have {item.quantity}.")
                break
        else:
            print(f"You don't have any {quest_item.plural}. You need {quantity}.")

        self.player.inventory = [i for i in self.player.inventory if i.quantity > 0]

    def battle_kickoff(self, words, attacking_mobs=None):
        attacking_mobs = attacking_mobs or None
        list_of_locals = self.player.building_local.mobs if self.player.building_local else self.player.square.mobs
        if not attacking_mobs:
            attacking_mobs = find_specifics(words, list_of_locals)
        if not attacking_mobs:
            print("Who are you attacking?")
            return
        else:
            m = comma_separated(formatted_items(attacking_mobs))
            print(f"Look out, {m[0].upper()}{m[1:]} {'is' if len(attacking_mobs) == 1 else 'are'} gearing up to fight!")
            battle = Battle(adventure=self, list_of_attackers=[self.player], list_of_defenders=attacking_mobs)
            battle.battle_loop()

    def equip(self, words):
        """ Select item from player inventory to use as battle weapon """
        if self.player.equipped_weapon is not None:
            i = self.player.equipped_weapon
            self.player.equipped_weapon = None
            self.add_item_to_inventory(i, i.quantity)
        w = find_specifics(words, self.player.inventory)
        if w:
            self.player.equipped_weapon = w[0]
            self.player.inventory.remove(w[0])
            # TODO standardize singular / plural nonsense
            print(f"Equipped {w[0].name if w[0].quantity == 1 else w[0].plural}")
        else:
            print(f"Can't find {words} in your inventory.")
