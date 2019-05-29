import unittest
from unittest import mock

from app.commands import Adventure
from app.common_functions import *
from app.main_classes import *
from data.text import wild_mobs


a = Adventure('player')


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
        mob = Mob(name="Bob", the_map=a.map, p=a.player, plural="Bobs", rarity="common")
        mob.inventory = []
        test_item = Item("a stick", quantity=5, plural="sticks")
        a.add_item_to_inventory(test_item, 1, mob)
        assert len(mob.inventory) == 1
        assert mob.inventory[0].name == "a stick"
        assert mob.inventory[0].quantity == 1

    def test_add_existing_item_to_inventory(self):
        mob = Mob(name="Bob", the_map=a.map, p=a.player, plural="Bobs", rarity="common")
        mob.inventory = [Item("a hat", quantity=1, plural="hats")]
        test_item = Item("a hat", quantity=5, plural="hats")
        a.add_item_to_inventory(test_item, 1, mob)
        assert len(mob.inventory) == 1
        assert mob.inventory[0].name == "a hat"
        assert mob.inventory[0].quantity == 2

    def test_add_item_to_equipped_weapon_stack(self):
        mob = Mob(name="Bob", the_map=a.map, p=a.player, plural="Bobs", rarity="common")
        mob.inventory = []
        mob.equipped_weapon = Item("a stick", quantity=1, plural="sticks")
        test_item = Item("a stick", quantity=5, plural="sticks")
        a.add_item_to_inventory(test_item, 1, mob)
        assert len(mob.inventory) == 0
        assert mob.equipped_weapon.quantity == 2


class TestEat(unittest.TestCase):
    def test_eat_a_bagel(self):
        food = Item("a bagel", quantity=10, plural="bagels", category="food")
        a.player.inventory = [food]
        a.eat_food("a bagel")
        self.assertTrue(len(a.player.inventory) == 1)
        self.assertTrue(a.player.inventory[0].quantity == 9)

    def test_eating_error(self):
        food = Item("a bagel", quantity=10, plural="bagels", category="food")
        a.player.inventory = [food]
        self.assertTrue(a.player.inventory == [food])
        a.eat_food("")
        self.assertTrue(a.player.inventory[0].quantity == 10)

    def test_eating_too_many(self):
        food = Item("a bagel", quantity=10, plural="bagels", category="food")
        a.player.inventory = [food]
        self.assertTrue(a.player.inventory == [food])
        a.eat_food("12 bagels")
        self.assertTrue(a.player.inventory[0].quantity == 10)

    def test_magic_pill(self):
        a.player.health = 50
        food = Item("a magic pill", quantity=1, plural="magic pills", category="food")
        a.player.inventory = [food]
        a.eat_food("a magic pill")
        self.assertTrue(a.player.health == 100)


class TestSpecifics(unittest.TestCase):
    mobs = []
    for k, v in wild_mobs["master"].items():
        mobs.append(Mob(name=k, the_map=a.map, p=a.player, **v))

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
        cashier = Job('cashier', p=a.player, salary=10)
        driver = Job('truck driver', p=a.player, salary=20)
        jobs = [cashier, driver]
        assert a.find_specific_job('driver', jobs) == driver


class TestEquip(unittest.TestCase):
    def test_equip(self):
        weapon = Item("weapon", quantity=10, plural="weapons", weapon_rating=5)
        a.player.inventory = [weapon]
        a.equip('weapon')
        assert a.player.inventory == []
        assert a.player.equipped_weapon == weapon
        assert a.player.equipped_weapon.weapon_rating == 5

    def test_equip_with_already_equipped_weapon(self):
        weapon_a = Item("weapon a", quantity=10, plural="weapons")
        a.player.inventory = [weapon_a]
        weapon_b = Item("weapon b", quantity=10, plural="weapons")
        a.player.equipped_weapon = weapon_b
        a.equip('weapon a')
        assert len(a.player.inventory) == 1
        assert a.player.equipped_weapon.name == 'weapon a'
        assert a.player.inventory[0].name == 'weapon b'

    def test_cant_find_to_equip(self):
        a.player.equipped_weapon = None
        weapon = Item("weapon a", quantity=10, plural="weapons")
        a.player.inventory = [weapon]
        a.equip('a dragon')
        assert len(a.player.inventory) == 1
        assert a.player.equipped_weapon is None


