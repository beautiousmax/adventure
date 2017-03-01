from main_classes import p
from commands import commands_manager


p.name = input("Welcome to the world, adventurer! What name would you like to be "
               "known as in this land? \n")

print("Nice to meet you, {}!".format(p.name))
print()
print("Use commands to interact with your world. At any time, type 'help' "
      "to see all available commands.")
print("Here is your current status: \n")
p.status()
while p.health > 0:
    commands_manager(input())


# things I want to add
# walk around (or swim in the ocean) to buildings, visit them
    # travel - in a car, on foot, swim, boat
# interact with mobs in buildings, and "wild" mobs
# talk, or start fights
# use weapons, vehicles
# you can lose health in fights
# buy stuff, trade, go on quests, apply for jobs
# player death
# ways to regen health - eat food or magic pills
# mini games to earn money, classic
# add time dimension, takes x seconds to travel, etc, every 'day' at work earn salary
# have the interview process include drug testing - screen for mushrooms, magic pills, etc
# multiplayer
