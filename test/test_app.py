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
        mob = Mob(name="Bob", p=a.player, plural="Bobs", rarity="common")
        mob.inventory = []
        test_item = Item("a stick", quantity=5, plural="sticks")
        a.add_item_to_inventory(test_item, 1, mob)
        assert len(mob.inventory) == 1
        assert mob.inventory[0].name == "a stick"
        assert mob.inventory[0].quantity == 1

    def test_add_existing_item_to_inventory(self):
        mob = Mob(name="Bob", p=a.player, plural="Bobs", rarity="common")
        mob.inventory = [Item("a hat", quantity=1, plural="hats")]
        test_item = Item("a hat", quantity=5, plural="hats")
        a.add_item_to_inventory(test_item, 1, mob)
        assert len(mob.inventory) == 1
        assert mob.inventory[0].name == "a hat"
        assert mob.inventory[0].quantity == 2

    def test_add_item_to_equipped_weapon_stack(self):
        mob = Mob(name="Bob", p=a.player, plural="Bobs", rarity="common")
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
        mobs.append(Mob(name=k, p=a.player, **v))

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
        all_mobs = find_specifics('all', self.mobs)
        assert all_mobs == self.mobs

    def test_misspelled_specifics(self):
        m = find_specifics('abcdefg', self.mobs)
        assert not m

    def test_capitalization_specific(self):
        squirrel = find_specifics('SQUIRREL', self.mobs)
        assert len(squirrel) == 1
        assert squirrel[0].name == 'a squirrel'

    def test_find_specific_job(self):
        cashier = Job('cashier', location=a.player.location, salary=10)
        driver = Job('truck driver', location=a.player.location, salary=20)
        jobs = [cashier, driver]
        assert a.find_specific_job('driver', jobs) == driver

    def test_find_specifics_returns_one_item_for_two_word_items(self):
        pie = Item('an apple pie', plural='apple pies', quantity=7, rarity='uncommon')
        assert len(find_specifics("apple pie", [pie])) == 1

    def test_find_specifics_with_none(self):
        pie = Item('an apple pie', plural='apple pies', quantity=7, rarity='uncommon')
        assert len(find_specifics(None, [pie])) == 1

    def test_find_specifics_with_everything(self):
        pie = Item('an apple pie', plural='apple pies', quantity=7, rarity='uncommon')
        assert len(find_specifics("everything", [pie])) == 1


class TestEquip(unittest.TestCase):
    def setUp(self):
        self.weapon = Item("weapon x", quantity=10, plural="weapons", weapon_rating=5)
        a.player.inventory = [self.weapon]
        a.player.equipped_weapon = None

    def test_equip(self):
        a.equip('weapon x')
        assert a.player.inventory == []
        assert a.player.equipped_weapon == self.weapon
        assert a.player.equipped_weapon.weapon_rating == 5

    def test_equip_with_already_equipped_weapon(self):
        weapon_b = Item("weapon b", quantity=10, plural="weapons")
        a.player.equipped_weapon = weapon_b
        a.equip('weapon x')
        assert len(a.player.inventory) == 1
        assert a.player.equipped_weapon.name == 'weapon x'
        assert a.player.inventory[0].name == 'weapon b'

    def test_cant_find_to_equip(self):
        weapon = Item("weapon x", quantity=10, plural="weapons")
        a.player.inventory = [weapon]
        a.equip('a dragon')
        assert len(a.player.inventory) == 1
        assert a.player.equipped_weapon is None


class TestJob(unittest.TestCase):
    def setUp(self):
        a.player.job = None
        a.player.money = 0
        a.player.skills = {}
        a.player.square = a.map[(0, 0)]
        a.player.phase = "day"

    def test_job(self):
        job = Job(name="a job", location=a.player.location, skills_learned=['communication'], salary=45)
        a.player.job = job
        a.go_to_work()
        assert a.player.money == 45
        assert a.player.skills['communication'] >= 0

    def test_job_no_skills(self):
        job = Job(name="a job", location=a.player.location, skills_learned=None, salary=45)
        a.player.job = job
        a.go_to_work()
        assert a.player.money == 45
        assert a.player.skills == {}

    def test_no_job(self):
        a.player.job = None
        a.go_to_work()
        assert a.player.money == 0

    def test_job_location(self):
        job = Job(name="a job", location=a.player.location,  skills_learned=None, salary=45)
        job.location = (10, 10)
        a.player.job = job
        a.go_to_work()
        assert a.player.money == 0

    def test_day_job_at_night(self):
        job = Job(name="a job", location=a.player.location,  skills_learned=None, salary=45)
        a.player.job = job
        a.player.phase = "night"
        a.go_to_work()
        assert a.player.money == 0

    def test_night_job_at_day(self):
        job = Job(name="a night job", location=a.player.location, skills_learned=None, salary=45)
        a.player.job = job
        a.go_to_work()
        assert a.player.money == 0

    def test_go_to_work_command(self):
        job = Job(name="a job", location=a.player.location, skills_learned=None, salary=45)
        a.player.job = job
        a.commands_manager('go to work')
        assert a.player.money == 45


