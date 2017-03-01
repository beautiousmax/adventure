items = {"master": {"a rock": {"rarity": "super common", "plural": "rocks"},
                    "an emerald necklace": {"rarity": "super rare", "plural": "emerald necklaces"},
                    "a red lamborghini": {"rarity": "super rare", "plural": "red lamborhinis", "type": "vehicle"},
                    "some broken glass": {"rarity": "uncommon", "plural": "piles of broken glass"},
                    "a shovel": {"rarity": "uncommon", "plural": "shovels"},
                    "a toothbrush": {"rarity": "uncommon", "plural": "toothbrushes"},
                    "a laptop": {"rarity": "rare", "plural": "laptops"},
                    "a box of kleenex": {"rarity": "rare", "plural": "boxes of kleenex", "flammable": True},
                    "a spool of thread": {"rarity": "rare", "plural": "spools of thread"},
                    "a spoon": {"rarity": "uncommon", "plural": "spoons"},
                    "a teapot": {"rarity": "uncommon", "plural": "teapots"},
                    "an arrowhead": {"rarity": "super rare", "plural": "arrowheads"},
                    "a handful of almonds": {"rarity": "uncommon", "plural": "handfuls of almonds", "type": "food"},
                    "a bagel": {"rarity": "common", "plural": "bagels", "type": "food"},
                    "a car dealership": {"rarity": "rare",
                                                                 "plural": "car dealerships",
                                                                 "mobs": ["shoppers"],
                                                                 "wares": {"white lamborghini": {"rarity": "uncommon",
                                                                                                 "price": 379888,
                                                                                                 "type": "vehicle"}},
                                                                 "jobs": {"car salesman": {"skills needed": ["charisma", "self loathing"],
                                                                                           "salary": 117},
                                                                          "general manager": {"skills needed": ["leadership", "communication"],
                                                                                              "salary": 318}},
                                                                 "type": "building"},

                    "a castle": {"rarity": "super rare",
                                 "plural": "castles",
                                 "jobs": {"servant": {"skills needed": ["strength", "patience", "cleanliness"],
                                                      "salary": 80},
                                          "security guard": {"skills needed": ["strength"],
                                                             "salary": 90}},
                                 "type": "building"},

                    "a convenience store": {"rarity": "uncommon",
                                            "plural": "convenience stores",
                                            "wares": {"a mars bar": {"rarity": "common",
                                                                     "price": 1,
                                                                     "type": "food",
                                                                     "plural": "mars bars"},
                                                      "a box of matches": {"rarity": "common",
                                                                           "price": 2,
                                                                           "plural": "boxes of matches"},
                                                      "a gallon of milk": {"rarity": "common",
                                                                           "price": 3,
                                                                           "type": "food",
                                                                           "plural": "gallons of milk",
                                                                           "perishable": True}},
                                            "jobs": {"cashier": {"skills needed": ["communication"],
                                                                 "skills learned": ["self loathing", "math", "communication", "patience"],
                                                                 "salary": 85}},
                                            "type": "building"},

                    "a hospital": {"rarity": "rare",
                                   "plural": "hospitals",
                                   "jobs": {"doctor": {"skills needed": ["science", "math", "communication", "patience", "cleanliness", "intelligence"],
                                                       "salary": 526}},
                                   "wares": {"miracle pills": {"rarity": "uncommon",
                                                               "price": 100,
                                                               "type": "medicine"}},
                                   "type": "building"},

                    "an office building": {"rarity": "uncommon",
                                           "plural": "hospitals",
                                           "jobs": {"software developer": {"skills needed": ["communication", "engineering"],
                                                                           "salary": 279},
                                                    "human resources manager": {"skills needed": ["communication"],
                                                                                "salary": 283},
                                                    "telemarketer": {"skills needed": ["charisma"],
                                                                     "salary": 57}},
                                           "type": "building"},
                    "a food mart": {"rarity": "common",
                                    "plural": "food marts",
                                    "wares": {"an apple": {"rarity": "common",
                                                           "plural": "apples",
                                                           "colors": ["red", "yellow", "green"],
                                                           "price": 1,
                                                           "type": "food"},
                                              "beef": {"rarity": "uncommon",
                                                       "price": 10,
                                                       "type": "food",
                                                       "perishable": True}},
                                    "jobs": {"delivery driver": {"skills needed": ["driving"],
                                                                 "salary": 75},
                                             "cashier": {"skills needed": ["communication"],
                                                         "skills learned": ["self loathing", "math", "communication", "patience"],
                                                         "salary": 85},
                                             "night stocker": {"skills needed": ["strength"],
                                                               "salary": 45}},
                                    "type": "building"},
                    "a house": {"rarity": "common",
                                "plural": "houses",
                                "jobs": {"lawn mower": {"skills needed": "strength",
                                                        "inventory needed": "lawn mower"}},
                                "type": "residence"}},
         "forest": {"a pinecone": {"rarity": "super common", "plural": "pinecones", "flammable": True},
                    "a stick": {"rarity": "common", "plural": "sticks", "flammable": True},
                    "a hunting knife": {"rarity": "uncommon", "plural": "hunting knives", "type": "weapon"},
                    "a mushroom": {"rarity": "uncommon", "plural": "mushrooms", "type": "food"},
                    "some kindling": {"rarity": "common", "plural": "piles of kindling", "flammable": True},
                    "some mysterious berries": {"rarity": "uncommon", "plural": "bushes full of mysterious berries", "type": "food"},
                    "an acorn": {"rarity": "common", "plural": "acorns"}},
         "desert": {"some sand": {"rarity": "super common", "plural": "mounds of sand"},
                    "a cactus": {"rarity": "common", "plural": "cacti"},
                    "a tumbleweed": {"rarity": "common", "plural": "tumbleweeds"},
                    "a dinosaur bone": {"rarity": "rare", "plural": "dinosaur bones"}},
         "city": {"a wad of gum": {"rarity": "super common", "plural": "wads of gum"},
                  "a cigarette butt": {"rarity": "super common", "plural": "cigarette butts"},
                  "a phone book": {"rarity": "uncommon", "plural": "phone books"},
                  "a souvenir magnet": {"rarity": "rare", "plural": "souvenir magnets"},
                  "an apartment": {"rarity": "uncommon",
                                    "plural": "apartment complexes",
                                    "type": "residence"},
                   "a bar": {"type": "building",
                             "rarity": "common",
                             "plural": "bars",
                             "jobs": {"bartender": {"skills needed": ["communication"],
                                                    "salary": 40,
                                                    "skills learned": ["patience", "intelligence"]}}},
                   "a starbucks": {"type": "building",
                                   "rarity": "common",
                                   "plural": "starbucks",
                                   "wares": {"cup of coffee": {"price": 5,
                                                               "type": "food",
                                                               "rarity": "super common",
                                                               "plural": "cups of coffee"},
                                             "fat free muffin": {"price": 4,
                                                                 "type": "food",
                                                                 "rarity": "super common",
                                                                 "plural": "fat free muffins"}}},
                   "a blacksmith": {"type": "building",
                                    "rarity": "uncommon",
                                    "plural": "blacksmiths"}},
         "mountains": {"a glacier": {"rarity": "super rare", "plural": "glaciers"},
                       "a wind power farm": {"rarity": "rare", "plural": "wind power farms"}},
         "swamp": {"some moss": {"rarity": "common", "plural": "patches of moss"},
                   "some mud": {"rarity": "common", "plural": "piles of mud"}},
         "ocean": {"a sea shell": {"rarity": "common", "plural": "sea shells"},
                   "a volcanic base": {"rarity": "super rare",
                                       "plural": "volcanic bases",
                                       "jobs": {"evil overlord":  {"skills needed": ["charisma", "strength", "science", "intelligence"]}},
                                       "type": "building"},
                   "some drift wood": {"rarity": "uncommon", "plural": "pieces of drift wood", "flammable": True}}}