class TestJob(unittest.TestCase):
    def setUp(self):
        a.player.job = None
        a.player.money = 0
        a.player.skills = {}
        a.player.location = (0, 0)
        a.player.phase = "day"

    def test_job(self):
        job = Job(name="a job", p=a.player, skills_learned=['communication'], salary=45)
        a.player.job = job
        a.go_to_work()
        assert a.player.money == 45
        assert a.player.skills['communication'] >= 0

    def test_job_no_skills(self):
        job = Job(name="a job", p=a.player, skills_learned=None, salary=45)
        a.player.job = job
        a.go_to_work()
        assert a.player.money == 45
        assert a.player.skills == {}

    def test_no_job(self):
        a.player.job = None
        a.go_to_work()
        assert a.player.money == 0

    def test_job_location(self):
        job = Job(name="a job", p=a.player,  skills_learned=None, salary=45)
        job.location = (10, 10)
        a.player.job = job
        a.go_to_work()
        assert a.player.money == 0

    def test_day_job_at_night(self):
        job = Job(name="a job", p=a.player,  skills_learned=None, salary=45)
        a.player.job = job
        a.player.phase = "night"
        a.go_to_work()
        assert a.player.money == 0

    def test_night_job_at_day(self):
        job = Job(name="a night job", p=a.player,  skills_learned=None, salary=45)
        a.player.job = job
        a.go_to_work()
        assert a.player.money == 0

    def test_go_to_work_command(self):
        job = Job(name="a job", p=a.player,  skills_learned=None, salary=45)
        a.player.job = job
        a.commands_manager('go to work')
        assert a.player.money == 45


class TestAttacks(unittest.TestCase):
    def test_throw(self):
        a.map[a.player.location].items = []
        weapon = Item("weapon", quantity=10, plural="weapons", weapon_rating=2)
        a.player.equipped_weapon = weapon
        mob_b = Mob("bob", the_map=a.map, p=a.player, plural="bobs", rarity="common")
        a.throw(a.player, mob_b)
        assert mob_b.health != 100
        assert a.map[a.player.location].items != []
        assert a.map[a.player.location].items[0].name == "weapon"
        assert a.map[a.player.location].items[0].quantity == 1
        assert a.player.equipped_weapon.quantity == 9

    def test_attack(self):
        weapon = Item("weapon", quantity=1, plural="weapons", weapon_rating=5)
        a.player.equipped_weapon = weapon
        mob_b = Mob("bob", the_map=a.map, p=a.player, plural="bobs", rarity="common")
        mob_b.health = 100
        a.attack(a.player, mob_b)
        assert mob_b.health <= 50