class TestApplyForJob(unittest.TestCase):
    def test_apply_for_job(self):
        building = Building(name="office", plural="offices", rarity="common", p=a.player)
        a.player.job = None
        a.player.square.buildings = [building]
        job_opening = Job('drudgeon', a.player.location, skills_needed=['communication'])
        a.player.square.buildings[0].jobs = [job_opening]
        a.player.building_local = a.player.square.buildings[0]
        a.player.skills = {'communication': 100}
        a.apply_for_job("drudgeon")

        assert a.player.job


class TestAttacks(unittest.TestCase):
    def test_throw(self):
        a.player.square.items = []
        weapon = Item("weapon", quantity=10, plural="weapons", weapon_rating=2)
        a.player.equipped_weapon = weapon
        mob_b = Mob("bob", p=a.player, plural="bobs", rarity="common")
        a.throw(a.player, mob_b)
        assert mob_b.health != 100
        assert a.player.square.items != []
        assert a.player.square.items[0].name == "weapon"
        assert a.player.square.items[0].quantity == 1
        assert a.player.equipped_weapon.quantity == 9

    def test_attack(self):
        weapon = Item("weapon", quantity=1, plural="weapons", weapon_rating=5)
        a.player.equipped_weapon = weapon
        mob_b = Mob("bob", p=a.player, plural="bobs", rarity="common")
        mob_b.health = 100
        a.attack(a.player, mob_b)
        assert mob_b.health <= 50


class TestChangeDirection(unittest.TestCase):
    def setUp(self):
        a.player.location = (0, 0)

    def test_go_directions(self):
        directions = {'north': (0, 1),
                      'n': (0, 1),
                      'up': (0, 1),
                      'ne': (1, 1),
                      'sw': (-1, -1)}
        for direction, position in directions.items():
            a.change_direction(direction)
            assert a.player.location == position
            a.player.location = (0, 0)

    def test_go_nowhere(self):
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
            a.player.square.items = [test_item]
            a.commands_manager(words)

            self.assertTrue(len(a.player.inventory) == 1)
            self.assertTrue(a.player.inventory[0].name == "a rock")
            self.assertTrue(a.player.inventory[0].quantity == quantity)
            if quantity == 10:
                self.assertFalse(a.player.square.items)
            else:
                self.assertTrue(a.player.square.items[0].quantity == 10 - quantity)

    def test_pick_up_quantity_directly(self):

        list_of_phrases = {"a rock": 1,
                           "the rocks": 10,
                           "all rocks": 10,
                           "1 rock": 1,
                           "rocks": 10}

        for words, quantity in list_of_phrases.items():

            a.player.inventory = []
            test_item = Item("a rock", quantity=10, plural="rocks")
            a.player.square.items = [test_item]
            a.pick_up(words)

            self.assertTrue(len(a.player.inventory) == 1)
            self.assertTrue(a.player.inventory[0].name == "a rock")
            self.assertTrue(a.player.inventory[0].quantity == quantity)

    def test_nothing_to_pick_up(self):
        a.player.square.items = []
        a.player.inventory = []
        a.pick_up("something")

        assert not a.player.inventory

    def test_cannot_pick_up_non_square_thing(self):
        a.player.square.items = [Item("a rock", quantity=10, plural="rocks")]
        a.player.inventory = []
        a.pick_up("something")

        assert not a.player.inventory
        assert len(a.player.square.items) == 1

    def test_cannot_pick_up_too_many(self):
        a.player.square.items = [Item("a rock", quantity=10, plural="rocks")]
        a.player.inventory = []
        a.pick_up("20 rocks")

        assert not a.player.inventory
        assert len(a.player.square.items) == 1


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
        squirrel = Mob('a squirrel', p=a.player, plural='squirrels', rarity='common')
        hat = Item('a hat', plural='hats', quantity=7, rarity='uncommon')
        assert are_is([squirrel, hat]).split(' ')[0] == "are"
        assert are_is([squirrel]).split(' ')[0] == "is"