buildings = {"city": {"an apartment": {"rarity": "uncommon",
                                       "plural": "apartment complexes",
                                       "type": "residence"},
                      "bar": {"type": "building"},
                      "starbucks": {"type": "building",
                                    "wares": {"cup of coffee": {"price": 5,
                                                                "type": "food",
                                                                "rarity": "super common",
                                                                "plural": "cups of coffee"},
                                              "fat free muffin": {"price": 4,
                                                                  "type": "food",
                                                                  "rarity": "super common",
                                                                  "plural": "fat free muffins"}}},
                      "blacksmith": {"type": "building"}}}


wild_mobs = {"master": {"a squirrel": {"rarity": "common",
                                       "plural": "squirrels"},
                        "a witch": {"rarity": "rare",
                                    "plural": "witches"},
                        "a cat": {"rarity": "uncommon",
                                  "plural": "cats"}},
             "forest": {"a wolf": {"rarity": "uncommon",
                                   "plural": "wolves"},
                        "a wood nymph": {"rarity":  "super rare",
                                         "plural": "wood nymphs"},
                        "a deer": {"rarity": "common",
                                   "plural": "deer"},
                        "a hermit monk": {"rarity": "rare",
                                          "plural": "hermit monks"}},
             "desert": {"a snake": {"rarity": "uncommon",
                                    "plural": "snakes"}},
             "swamp": {"a mosquito": {"rarity": "super common",
                                      "plural": "mosquitoes"}},
             "ocean": {"a jellyfish": {"rarity": "uncommon",
                                       "plural": "jellyfish"},
                       "a crab": {"rarity": "uncommon",
                                  "plural": "crabs"}},
             "mountains": {"a goat": {"rarity": "uncommon",
                                      "plural": "goats"},
                           "a goat herder": {"rarity": "uncommon",
                                             "plural": "goat herders"}},
             "city": {"a hipster": {"rarity": "uncommon",
                                    "plural": "hipsters"},
                      "a homeless man": {"rarity": "uncommon",
                                         "plural": "homeless men"}}}

numbers = {0: "zero",
           1: "one",
           2: "two",
           3: "three",
           4: "four",
           5: "five",
           6: "six",
           7: "seven",
           8: "eight",
           9: "nine",
           10: "ten",
           11: "eleven",
           12: "twelve",
           13: "thirteen",
           14: "fourteen",
           15: "fifteen",
           16: "sixteen",
           17: "seventeen",
           18: "eighteen",
           19: "nineteen",
           20: "twenty",
           30: "thirty",
           40: "forty",
           50: "fifty",
           60: "sixty",
           70: "seventy",
           80: "eighty",
           90: "ninety"}

groups = {1: "",
          2: "thousand",
          3: "million",
          4: "billion",
          5: "trillion",
          6: "quadrillion",
          7: "quintillion",
          8: "sextillion",
          9: "septillion",
          10: "octillion",
          11: "nonillion",
          12: "decillion"}