class TestChangeDirection(unittest.TestCase):
    def test_go_directions(self):
        directions = ['north', 'n', 'up']
        for direction in directions:
            a.player.location = (0, 0)
            a.change_direction(direction)
            assert a.player.location == (0, 1)

    def test_go_nowhere(self):
        a.player.location = (0, 0)
        a.change_direction("sideways")
        assert a.player.location == (0, 0)


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

            a.player.inventory = []
            test_item = Item("a rock", quantity=10, plural="rocks")
            a.map[a.player.location].items = [test_item]
            a.commands_manager(words)

            self.assertTrue(len(a.player.inventory) == 1)
            self.assertTrue(a.player.inventory[0].name == "a rock")
            self.assertTrue(a.player.inventory[0].quantity == quantity)
            if quantity == 10:
                self.assertFalse(a.map[a.player.location].items)
            else:
                self.assertTrue(a.map[a.player.location].items[0].quantity == 10 - quantity)

    def test_pick_up_quantity_directly(self):

        list_of_phrases = {"a rock": 1,
                           "the rocks": 10,
                           "all rocks": 10,
                           "1 rock": 1,
                           "rocks": 10}

        for words, quantity in list_of_phrases.items():

            a.player.inventory = []
            test_item = Item("a rock", quantity=10, plural="rocks")
            a.map[a.player.location].items = [test_item]
            a.pick_up(words)

            self.assertTrue(len(a.player.inventory) == 1)
            self.assertTrue(a.player.inventory[0].name == "a rock")
            self.assertTrue(a.player.inventory[0].quantity == quantity)


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

    def test_the_name(self):
        assert the_name('a squirrel named Hobb') == 'Hobb'
        assert the_name('a squirrel') == 'the squirrel'

    def test_are_is(self):
        squirrel = Mob('a squirrel', the_map=a.map, p=a.player, plural='squirrels', rarity='common')
        hat = Item('a hat', plural='hats', quantity=7, rarity='uncommon')
        assert are_is([squirrel, hat]).split(' ')[0] == "are"
        assert are_is([squirrel]).split(' ')[0] == "is"


class TestQuestCompletion(unittest.TestCase):
    def setUp(self):
        a.player.skills = {}
        a.player.location = (0, 0)
        self.mob = Mob("a cat", the_map=a.map, p=a.player, plural="cats", rarity="common")
        self.mob.inventory = []
        quest_item = Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=3)
        self.mob.quest = quest_item, 3, "quest description string."
        self.mob.skills = ['patience']
        a.player.quest = self.mob, a.player.location

    def test_not_enough_items(self):
        a.player.inventory = [Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=1)]
        a.turn_in_quest()
        assert not a.player.skills
        assert a.player.inventory[0].quantity == 1
        assert len(self.mob.inventory) == 0

    def test_not_correct_location(self):
        a.player.inventory = [Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=3)]
        a.player.location = (10, 10)
        a.turn_in_quest()
        assert not a.player.skills
        assert a.player.inventory[0].quantity == 3
        assert len(self.mob.inventory) == 0

    def test_enough_items(self):
        a.player.inventory = [Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=3)]
        a.turn_in_quest()
        assert a.player.inventory == []
        assert len(self.mob.inventory) == 1
        assert self.mob.inventory[0].quantity == 3
        assert a.player.skills['patience'] != 0

    def test_not_correct_items(self):
        a.player.inventory = [Item("a teapot", rarity="uncommon", plural="teapots", quantity=1)]
        a.turn_in_quest()
        assert not a.player.skills
        assert a.player.inventory[0].quantity == 1
        assert len(self.mob.inventory) == 0


class TestHaggle(unittest.TestCase):
    def setUp(self):
        a.player.inventory = []
        a.player.money = 20
        self.item = Item("a cake", plural="cakes", rarity="common", price=10, quantity=3)

    def test_offer_zero(self):
        a.haggle([self.item], 1, 0)
        assert a.player.money == 20
        assert not a.player.inventory

    def test_offer_price(self):
        a.haggle([self.item], 1, 10)
        assert a.player.money == 10
        assert len(a.player.inventory) == 1

    def test_no_cash(self):
        a.player.money = 0
        a.haggle([self.item], 1, 10)
        assert a.player.money == 0
        assert not a.player.inventory

    @mock.patch('app.commands.odds', return_value=True)
    def test_lower_offer(self, odds):
        a.haggle([self.item], 1, 5)
        assert a.player.money == 15
        assert len(a.player.inventory) == 1

    def test_buy_two(self):
        a.haggle([self.item], 2, 20)
        assert a.player.money == 0
        assert a.player.inventory[0].quantity == 2


