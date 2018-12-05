from app.main_classes import MapSquare, the_map, p, Mob
from app.common_functions import formatted_items, comma_separated, parse_inventory_action, odds, remove_little_words, \
    are_is, capitalize_first, find_specifics, the_name
import time
import sys
import random
from reusables.string_manipulation import int_to_words


def help_me():
    command_list = {"look around": True,
                    "go <southwest>": True,
                    "inventory": True,
                    "status": True,
                    "pick up <something>": True if the_map[p.location].items and p.building_local is False else False,
                    "eat <something>": True if [x for x in p.inventory if x.category == "food"] else False,
                    "visit <a building>": True if the_map[p.location].buildings else False,
                    "leave <the building>": True if p.building_local else False,
                    "buy <something>": True if p.building_local and p.building_local.wares else False,
                    "apply <for a job>": True if p.building_local and p.building_local.jobs else False,
                    "battle <a mob>": True if the_map[p.location].mobs or p.building_local.mobs else False,
                    "equip <something>": True if p.inventory else False,
                    "ask <a mob> for a quest": True if the_map[p.location].mobs or p.building_local.mobs else False,
                    "say hi to <a mob>": True if the_map[p.location].mobs or p.building_local.mobs else False,
                    "turn in quest": True if p.quest else False,
                    "go to work": True if p.job else False,
                    "exit": True}

    for command, status in command_list.items():
        if status:
            print(command)


def commands_manager(words):
    """ Command handler. """
    words = words.lower().split(" ")
    if words[0] == "help":
        help_me()

    elif words[0] == "go" and ' '.join(words) != "go to work":
        if words[1:] and ' '.join(words[1:]).strip() in ["n", "ne", "nw", "s", "se", "sw", "e", "w", "north",
                                                         "northeast", "northwest", "south", "southeast", "southwest",
                                                         "east", "west", "up", "down", "left", "right"]:
            change_direction(" ".join(words[1:]).strip())
        else:
            print("Looks like you're headed nowhere fast!")

    elif words[0] == "visit":
        interact_with_building(" ".join(words[1:]))

    elif words[0] == "leave" or words[0] == "exit" and p.building_local:
        leave_building()

    elif " ".join(words) == "look around" or "look" in words:
        look_around()

    elif " ".join(words) == "inventory":
        p.pretty_inventory()

    elif " ".join(words[0:2]) == "pick up":
        # TODO add inventory limit
        pick_up(" ".join(words[2:]))

    elif words[0] == "take":
        pick_up(" ". join(words[1:]))

    elif " ".join(words) == "status":
        p.status()

    elif words[0] == "eat":
        eat_food(" ".join(words[1:]))

    elif words[0] == "buy":
        buy(" ".join(words[1:]))

    elif "say" in words or "talk" in words or "ask" in words:
        talk(words)

    elif "turn in" in " ".join(words) or " ".join(words) == "complete quest":
        turn_in_quest()

    elif words[0] == "equip":
        equip(" ".join(words[1:]))

    elif words[0] in ("attack", "fight", "battle"):
        battle(" ".join(words[1:]), aggressing=True)

    elif words[0] == "exit" and p.building_local is None:
        p.health = 0
        print("Goodbye!")
        # TODO save game before exiting?
    elif words[0] == "apply" and p.building_local is not None:
        # TODO can't apply for job you already have
        apply_for_job(' '.join(words[1:]))
    elif words[0] == "work" or ' '.join(words) == "go to work":
        # TODO shouldn't be able to work back to back
        go_to_work()
    elif words[0] == "ls":
        print("What, you think this is Linux?")
    else:
        print("I don't know that command.")


