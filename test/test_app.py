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

    def test_find_specific_job(self):
        cashier = Job('cashier', salary=10)
        driver = Job('truck driver', salary=20)
        jobs = [cashier, driver]
        assert find_specific_job('driver', jobs) == driver


class TestEquip(unittest.TestCase):
    def test_equip(self):
        weapon = Item("weapon", quantity=10, plural="weapons", weapon_rating=5)
        p.inventory = [weapon]
        equip('weapon')
        assert p.inventory == []
        assert p.equipped_weapon == weapon
        assert p.equipped_weapon.weapon_rating == 5

    def test_equip_with_already_equipped_weapon(self):
        weapon_a = Item("weapon a", quantity=10, plural="weapons")
        p.inventory = [weapon_a]
        weapon_b = Item("weapon b", quantity=10, plural="weapons")
        p.equipped_weapon = weapon_b
        equip('weapon a')
        assert len(p.inventory) == 1
        assert p.equipped_weapon.name == 'weapon a'
        assert p.inventory[0].name == 'weapon b'

    def test_cant_find_to_equip(self):
        p.equipped_weapon = None
        weapon = Item("weapon a", quantity=10, plural="weapons")
        p.inventory = [weapon]
        equip('a dragon')
        assert len(p.inventory) == 1
        assert p.equipped_weapon is None


class TestJob(unittest.TestCase):
    def setUp(self):
        p.job = None
        p.money = 0
        p.skills = {}
        p.location = (0, 0)
        p.phase = "day"

    def test_job(self):
        job = Job(name="a job", skills_learned=['communication'], salary=45)
        p.job = job
        go_to_work()
        assert p.money == 45
        assert p.skills['communication'] >= 0

    def test_job_no_skills(self):
        job = Job(name="a job", skills_learned=None, salary=45)
        p.job = job
        go_to_work()
        assert p.money == 45
        assert p.skills == {}

    def test_no_job(self):
        p.job = None
        go_to_work()
        assert p.money == 0

    def test_job_location(self):
        job = Job(name="a job", skills_learned=None, salary=45)
        job.location = (10, 10)
        p.job = job
        go_to_work()
        assert p.money == 0

    def test_day_job_at_night(self):
        job = Job(name="a job", skills_learned=None, salary=45)
        p.job = job
        p.phase = "night"
        go_to_work()
        assert p.money == 0

    def test_night_job_at_day(self):
        job = Job(name="a night job", skills_learned=None, salary=45)
        p.job = job
        go_to_work()
        assert p.money == 0

    def test_go_to_work_command(self):
        job = Job(name="a job", skills_learned=None, salary=45)
        p.job = job
        commands_manager('go to work')
        assert p.money == 45


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


class TestQuestCompletion(unittest.TestCase):
    def setUp(self):
        p.skills = {}
        p.location = (0, 0)
        self.mob = Mob("a cat", plural="cats", rarity="common")
        self.mob.inventory = []
        quest_item = Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=3)
        self.mob.quest = quest_item, 3, "quest description string."
        self.mob.skills = ['patience']
        p.quest = self.mob, p.location

    def test_not_enough_items(self):
        p.inventory = [Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=1)]
        turn_in_quest()
        assert not p.skills
        assert p.inventory[0].quantity == 1
        assert len(self.mob.inventory) == 0

    def test_not_correct_location(self):
        p.inventory = [Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=3)]
        p.location = (10, 10)
        turn_in_quest()
        assert not p.skills
        assert p.inventory[0].quantity == 3
        assert len(self.mob.inventory) == 0

    def test_enough_items(self):
        p.inventory = [Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=3)]
        turn_in_quest()
        assert p.inventory == []
        assert len(self.mob.inventory) == 1
        assert self.mob.inventory[0].quantity == 3
        assert p.skills['patience'] != 0

    def test_not_correct_items(self):
        p.inventory = [Item("a teapot", rarity="uncommon", plural="teapots", quantity=1)]
        turn_in_quest()
        assert not p.skills
        assert p.inventory[0].quantity == 1
        assert len(self.mob.inventory) == 0


class TestHaggle(unittest.TestCase):
    def setUp(self):
        p.inventory = []
        p.money = 20
        self.item = Item("a cake", plural="cakes", rarity="common", price=10, quantity=3)

    def test_offer_zero(self):
        haggle([self.item], 1, 0)
        assert p.money == 20
        assert not p.inventory

    def test_offer_price(self):
        haggle([self.item], 1, 10)
        assert p.money == 10
        assert len(p.inventory) == 1

    def test_no_cash(self):
        p.money = 0
        haggle([self.item], 1, 10)
        assert p.money == 0
        assert not p.inventory