class TestQuestCompletion(unittest.TestCase):
    def setUp(self):
        a.player.skills = {}
        a.player.square = a.map[(0, 0)]
        self.mob = Mob("a cat", p=a.player, plural="cats", rarity="common")
        a.player.square.mobs = [self.mob]
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

    def test_mob_is_missing(self):
        a.player.inventory = [Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=3)]
        a.player.square.mobs.remove(self.mob)
        a.turn_in_quest()
        assert not a.player.skills
        assert a.player.inventory[0].quantity == 3
        assert a.player.quest is None


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
    def test_lower_offer(self, _):
        a.haggle([self.item], 1, 5)
        assert a.player.money == 15
        assert len(a.player.inventory) == 1

    def test_buy_two(self):
        a.haggle([self.item], 2, 20)
        assert a.player.money == 0
        assert a.player.inventory[0].quantity == 2


class TestIrritateTheLocals(unittest.TestCase):
    @mock.patch('app.commands.odds', return_value=True)
    def test_irritated(self, _):
        item = Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=3)
        mob = Mob("a cat", p=a.player, plural="cats", rarity="common")
        a.player.square.mobs = [mob]
        assert a.irritate_the_locals(item) == [mob]

    def test_not_rare_item(self):
        item = Item("a teapot", rarity="uncommon", plural="teapots", quantity=1)
        mob = Mob("a cat", p=a.player, plural="cats", rarity="common")
        a.player.square.mobs = [mob]
        assert a.irritate_the_locals(item) is False

    @mock.patch('app.commands.odds', return_value=True)
    def test_large_mob(self, _):
        item = Item("an emerald necklace", rarity="super rare", plural="necklaces", quantity=3)
        mob_a = Mob("a cat", p=a.player, plural="cats", rarity="common")
        mob_b = Mob("a sheep", p=a.player, plural="sheep", rarity="common")
        mob_c = Mob("a bat", p=a.player, plural="bats", rarity="common")
        a.player.square.mobs = [mob_a, mob_b, mob_c]
        assert len(a.irritate_the_locals(item)) == 3


class TestVisitBuildings(unittest.TestCase):
    def setUp(self):
        self.house = Building('a house', p=a.player, plural='houses')
        self.office = Building('an office', p=a.player, plural='offices', ware_list=None)
        a.player.square.buildings = [self.house, self.office]
        a.player.building_local = None
        a.player.phase = "day"

    @mock.patch('app.commands.odds', return_value=True)
    def test_visit_house(self, _):
        a.interact_with_building('house')
        assert a.player.building_local == self.house

    @mock.patch('app.commands.odds', return_value=True)
    def test_visit_house_at_night(self, _):
        a.player.phase = "night"
        a.interact_with_building('house')
        assert a.player.building_local is None

    @mock.patch('app.commands.odds', return_value=False)
    def test_kicked_out_of_house(self, _):
        a.interact_with_building('house')
        assert a.player.building_local is None

    @mock.patch('app.commands.odds', return_value=True)
    def test_visit_office(self, _):
        a.interact_with_building('office')
        assert a.player.building_local == self.office

    @mock.patch('app.commands.odds', return_value=False)
    def test_office_closed(self, _):
        a.interact_with_building('office')
        assert a.player.building_local is None


