import random

from termcolor import colored

from app.common_functions import find_specifics, parse_inventory_action
from app.load_data import buildings


class Eat:
    def __init__(self, adventure, raw_words):
        self.adventure = adventure
        self.raw_words = raw_words
        self.list_of_food_objects_to_eat = self.determine_food_and_quantity()

    def determine_food_and_quantity(self):
        words = self.raw_words.replace(',', '')
        quantity, item_text = parse_inventory_action(words)
        if quantity is None or quantity == 'all' and item_text is None:
            return [(x, x.quantity) for x in self.adventure.player.inventory if x.category == 'food']

        specific_items = find_specifics(item_text, self.adventure.player.inventory)
        if not specific_items:
            print("Can't figure out what you want to eat.")
            return []
        else:
            food = []
            for f in specific_items:
                if f.category == 'food':
                    q = f.quantity if quantity is None or quantity is 'all' else quantity
                    if q > f.quantity:
                        print(f"Can't eat that many {f.plural}.")
                        q = f.quantity
                    food.append((f, q))
            return food

    def eat_foods(self):
        for food, quantity in self.list_of_food_objects_to_eat:
            if self.adventure.player.health < 100:
                for _ in range(0, quantity):
                    if self.adventure.player.health < 100:
                        self.adventure.player.food_count += 1
                        if self.adventure.player.food_count == 500:
                            print("Congratulations, you have earned the Vigorous Snacker achievement.")
                        for i in self.adventure.player.inventory:
                            if i.name == food.name:
                                i.quantity -= 1
                        regenerate = self.determine_restorative_properties(food)
                        self.adventure.player.health += regenerate
                        print(f"Regenerated {regenerate} health by eating {food.name}. "
                              f"You now have {colored(self.adventure.player.health, 'yellow')}% health.")
                    else:
                        print("You have perfect health, no need to eat!")
                        self.adventure.player.clean_up_inventory()
                        return
        self.adventure.player.clean_up_inventory()

    def determine_restorative_properties(self, food_item):
        food_wares = []
        for biome, building in buildings.items():
            for b, attributes in building.items():
                if attributes.get('ware_list'):
                    for k in attributes['ware_list']:
                        food_wares.append(k)

        if food_item.name == 'a magic pill':
            return 150 - self.adventure.player.health
        elif food_item.name in food_wares:
            if food_item.name == "cup of coffee":
                self.adventure.player.speed_bonus = True
            if self.adventure.player.health > 80:
                return 100 - self.adventure.player.health
            else:
                return random.randint(20, 100 - self.adventure.player.health)
        else:
            return random.randint(1, 100 - self.adventure.player.health)
