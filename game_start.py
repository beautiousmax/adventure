from app.main_classes import p
from app.commands import commands_manager


p.name = input("Welcome to the world, adventurer! What name would you like to be "
               "known as in this land? \n")

print(f"Nice to meet you, {p.name}!")
print()
print("Use commands to interact with your world. At any time, type 'help' "
      "to see all available commands.")
print("Here is your current status: \n")
p.status()
while p.health > 0:
    commands_manager(input())


# things I want to add
# walk around (or swim in the ocean) to buildings in a single square, visit them
    # travel - in a car, on foot, swim, boat
# interact with mobs in buildings, and "wild" mobs
# talk, or start fights
# use weapons, vehicles
# you can lose health in fights
# buy stuff, trade, go on quests, apply for jobs
# player death
# mini games to earn money
# add time dimension, takes x seconds to travel, night / day
# have the interview process include drug testing - screen for mushrooms, magic pills, etc
# multiplayer
# quests - throw away 100 cigarette butts, clean up the city!, etc
# deal with multiple buildings of the same sort on a square at a time.. maybe unique names?
# steal wares, have cops chase you - criminal record that prevents you from getting certain jobs