class TestIrritateTheLocals(unittest.TestCase):
    @mock.patch('app.commands.odds', return_value=True)
    def test_irritated(self, odds):
        item = Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=3)
        mob = Mob("a cat", the_map=a.map, p=a.player, plural="cats", rarity="common")
        a.map[a.player.location].mobs = [mob]
        assert a.irritate_the_locals(item) == [mob]

    def test_not_rare_item(self):
        item = Item("a teapot", rarity="uncommon", plural="teapots", quantity=1)
        mob = Mob("a cat", the_map=a.map, p=a.player, plural="cats", rarity="common")
        a.map[a.player.location].mobs = [mob]
        assert a.irritate_the_locals(item) is False

    @mock.patch('app.commands.odds', return_value=True)
    def test_large_mob(self, odds):
        item = Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=3)
        mob_a = Mob("a cat", the_map=a.map, p=a.player, plural="cats", rarity="common")
        mob_b = Mob("a sheep", the_map=a.map, p=a.player, plural="sheep", rarity="common")
        mob_c = Mob("a bat", the_map=a.map, p=a.player, plural="bats", rarity="common")
        a.map[a.player.location].mobs = [mob_a, mob_b, mob_c]
        assert len(a.irritate_the_locals(item)) == 3


class TestVisitBuildings(unittest.TestCase):
    def setUp(self):
        self.house = Building('a house', the_map=a.map, p=a.player, plural='houses')
        self.office = Building('an office', the_map=a.map, p=a.player, plural='offices', ware_list=None)
        a.map[a.player.location].buildings = [self.house, self.office]
        a.player.building_local = None
        a.player.phase = "day"

    @mock.patch('app.commands.odds', return_value=True)
    def test_visit_house(self, odds):
        a.interact_with_building('house')
        assert a.player.building_local == self.house

    @mock.patch('app.commands.odds', return_value=True)
    def test_visit_house_at_night(self, odds):
        a.player.phase = "night"
        a.interact_with_building('house')
        assert a.player.building_local is None

    @mock.patch('app.commands.odds', return_value=False)
    def test_kicked_out_of_hosue(self, odds):
        a.interact_with_building('house')
        assert a.player.building_local is None

    @mock.patch('app.commands.odds', return_value=True)
    def test_visit_office(self, odds):
        a.interact_with_building('office')
        assert a.player.building_local == self.office

    @mock.patch('app.commands.odds', return_value=False)
    def test_office_closed(self, odds):
        a.interact_with_building('office')
        assert a.player.building_local is None


class TestPlayer(unittest.TestCase):
    def test_phase_change(self):
        a.player.phase = "day"
        a.player.phase_change(a.map, a.player)
        assert a.player.phase == "night"
        a.player.phase_change(a.map, a.player)
        assert a.player.phase == "day"

    def test_inventory(self):
        a.player.equipped_weapon = None
        a.player.inventory = [Item("a rock", quantity=3, plural="rocks", rarity="common")]
        assert a.player.pretty_inventory() == "You have three rocks in your inventory."

    def test_inventory_with_weapon(self):
        a.player.inventory = [Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=3)]
        a.player.equipped_weapon = Item("a rock", quantity=3, plural="rocks", rarity="common")
        assert a.player.pretty_inventory() == "You have three necklaces in your inventory.\nYou are wielding three rocks."

    def test_status(self):
        a.player.building_local = None
        a.player.equipped_weapon = None
        a.player.inventory = []
        a.player.money = 0
        a.player.skills = {}
        a.player.location = (0, 0)
        a.player.health = 100
        a.player.job = None
        a.player.quest = None
        s = "Currently, you have 100 health.\nYou are located on map coordinates (0, 0), which " \
            f"is {a.map[a.player.location].square_type}.\nYou don't have any skills.\nYou have nothing in your inventory." \
            f"\nYou have $0 in your wallet.\nYou do not have a job, and you are not contributing to society."

        assert a.player.status(a.map, a.player) == s

    def test_status_with_quest(self):
        a.player.building_local = None
        a.player.equipped_weapon = None
        a.player.inventory = []
        a.player.money = 0
        a.player.skills = {}
        a.player.location = (0, 0)
        a.player.health = 100
        a.player.job = None
        a.player.quest = True

        assert 'quest' in a.player.status(a.map, a.player)