def change_direction(direction):
    """
    Change direction:

    go north
    go southwest
    go n
    go sw
    """

    # TODO travel to distant squares
    sys.stdout.write("Traveling . . .")
    sys.stdout.flush()
    count = 5
    travel_time = 1 if not [x for x in p.inventory if x.category == 'vehicle'] else .2
    while count > 0:
        time.sleep(travel_time)
        sys.stdout.write(" .")
        sys.stdout.flush()
        count -= 1
    print()

    leave_building()
    x = p.location[0]
    y = p.location[1]
    if direction.lower() in ("n", "ne", "nw", "north", "northeast", "northwest", "up"):
        y += 1
    if direction.lower() in ("e", "ne", "se", "east", "northeast", "southeast", "right"):
        x += 1
    if direction.lower() in ("s", "se", "sw", "south", "southeast", "southwest", "down"):
        y -= 1
    if direction.lower() in ("w", "nw", "sw", "west", "northwest", "southwest", "left"):
        x -= 1

    p.location = (x, y)
    if p.location not in the_map.keys():
        the_map[p.location] = MapSquare()
        the_map[p.location].generate_buildings()
        the_map[p.location].generate_mobs()
        the_map[p.location].generate_items()
    print(f"You are now located on map coordinates {p.location}, which is {the_map[p.location].square_type}.")

    # TODO add limits for items generated
    look_around()


def look_around():
    if p.building_local is None:
        if the_map[p.location].items:
            print(f"You can see {comma_separated(formatted_items(the_map[p.location].items))} near you.")
        if the_map[p.location].buildings:
            q = len(the_map[p.location].buildings)
            if q == 1:
                q = the_map[p.location].buildings[0].quantity
            print(f"The building{'s'  if q > 1 else ''} here {are_is(the_map[p.location].buildings)}.")
        if the_map[p.location].mobs:
            print(f"There {are_is(the_map[p.location].mobs)} here.")
        if the_map[p.location].items == [] and the_map[p.location].buildings == [] and the_map[p.location].mobs == []:
            print("Nothing seems to be nearby.")

    else:
        if p.building_local.wares:
            wares = []
            for x in p.building_local.wares:
                if x.quantity > 1:
                    wares.append(f"{int_to_words(x.quantity)} {x.plural}")
                else:
                    wares.append(x.name)
            print(f"This {p.building_local.name} has these items for sale: {comma_separated(wares)}")

        if p.building_local.mobs:
            print(f"There {are_is(p.building_local.mobs)} here.")
        if p.building_local.jobs:
            print(f"You can apply for the following open positions here: "
                  f"{comma_separated([x.name for x in p.building_local.jobs])}")
        if (p.building_local.mobs is None or p.building_local.mobs == []) and \
                (p.building_local.wares is None or p.building_local.wares == []):
            print("There isn't anything here.")


def irritate_the_locals(i):
    if i.rarity in ('rare', 'super rare') and odds(2) and the_map[p.location].mobs != []:
        angry_mob = [x for x in the_map[p.location].mobs if odds(2)]
        angry_mob = angry_mob if len(angry_mob) >= 1 else [the_map[p.location].mobs[0]]
        return angry_mob
    else:
        return False


def clean_up_map():
    the_map[p.location].items = [i for i in the_map[p.location].items if i.quantity != 0]


def pick_up(words):
    if not the_map[p.location].items:
        print("Nothing to pick up.")
        return

    quantity, item_text = parse_inventory_action(words)
    item_text = 'all' if item_text is None else item_text

    specific_items = find_specifics(item_text, the_map[p.location].items)
    if not specific_items:
        print("Sorry, I can't find that.")
        return

    items_added = []
    for item in specific_items:
        angry_mob = irritate_the_locals(item)
        if angry_mob is False:
            q = item.quantity if quantity == "all" or quantity is None else quantity
            if q > item.quantity:
                print("Can't pick up that many.")
                break
            add_item_to_inventory(item, q)
            items_added.append((item, q))
            item.quantity -= q
        else:
            clean_up_map()
            # TODO if you 'take sea shells' it prints added sea shell and sea shells to your inventory....
            if items_added:
                print(f"Added {comma_separated([x[0].name if x[1] == 1 else x[0].plural for x in items_added])} "
                      f"to your inventory.")
            print(f"""Uh oh, {"the locals don't" if len(angry_mob) > 1 else "someone doesn't"} like you """
                  f"""trying to take """
                  f"""their {remove_little_words(item.name) if item.quantity == 1 else item.plural}!""")
            battle(angry_mob)
            break
    else:
        clean_up_map()
        if items_added:
            print(f"Added {comma_separated([x[0].name if x[1] == 1 else x[0].plural for x in items_added])} "
                  f"to your inventory.")


