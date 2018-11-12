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
# non-inventory based quests
# mini games to earn money
# add time dimension - takes x seconds to travel, night / day
# have the interview process include drug testing - screen for mushrooms, magic pills, etc
# multiplayer
# steal wares, have cops chase you - criminal record that prevents you from getting certain jobs
# set stuff on fire
