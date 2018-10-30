from app.main_classes import p
from app.commands import commands_manager, look_around


p.name = input("Welcome to the world, adventurer! What name would you like to be "
               "known as in this land? \n")

print(f"Nice to meet you, {p.name}!")
print()
print("Use commands to interact with your world. At any time, type 'help' "
      "to see all available commands.")
print("Here is your current status: \n")
p.status()
print()
look_around()
while p.health > 0:
    commands_manager(input())


# things I want to add

# inventory limits
# word wrap?
# travel - in a car, on foot, swim, boat
# interact with mobs in buildings, interview for jobs
# be able to turn in quests
# non-inventory based quests
# talk, or start fights
# use weapons
# you can lose health in fights
# player death
# mini games to earn money
# add time dimension - takes x seconds to travel, night / day
# have the interview process include drug testing - screen for mushrooms, magic pills, etc
# multiplayer
# quests - throw away 100 cigarette butts, clean up the city!, etc
# deal with multiple buildings, mobs of the same sort on a square at a time.. maybe unique names?
# steal wares, have cops chase you - criminal record that prevents you from getting certain jobs