def add_item_to_inventory(item_to_add, quantity, mob=p):
    if mob.equipped_weapon is not None and item_to_add.name == mob.equipped_weapon.name:
        mob.equipped_weapon.quantity += quantity

    elif item_to_add.name in [x.name for x in mob.inventory]:
        for x in mob.inventory:
            if item_to_add.name == x.name:
                x.quantity += int(quantity)
    else:
        new_item = item_to_add.copy()
        new_item.quantity = quantity
        mob.inventory.append(new_item)


def add_dropped_item_to_map(item_to_add, quantity):
    if item_to_add.name in [x.name for x in the_map[p.location].items]:
        for x in the_map[p.location].items:
            if item_to_add.name == x.name:
                x.quantity += int(quantity)

    else:
        new_item = item_to_add.copy()
        new_item.quantity = quantity
        the_map[p.location].items.append(new_item)


def eat_food(words):
    """
    Eat food in your inventory:

    eat a mars bar
    eat 1 mars bar
    eat three mars bars
    eat 3 mars bars
    eat all mars bars
    eat the mars bars
    eat all food
    eat everything
    eat the food
    eat some food
    eat the perishable food
    """
    # TODO add drinking for coffee and whiskey shots
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
            p.inventory.remove(item_eaten)
        # TODO chance to loose health eating mysterious berries?
        # TODO stop eatting when health is 100
        # TODO eat bagel ate all bagels not singular bagel
        for x in range(0, q):
            if p.health < 100:
                if item_eaten.name == "a magic pill":
                    regenerate = 100 - p.health
                else:
                    regenerate = random.randint(0, 100-p.health)
                p.health += regenerate
                print(f"Regenerated {regenerate} health by eating {item_eaten.name}.")

    food = [x for x in p.inventory if x.category == "food"]
    if item_text and "perishable" in item_text:
        food = [x for x in p.inventory if x.category == "food" and x.perishable]

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


def go_to_work():
    if p.job:
        if p.phase == "day":
            if p.job.location == p.location:
                sys.stdout.write("Working . . .")
                sys.stdout.flush()
                count = 8
                while count > 0:
                    time.sleep(1.5)
                    sys.stdout.write(" .")
                    sys.stdout.flush()
                    count -= 1
                print()
                print(f"You earned ${p.job.salary}.")
                p.money += p.job.salary
                if p.job.skills_learned:
                    for skill in p.job.skills_learned:
                        percentage = random.randint(0, 20)
                        try:
                            p.skills[skill] += percentage
                        except KeyError:
                            p.skills[skill] = percentage

                    mastery = [f"{s} - {m}" for s, m in p.skills.items()]
                    if mastery:
                        print(f"You gained some skill mastery at work: {comma_separated(mastery)}%")

            else:
                print(f"Your job is not here. You need to go here: {p.job.location}")
        else:
            print("You can only work in the daytime.")
            # TODO night stockers work at night.. add phase to job description
    else:
        print("Sorry, you don't have a job. Try applying for one.")


def find_specific_job(words, location):
    for j in location.jobs:
        for word in remove_little_words(words):
            if word in j.name or word == j.name:
                return j


def apply_for_job(words):
    if not words:
        if len(p.building_local.jobs) == 1:
            job = p.building_local.jobs[0]
        else:
            print("What job are you applying for?")
            return
    else:
        job = find_specific_job(words, p.building_local)
    if job:
        if job.inventory_needed and job.inventory_needed not in p.inventory:
            print(f"You need {job.inventory_needed} for this job.")
            return

        match_score = 100

        for skill in job.skills_needed:
            if skill in p.skills.keys():
                if p.skills[skill] > 90:
                    print(f"Wow, it says here you are really good at {skill}.")
                match_score -= p.skills[skill] / len(job.skills_needed)

        match_score = 1 if match_score <= 0 else match_score

        if odds(match_score):
            print(f"Congratulations {p.name}, you got the job!")
            p.job = job
            # TODO clean-up job so it doesn't show on job listing?

        else:
            bad_news = [f"I'm sorry, we're looking for candidates with more "
                        f"{comma_separated(job.skills_needed)} right now.",
                        "We'll let you know."]
            print(bad_news[random.randint(0, len(bad_news)-1)])


