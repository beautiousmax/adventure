import time

from termcolor import colored

from app.commands import Adventure


name = input("Welcome to the world, adventurer! What name would you like to be "
             "known as in this land? \n")

adventure = Adventure(name)

print(f"Nice to meet you, {name}!\nUse commands to interact with your world. At any time, type 'help' to see all "
      f"available commands.\nHere is your current status: \n")

print(adventure.player.status(adventure.player))
print()
adventure.look_around()

while adventure.player.health > 0:
    cycle_start = time.time()
    while adventure.player.health > 0 and time.time() - cycle_start < 80:
        adventure.commands_manager(input())
        if adventure.player.health <= 0:
            break
    else:
        if adventure.player.health > 0:
            adventure.player.phase_change(adventure.map, adventure.player)
            print(colored(f"It is now {adventure.player.phase}time.", "blue"))


# next version ideas

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
