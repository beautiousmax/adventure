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

p.status()
print()
look_around()
game_loop()


# things I want to add

# inventory limits
# word wrap?
# travel - in a car, on foot, swim, boat
# non-inventory based quests
# mini games to earn money
# add time dimension - takes x seconds to travel, night / day
# have the interview process include drug testing - screen for mushrooms, magic pills, etc
# multiplayer
# steal wares, have cops chase you - criminal record that prevents you from getting certain jobs
# set stuff on fire