def interact_with_building(words):
    building = find_specifics(words, the_map[p.location].buildings)
    building = building[0] if building else None
    if building is not None:
        if building.category == 'building':
            if odds(8) is True:
                print(f"Too bad, {building.name} is closed right now. Try again later.")
            else:
                p.building_local = building
                print(f"You are now inside {building.name}.")
                look_around()

        else:
            if odds(10) is False or p.phase == 'night':
                print("The occupants of this residence have kicked you out.")
            else:
                p.building_local = building
                print("You are now inside a house.")
                look_around()

    else:
        print("That's not a place you can visit.")


def leave_building():
    if p.building_local is not None:
        print(f"Leaving {p.building_local.name}")
        p.building_local = None


def buy(words):
    wares = []
    haggle_for = True
    quantity, item_text = parse_inventory_action(words)

    if quantity == 'all' and item_text is None:
        wares = [x for x in p.building_local.wares]
        ware_list = [f"{ware.plural} x {ware.quantity}" for ware in p.building_local.wares]
        price_total = sum([ware.price*ware.quantity for ware in p.building_local.wares])
        print(f"For {comma_separated(ware_list)}, that comes to ${price_total}.")

    else:
        for ware in p.building_local.wares:

            if remove_little_words(item_text) in ware.name or remove_little_words(item_text) in ware.plural:
                wares = [ware]
                if quantity == "all":
                    quantity = ware.quantity

                if quantity > ware.quantity:
                    print(f"Sorry, we only have {ware.quantity} for sale.")
                    haggle_for = False
                else:
                    print(f"For {ware.plural} x {quantity}, that comes to ${ware.price*quantity}.")
                break
        else:
            print("I can't figure out what you want.")
            haggle_for = False

    if haggle_for is True:
        price_offered = input("Make me an offer:")
        try:
            price_offered = int(price_offered.strip(" "))
            haggle(wares, quantity, price_offered)
        except ValueError:
            print("I was hoping for a number, sorry.")
        except TypeError:
            print("I was hoping for a number, sorry.")


def haggle(items, quantity, price_offered):
    if price_offered > p.money:
        print("Sorry you don't have enough cash to make that offer. Try getting a job.")
        return

    if quantity == 'all':
        price = sum([item.price * item.quantity for item in items])
    else:
        price = sum([item.price for item in items]) * quantity

    if price <= price_offered <= p.money:
        buy_items(items, quantity, price_offered)
        print("Purchase complete")

    elif price > price_offered > 0:
        if odds(price-price_offered) is True:
            print("Ok, sounds like a deal.")
            buy_items(items, quantity, price_offered)
        else:
            print("Sorry, I can't sell for that price.")
    else:
        print("Sorry, I can't sell for that price")


def buy_items(items, quantity, cost):
    for item in items:
        q = item.quantity if quantity == 'all' else quantity
        add_item_to_inventory(item, q)
        if q == item.quantity:
            p.building_local.wares.remove(item)
        else:
            item.quantity -= q
    p.money -= cost


