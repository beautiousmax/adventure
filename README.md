Adventure
=========

A text-based adventure full of mystery, intrigue, and adventure!

This game takes place in a randomly generated world that you can explore. You 'win' the game by defeating a terrible monster and 
becoming the King of the Realm or Evil Overlord. Until then, you can go on quests to learn skills, apply for jobs and go to work to earn 
some cash, do battle with wood nymphs and homeless men named Susan, or work on your spoon collection. 

> This is a work in progress. Let me know if you have suggestions or feedback!

Requirements
============

This game requires Python 3.6 or above. Don't forget to install the requirements.

```bash
pip install -r requirements.txt
```


Game Play
=========
Start the game by running game_start.py.

```bash
python3 game_start.py
```

Commands
========

All available commands can be viewed anytime by typing "help"

**General** 

| Command                      | Description |
| :--------------------------- | :---------- |
| help                         | View the currently available commands |
| look *around*                | See what is on the current square |
| pick up \<*num*\> \<object\> | Add an object to your inventory, watch out, it may belong to someone! |
| take \<*num*\> \<object\>    | (`pick up` and `take` are interchangeable) |  
| go \<direction\>             | Travel to another square (north, southwest, s, ne, left, etc...) |
| eat \<*num*\>  \<object\>    | Try to ingest something from your inventory to gain health | 
| inventory                    | View your inventory |
| status                       | View your health, job info, current quest, etc... |
| statistics                   | See how many mobs you've killed, food items you've eaten, etc. |
| hit list                     | View the list of mobs you've been commissioned to kill |
| visit \<place\>              | Go into a shop, place of worship, workplace or even people's houses |
| apply *for a* \<job>         | Apply for a job opening  |
| *go to* work                 | Earn some money by working at your job |
| equip \<object\>             | Choose your weapon and armor for battle! |
| battle \<mob\>               | Pick a fight with someone |
| ask \<mob\> *for a* quest    | Bother almost anything for the possibility of a quest |
| turn in quest                | Complete a quest, you must be on the map square you picked it up from  | 
| say hi to \<mob\>            | Try talking to people |
| map                          | Get an overview of nearby explored areas |
| exit                         | Quit the game |
   
\* *Italicized* words are optional

**Battle Commands** 
   
| Command  | Description |
| :------- | :---------- |
| attack   | Hit your opponent(s) to inflict damage! |
| throw    | Toss your equipped item at your opponent | 
| run away | Escape battle with the mean shovel-wielding squirrel |

