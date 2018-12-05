import unittest

from app.commands import *
from app.main_classes import *
from data.text import wild_mobs


class TestParseInventoryAction(unittest.TestCase):

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

    def test_add_new_item_to_inventory(self):
        mob = Mob(name="Bob", plural="Bobs", rarity="common")
        mob.inventory = []
        test_item = Item("a stick", quantity=5, plural="sticks")
        add_item_to_inventory(test_item, 1, mob)
        assert len(mob.inventory) == 1
        assert mob.inventory[0].name == "a stick"
        assert mob.inventory[0].quantity == 1

    def test_add_existing_item_to_inventory(self):
        mob = Mob(name="Bob", plural="Bobs", rarity="common")
        mob.inventory = [Item("a hat", quantity=1, plural="hats")]
        test_item = Item("a hat", quantity=5, plural="hats")
        add_item_to_inventory(test_item, 1, mob)
        assert len(mob.inventory) == 1
        assert mob.inventory[0].name == "a hat"
        assert mob.inventory[0].quantity == 2

    def test_add_item_to_equipped_weapon_stack(self):
        mob = Mob(name="Bob", plural="Bobs", rarity="common")
        mob.inventory = []
        mob.equipped_weapon = Item("a stick", quantity=1, plural="sticks")
        test_item = Item("a stick", quantity=5, plural="sticks")
        add_item_to_inventory(test_item, 1, mob)
        assert len(mob.inventory) == 0
        assert mob.equipped_weapon.quantity == 2


class TestEat(unittest.TestCase):
    def test_eat_a_bagel(self):
        food = Item("a bagel", quantity=10, plural="bagels", category="food")
        p.inventory = [food]
        eat_food("a bagel")
        self.assertTrue(len(p.inventory) == 1)
        self.assertTrue(p.inventory[0].quantity == 9)

    def test_eating_error(self):
        food = Item("a bagel", quantity=10, plural="bagels", category="food")
        p.inventory = [food]
        self.assertTrue(p.inventory == [food])
        eat_food("")
        self.assertTrue(p.inventory[0].quantity == 10)

    def test_eating_too_many(self):
        food = Item("a bagel", quantity=10, plural="bagels", category="food")
        p.inventory = [food]
        self.assertTrue(p.inventory == [food])
        eat_food("12 bagels")
        self.assertTrue(p.inventory[0].quantity == 10)

    def test_magic_pill(self):
        p.health = 50
        food = Item("a magic pill", quantity=1, plural="magic pills", category="food")
        p.inventory = [food]
        eat_food("a magic pill")
        self.assertTrue(p.health == 100)


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

    def test_misspelled_specifics(self):
        m = find_specifics('abcdefg', self.mobs)
        assert not m

    def test_capitalization_specific(self):
        squirrel = find_specifics('SQUIRREL', self.mobs)
        assert len(squirrel) == 1
        assert squirrel[0].name == 'a squirrel'


class TestEquip(unittest.TestCase):
    def test_equip(self):
        weapon = Item("weapon", quantity=10, plural="weapons", weapon_rating=5)
        p.inventory = [weapon]
        equip('weapon')
        assert p.inventory == []
        assert p.equipped_weapon == weapon
        assert p.equipped_weapon.weapon_rating == 5


class TestJob(unittest.TestCase):

    def test_job(self):
        p.money = 0
        p.skills = {}
        job = Job(name="a job", skills_learned=['communication'], salary=45)
        p.job = job
        go_to_work()
        assert p.money == 45
        assert p.skills['communication'] >= 0

    def test_job_no_skills(self):
        p.money = 0
        p.skills = {}
        job = Job(name="a job", skills_learned=None, salary=45)
        p.job = job
        go_to_work()
        assert p.money == 45
        assert p.skills == {}


class TestAttacks(unittest.TestCase):
    def test_throw(self):
        the_map[p.location].items = []
        weapon = Item("weapon", quantity=10, plural="weapons", weapon_rating=2)
        p.equipped_weapon = weapon
        mob_b = Mob("bob", plural="bobs", rarity="common")
        throw(p, mob_b)
        assert mob_b.health != 100
        assert the_map[p.location].items != []
        assert the_map[p.location].items[0].name == "weapon"
        assert the_map[p.location].items[0].quantity == 1
        assert p.equipped_weapon.quantity == 9

    def test_attack(self):
        weapon = Item("weapon", quantity=1, plural="weapons", weapon_rating=5)
        p.equipped_weapon = weapon
        mob_b = Mob("bob", plural="bobs", rarity="common")
        mob_b.health = 100
        attack(p, mob_b)
        assert mob_b.health <= 50


class TestChangeDirection(unittest.TestCase):
    def test_go_directions(self):
        directions = ['north', 'n', 'up']
        for direction in directions:
            p.location = (0, 0)
            change_direction(direction)
            assert p.location == (0, 1)


class TestPickUpCommand(unittest.TestCase):
    def test_pick_up_quantity_command_manager(self):
        list_of_phrases = {"pick up a rock": 1,
                           "pick up the rocks": 10,
                           "pick up all rocks": 10,
                           "pick up 3 rocks": 3,
                           "pick up three rocks": 3,
                           "pick up rocks": 10,
                           "pick up": 10,
                           "take all": 10,
                           "take the rocks": 10}

        for words, quantity in list_of_phrases.items():

            p.inventory = []
            test_item = Item("a rock", quantity=10, plural="rocks")
            the_map[p.location].items = [test_item]
            commands_manager(words)

            self.assertTrue(len(p.inventory) == 1)
            self.assertTrue(p.inventory[0].name == "a rock")
            self.assertTrue(p.inventory[0].quantity == quantity)
            if quantity == 10:
                self.assertFalse(the_map[p.location].items)
            else:
                self.assertTrue(the_map[p.location].items[0].quantity == 10 - quantity)

    def test_pick_up_quantity_directly(self):

        list_of_phrases = {"a rock": 1,
                           "the rocks": 10,
                           "all rocks": 10,
                           "1 rock": 1,
                           "rocks": 10}

        for words, quantity in list_of_phrases.items():

            p.inventory = []
            test_item = Item("a rock", quantity=10, plural="rocks")
            the_map[p.location].items = [test_item]
            pick_up(words)

            self.assertTrue(len(p.inventory) == 1)
            self.assertTrue(p.inventory[0].name == "a rock")
            self.assertTrue(p.inventory[0].quantity == quantity)


class TestCommonFunctions(unittest.TestCase):
    def test_comma_separated(self):
        list_of_words = ["cat", "dog", "horse"]
        assert comma_separated(list_of_words) == "cat, dog and horse"
        shorter_list = ["cat", "dog"]
        assert comma_separated(shorter_list) == "cat and dog"
        shortest_list = ["cat"]
        assert comma_separated(shortest_list) == "cat"

    def test_add_dicts_together(self):
        dict_a = {"a": "cat", "b": "dog"}
        dict_b = {"c": "horse", "d": "fish"}
        assert add_dicts_together(dict_a, dict_b) == {"a": "cat", "b": "dog", "c": "horse", "d": "fish"}

    def test_remove_little_words(self):
        phrase = "AN APPLE PIE, the fish sticks, this that and the other."
        assert remove_little_words(phrase) == "APPLE PIE, fish sticks, and other."

    def test_odds(self):
        assert odds(1) is True