def talk(words):
    """
    ask for a quest
    ask the squirrel for a quest
    say hi to the squirrel
    talk to the squirrel
    """

    mobs = the_map[p.location].mobs if p.building_local is None else p.building_local.mobs

    specific_mob = find_specifics(words, mobs)

    if not specific_mob:
        print("Don't know who to talk to.")
    else:
        specific_mob = specific_mob[0]
        single_mob = remove_little_words(specific_mob.name)
        non_responses = [f"The {single_mob} just looks at you.",
                         f"The {single_mob} doesn't respond.",
                         f"The {single_mob} might not speak english.",
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

        if "quest" in words:
            specific_mob.generate_quest()
            if specific_mob.quest is None:
                print(no_quest_responses[random.randint(0, len(no_quest_responses)-1)])

            else:
                print(yes_quest_responses[random.randint(0, len(yes_quest_responses)-1)])
                print(specific_mob.quest[2])
                if input("Do you accept the quest? yes/no:").lower() == "yes":
                    p.quest = (specific_mob, p.location)

        else:
            print(non_responses[random.randint(0, len(non_responses)-1)])


def turn_in_quest():
    if p.quest is None:
        print("You don't have a quest.")
    else:
        mob_name = remove_little_words(p.quest[0].name)
        mob = p.quest[0]
        if p.quest[1] != p.location:
            print(f"The {mob_name} who gave you your quest is not here. You need to go to {p.quest[1]}.")
        else:
            item = mob.quest[0]
            quantity = mob.quest[1]
            for i in p.inventory:
                if i.name == item.name:
                    if i.quantity >= quantity:
                        print(f"You have enough {item.plural} the {mob_name} requested.")
                        i.quantity -= quantity

                        add_item_to_inventory(i, quantity, mob)

                        skill = mob.skills[random.randint(0, len(mob.skills)-1)]
                        percentage = random.randint(1, 100)
                        print(f"In exchange, the {mob_name} teaches you {skill}. You gain {percentage}% mastery.")
                        try:
                            p.skills[skill] += percentage
                        except KeyError:
                            p.skills[skill] = percentage
                        p.quest = None
                    else:
                        # TODO you have to un-equip the thing to turn in if you are wielding it
                        # TODO turning in the same quest twice doesn't seem to work if you have the item
                        print(f"You don't have enough {item.plural}. The {mob_name} requested {quantity}, "
                              f"and you have {i.quantity}.")
                    break
            else:
                print(f"You don't have any {item.plural}. You need {quantity}.")


def attack(mob_a, mob_b):
    """
    mob a uses equipped weapon, finds damage based on weapon rating, subtracts it from p.health
    (no weapon = punching, kicking, etc for '0' rating)
    """
    weapon_usefulness = {0: (0, 10),
                         1: (10, 15),
                         2: (15, 25),
                         3: (25, 32),
                         4: (32, 50),
                         5: (50, 60)}

    w = mob_a.equipped_weapon
    try:
        usefulness = weapon_usefulness[w.weapon_rating]
        damage = random.randint(usefulness[0], usefulness[1])
    except (AttributeError, KeyError):
        damage = random.randint(weapon_usefulness[0][0], weapon_usefulness[0][1])

    # TODO this needs capitalized too
    mob_b.health -= damage
    print(f"{mob_a.name} inflicted {damage} damage to {mob_b.name}. {mob_b.name} has {mob_b.health} health left.")


def throw(mob_a, mob_b):
    """
    While you can toss higher level weapons, it doesn't do as much damage as weilding them would
    """
    # TODO only throw equipped weapons??
    weapon_usefulness = {0: (0, 20),
                         1: (10, 30),
                         2: (20, 40),
                         3: (10, 25),
                         4: (5, 15),
                         5: (0, 10)}
    w = mob_a.equipped_weapon
    try:
        usefulness = weapon_usefulness[w.weapon_rating]
        damage = random.randint(usefulness[0], usefulness[1])
    except (AttributeError, KeyError):
        damage = random.randint(weapon_usefulness[0][0], weapon_usefulness[0][1])

    # TODO this needs capitalized too
    mob_b.health -= damage
    w.quantity -= 1
    add_dropped_item_to_map(w, 1)
    print(f"{mob_a.name} inflicted {damage} damage to {mob_b.name}. {mob_b.name} has {mob_b.health} health left.")
    if w.quantity == 0:
        print(f"You are out of {w.plural}.")
        mob_a.equipped_weapon = None


def battle_help(agro):
    command_list = {"attack": True,
                    "throw": True if p.equipped_weapon else False,
                    "eat <something>": True if [x for x in p.inventory if x.category == "food"] else False,
                    "run away": True,
                    "leave": True if agro is False else False,
                    "inventory": True,
                    "equip": True if p.inventory else False,
                    "status": True
    }
    for command, status in command_list.items():
        if status:
            print(command)


def battle_manager(words, mobs, aggressing):
    """battle command manager"""
    words = words.lower().split(" ")
    if words[0] == "help":
        battle_help(aggressing)
        battle_manager(input(), mobs, aggressing)
    elif words[0] == "attack":
        for mob in mobs:
            attack(p, mob)
        return True
    elif words[0] == "throw":
        if len(mobs) == 0:
            mob = mobs[0]
        else:
            mob = find_specifics(remove_little_words(' '.join(words)), mobs)
            if not mob:
                mob = mob[0] if mob else mobs[0]
        throw(p, mob)
        return True
    elif words[0] in ("leave", "exit"):
        if aggressing is False:
            print("The battle is over.")
            return False
        else:
            print("You can't leave the battle. You must fight!")
            return True
    elif words == "run" or "run away" in " ".join(words):
        dirs = ["north", "south", "east", "west"]
        random_dir = dirs[random.randint(0, len(dirs)-1)]
        print(f"You run away in a cowardly panic.")
        change_direction(random_dir)
        return False
    elif words[0] == "equip":
        equip(" ".join(words[1:]))
        return True
    elif words[0] == "eat":
        eat_food(" ".join(words[1:]))
        return True
    elif words[0] == "inventory":
        p.pretty_inventory()
        battle_manager(input(), mobs, aggressing)
    elif words[0] == "status":
        p.status()
        battle_manager(input(), mobs, aggressing)
    else:
        print("You can't do that right now.")
        battle_manager(input(), mobs, aggressing)


def battle(attacking_mobs, aggressing=False):
    # TODO all of this needs colors
    list_of_locals = p.building_local.mobs if p.building_local else the_map[p.location].mobs
    if not attacking_mobs:
        print("Who are you attacking?")
        return
    elif not isinstance(attacking_mobs[0], Mob):
        attacking_mobs = find_specifics(attacking_mobs, list_of_locals)
    if not attacking_mobs:
        print("Can't find anyone to pick a fight with.")
        return
    else:
        m = comma_separated(formatted_items(attacking_mobs))
        print(f"Look out, {m[0].upper()}{m[1:]} {'is' if len(attacking_mobs) == 1 else 'are'} gearing up to fight!")
        weapons = []
        for n in attacking_mobs:
            w = n.equipped_weapon
            if n.equipped_weapon is not None:
                mob_id = the_name(n.name)

                weapons.append(f"{mob_id} is wielding {w.name if w.quantity == 1 else w.plural}")
        # TODO this needs capitalized eventually
        if weapons:
            print(f"{comma_separated(weapons)}.")
    attacking = True
    while attacking is True:
        if aggressing is False:
            for m in attacking_mobs:
                attack(m, p)

        if p.health > 0:
            attacking = battle_manager(input(), attacking_mobs, aggressing)

        mob_health = []
        for mob in attacking_mobs:
            mob_id = the_name(mob.name)
            if mob.health <= 0:
                s = f" You add {comma_separated(formatted_items(mob.inventory))} to your " \
                    f"inventory." if mob.inventory else ''
                print(f"You killed {mob_id}.{s}")
                for i in mob.inventory:
                    add_item_to_inventory(i, i.quantity)
                list_of_locals.remove(mob)
            else:
                mob_health.append(f"{mob_id} has {mob.health}")
            if 0 < mob.health <= 50 and aggressing is False:
                print(f"{mob_id} decided the fight's not worth it and has bowed out.")
                attacking = False
        attacking_mobs = [m for m in attacking_mobs if m.health > 0]
        if not attacking_mobs:
            print("Everyone attacking you is now dead. Carry on.")
            attacking = False
        if aggressing is True and attacking is True:
            for m in attacking_mobs:
                attack(m, p)
        if p.health <= 0:
            print("You died. The end.")
            attacking = False


def equip(words):
    if p.equipped_weapon is not None:
        i = p.equipped_weapon
        p.equipped_weapon = None
        add_item_to_inventory(i, i.quantity)
    w = find_specifics(words, p.inventory)
    if w:
        p.equipped_weapon = w[0]
        p.inventory.remove(w[0])
        # TODO standardize singular / plural nonsense
        print(f"Equipped {w[0].name if w[0].quantity == 1 else w[0].plural}")
    else:
        print(f"Can't find {words} in your inventory.")
