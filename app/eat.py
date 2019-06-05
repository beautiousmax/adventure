import random

from app.common_functions import find_specifics, parse_inventory_action


class Eat:
    def __init__(self, adventure, raw_words):
        self.adventure = adventure
        self.raw_words = raw_words
        self.list_of_food_objects_to_eat = self.determine_food_and_quantity()

    def determine_food_and_quantity(self):
        words = self.raw_words.replace(',', '')
        quantity, item_text = parse_inventory_action(words)
        if quantity is None or quantity == 'all' and item_text is None:
            return [(x, x.quantity) for x in self.adventure.player.inventory if x.catagory == 'food']

        specific_items = find_specifics(item_text, self.adventure.player.inventory)
        if not specific_items:
            print("Can't figure out what you want to eat.")
            return []
        else:
            food = []
            for f in specific_items:
                if f.category == 'food':
                    q = f.quantity if quantity is None or quantity is 'all'
                    if q > f.quantity:
                        print(f"Can't eat that many {f.plural}")
                        q = f.quantity
                    food.append((f, f.quantity if quantity is None or quantity is 'all' else quantity))

    def eat_foods(self):
        for food, quantity in self.list_of_food_objects_to_eat:
            if self.adventure.player.health < 100:
                for _ in range(0, quantity):
                    # remove quantity from self.adventure.player.inventory
                    # print "Regenerated {} health by eating {food.name}
                    pass
            else:
                print("You have 100% health, no need to eat anything!")
                break

    def determine_restorative_properties(self, food_item):
        if food_item.name == 'a magic pill':
            return 150 - self.adventure.health
        else:
            return random.randint(0, 100 - self.adventure.health)
        # if food_item is bought, it should do better at healing you than wild food
        # unless it is a beverage
        # in which case, coffee increases travel speed slightly?
        # whiskey makes you slower
        pass
