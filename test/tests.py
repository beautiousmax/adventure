import unittest
from app.commands import *
from app.main_classes import *
from data.text import wild_mobs


class AdventureTest(unittest.TestCase):

    def test_parse_inventory_action(self):
        quantity, word = parse_inventory_action("a rock")
        self.assertTrue(quantity == 1 and word == "rock")

        quantity, word = parse_inventory_action("some rocks")
        self.assertTrue(quantity == 1 and word == "rocks")

        quantity, word = parse_inventory_action("the rocks")
        self.assertTrue(quantity == "all" and word == "rocks")

        quantity, word = parse_inventory_action("all rocks")
        self.assertTrue(quantity == "all" and word == "rocks")

        quantity, word = parse_inventory_action("1 rock")
        self.assertTrue(quantity == 1 and word == "rock")

        quantity, word = parse_inventory_action("10 rocks")
        self.assertTrue(quantity == 10 and word == "rocks")

        quantity, word = parse_inventory_action("ten rocks")
        self.assertTrue(quantity == 10 and word == "rocks")

        quantity, word = parse_inventory_action("rocks")
        self.assertTrue(quantity == "all" and word == "rocks")

        quantity, word = parse_inventory_action("everything")
        self.assertTrue(quantity == "all" and word is None)

        quantity, word = parse_inventory_action("all")
        self.assertTrue(quantity == "all" and word is None)

        quantity, word = parse_inventory_action("")
        self.assertTrue(quantity is None and word is None)

    def test_pick_up_quantity(self):

        list_of_phrases = {"a rock": 1,
                           "the rocks": 10,
                           "all rocks": 10,
                           "1 rock": 1,
                           "rocks": 10}

        for words, quantity in list_of_phrases.items():

            p.inventory = []
            the_map[p.location].items = []
            test_item = Item("a rock", quantity=10, plural="rocks")
            the_map[p.location].items.append(test_item)
            pick_up(words)

            self.assertTrue(len(p.inventory) > 0)
            self.assertTrue(p.inventory[0].name == "a rock")
            self.assertTrue(p.inventory[0].quantity == quantity)

    def test_eat_a_bagel(self):
        food = Item("a bagel", quantity=10, plural="bagels", type="food")
        p.inventory = [food]
        eat_food("a bagel")

        self.assertTrue(len(p.inventory) == 1)
        self.assertTrue(p.inventory[0].quantity == 9)

    def test_eating_error(self):
        food = Item("a bagel", quantity=10, plural="bagels", type="food")
        p.inventory = [food]
        self.assertTrue(p.inventory == [food])
        eat_food("")

        self.assertTrue(p.inventory[0].quantity == 10)

    def test_eating_too_many(self):
        food = Item("a bagel", quantity=10, plural="bagels", type="food")
        p.inventory = [food]
        self.assertTrue(p.inventory == [food])
        eat_food("12 bagels")

        self.assertTrue(p.inventory[0].quantity == 10)


class TestSpecifics(unittest.TestCase):
    mobs = []
    for k, v in wild_mobs["master"].items():
        mobs.append(Mob(name=k, **v))

    def test_find_specifics_singular(self):
        squirrel = find_specifics('squirrel', self.mobs)
        assert len(squirrel) == 1
        assert squirrel[0].name == 'a squirrel'

    def test_find_specifics_plural(self):
        squirrel = find_specifics('squirrels', self.mobs)
        assert len(squirrel) == 1
        assert squirrel[0].name == 'a squirrel'

    def test_find_specifics_partial(self):
        squirrel = find_specifics('squir', self.mobs)
        assert len(squirrel) == 1
        assert squirrel[0].name == 'a squirrel'

    def test_find_specifics_all(self):
        all = find_specifics('all', self.mobs)
        assert all == self.mobs
