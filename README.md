Adventure
=========

A text-based adventure full of mystery, intrigue, and adventure!

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
| eat \<*num*\>  \<object\>    | Try to ingest something from your inventory | 
| inventory                    | View your inventory |
| status                       | View your health, job info, current quest, etc... |
| visit \<place\>              | Go into a shop, place of worship, workplace or even people's houses |
| equip \<object\>             | Choose your weapon for battle! |
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
| throw    | Toss your equipped item at them | 
| run away | Escape battle with the mean shovel-wielding squirrel |

