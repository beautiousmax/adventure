import time

from termcolor import colored

from app.commands import commands_manager, look_around
from app.main_classes import p


def game_loop():
    """Loop that accepts player commands while player is alive"""
    cycle_start = time.time()
    while p.health > 0 and time.time() - cycle_start < 80:
        commands_manager(input())
    else:
        if p.health > 0:
            p.phase_change()
            print(colored(f"It is now {p.phase}time.", "blue"))
            game_loop()


p.name = input("Welcome to the world, adventurer! What name would you like to be "
               "known as in this land? \n")

print(f"Nice to meet you, {p.name}!\nUse commands to interact with your world. At any time, type 'help' to see all "
      f"available commands.\nHere is your current status: \n")

print(p.status())
print()
look_around()
game_loop()


# next version ideas

# night and day
# you can only work in the day time
# inventory limits, square items and wares update at sunup and sundown
# loose a bit of health if you don't sleep at night
# possibility of highway robbery when travelling
# sell inventory items for money
# non-inventory based quests
# mini games to earn money
# have the interview process include drug testing - screen for mushrooms, magic pills, etc
# jobs provide health insurance, at death - it will cost x dollars to revive you
# multiplayer
# hospital doctors can heal you (but you need health insurance probably)
# adopt animals
# have multiple choice conversations with mobs, trade items, etc
# map items evolve over time as player levels up
# home base on spawn to store stuff
# armor to not die as fast
# magic spells
