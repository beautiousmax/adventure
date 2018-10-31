from app.main_classes import MapSquare, the_map, p
from app.common_functions import formatted_items, comma_separated, parse_inventory_action, odds, remove_little_words, \
    are_is
import random
from reusables.string_manipulation import int_to_words

command_list = {"help": True,
                "look around": True,
                "go <southwest>": True,
                "inventory": True,
                "status": True,
                "pick up <something>": False,
                "eat <something>": False,
                "visit <a building>": False,
                "buy <something>": False}


def commands_manager(words):
    """ Command handler. """
    words = words.lower().split(" ")
    if words[0] == "help":
        if the_map[p.location].items:
            command_list["pick up <something>"] = True
        else:
            command_list["pick up <something>"] = False
        for x in p.inventory:
            if x.category == "food":
                command_list["eat <something>"] = True
                break
        else:
            command_list["eat <something>"] = False

        for command, status in command_list.items():
            if status:
                print(command)

        if the_map[p.location].buildings:
            command_list["visit <a building>"] = True
        else:
            command_list["visit <a building>"] = False

    elif words[0] == "go":
        change_direction(" ".join(words[1:]))

    elif words[0] == "visit":
        interact_with_building(" ".join(words[1:]))

    elif words[0] == "leave" or words[0] == "exit":
        leave_building()

    elif " ".join(words) == "look around" or "look" in words:
        look_around()

    elif " ".join(words) == "inventory":
        print(f"You have {p.formatted_inventory()} in your inventory.")

    elif " ".join(words[0:2]) == "pick up":
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

    elif "turn in" in " ".join(words) and "quest" in words:
        turn_in_quest()

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
    leave_building()
    x = p.location[0]
    y = p.location[1]
    if direction.lower() in ("n", "ne", "nw", "north", "northeast", "northwest"):
        y += 1
    if direction.lower() in ("e", "ne", "se", "east", "northeast", "southeast"):
        x += 1
    if direction.lower() in ("s", "se", "sw", "south", "southeast", "southwest"):
        y -= 1
    if direction.lower() in ("w", "nw", "sw", "west", "northwest", "southwest"):
        x -= 1

    p.location = (x, y)
    if p.location not in the_map.keys():
        the_map[p.location] = MapSquare()
        the_map[p.location].generate_buildings()
        the_map[p.location].generate_mobs()
    print(f"You are now located on map coordinates {p.location}, which is {the_map[p.location].square_type}.")
    the_map[p.location].generate_items()
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
    # TODO generate more items to look at / find after picking up stuff?

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
        if p.building_local.mobs is None and (p.building_local.wares is None or p.building_local.wares == []):
            print("There isn't anything here.")


def pick_up(words):
    quantity, item_text = parse_inventory_action(words)

    if item_text is None:
        for i in the_map[p.location].items:
            add_item_to_inventory(i, i.quantity)
        print(f"Added {comma_separated([x.name for x in the_map[p.location].items])} to your inventory.")
        the_map[p.location].items = []

    else:
        item = None
        for i in the_map[p.location].items:
            if item_text in i.name or item_text in i.plural:
                item = i
                break
        else:
            print(f"Couldn't pick up {item_text}")

        if item:
            if quantity == "all":
                quantity = item.quantity

            if item.quantity >= quantity:
                add_item_to_inventory(item, quantity)
                item.quantity -= quantity
                if item.quantity == 0:
                    the_map[p.location].items.remove(item)
                print(f"Added {item.name if quantity == 1 else item.plural} to your inventory.")
            elif item.quantity < quantity:
                print("Can't pick up that many.")


def add_item_to_inventory(item_to_add, quantity):
    if item_to_add.name in [x.name for x in p.inventory]:
        for x in p.inventory:
            if item_to_add.name == x.name:
                x.quantity += int(quantity)
    else:
        new_item = item_to_add.copy()
        new_item.quantity = quantity
        p.inventory.append(new_item)


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

        if p.health < 100:
            regenerate = random.randint(0, 100-p.health)
            p.health += regenerate
            print(f"Regenerated {regenerate}% health by eating {item_eaten.name}.")

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


def apply_for_job():
    if p.building_local.jobs():

        print(f"Hello! We are looking to hire {p.building_local.jobs} currently.")


def interact_with_building(words):
    for building in the_map[p.location].buildings:
        if remove_little_words(words) in remove_little_words(building.name):
            if building.category == 'building':
                if odds(8) is True:
                    print(f"Too bad, {building.name} is closed right now. Try again later.")
                else:
                    p.building_local = building
                    command_list['visit <a building>'] = False
                    command_list['leave'] = True
                    if p.building_local.wares:
                        command_list['buy <something>'] = True
                    print(f"You are now inside {building.name}.")
                    look_around()

            else:
                if odds(10) is False:
                    print("The occupants of this residence have kicked you out.")
                else:
                    command_list['visit <a building>'] = False
                    command_list['leave'] = True
                    p.building_local = building
                    print("You are now inside a house")
                    look_around()
            break

    else:
        print("That's not a place you can visit.")


def leave_building():
    if p.building_local is not None:
        command_list['visit <a building>'] = True
        command_list['leave'] = False
        command_list['buy <something>'] = False
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
    mobs = the_map[p.location].mobs

    specific_mob = None
    for w in remove_little_words(words).split(' '):
        for m in mobs:
            if w in remove_little_words(m.name).split(' ') or w in m.plural:
                specific_mob = m
                break

    if specific_mob is not None:
        single_mob = remove_little_words(specific_mob.name)
        non_responses = [f"The {single_mob} just looks at you.",
                         f"The {single_mob} doesn't respond.",
                         f"The {single_mob} might not speak english."]

        no_quest_responses = [f"The {single_mob} shakes his head gravely.",
                              # TODO add mob gender
                              f"The {single_mob} says 'No quests today.'"]

        yes_quest_responses = [f"The ground shakes as the {single_mob} roars 'YES, I HAVE A QUEST FOR YOU!'",
                               f"The {single_mob} says 'Yup, I've got a quest for you.'"]

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
        mob = remove_little_words(p.quest[0].name)
        if p.quest[1] != p.location:
            print(f"The {mob} who gave you your quest is not here. You need to go to {p.quest[1]}.")
        else:
            item = p.quest[0].quest[0]
            quantity = p.quest[0].quest[1]
            for i in p.inventory:
                if i.name == item.name:
                    if i.quantity >= quantity:
                        print(f"You have enough {item.plural} the {mob} requested.")
                        i.quantity -= quantity
                        skill = p.quest[0].skills[random.randint(0, len(p.quest[0].skills)-1)]
                        print(f"In exchange, the {mob} teaches you {skill}.")
                        p.skills.append(skill)
                    else:
                        print(f"You don't have enough {item.plural}. The {mob} requested {quantity}, "
                              f"and you have {i.quantity}.")
                    break
            else:
                print(f"You don't have any {item.plural}. You need {quantity}.")
