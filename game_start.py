import time
import os
from pathlib import Path
import traceback

from termcolor import colored

from app.commands import Adventure


name = input("Welcome to the world, adventurer! What name would you like to be "
             "known as in this land? \n")

adventure = Adventure(name)

print(f"Nice to meet you, {name}!\nUse commands to interact with your world. At any time, type 'help' to see all "
      f"available commands.\nHere is your current status: \n")

print(adventure.player.status())
print()
adventure.look_around()

while adventure.player.health > 0:
    cycle_start = time.time()
    while adventure.player.health > 0 and time.time() - cycle_start < 80:
        try:
            adventure.commands_manager(input())
        except EOFError:
            pass
        except Exception as err:
            print(colored(f"Holy moly, you came across a huge issues!", 'red'))
            with open(Path(os.path.abspath(os.path.dirname(__file__)), 'errors.log'), 'a', encoding='utf-8') as err_log:
                err_log.write(traceback.format_exc())
                err_log.write("\n\n")
            print('We wrote the issue to "errors.log", I will try to keep going, but I am unsure if it will work')

        if adventure.player.health <= 0:
            break
    else:
        if adventure.player.health > 0:
            adventure.player.phase_change(adventure.map)
            print(colored(f"It is now {adventure.player.phase}time.", "blue"))


# next version ideas

# inventory limits
# loose a bit of health if you don't sleep at night
# possibility of highway robbery when travelling
# sell inventory items for money
# mini games to earn money
# have the interview process include drug testing - screen for mushrooms, magic pills, etc
# multiplayer
# hospital doctors can heal you (but you need health insurance probably)
# adopt animals
# have multiple choice conversations with mobs, trade items, etc
# map items evolve over time as player levels up
# home base on spawn to store stuff
# armor to not die as fast
# magic spells


# win the game
# kill the evil volcano base / castle uber boss, become king / evil overlord
# achievements
# win the game without running away from any battles
# kill x mobs
# intelligence over 300%
# perform 3 assassinations
# eat x food items
# talk to x mobs