class TestPlayer(unittest.TestCase):
    def test_phase_change(self):
        a.player.phase = "day"
        a.player.phase_change(a.map)
        assert a.player.phase == "night"
        a.player.phase_change(a.map)
        assert a.player.phase == "day"

    @mock.patch('app.common_functions.odds', return_value=True)
    @mock.patch('app.main_classes.dropper', return_value=1)
    def test_phase_change_generates_new_mobs(self, dropper, odds):
        mob = Mob(name="Bob", p=a.player, plural="Bobs", rarity="common")
        a.player.square.mobs = [mob]
        a.player.phase = "night"
        a.player.phase_change(a.map)
        assert len(a.player.square.mobs) > 1

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
        a.player.square = a.map[(0, 0)]
        a.player.health = 100
        a.player.job = None
        a.player.quest = None
        s = "Currently, you have 100 health.\nYou are located on map coordinates (0, 0), which " \
            f"is {a.player.square.square_type}.\nYou don't have any skills.\nYou have nothing in your inventory." \
            f"\nYou have $0 in your wallet.\nYou do not have a job, and you are not contributing to society."

        assert a.player.status(a.player) == s

    def test_status_with_quest(self):
        a.player.building_local = None
        a.player.equipped_weapon = None
        a.player.inventory = []
        a.player.money = 0
        a.player.skills = {}
        a.player.location = (0, 0)
        a.player.square = a.map[(0, 0)]
        a.player.health = 100
        a.player.job = None
        a.player.quest = True

        assert 'quest' in a.player.status(a.player)


class TestTalk(unittest.TestCase):
    def setUp(self):
        self.mob = Mob("a cat", p=a.player, plural="cats", rarity="common")
        self.mob.irritation_level = 0
        a.player.square.mobs = [self.mob]
        a.player.greeting_count = 0

    @mock.patch('app.commands.odds', return_value=False)
    def test_say_hello_increases_player_greeting_count(self, _):
        a.talk('say hello to the cat')
        assert a.player.greeting_count == 1

    @mock.patch('app.commands.odds', return_value=False)
    def test_talking_with_only_mob_on_square(self, _):
        a.talk('say hello')
        assert self.mob.irritation_level == 1
        assert a.player.greeting_count == 1

    @mock.patch('app.commands.odds', return_value=False)
    def test_outgoing_talking(self, _):
        a.player.greeting_count = 14
        a.player.skills = {}
        a.talk('say hello')
        assert self.mob.irritation_level == 1
        assert a.player.greeting_count == 15
        assert a.player.skills['communication']


class TestSortTheDead(unittest.TestCase):
    def setUp(self):
        self.mob_a = Mob("a cat", p=a.player, plural="cats", rarity="common")
        self.mob_b = Mob("a man", p=a.player, plural="men", rarity="common")
        self.mob_a.inventory, self.mob_b.inventory = [], []
        a.player.skills = {}
        self.roster = [self.mob_a, self.mob_b]
        self.list_of_mobs = [self.mob_a, self.mob_b]

    def test_nobody_is_dead(self):
        mobs = a.sort_the_dead(self.list_of_mobs, self.roster)
        assert len(self.roster) == 2
        assert len(mobs) == 2

    def test_everyone_is_dead(self):
        self.mob_a.health = 0
        self.mob_b.health = 0
        mobs = a.sort_the_dead(self.list_of_mobs, self.roster)
        assert not self.roster
        assert not mobs

    def test_hitlist_guy_is_dead(self):
        a.player.hit_list = ['a man']
        a.player.money = 0
        self.mob_b.health = 0
        a.sort_the_dead(self.list_of_mobs, self.roster)
        assert a.player.money >= 100
        assert a.player.hit_list == []

    def test_inventory_is_added_to_player(self):
        weapon = Item("weapon", quantity=10, plural="weapons", weapon_rating=2)
        self.mob_a.equipped_weapon = weapon
        self.mob_a.health = 0
        a.player.inventory = []
        a.sort_the_dead(self.list_of_mobs, self.roster)
        assert a.player.inventory[0].name == "weapon"

    @mock.patch('app.commands.odds', return_value=True)
    def test_strength_increase(self, _):
        self.mob_a.health = 0
        self.mob_b.health = 0
        a.sort_the_dead(self.list_of_mobs, self.roster)
        assert a.player.skills['strength'] == 4

    def test_self_loathing_increase(self):
        a.player.body_count = 4
        self.mob_a.health = 0
        a.sort_the_dead(self.list_of_mobs, self.roster)
        assert a.player.skills['self loathing'] >= 2


class TestDropper(unittest.TestCase):
    @mock.patch('app.main_classes.dropper', return_value=25)
    def test_drop_with_limit(self, _):
        list_of_mobs = drop_mob(wild_mobs['master'], a.player, limit=20)
        assert len(list_of_mobs) == 20
