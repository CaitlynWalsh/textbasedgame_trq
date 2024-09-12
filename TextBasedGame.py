# Caitlyn Walsh

"""
TextBasedGame: Caitlyn Walsh
_______________________________________________________________________________________________________________________
Hello!

For my final project, I started planning this game in week one, and coding it early. In other words, I've put in a
lot of additions. The game has a lot of printed text and storytelling. So, I've made game options to disable the
narrations and to have the game flow faster for grading.

If you want to skip the storytelling at any point, type in "config" in the console during any input prompt,
and change the game options of narration and/or entity dialogue to false. Also, you can change the print speed to go
faster or slower. If you want to disable the print delay altogether, you can set it to 0.

The game will also tell you about the config command, and will walk you through the game options.

Thank you for your time, and I'm excited to start the next class!

Important Information:
_______________________________________________________________________________________________________________________

- Some game items like the Magic Orb and the Ancient Potion require the player to have certain items in their inventory
  in order to obtain. Until the player obtains the required items, that specific item won't have an option
  for the player to take it.

- Other items like the Abandoned Boat and the Ominous Key are needed to move between certain areas.

- All items play a key role in the final battle, and require strategy. If the player does not have them, the player
  will lose the battle. So, having all the items unlocks the win for the player.

Battle Items and their use:
_______________________________________________________________________________________________________________________

- Heavenly Sword: deals 200 damage to the villain. Breaks on use.
- Food Basket: regains a random amount of health to the player and their partner.
- Magic Orb: deals a higher amount of damage to the villain, the amount increased by the player and their partner's
  magic stats.
- Ancient Potion: regains 100% of the player and their partner's health. Breaks on use.
- Dragon Egg: hatches a baby dragon entity that deals 10 damage to the villain every round. Breaks on use.
"""
import warnings
import random
import re
import sys
import time
from collections import namedtuple  # I love named tuples!!
import logging

# Used to check if the game is active, won or lost
game_states = {
    0: "active",
    1: "won the game",
    2: "lost the game"
}

# Different options of the game to change narration and print speed.
config = {
    "narrate_game": True,
    "read_dialogue": True,
    "print_speed": 0.8
}

# ****************** ITEMS ******************
# Items are a named tuple that take in a key, display name, and other required items.
item = namedtuple("Item", ['key', 'name', "required"])
heavenly_sword = item("heavenly_sword", "Heavenly Sword", [])
dungeon_key = item("dungeon_key", "Dungeon Key", [])
food_basket = item("food_basket", "Food Basket", [])
magic_lily = item("magic_lily", "Magic Lily", [])
pearl_stone = item("pearl_stone", "Pearly Stone", [])
# magic orb requires the magic lily and pearl stone to obtain.
magic_orb = item("magic_orb", "Magical Orb", [magic_lily.key, pearl_stone.key])
abandoned_boat = item("abandoned_boat", "Abandoned Boat", [])
# ancient potion requires the magic orb to obtain.
ancient_potion = item("ancient_potion", "Ancient Potion", [magic_orb.key])
dragon_egg = item("dragon_egg", "Dragon Egg", [])
ominous_key = item("ominous_key", "Ominous Key", [])

# The reference dictionary of all the items.
items = {
    heavenly_sword.key: heavenly_sword,
    dungeon_key.key: dungeon_key,
    food_basket.key: food_basket,
    magic_lily.key: magic_lily,
    pearl_stone.key: pearl_stone,
    magic_orb.key: magic_orb,
    abandoned_boat.key: abandoned_boat,
    ancient_potion.key: ancient_potion,
    dragon_egg.key: dragon_egg,
    ominous_key.key: ominous_key
}

# The Food Basket's possible options of food.
# The key is the food's display name and the amount it heals.
food = {
    "Bread": 20,
    "Fruit": 15,
    "Cooked Meat": 50
}

# ****************** ENTITIES AND PLAYER TYPES ******************
# Entities are a named tuple that takes in a key, display name, max health, attack damage, magic damage, swiftness,
# accuracy, and their dialogue within the game.
entity = namedtuple('Entity', ['key', 'name', 'max_health', 'attack', 'magic', 'swift', 'accuracy', 'dialogue'])

# PLAYERS
knight = entity('knight', "Knight", 150, 35, 0, 5, 95, {
    "art": ["      _,.\n"
            "    ,` -.)\n"
            "   ( _/-\\\\-._\n"
            "  /,|`--._,-^|           ,\n"
            "  \_| |`-._/||         ,'|\n"
            "    |  `-, / |        /  /\n"
            "     `r-._||/   __   /  /\n"
            " __,-<_ ____)`-/  `./  /\n"
            "'  \           \   /  /\n"
            "    |           |./  /\n"
            "    /     _/\\_ / /  /\n"
            "\_/' \         |/  /\n"
            " |    |   _,^-'/  /\n"
            " |    , ``  (\/  /_\n"
            "  \,.->._    \X-=/^\n"
            "  (  /   `-._//^`\n"
            "   `Y-.____(__}\n"
            "    |     {__)\n"
            "          ()\n"
            ],
    "start": ["You have enlisted in the Royal Army, becoming a high-ranking Knight."]
})
mage = entity('mage', "Mage", 120, 10, 20, 30, 88, {
    "art": [
        "                  (__)\n"
        "                  /  \\\n"
        "                _/    \_\n"
        "               /   ..   \\\n"
        "              /  _----_  \\\n"
        "             (  /      \  )\n"
        "              \ \      / /\n"
        "             _-\ \_  _/ /_\n"
        "           _/ '  ==\/==   \\\n"
        "          /  _ \ - | - /_  \\\n"
        "          (   ( .;''';. .'  )\n"
        "          _\\\"__ /    )\ __\"/_\n"
        "            \/  \   ' /  \/\n"
        "             .'  '...' ' )\n"
        "              / /  |  \ \\\n"
        "             / .   .   . \\\n"
        "            /   .      .  \\\n"
        "           /  /    |    \  \\\n"
        "        .'   /    .*.     '.'.\n"
        "     _.'    /     .*.      '-.'.\n"
        "  .-'      |      .*.        '-. '-.\n"
        " (__________\____..*..________)______)\n"
    ],
    "start": ["As a trained Mage, You've had magical abilities since birth, and are enemies with the Kingdom."]
})
archer = entity('archer', "Archer", 100, 25, 0, 50, 100, {
    "art": [
        "                                                       |\n"
        "                                                        \.\n"
        "                                                        /|.\n"
        "                                                      /  `|.\n"
        "                                                    /     |.\n"
        "                                                  /       |.\n"
        "                                                /         `|.\n"
        "                                              /            |.\n"
        "                                            /              |.\n"
        "                                          /                |.\n"
        "     __                                 /                  `|.\n"
        "      -\                              /                     |.\n"
        "        \\\\                          /                       |.\n"
        "          \\\\                      /                         |.\n"
        "           \|                   /                           |\\\n"
        "             \#####\          /                             ||\n"
        "         ==###########>     /                               ||\n"
        "          \##==      \    /                                 ||\n"
        "     ______ =       =|__/___                                ||\n"
        " ,--'  _____________/'  --,-`-==============================##==========>\n"
        "\    '                   ##_______ ______   ______,--,____,=##,__\n"
        " `,    __==    ___,-,__,--'#'  ==='      `-'              | ##,-/\n"
        "   `-,____,---'       \####\              |        ____,--\_##,/\n"
        "       #_              |##   \  _____,---==,__,---'         ##\n"
        "        #              ]===--==\                            ||\n"
        "        #,             ]         \                          ||\n"
        "         #_            |           \                        ||\n"
        "          ##_       __/'             \                      ||\n"
        "           ####='     |                \                    |/\n"
        "            ###       |                  \                  |.\n"
        "           ###=======]                     \                |.\n"
        "          ///        |                       \             ,|.\n"
        "                                               \           |.\n"
        "                                                 \        ,|.\n"
        "                                                   \      |.\n"
        "                                                     \   |.\n"
        "                                                       \|.\n"
        "                                                        /.\n"
        "                                                        |\n"
    ],
    "start": ["Born with a keen eye and swift moves, you are a naturally skilled Archer that never misses a target."]
})
warrior = entity('warrior', "Warrior", 140, 30, 0, 15, 90, {
    "art": [
        "                        ______\n"
        "                     __'____  )\\\n"
        "                   ,__)_        \\\n"
        "                    \_\  \   = \ \\\n"
        "                    /\- \ \     \ |\n"
        "                   .\\\\- \  \   /  |\n"
        "                   /   \-_\___-  /\n"
        "                   |    \..\  )_/\n"
        "                  ./     \--\\\n"
        "                          \. \\\n"
        "                 _         \. \/)\n"
        "            _ _-' ')__     (\.\/)\n"
        "           /       /  \.'`'-\/)\\\\\n"
        "           \__ ,.-'(_  \    (_\.\)\n"
        "            / <     ,\  \    ,\\\\.\\\\\n"
        "            \_ \ _. / (_|    : |\.\|\n"
        "             _\_\\\\   |    : | \. \ \\\n"
        "            (   `'-._>/ )     \|  \.\\\n"
        "            \         `:=.    (\   \.\\\n"
        "             \_      (    `--._)`--'\.\\\n"
        "            _/|\_    \-._     `-:_ /```\\\n"
        "           /  |  `-   \   '--._    |    _\\\n"
        "        ,-'   |       /  |   /``'-.\--' x\\\n"
        "      _/     _(    ,./  /   (          \ x\\\n"
        "         _.-/  \  /    <     \          \_x\\\n"
    ],
    "start": ["With a bold temper and strong nature, you are naturally a Warrior, and fight for no one but yourself."]
})

# Player Partners
young_mage = entity("young_mage", "Young Mage", 120, 10, 20, 30, 88, {
    knight.key: [
        "What's going on? You... want to free me?",
        "\nHow is this happening?",
        "I did not expect you to be my savior, but I'm forever in you're debt!",
        "Your armor is very shiny! What material is it?",
        "I can't see your face, But I bet you're awesome-looking!",
        "Can we get something to eat? I'm pretty hungry!",
        "\nYou want me to shut up? Yes, anything for you my savior!",
        "\n...",
        "\nSo, Where are we going now?"
    ],
    archer.key: [
        "What's going on? I'm being freed?",
        "\nHow is this happening?",
        "I did not expect a thief to be my savior, but I'm forever in you're debt!",
        "I like the feather on your hat!",
        "You use a bow and arrow? That's amazing! Can you teach me archery someday?",
        "Can we get something to eat? I'm pretty hungry!",
        "\nYou want me to shut up? Yes, anything for you my savior!",
        "\n...",
        "\nSo, Where are we going now?"
    ],
    warrior.key: [
        "What's going on? I'm being freed?",
        "\nHow is this happening?",
        "I did not expect a brute to be my savior, but I'm forever in you're debt!",
        "I like your axe! Very intimidating!",
        "You have awesome battle scars! Have you killed people?",
        "Can we get something to eat? I'm pretty hungry!",
        "\nYou want me to shut up? Yes, anything for you my savior!",
        "\n...",
        "\nSo, Where are we going now?"
    ]
})
traitor_knight = entity("traitor_knight", "Traitor Knight", 150, 30, 0, 5, 95, {
    mage.key: [
        "I've overheard the King's plans to save the world.",
        "I was his Royal Knight, before being accused of witchcraft.",
        "Then, I was sent down here to rot in a cell.",
        "The irony, that a Mage is the chosen one.",
        "\n...Well, you lead the way. I will accompany you.",
        "The fate of the world is in our hands."
    ]
})
rouge_archer = entity("rouge_archer", "Rouge Archer", 100, 25, 0, 50, 100, {
    mage.key: [
        "I'm not sure if this is my lucky day.",
        "But if I get to see the sun again, It sure is worth it.",
        "I will accompany you, Mage.",
        "Lead the way, and I will follow.",
        "\n...As long as we get something to eat, first."
    ]
})
brute_warrior = entity("brute_warrior", "Brute Warrior", 140, 35, 0, 15, 90, {
    mage.key: [
        "Hm. So, you really want to take your chances with a brute?",
        "Ha! Don't worry, I won't hurt you.",
        "I trust you, Mage.",
        "I can tell we will get along on this journey.",
        "You lead the way. I will accompany you on this quest."
    ]
})

# Game Entities
king = entity("king", "The Royal King", 250, 30, 0, 10, 90, {
    knight.key: [
        "My Knight, I have a very important quest that I can only entrust to you.",
        "It is a highly dangerous mission, and the fate of this world depends on you.",
        "You must sail overseas, and defeat the Shadow Lord once and for all.",
        "\n...Now, I understand this is much to take in.",
        "But there is a reason why I have given you the ranking you have today.",
        "There is something different about you... Something deep inside you makes you so powerful.",
        "Something stronger than myself, and even stronger than The Shadow Lord.",
        "I want you to channel that inner power, and turn it to strength.",
        "\nThe powers you contain will be difficult to unlock on your own.",
        "...So, I will entrust you a partner for your quest.",
        "They are in the Dungeon to the East. A Young Mage.",
        "Tell the guard you have orders from me, and he will give you the key.",
        "\n...Now, take my sword with you. Use it only when necessary.",
        "This glistening sword is blessed by the Heavens, and will deal great damage to the shadows.",
        "\nNow go... You and your partner must save the world from the evils at bay!"
    ],
    mage.key: [
        "Mage, I understand this may be confusing to you.",
        "My Kingdom has not welcomed magic for generations now.",
        "But you are not a prisoner. Far from that.",
        "I have a very important quest that I can only entrust to you.",
        "It is a highly dangerous mission, and the fate of this world depends on you.",
        "You must sail overseas, and defeat the Shadow Lord once and for all.",
        "\n...Now, I understand this is much to take in.",
        "But there is a reason why I have ordered you to be the savior.",
        "There is something different about you... Something deep inside you makes you so powerful.",
        "Something stronger than myself, and even stronger than The Shadow Lord.",
        "I want you to channel that inner power, and turn it to strength.",
        "\nThe powers you contain will be difficult to unlock on your own.",
        "...So, I will entrust you a partner for your quest.",
        "They are locked in the Dungeon to the East.",
        "Show the guard this note, and he will give you the key.",
        "\n...Now, take my sword with you. Use it only when necessary.",
        "This glistening sword is blessed by the Heavens, and will deal great damage to the shadows.",
        "\nNow go... You and your partner must save the world from the evils at bay!"
    ],
    archer.key: [
        "...Hm. I can see you are prepared to enter the Dungeon once more for your thieving.",
        "The Kingdom does not tolerate outlaws.",
        "...But, that is not the reason I have ordered you to face me.",
        "Your talents have proven to me your potential.",
        "It is far greater than any soldier of mine.",
        "So, you are not a prisoner now. Far from that.",
        "I have a very important quest that I can only entrust to you.",
        "It is a highly dangerous mission, and the fate of this world depends on you.",
        "You must sail overseas, and defeat the Shadow Lord once and for all.",
        "\n...Now, I understand this is much to take in. Even more for myself.",
        "But there is a reason why I have ordered you to be the savior.",
        "There is something different about you... Something deep inside you makes you so powerful.",
        "Something stronger than myself, and even stronger than The Shadow Lord.",
        "I want you to channel that inner power, and turn it to strength.",
        "\nThe powers you contain will be difficult to unlock on your own.",
        "...So, I will entrust you a partner for your quest.",
        "They are in the Dungeon to the East. A Young Mage.",
        "Show the guard this note, and he will give you the key.",
        "\n...Now, take my sword with you. Use it only when necessary.",
        "This glistening sword is blessed by the Heavens, and will deal great damage to the shadows.",
        "Take it, and prove to me that I haven't made a mistake... That you are the one to save this world."
    ],
    warrior.key: [
        "Brave Warrior, I can see the confidence and pride within you.",
        "However, I am hoping you can put that aside for me today. For the greater good...",
        "Since I have a very important quest that I can only entrust to you.",
        "\nI understand you fight your own battles. But the fate of this world depends on you.",
        "It is a highly dangerous mission, and you are the world's only hope.",
        "You must sail overseas, and defeat the Shadow Lord once and for all.",
        "\n...Now, I understand this is much to take in.",
        "But there is a reason why I have chosen you over my soldiers.",
        "There is something different about you... Something deep inside you makes you so powerful.",
        "Something stronger than myself, and even stronger than The Shadow Lord.",
        "I want you to channel that inner power, and turn it to strength.",
        "\nThe powers you contain will be difficult to unlock on your own.",
        "...So, I will entrust you a partner for your quest.",
        "They are in the Dungeon to the East. A Young Mage.",
        "Show the guard this note, and he will give you the key.",
        "\n...Now, take my sword with you. Use it only when necessary.",
        "I know you prefer axes, but do make an exception.",
        "This glistening sword is blessed by the Heavens, and will deal great damage to the shadows.",
        "\nNow go... You and your partner must save the world from the evils at bay!"
    ]
})
royal_guard = entity("royal_guard", "Royal Guard", 150, 25, 0, 2, 90, {
    knight.key: [
        "ZZZZzzzz..... Gasp!",
        "What? Who is it?!",
        "The King's Knight?! Uh- This is where I salute...",
        "\nWhat brings you here, Royal Knight?",
        "\nHuh? The King wants to pardon that witch? But that's-",
        "...N-No, I would never disobey an order from His Majesty!",
        "\nHere, take this key Royal Knight.",
        "Be careful now, they may cast a spell on you!"
    ],
    mage.key: [
        "ZZZZzzzz..... Gasp!",
        "What? Who is it?!",
        "A Witch?! Stay back you fiend!!",
        "\nWhat is this? A note from the King? Where did you get this?!",
        "\n...",
        "\n...So, you're telling me... the King... gave a Witch... high ranking authority?!",
        "How can this be?! He's lost his holy mind! You're an enemy of the Kingdom!",
        "\nThe Dungeon Key? You want to pardon a prisoner? Why yes, my \'Royal Witch!\'",
        "This is absolutely ludicrous.",
        "\nPrisoner, make sure to keep an eye on this witch. I don't trust them one bit..."
    ],
    archer.key: [
        "ZZZZzzzz..... Gasp!",
        "What? Who is it?!",
        "A prisoner?! Get back at once! Mutiny!!",
        "\nThe King, has pardoned you? As if I'd believe that, you thief!",
        "...What's this? A note from the king? Where did you get this?!",
        "\nYou... really are pardoned...",
        "\nFine then. Take this key, thief. It's your lucky day."
    ],
    warrior.key: [
        "ZZZZzzzz..... Gasp!",
        "What? Who is it?!",
        "Who are you?! Get back at once, trespasser!",
        "You have orders from the king? Let me see the note...",
        "\n...Alright then. Take this key, Warrior.",
        "\n...And by the way, you saw nothing.",
        "I was guarding this dungeon with a keen eye!"
    ]
})
old_lady = entity("old_lady", "Old Townslady", 50, 1, 0, 0, 80, {
    knight.key: [
        "Oh, my Knight. You have a long journey ahead.",
        "Please take this basket...",
        "A strong Knight like you mustn't go hungry."
    ],
    mage.key: [
        "My, You have a long journey ahead.",
        "The world needs you, my witch.",
        "Please, take this basket. It is the least I can do."
    ],
    archer.key: [
        "...You are the one who tried to steal from me earlier.",
        "And now, you are the savior?",
        "My, how strange life can be.",
        "Hopefully this journey will humble you.",
        "...Here, you may have the basket. Please, take it with you.",
        "I pray for your safety, Archer."
    ],
    warrior.key: [
        "My, You have a long journey ahead.",
        "The world needs you, brave Warrior.",
        "Please, take this basket. It is the least I can do.",
        "A strong Warrior like you mustn't go hungry."
    ]
})
elder_mage = entity("elder_mage", "Elder Mage", 200, 20, 50, 10, 70, {
    knight.key: [
        "I see the Kingdom has sent you.",
        "Interesting. I did not expect one of their Knights to be the savior.",
        "By the way your people look at magic, I expected the King to lock you up.",
        "Even he sees the future we are headed...",
        "\n...I must give you something for your journey.",
        "I need a Magic Lily, and a Pearly Stone.",
        "Once you find these items, come speak to me again."
    ],
    mage.key: [
        "I see. Quite interesting.",
        "The King has sent you on his behalf, to save this world from corruption.",
        "I did not expect him to do this. To go against his strong hatred for magic.",
        "Even he sees the future we are headed...",
        "\n...I must give you something for your journey.",
        "I need a Magic Lily, and a Pearly Stone.",
        "Once you find these items, come speak to me again."
    ],
    archer.key: [
        "So the Kingdom has sent you.",
        "A thieving Archer is the savior of this world.",
        "Interesting indeed.",
        "Yet the Heavens have chosen you for a reason.",
        "\n...I must give you something for your journey.",
        "I need a Magic Lily, and a Pearly Stone.",
        "Once you find these items, come speak to me again."
    ],
    warrior.key: [
        "So the Kingdom has sent you.",
        "A strong Warrior with great potential inside.",
        "By the way the Kingdom looks at magic, I expected the King to lock you up.",
        "Even he sees the future we are headed...",
        "\n...I must give you something for your journey.",
        "I need a Magic Lily, and a Pearly Stone.",
        "Once you find these items, come speak to me again."
    ],
    magic_orb.key: [
        "...I see you have obtained the items I need.",
        "Hand them to me.",
        "\nWith a strong shine of light, the Elder Mage turns the flower and the stone into a glowing orb",
        "\nYou must take this orb with you. It will be crucial for surviving your quest ahead."
    ]
})
empty_knight = entity("empty_knight", "Empty Knight", 300, 25, 10, 5, 88, {
    knight.key: [
        "...",
        "...T-ake....",
        "...Tak..e......k-ey....",
        "\nThe corrupted Knight speaks in pained whispers before he loosens his stiff grip.",
        "The palm of his hand reveals a key with a dark aura emanating from it."
    ],
    mage.key: [
        "...",
        "...T-ake....",
        "...Tak..e......k-ey....",
        "\nThe corrupted Knight speaks in pained whispers before he loosens his stiff grip.",
        "The palm of his hand reveals a key with a dark aura emanating from it."
    ],
    archer.key: [
        "...",
        "...T-ake....",
        "...Tak..e......k-ey....",
        "\nThe corrupted Knight speaks in pained whispers before he loosens his stiff grip.",
        "The palm of his hand reveals a key with a dark aura emanating from it."
    ],
    warrior.key: [
        "...",
        "...T-ake....",
        "...Tak..e......k-ey....",
        "\nThe corrupted Knight speaks in pained whispers before he loosens his stiff grip.",
        "The palm of his hand reveals a key with a dark aura emanating from it."
    ]
})
shadow_lord = entity("shadow_lord", "The Shadow Lord", 500, 20, 40, 20, 90, {
    knight.key: [
        "So... this is what the King has to offer...",
        "Pathetic.",
        "You must have seen the last ones to challenge me.",
        "The entire army has been consumed by the darkness.",
        "And you come here, thinking you alone will defeat me.",
        "Well, I have a rude awakening for you, Royal Knight...",
        "The darkness will consume you too.",
        "You will corrupt like the Knight outside my castle.",
        "But I will make sure the shadows do not fully consume you...",
        "Because you, will become one with me...",
        "And with your corrupted husk at my service... I will rule this world, in darkness."
    ],
    mage.key: [
        "So... this is what the King has to offer...",
        "Pathetic.",
        "You must have seen the last ones to challenge me.",
        "The entire army has been consumed by the darkness.",
        "And you come here, thinking you alone will defeat me.",
        "Well, I have a rude awakening for you, foolish Mage...",
        "The darkness will consume you too.",
        "You will corrupt like the Knight outside my castle.",
        "But I will make sure the shadows do not fully consume you...",
        "Because you, will become one with me...",
        "And with your corrupted husk at my service... I will rule this world, in darkness."
    ],
    archer.key: [
        "So... this is what the King has to offer...",
        "Pathetic.",
        "You must have seen the last ones to challenge me.",
        "The entire army has been consumed by the darkness.",
        "And you come here, thinking you alone will defeat me.",
        "Well, I have a rude awakening for you, Archer...",
        "Your keen eye will not save you..."
        "Because the darkness will consume you too.",
        "You will corrupt like the Knight outside my castle.",
        "But I will make sure the shadows do not fully consume you...",
        "Because you, will become one with me...",
        "And with your corrupted husk at my service... I will rule this world, in darkness."
    ],
    warrior.key: [
        "So... this is what the King has to offer...",
        "Pathetic.",
        "You must have seen the last ones to challenge me.",
        "The entire army has been consumed by the darkness.",
        "And you come here, thinking you alone will defeat me.",
        "Well, I have a rude awakening for you, brave Warrior...",
        "The darkness will consume you too.",
        "You will corrupt like the Knight outside my castle.",
        "But I will make sure the shadows do not fully consume you...",
        "Because you, will become one with me...",
        "And with your corrupted husk at my service... I will rule this world, in darkness."
    ]
})
baby_dragon = entity("baby_dragon", "Baby Dragon", 80, 5, 5, 100, 100, {
    knight.key: [],
    mage.key: [],
    archer.key: [],
    warrior.key: []
})

# The reference dictionary of all Game Entities
entities = {
    king.key: king,
    royal_guard.key: royal_guard,
    old_lady.key: old_lady,
    elder_mage.key: elder_mage,
    empty_knight.key: empty_knight,
    shadow_lord.key: shadow_lord,
    baby_dragon.key: baby_dragon
}

# The reference dictionary of all Players
players = {
    knight.key: knight, mage.key: mage, archer.key: archer, warrior.key: warrior
}

# The reference dictionary of all Player Partners
partners = {
    knight.key: [young_mage],
    mage.key: [traitor_knight, rouge_archer, brute_warrior],
    archer.key: [young_mage],
    warrior.key: [young_mage]
}


# Creates a new instance of an entity type, with modifiable stats
def create_entity(ent: entity):
    return {
        "name": ent.name,
        "health": ent.max_health,
        "max_health": ent.max_health,
        "attack": ent.attack,
        "magic": ent.magic,
        "swift": ent.swift,
        "accuracy": ent.accuracy,
        "dialogue": ent.dialogue
    }


# ****************** AREAS ******************
# Areas/Rooms are a named tuple that takes in a key, a display name,
# an optional entity, an optional item, and narration.
# Narration also depends on player types for different storytelling.
area = namedtuple('Area', ['key', 'name', 'ent', 'itm', 'narration'])

# Kingdom is the starting area.
kingdom = area("kingdom", "Kingdom", " ", " ", {
    knight.key: [
        "Inside the walls of the Kingdom is a lively city.",
        "It is full of wealth, roads of brick, and statues carved in marble.",
        "To the North, the Castle of gold and pearly bricks looms over you.",
        "Inside awaits The Royal King for you to meet."
    ],
    mage.key: [
        "The Knights dressed in Iron lead you throughout the Kingdom.",
        "Your hands are chained behind your back.",
        "The citizens shout out to you, throwing rocks as you pass through the street.",
        "\"Witch!\", \"Burn at the stake!\"",
        "They all chant.",
        "The Knights pass through quickly, pushing through the unruly crowd.",
        "And to the North, you see a Castle of gold and pearly bricks.",
        "One of the Knights quickly unchains your arms.",
        "You look up at him, his face covered in Iron.",
        "\"You are to meet His Majesty, The Royal King. He awaits for you inside.\"",
        "He speaks with a muffled voice."
    ],
    archer.key: [
        "The Knights dressed in Iron lead you throughout the Kingdom.",
        "Your hands are chained behind your back.",
        "The citizens shout out to you, shaming you in the streets.",
        "\"Thief!\", \"Criminal!\"",
        "Some of them yell, and others quickly join in on the crowd.",
        "The Knights protect you as their prisoner, pushing through the unruly citizens.",
        "And to the North, you see a Castle of gold and pearly bricks.",
        "One of the Knights quickly unchains your arms.",
        "You look up at him confused, his face covered in Iron.",
        "\"You are to meet His Majesty, The Royal King. He awaits for you inside.\"",
        "He speaks with a muffled voice."
    ],
    warrior.key: [
        "Inside the walls of the Kingdom is a lively city.",
        "It is full of wealth, roads of brick, and statues carved in marble.",
        "It is much more lavish than the nomadic lifestyle you were born into.",
        "Covered in deer skins and wolf fur, along with an giant axe strapped to your back,",
        "You are most definitely an outsider.",
        "To the North, the Castle of gold and pearly bricks looms over you.",
        "Inside awaits The Royal King for you to meet.",
        "Staring up into the heavenly Castle,",
        "You can't help but wonder what the King has planned for you."
    ]
})
castle = area("castle", "Castle", king.key, heavenly_sword.key, {
    knight.key: [
        "As you hand the guards the sealed note of the King,",
        "the giant wooden door cracks open, and the Guards salute as you enter.",
        "Inside, servants lead you through the grand halls, and into the main room.",
        "His Majesty sits on his throne, looking down at you.",
        "You take off your Iron Helmet, kneeling before him."
    ],
    mage.key: [
        "You walk up to the castle doors, feeling the nerves churn your stomach.",
        "The Guards stand stiff as you walk past them.",
        "Inside, servants lead you through the grand halls, and into the main room.",
        "The King sits on his throne, looking down at you.",
        "\'You must kneel for the king...\' One of the servants whispers to you.",
        "You quickly take a knee, and the King breaks a smile."
    ],
    archer.key: [
        "You walk up to the castle doors, feeling the nerves churn your stomach.",
        "The Guards stand stiff as you walk past them.",
        "Inside, servants lead you through the grand halls, and into the main room.",
        "The King sits on his throne, looking down at you.",
        "You look down, kneeling before him."
    ],
    warrior.key: [
        "As you hand the guards the sealed note of the King,",
        "the giant wooden door cracks open, and the Guards sheath their swords for you to enter.",
        "Inside, servants lead you through the grand halls, and into the main room.",
        "There, the King sits on his throne, looking down at you. You do not kneel.",
        "\'You must kneel for the king...\' One of the servants frantically whispers to you.",
        "The king breaks a smile."
    ]
})
dungeon = area("dungeon", "Dungeon", royal_guard.key, dungeon_key.key, {
    knight.key: [
        "You creak open the heavy iron doors of the Dungeon.",
        "The wall torches cast a flickering glow across the room.",
        "Amidst the dull bricks and the cobwebs is a faint shine of armor slumped in a chair.",
        "You can hear him snoring loudly.",
        "You turn your head, and see the Young Mage.",
        "They are dressed in raggedy cloths, with a poor attempt at hiding in the corner.",
        "The Mage peeks above the bed, only to hide once more once your eyes lock onto theirs.",
        "You turn to the guard, shaking him furiously."
    ],
    mage.key: [
        "You creak open the heavy iron doors of the Dungeon.",
        "The wall torches cast a flickering glow across the room.",
        "Amidst the dull bricks and the cobwebs is a faint shine of armor slumped in a chair.",
        "You can hear him snoring loudly.",
        "You turn your head, and see the prisoner.",
        "They are dressed in raggedy cloths, slumped over by the bars and staring up at you.",
        "Hesitantly, You turn to the guard, shaking him awake."
    ],
    archer.key: [
        "You creak open the heavy iron doors of the Dungeon.",
        "The wall torches cast a flickering glow across the room.",
        "Amidst the dull bricks and the cobwebs is a faint shine of armor slumped in a chair.",
        "You can hear him snoring loudly.",
        "You turn your head, and see the Young Mage.",
        "They are dressed in raggedy cloths, staring up at you curiously.",
        "You turn to the guard, shaking him awake."
    ],
    warrior.key: [
        "You creak open the heavy iron doors of the Dungeon.",
        "The wall torches cast a flickering glow across the room.",
        "Amidst the dull bricks and the cobwebs is a faint shine of armor slumped in a chair.",
        "You can hear him snoring loudly.",
        "You turn your head, and see the Young Mage.",
        "They are dressed in raggedy cloths and hiding in the corner.",
        "The Mage peeks above the bed, only to hide once more once your eyes lock onto theirs.",
        "You turn to the guard, shaking him awake."
    ]
})
kingstown = area("kingstown", "Kingstown", old_lady.key, food_basket.key, {
    knight.key: [
        "You walk down the winding path, making your way to Kingstown.",
        "The marketplace is busy with commoners, selling food and cheap wears.",
        "They all turn their heads, staring and pointing at you in awe.",
        "You roll your eyes, continuing to push forward.",
        "But then you are stopped, only to feel a gentle grasp of a hand.",
        "You look down, and a frail old lady smiles up at you."
    ],
    mage.key: [
        "You walk down the winding path, making your way to Kingstown.",
        "The marketplace is busy with commoners, selling food and cheap wears.",
        "They all turn their heads, staring and pointing at you.",
        "...But not out of contempt. Unlike the Kingdom, the commoners seemed interested.",
        "You wave at them, only to be stopped by a gentle grasp.",
        "You look down, and a frail old lady smiles up at you."
    ],
    archer.key: [
        "You walk down the winding path, making your way to Kingstown.",
        "The marketplace is busy with commoners, selling food and cheap wears.",
        "They all turn their heads, staring and pointing at you, whispering to each other.",
        "You continue to push through the crowd.",
        "But then you are stopped, only to feel a gentle grasp of a hand.",
        "You look down, greeted by a familiar old lady..."
    ],
    warrior.key: [
        "You walk down the winding path, making your way to Kingstown.",
        "The marketplace is busy with commoners, selling food and cheap wears.",
        "They all turn their heads, staring and pointing at you in awe.",
        "huffing out in annoyance, you continue to push forward.",
        "But then you are stopped, only to feel a gentle grasp of a hand.",
        "You quickly tense, looking down.",
        "A frail old lady smiles up at you."
    ]
})
deep_woods = area("deep_woods", "Deepwoods", " ", magic_lily.key, {
    knight.key: [
        "You make your way through the thick foliage of the forest.",
        "The trees are dense, and cover the forest with faint rays of sunshine.",
        "But in the dark corner, you see a particular plant that sticks out from the rest.",
        "A small lily gives off a magical glow in the shadows of the forest.",
        "You walk closer to it, suddenly feeling fluttering in your stomach..."
    ],
    mage.key: [
        "You make your way through the thick foliage of the forest.",
        "The trees are dense, and cover the forest with faint rays of sunshine.",
        "But in the dark corner, you see a particular plant that sticks out from the rest.",
        "A small lily gives off a magical glow in the shadows of the forest.",
        "You walk closer to it, suddenly feeling fluttering in your stomach..."
    ],
    archer.key: [
        "You make your way through the thick foliage of the forest.",
        "The trees are dense, and cover the forest with faint rays of sunshine.",
        "But in the dark corner, you see a particular plant that sticks out from the rest.",
        "A small lily gives off a magical glow in the shadows of the forest.",
        "You walk closer to it, suddenly feeling fluttering in your stomach..."
    ],
    warrior.key: [
        "You make your way through the thick foliage of the forest.",
        "The trees are dense, and cover the forest with faint rays of sunshine.",
        "But in the dark corner, you see a particular plant that sticks out from the rest.",
        "A small lily gives off a magical glow in the shadows of the forest.",
        "You walk closer to it, suddenly feeling fluttering in your stomach..."
    ]
})
steep_hills = area("steep_hills", "Steep Hills", " ", pearl_stone.key, {
    knight.key: [
        "Climbing up the steep mountainous rocks towering over the land,",
        "A pearly-white stone catches your eye.",
        "It seems to be the same material the Castle bricks are made of.",
        "You pick it up, examining it further.",
        "A ray of sunshine gleams down on it as you hold it in your hand..."
    ],
    mage.key: [
        "Climbing up the steep mountainous rocks towering over the land,",
        "A pearly-white stone catches your eye.",
        "It seems to be the same material the Kingdom's Castle bricks are made of.",
        "You pick it up, examining it further.",
        "A ray of sunshine gleams down on it as you hold it in your hand..."
    ],
    archer.key: [
        "Climbing up the steep mountainous rocks towering over the land,",
        "A pearly-white stone catches your eye.",
        "It seems to be the same material the Kingdom's Castle bricks are made of.",
        "You pick it up, examining it further.",
        "A ray of sunshine gleams down on it as you hold it in your hand..."
    ],
    warrior.key: [
        "Climbing up the steep mountainous rocks towering over the land,",
        "A pearly-white stone catches your eye.",
        "It seems to be the same material the Kingdom's Castle bricks are made of.",
        "You pick it up, examining it further.",
        "A ray of sunshine gleams down on it as you hold it in your hand..."
    ]
})
peaks = area("peaks", "Giant Peaks", elder_mage.key, magic_orb.key, {
    knight.key: [
        "Soon, the Giant Peaks are within reach.",
        "You can see a figure at the very top of the mountain, meditating in the clouds.",
        "Once you reach the top, You can see it is an old Mage.",
        "He opens his eyes as you walk closer, Stroking his white beard in wonder..."
    ],
    mage.key: [
        "Soon, the Giant Peaks are within reach.",
        "You can see a figure at the very top of the mountain, meditating in the clouds.",
        "Once you reach the top, You can see it is an old Mage.",
        "He opens his eyes as you walk closer, Stroking his white beard in wonder..."
    ],
    archer.key: [
        "Soon, the Giant Peaks are within reach.",
        "You can see a figure at the very top of the mountain, meditating in the clouds.",
        "Once you reach the top, You can see it is an old Mage.",
        "He opens his eyes as you walk closer, Stroking his white beard in wonder..."
    ],
    warrior.key: [
        "Soon, the Giant Peaks are within reach.",
        "You can see a figure at the very top of the mountain, meditating in the clouds.",
        "Once you reach the top, You can see it is an old Mage.",
        "He opens his eyes as you walk closer, Stroking his white beard in wonder..."
    ]
})
lost_shore = area("lost_shore", "Lost Shore", " ", abandoned_boat.key, {
    knight.key: [
        "The gulls of the sea squall in the air as your steps sink into the sand.",
        "Many shipwrecks have collected on the edges of the beach.",
        "Yet there are no bodies within them. Just ghostly, abandoned boats.",
        "The Forbidden Sea lives up to it's name.",
        "The sailors who entered the deadly waters have never been seen again.",
        "\nOne boat in particular seems to be in very good shape.",
        "You examine it closer. It is as if it never set sail."
    ],
    mage.key: [
        "The gulls of the sea squall in the air as your steps sink into the sand.",
        "Many shipwrecks have collected on the edges of the beach.",
        "Yet there are no bodies within them. Just ghostly, abandoned boats.",
        "The Forbidden Sea lives up to it's name.",
        "The sailors who entered the deadly waters have never been seen again.",
        "\nOne boat in particular seems to be in very good shape.",
        "You examine it closer. It is as if it never set sail."
    ],
    archer.key: [
        "The gulls of the sea squall in the air as your steps sink into the sand.",
        "Many shipwrecks have collected on the edges of the beach.",
        "Yet there are no bodies within them. Just ghostly, abandoned boats.",
        "The Forbidden Sea lives up to it's name.",
        "The sailors who entered the deadly waters have never been seen again.",
        "\nOne boat in particular seems to be in very good shape.",
        "You examine it closer. It is as if it never set sail."
    ],
    warrior.key: [
        "The gulls of the sea squall in the air as your steps sink into the sand.",
        "Many shipwrecks have collected on the edges of the beach.",
        "Yet there are no bodies within them. Just ghostly, abandoned boats.",
        "The Forbidden Sea lives up to it's name.",
        "The sailors who entered the deadly waters have never been seen again.",
        "\nOne boat in particular seems to be in very good shape.",
        "You examine it closer. It is as if it never set sail."
    ]
})
forbidden_sea = area("forbidden_sea", "Forbidden Sea", " ", ancient_potion.key, {
    knight.key: [
        "As you sail, The sea fog begins to get denser. Until the skyline is covered.",
        "A dark, smoky mist with no smell. It only leaves you with a pounding headache.",
        "You have lost all sense of direction, and you feel yourself steering into nothing.",
        "Then, you see something shining in the distance.",
        "You follow the light, the only option you have.",
        "It gets closer, revealing a bottle in the bottom of the ocean.",
        "An ancient bottle containing immense magic.",
        "You cannot swim to the bottom of the sea to get it.",
        "But with the help of a {}, you may be able to obtain it...".format(magic_orb.name)
    ],
    mage.key: [
        "As you sail, The sea fog begins to get denser. Until the skyline is covered.",
        "A dark, smoky mist with no smell. It only leaves you with a pounding headache.",
        "You have lost all sense of direction, and you feel yourself steering into nothing.",
        "Then, you see something shining in the distance.",
        "You follow the light, the only option you have.",
        "It gets closer, revealing a bottle in the bottom of the ocean.",
        "An ancient bottle containing immense magic.",
        "Your abilities alone cannot levitate the bottle of ancient magic.",
        "But with the help of a {}, you may be able to obtain it...".format(magic_orb.name)
    ],
    archer.key: [
        "As you sail, The sea fog begins to get denser. Until the skyline is covered.",
        "A dark, smoky mist with no smell. It only leaves you with a pounding headache.",
        "You have lost all sense of direction, and you feel yourself steering into nothing.",
        "Then, you see something shining in the distance.",
        "You follow the light, the only option you have.",
        "It gets closer, revealing a bottle in the bottom of the ocean.",
        "An ancient bottle containing immense magic.",
        "You cannot swim to the bottom of the sea to get it.",
        "But with the help of a {}, you may be able to obtain it...".format(magic_orb.name)
    ],
    warrior.key: [
        "As you sail, The sea fog begins to get denser. Until the skyline is covered.",
        "A dark, smoky mist with no smell. It only leaves you with a pounding headache.",
        "You have lost all sense of direction, and you feel yourself steering into nothing.",
        "Then, you see something shining in the distance.",
        "You follow the light, the only option you have.",
        "It gets closer, revealing a bottle in the bottom of the ocean.",
        "An ancient bottle containing immense magic.",
        "You cannot swim to the bottom of the sea to get it.",
        "But with the help of a {}, you may be able to obtain it...".format(magic_orb.name)
    ]
})
volcanic_islands = area("volcanic_islands", "Volcanic Islands", " ", dragon_egg.key, {
    knight.key: [
        "Continuing forth, the fog seems to have dissipated along a rocky shore of steep islands.",
        "The Volcanic Islands are covered in torched rocks and hardened ash.",
        "You anchor the boat on the shore to explore further.",
        "Roars of dragons can be heard in the distance, streams of lava flowing through cracks on the ground.",
        "And in the very center of the island is a giant egg.",
        "It seems to have fallen from the dragon nest above.",
        "A plan goes through your mind. It is a dangerous one, but highly effective at best.",
        "Looking at the egg, you assess your options..."
    ],
    mage.key: [
        "Continuing forth, the fog seems to have dissipated along a rocky shore of steep islands.",
        "The Volcanic Islands are covered in torched rocks and hardened ash.",
        "You anchor the boat on the shore to explore further.",
        "Roars of dragons can be heard in the distance, streams of lava flowing through cracks on the ground.",
        "And in the very center of the island is a giant egg.",
        "It seems to have fallen from the dragon nest above.",
        "A plan goes through your mind. It is a dangerous one, but highly effective at best.",
        "Looking at the egg, you assess your options..."
    ],
    archer.key: [
        "Continuing forth, the fog seems to have dissipated along a rocky shore of steep islands.",
        "The Volcanic Islands are covered in torched rocks and hardened ash.",
        "You anchor the boat on the shore to explore further.",
        "Roars of dragons can be heard in the distance, streams of lava flowing through cracks on the ground.",
        "And in the very center of the island is a giant egg.",
        "It seems to have fallen from the dragon nest above.",
        "A plan goes through your mind. It is a dangerous one, but highly effective at best.",
        "Looking at the egg, you assess your options..."
    ],
    warrior.key: [
        "Continuing forth, the fog seems to have dissipated along a rocky shore of steep islands.",
        "The Volcanic Islands are covered in torched rocks and hardened ash.",
        "You anchor the boat on the shore to explore further.",
        "Roars of dragons can be heard in the distance, streams of lava flowing through cracks on the ground.",
        "And in the very center of the island is a giant egg.",
        "It seems to have fallen from the dragon nest above.",
        "A plan goes through your mind. It is a dangerous one, but highly effective at best.",
        "Looking at the egg, you assess your options..."
    ]
})
shadow_lands = area("shadow_lands", "Shadow Lands", empty_knight.key, ominous_key.key, {
    knight.key: [
        "You run to the boat, retreating from the dragon-infested islands.",
        "Setting sail, you once again enter deep black fog.",
        "It is even denser than before, all seeming to emanate from one location.",
        "The deeper you enter the fog, the more reality sets in.",
        "Soon, strong freezing winds rock the boat in giant waves.",
        "Thunder roars, and lightning strikes in the ocean.",
        "Yet no rain falls.",
        "And with a sudden crash, the boat hits shore.",
        "A small island in a dark, corrupted world.",
        "No birds, no sound, just silence...",
        "Corrupted Bodies of knights, and horses litter the island.",
        "All of them surrounded by clouds of black fog.",
        "\nBreathing in a shaky breath, You walk up to the giant castle with your sword in hand.",
        "Right before the door, you see the armor of a knight",
        "It looks hollow... yet somehow not empty.",
        "You look closer, seeing a corrupted husk of a man. His body consumed by shadows.",
        "You are taken aback, when he opens one of his eyes..."
    ],
    mage.key: [
        "You run to the boat, retreating from the dragon-infested islands.",
        "Setting sail, you once again enter deep black fog.",
        "It is even denser than before, all seeming to emanate from one location.",
        "The deeper you enter the fog, the more reality sets in.",
        "Soon, strong freezing winds rock the boat in giant waves.",
        "Thunder roars, and lightning strikes in the ocean.",
        "Yet no rain falls.",
        "And with a sudden crash, the boat hits shore.",
        "A small island in a dark, corrupted world.",
        "No birds, no sound, just silence...",
        "Corrupted Bodies of knights, and horses litter the island.",
        "All of them surrounded by clouds of black fog.",
        "\nBreathing in a shaky breath, You walk up to the giant castle, your wooden staff in hand.",
        "Right before the door, you see the armor of a knight",
        "It looks hollow... yet somehow not empty.",
        "You look closer, seeing a corrupted husk of a man. His body consumed by shadows.",
        "You are taken aback, when he opens one of his eyes..."
    ],
    archer.key: [
        "You run to the boat, retreating from the dragon-infested islands.",
        "Setting sail, you once again enter deep black fog.",
        "It is even denser than before, all seeming to emanate from one location.",
        "The deeper you enter the fog, the more reality sets in.",
        "Soon, strong freezing winds rock the boat in giant waves.",
        "Thunder roars, and lightning strikes in the ocean.",
        "Yet no rain falls.",
        "And with a sudden crash, the boat hits shore.",
        "A small island in a dark, corrupted world.",
        "No birds, no sound, just silence...",
        "Corrupted Bodies of knights, and horses litter the island.",
        "All of them surrounded by clouds of black fog.",
        "\nBreathing in a shaky breath, You walk up to the giant castle, your longbow in hand.",
        "Right before the door, you see the armor of a knight",
        "It looks hollow... yet somehow not empty.",
        "You look closer, seeing a corrupted husk of a man. His body consumed by shadows.",
        "You are taken aback, when he opens one of his eyes..."
    ],
    warrior.key: [
        "You run to the boat, retreating from the dragon-infested islands.",
        "Setting sail, you once again enter deep black fog.",
        "It is even denser than before, all seeming to emanate from one location.",
        "The deeper you enter the fog, the more reality sets in.",
        "Soon, strong freezing winds rock the boat in giant waves.",
        "Thunder roars, and lightning strikes in the ocean.",
        "Yet no rain falls.",
        "And with a sudden crash, the boat hits shore.",
        "A small island in a dark, corrupted world.",
        "No birds, no sound, just silence...",
        "Corrupted Bodies of knights, and horses litter the island.",
        "All of them surrounded by clouds of black fog.",
        "\nBreathing in a shaky breath, You walk up to the giant castle, your iron axe in hand.",
        "Right before the door, you see the armor of a knight",
        "It looks hollow... yet somehow not empty.",
        "You look closer, seeing a corrupted husk of a man. His body consumed by shadows.",
        "You are taken aback, when he opens one of his eyes..."
    ]
})
# Dark Castle is the final room in the game.
dark_castle = area("dark_castle", "Dark Castle", shadow_lord.key, " ", {
    knight.key: [
        "Entering the castle, you ready your sword.",
        "A black silhouette of a robe can be seen sitting on a throne in the main hall.",
        "Darkness swirls around him.",
        "It seems The Shadow Lord has been waiting..."
    ],
    mage.key: [
        "Entering the castle, you ready your magic.",
        "A black silhouette of a robe can be seen sitting on a throne in the main hall.",
        "Darkness swirls around him.",
        "It seems The Shadow Lord has been waiting..."
    ],
    archer.key: [
        "Entering the castle, you ready your aim.",
        "A black silhouette of a robe can be seen sitting on a throne in the main hall.",
        "Darkness swirls around him.",
        "It seems The Shadow Lord has been waiting..."
    ],
    warrior.key: [
        "Entering the castle, you ready your axe.",
        "A black silhouette of a robe can be seen sitting on a throne in the main hall.",
        "Darkness swirls around him.",
        "It seems The Shadow Lord has been waiting..."
    ]
})

# The reference map of all the areas in the game.
areas = {
    kingdom.key: kingdom,
    castle.key: castle,
    dungeon.key: dungeon,
    kingstown.key: kingstown,
    deep_woods.key: deep_woods,
    steep_hills.key: steep_hills,
    peaks.key: peaks,
    lost_shore.key: lost_shore,
    forbidden_sea.key: forbidden_sea,
    volcanic_islands.key: volcanic_islands,
    shadow_lands.key: shadow_lands,
    dark_castle.key: dark_castle
}


# Creates a modifiable dictionary of an area on a map
# Adds directional parameters for the area to link it with other areas.
def create_area(area_type: area, north: str, south: str, east: str, west: str):
    ent = str(area_type.ent)
    itm = str(area_type.itm)
    if not ent.isspace():
        ent = create_entity(entities[ent])
    else:
        ent = None
    if not itm.isspace():
        itm = [items[itm]]
    else:
        itm = None
    return {
        "key": area_type.key, "name": area_type.name, "entity": ent, "item": itm, "narration": area_type.narration,
        "north": north, "south": south, "east": east, "west": west
    }


# Creates a new instance of the game's map using the function above
def create_game_map():
    return {
        kingdom.key: create_area(kingdom, castle.key, deep_woods.key, kingstown.key, steep_hills.key),
        castle.key: create_area(castle, " ", kingdom.key, dungeon.key, " "),
        dungeon.key: create_area(dungeon, " ", kingstown.key, " ", castle.key),
        kingstown.key: create_area(kingstown, dungeon.key, lost_shore.key, " ", kingdom.key),
        deep_woods.key: create_area(deep_woods, kingdom.key, " ", lost_shore.key, steep_hills.key),
        steep_hills.key: create_area(steep_hills, peaks.key, deep_woods.key, kingdom.key, " "),
        peaks.key: create_area(peaks, " ", steep_hills.key, " ", " "),
        lost_shore.key: create_area(lost_shore, kingstown.key, forbidden_sea.key, " ", deep_woods.key),
        forbidden_sea.key: create_area(forbidden_sea, lost_shore.key, volcanic_islands.key, " ", " "),
        volcanic_islands.key: create_area(volcanic_islands, forbidden_sea.key, shadow_lands.key, " ", " "),
        shadow_lands.key: create_area(shadow_lands, volcanic_islands.key, dark_castle.key, " ", " "),
        dark_castle.key: create_area(dark_castle, " ", " ", " ", " ")
    }


# ****************** COMMANDS AND I.O. ******************
# Commands are a named tuple that takes in the display name, and a list of inputs
command = namedtuple("Command", ['name', 'commands'])
main_command = command("Main", ["inv", "health", "map", "partner", "stats"])
config_command = command("Config", ["config"])
move_command = command("Move", ["north", "south", "east", "west"])
bool_command = command("Boolean", ["y", "n", "yes", "no"])
battle_command = command("Battle", ["fight", heavenly_sword.key, ancient_potion.key, food_basket.key, dragon_egg.key,
                                    magic_orb.key])
create_plr_command = command("Player Creation", [knight.key, mage.key, archer.key, warrior.key])


# just print(), followed by a time.sleep delay dependent on the config option "print_speed"
def delay_print(*outputs):
    print(*outputs)
    time.sleep(config["print_speed"])


# Prints an input prompt, delays, then returns the input
def print_command(output: str):
    com = input(output + "\n")
    time.sleep(config["print_speed"])
    if com.lower() == "quit":
        delay_print("Exiting the game...")
        time.sleep(0.8)
        sys.exit()
    return com


# Narrates a list of strings, then appends the key "__READ__" at the end of the list
# the key is used to check if a narration is read or not.
def narrate(narration: list):
    if "__READ__" not in narration:
        for n in narration:
            delay_print(n)
        narration.append("__READ__")
        return True
    return False


# Checks if the narration contains "__READ__"
# Used so the game does not repeat narrations.
def check_if_read(narration: list):
    return "__READ__" in narration


# Handles the Main Commands, and returns nothing, so the game will prompt the original command again.
def handle_main_commands(com_input, plr: dict, game_map: dict):
    if plr is None:
        return None
    if com_input == "inv":
        delay_print("Inventory:", plr["inv"])
    if com_input == "health":
        print("Health: {}/{}".format(plr["health"], plr["max_health"]))
    if com_input == "stats":
        delay_print("Player Stats:")
        print("\tType:", plr["name"])
        print("\tHealth: {}/{}".format(plr["health"], plr["max_health"]))
        print("\tAttack Damage:", plr["attack"])
        print("\tMagic Damage:", plr["magic"])
        print("\tSwiftness:", plr["swift"])
        print("\tAccuracy:", plr["accuracy"])
        print("\tInventory:", plr["inv"])
        prt = plr["partner"]
        if prt != {}:
            delay_print("." * 48)
            delay_print("Partner Stats:")
            print("\tName:", prt["name"])
            print("\tHealth: {}/{}".format(prt["health"], prt["max_health"]))
            print("\tAttack Damage:", prt["attack"])
            print("\tMagic Damage:", prt["magic"])
            print("\tSwiftness:", prt["swift"])
            print("\tAccuracy:", prt["accuracy"])
    if com_input == "partner":
        prt = plr["partner"]
        if prt != {}:
            delay_print("Partner Stats:")
            print("\tName:", prt["name"])
            print("\tHealth: {}/{}".format(prt["health"], prt["max_health"]))
            print("\tAttack Damage:", prt["attack"])
            print("\tMagic Damage:", prt["magic"])
            print("\tSwiftness:", prt["swift"])
            print("\tAccuracy:", prt["accuracy"])
    if com_input == "map":
        traveled = plr["map"]
        delay_print("Your Current Map:")
        for place in traveled:
            map_area = areas[place]
            print(map_area.name)
            for i in move_command.commands:
                value = game_map[map_area.key][i]
                if not value.isspace() and value not in traveled:
                    value = "?"
                if value.isspace():
                    value = "-"
                print("\t{} of {}: {}".format(
                    i.capitalize(),
                    map_area.name,
                    areas[value].name if areas.get(value) is not None else value
                ))

    return None


# Handles all commands in the game, and returns the value of the input dependent on the type of command.
# For example, if the command is a bool command, the values will be either true or false.
# Will return nothing if the player's input is invalid.
def handle_command(com: command, com_input: str, plr: dict | None, game_map: dict | None, current_area: str | None):
    if com is None:
        return None
    low_com = com_input.lower()
    if low_com in config_command.commands and com != config_command:
        update_config()
        return None
    if low_com in main_command.commands:
        if plr is not None and game_map is not None:
            return handle_main_commands(low_com, plr, game_map)
        return None
    if low_com not in com.commands:
        delay_print("\nInvalid Command.")
        format_com = "{}".format(com.commands)[1: -2].replace("\'", "")
        delay_print("Valid {} Commands are:".format(com.name))
        delay_print(format_com)
        return None
    if com.name == "Boolean":
        if "y" in low_com:
            return True
        if 'n' in low_com:
            return False
    if com.name == "Move":
        if current_area is not None:
            return game_map[current_area][low_com]
    return low_com


# ****************** EVENTS ******************
# Events are actions within the game, and determines storytelling and game progression.

# Move event prompts the player to move between different areas.
# Checks if the directional input is valid and the player can move in that direction.
# If the player can move there, returns the new area on the game's map.
# If the player cannot move in that direction, returns nothing.
def move_event(plr: dict, game_map: dict, current_area: str):
    c_input = print_command("Where should you travel?")
    c_value = handle_command(move_command, c_input, plr, game_map, current_area)
    if c_value is not None and not c_value.isspace():
        if c_value == forbidden_sea.key and current_area == lost_shore.key and abandoned_boat.key not in plr["inv"]:
            delay_print("You cannot enter {} without a boat...".format(forbidden_sea.name))
            return None
        if c_value == dark_castle.key and current_area == shadow_lands.key and ominous_key.key not in plr["inv"]:
            delay_print("The door to the {} cannot be opened without a key...".format(dark_castle.name))
            return None
        while True:
            delay_print("You are about to enter {}".format(areas[c_value].name))
            new_input = print_command("Should you enter?")
            new_value = handle_command(bool_command, new_input, plr, game_map, current_area)
            if new_value is None:
                continue
            if new_value is False:
                delay_print("You have traveled back to {}".format(areas[current_area].name))
                return current_area
            if new_value is True:
                if c_value not in plr["map"]:
                    plr["map"].append(areas[c_value].key)
                delay_print("You have entered {}".format(areas[c_value].name))
                return c_value
    if c_value is not None and c_value.isspace():
        delay_print("You cannot go in that direction.")
        return None


# A small event used to narrate an area using the narrate() function.
def narrate_area_event(plr: dict, current_area: dict):
    narration = current_area["narration"][plr["name"].lower()]
    return narrate(narration)


# A small event used to narrate entity dialogue.
# special_key is used to get a specific key in the entity's dialogue dictionary,
# instead of reading the default keys
def narrate_entity_event(plr: dict, current_area: dict, special_key=None):
    ent = current_area["entity"]
    if ent is not None:
        if special_key is not None:
            narration = ent["dialogue"][special_key]
        else:
            narration = ent["dialogue"][plr["name"].lower()]
        delay_print("{}:".format(ent["name"]))
        return narrate(narration)
    return False


# An event that prompts the player to take an item out of an area, and store in their inventory.
# Returns true or false whether the player chose to take the item or not.
def take_item_event(plr: dict, current_area: dict):
    itm = current_area["item"]
    if itm:
        itm_name = itm[0].name
        while True:
            c_input = print_command("Will you take the {}?".format(itm_name))
            c_value = handle_command(bool_command, c_input, plr, None, None)
            if c_value is None:
                continue
            if c_value:
                if itm_name == magic_orb.name:
                    plr["inv"].remove(magic_lily.key)
                    plr["inv"].remove(pearl_stone.key)
                plr["inv"].append(itm[0].key)
                current_area["item"].clear()
                delay_print("You added", itm_name, "to your Inventory.")
                return True
            if not c_value:
                delay_print("You refused to take the {}.".format(itm_name))
                return False


# An event that chooses if the player should use an item.
# Returns true or false dependent on if the player used the item or not.
def use_item_event(plr: dict, use_itm: item, current_area: dict):
    itm_key = use_itm.key
    itm_name = use_itm.name
    if itm_key in plr["inv"]:
        while True:
            c_input = print_command("Will you use the {}?".format(itm_name))
            c_value = handle_command(bool_command, c_input, plr, None, None)
            if c_value is None:
                continue
            if c_value:
                delay_print("You used the {}.".format(itm_name))
                break
            if not c_value:
                delay_print("You refused to use the {}.".format(itm_name))
                return False
        if itm_key in battle_command.commands and current_area == dark_castle.key:
            return True
        if itm_key == dungeon_key.key and current_area["key"] == dungeon.key:
            prt_list = partners[plr["name"].lower()]
            prt = create_entity(random.choice(prt_list))
            plr["partner"] = prt
            if config["read_dialogue"]:
                delay_print("\n" + ("*" * 48))
                delay_print("{}:".format(prt["name"]))
                narrate(prt["dialogue"][plr["name"].lower()])
            return True
    return False


# ****************** BATTLE EVENTS ******************
# Special events specifically used for battling the main villain.

# Handles the main battle of the game.
def battle_event(plr: dict, villain: dict):
    dragon_baby = None
    delay_print("\n")
    delay_print("." * 24, "BATTLE", "." * 24)
    while True:
        companion = plr["partner"]
        if plr["health"] <= 0:
            return False
        if villain["health"] <= 0:
            return True
        if companion is not None and companion["health"] <= 0:
            if magic_orb.key in plr["inv"]:
                plr["magic"] = plr["magic"] + 100
                plr["swift"] = plr["swift"] + 40
                if config["narrate_game"]:
                    narrate([
                        "." * 48,
                        "{} falls to their knees after {}'s attack.".format(companion["name"], villain["name"]),
                        "Then, they collapse to the floor. Their body consumed by the shadows.",
                        "You are now on your own, the fate of the world on your shoulders.",
                        "." * 48,
                        "The loss of your partner fills you with immense rage.",
                        "You feel a new type of strength flood through your veins.",
                        "You have unlocked a new power, and now you are the strongest you've ever been.",
                        "." * 48,
                        "*** Your Magic Damage has increased by 100 points! ***",
                        "*** Your Swiftness has increased by 40 points! ***"
                    ])
                    delay_print("." * 48)
            plr["partner"] = None
        print("\n")
        delay_print("*" * 18)
        delay_print("{}'s Health: {}/{}".format(plr["name"], plr["health"], plr["max_health"]))
        if companion is not None and companion["health"] > 0:
            delay_print("{}'s Health: {}/{}".format(companion["name"], companion["health"], companion["max_health"]))
        delay_print("Inventory:", plr["inv"])
        delay_print("*" * 18)
        delay_print("{}'s Health: {}/{}".format(villain["name"], villain["health"], villain["max_health"]))
        delay_print("*" * 18)

        c_input = print_command("Choose your next move:")
        if c_input.lower() == "fight":
            handle_battle_moves(plr, villain)
        else:
            use_item = items.get(c_input.lower())
            if use_item is not None and use_item.key in plr["inv"]:
                used_result = handle_battle_items(plr, use_item, companion, villain)
                if used_result is not None:
                    dragon_baby = used_result
        if companion is not None and companion["health"] > 0:
            handle_battle_moves(companion, villain)
            handle_battle_moves(villain, random.choice([companion, companion, companion, plr]))
        else:
            handle_battle_moves(villain, plr)

        if dragon_baby is not None and villain["health"] > 0:
            handle_battle_moves(dragon_baby, villain)


# Used to check damage on battle moves, and if an entity dodged an attack.
def handle_battle_moves(ent1: dict, ent2: dict):
    if ent1["health"] > 0 and ent2["health"] > 0:
        delay_print("\n")
        damage = ent1["attack"] + ent1["magic"]
        dodge = random.random() < float(ent2["swift"] / ent1["accuracy"])
        if dodge:
            delay_print("{} swiftly dodged {}'s attack!".format(ent2["name"], ent1["name"]))
        else:
            ent2["health"] = ent2["health"] - damage
            delay_print("{} dealt {} damage against {}!".format(ent1["name"], damage, ent2["name"]))


# Uses battle items in the game, and triggers their special functions.
def handle_battle_items(plr: dict, battle_item: item, companion: dict, villain: dict):
    damage = 0
    break_on_use = False
    dragon = None
    if battle_item.key == magic_orb.key:
        damage = random.choice([20, 25, 30, 35, 40, 45, 50]) + plr["magic"]
        damage = damage + companion["magic"] if companion is not None else damage
        delay_print("{} channeled the power of the {}!".format(plr["name"], battle_item.name))
    elif battle_item.key == heavenly_sword.key:
        damage = 200
        break_on_use = True
    elif battle_item.key == ancient_potion.key:
        break_on_use = True
        plr["health"] = plr["max_health"]
        if companion is not None and companion["health"] > 0:
            companion["health"] = companion["max_health"]
            delay_print("{e1} splashed the {i} on the ground, healing {e1}'s and {e2}'s wounds!"
                        .format(e1=plr["name"], i=battle_item.name, e2=companion["name"]))
        else:
            delay_print("{} drank {}, and regained full health!".format(plr["name"], battle_item.name))
    elif battle_item.key == food_basket.key:
        food_to_eat = random.choice(list(food.keys()))
        plr["health"] = min(plr["health"] + food[food_to_eat], plr["max_health"])
        if companion is not None and companion["health"] > 0:
            companion["health"] = min(companion["health"] + food[food_to_eat], companion["max_health"])
            delay_print("{} ate and tossed some {} to {}, and both regained {} health!"
                        .format(plr["name"], food_to_eat, companion["name"], food[food_to_eat]))
        else:
            delay_print("{} ate {}, and regained {} health!"
                        .format(plr["name"], food_to_eat, food[food_to_eat]))
    elif battle_item.key == dragon_egg.key:
        break_on_use = True
        dragon = create_entity(baby_dragon)
        delay_print("While fighting, {} fell from {}'s bag onto the ground, and hatched {}!"
                    .format(battle_item.name, plr["name"], baby_dragon.name))
    if damage > 0:
        villain["health"] = villain["health"] - damage
        delay_print("{} dealt {} damage against {}!".format(battle_item.name, damage, villain["name"]))
    if break_on_use:
        delay_print(battle_item.name, "has broken, and cannot be used again!")
        plr["inv"].remove(battle_item.key)
    return dragon


# ****************** GAME FUNCTIONS ******************
# Used to print game info and handle important functions,
# Like creating events, and choosing player types.

# Used to print the game's title.
def intro():
    delay_print("  _______ _            _____                   _    ____                 _   \n"
                " |__   __| |          |  __ \                 | |  / __ \               | |  \n"
                "    | |  | |__   ___  | |__) |___  _   _  __ _| | | |  | |_   _  ___ ___| |_ \n"
                "    | |  | '_ \ / _ \ |  _  // _ \| | | |/ _` | | | |  | | | | |/ _ / __| __|\n"
                "    | |  | | | |  __/ | | \ | (_) | |_| | (_| | | | |__| | |_| |  __\__ | |_ \n"
                "    |_|  |_| |_|\___| |_|  \_\___/ \__, |\__,_|_|  \___\_\\\\__,_|\___|___/\__|\n"
                "                                    __/ |                                    \n"
                "                                   |___/                                     ")
    print("\t\t        .---.        .---.\n"
          "\t\t       /     \  __  /     \\\n"
          "\t\t      / /     \(  )/     \\ \\\n"
          "\t\t     //////   ' \/ `   \\\\\\\\\\\\\n"
          "\t\t    //// / // :    : \\\\ \\ \\\\\\\\\n"
          "\t\t   // / /  /  `    '  \\  \\ \\ \\\\\n"
          "\t\t  //   /      //UU\\\\      \   \\\\\n"
          "\t\t               /||\\  \n"
          "\t\t              //||\\\\ \n"
          "\t\t              ''``''")
    delay_print("\n")
    delay_print()


# Narrates the story of the game
def tell_story():
    delay_print("*" * 80)
    narrate([
        "There are two kingdoms within this world.",
        "One is a bustling and rich Kingdom, full of prosperity.",
        "The other is in land far away...",
        "Across the Forbidden Sea, and through the Volcanic Islands of dragons.",
        "Yet despite the distance, this kingdom is wreaking havoc.",
        "Slowly corrupting this world into darkness.",
        "The Royal King knows that the world has a tainted future.",
        "He has no choice but to find the chosen one, and assign them a royal quest:",
        "To travel across the Forbidden Sea,",
        "Enter the Dark Castle,",
        "And defeat The Shadow Lord once and for all."
    ])
    delay_print("*" * 80)


# Miscellaneous function used to print out commands in show_instructions()
def format_commands(com: command):
    print()
    delay_print(com.name, "Command")
    delay_print("Inputs:", *com.commands)
    print()
    delay_print("*" * 24)


# Outputs the instructions and the commands of the game.
def show_instructions():
    print()
    delay_print("*" * 12, "HOW TO PLAY", "*" * 12)
    print()
    delay_print("Objective:")
    delay_print("Collect all the items in the game, before facing The Shadow Lord.")
    print()
    delay_print("Commands:")
    delay_print("*" * 24)
    format_commands(move_command)
    format_commands(bool_command)
    format_commands(main_command)
    format_commands(create_plr_command)
    format_commands(battle_command)
    print()
    delay_print("To exit the game, enter: quit")
    delay_print("To open the Game Options, enter: config")
    print()
    delay_print("*" * 48)
    print()


# Shows the possible player types to choose from, and their stats.
def show_player_types():
    delay_print()
    plr_types = [knight, mage, archer, warrior]
    for p in plr_types:
        delay_print("\t{}:".format(p.name))
        format_stat = "{stat:<16}{value:>8}"
        print(format_stat.format(stat="Max Health:", value=p.max_health))
        print(format_stat.format(stat="Attack Damage:", value=p.attack))
        print(format_stat.format(stat="Magic Damage:", value=p.magic))
        print(format_stat.format(stat="Swiftness:", value=p.swift))
        print(format_stat.format(stat="Accuracy:", value=p.accuracy))
        delay_print("")


# A separate command function used to choose a player's type based on the input.
# Returns nothing if the input is invalid.
def create_player(plr_type: str):
    if plr_type.lower() == "quit":
        delay_print("Exiting the game...")
        time.sleep(0.8)
        sys.exit()
    elif plr_type.lower() == "config":
        update_config()
        return None
    if plr_type.lower() in create_plr_command.commands:
        ent = players[plr_type.lower()]
        plr = create_entity(ent)
        plr['partner'] = {}
        plr['inv'] = []
        plr['map'] = []
        return plr
    delay_print("\nInvalid Command.")
    format_com = "{}".format(create_plr_command.commands)[1: -2].replace("\'", '')
    delay_print("Valid {} Commands are:".format(create_plr_command.name))
    delay_print(format_com)
    return None


# Chooses an event type based on the context of the game.
# Returns an integer that will determine the type of event it is for the new_event function.
def create_event(plr: dict, current_area: dict, last_event: int):
    ent = current_area["entity"]
    itm = current_area["item"]

    if config["narrate_game"]:
        if not check_if_read(current_area["narration"][plr["name"].lower()]):
            return 1
    else:
        current_area["narration"][plr["name"].lower()].append("__READ__")

    if ent is not None:
        if config["read_dialogue"]:
            if not check_if_read(ent["dialogue"][plr["name"].lower()]):
                return 2
        else:
            for key in ent["dialogue"]:
                ent["dialogue"][key].append("__READ__")
        if not plr["partner"] and dungeon_key.key in plr["inv"]:
            if current_area["key"] == dungeon.key and last_event != 4:
                return 4
        if current_area["key"] == dark_castle.key:
            return 5

    if itm and len(itm) > 0 and last_event != 3:
        it: item = items.get(itm[0].key)
        flag = True
        for i in it.required:
            if i not in plr["inv"]:
                flag = False
        if flag:
            if ent is not None and ent["name"] == elder_mage.name and not check_if_read(ent["dialogue"][magic_orb.key]):
                return 2
            return 3
    return 0


# Triggers a new event in the game based on the event type, and returns the value of the event.
def new_event(event_type: int, plr: dict, game_map: dict, current_area: dict):
    if event_type == 0:
        value = move_event(plr, game_map, current_area["key"])
        return value
    if event_type == 1:
        value = narrate_area_event(plr, current_area)
        return value
    if event_type == 2:
        flag = current_area["entity"] is not None and current_area["entity"]["name"] == elder_mage.name and \
               check_if_read(current_area["entity"]["dialogue"][plr["name"].lower()])
        value = narrate_entity_event(
            plr,
            current_area,
            magic_orb.key if flag and magic_lily.key in plr["inv"] and pearl_stone.key in plr["inv"] else None
        )
        return value
    if event_type == 3:
        value = take_item_event(plr, current_area)
        return value
    if event_type == 4:
        value = use_item_event(plr, items[areas[current_area["key"]].itm], current_area)
        return value
    if event_type == 5:
        value = battle_event(plr, current_area["entity"])
        return value


# Used to check the game's state based on game context.
# If it returns something other than zero, the game will end.
def check_game_state(plr: dict, event_type: int, current_event):
    if plr["health"] <= 0:
        return 2
    if event_type == 5 and current_event is True:
        return 1
    return 0


# Changes the values of the config dictionary at the beginning of the file.
# Prompts the player to input the values in game, and changes the dictionary based on the inputs.
def update_config():
    int_pattern = re.compile("^[0-9]*$")
    float_pattern = re.compile("^[0-9]*.[0-9]*$")  # Used to see if input is a float or int value.
    print()
    delay_print("Game Options:")
    delay_print("*" * 24)
    while True:
        com = print_command("Narrate Areas? yes/no")
        val = handle_command(bool_command, com, None, None, None)
        if val is None:
            continue
        config["narrate_game"] = val
        delay_print("Narrate Areas is set to:", val)
        break
    print()
    while True:
        com = print_command("Read Entity Dialogue? yes/no")
        val = handle_command(bool_command, com, None, None, None)
        if val is None:
            continue
        config["read_dialogue"] = val
        delay_print("Entity Dialogue is set to:", val)
        break
    print()
    while True:
        com = print_command("Print Speed (default is 0.8)").strip()
        val = float(com) if int_pattern.match(com) or float_pattern.match(com) else None
        if val is None:
            delay_print("Must input a decimal or integer value.")
            continue
        config["print_speed"] = val
        delay_print("Print Speed is set to:", com)
        break
    delay_print("*" * 24)
    print()


# ****************** CORE ******************
# Core functions for the game, like game loops.

# Creates a new game, and loops it.
def game():
    game_state = 0

    while True:
        com_input = print_command("\nChoose your type:")
        plr = create_player(com_input)
        if plr is not None:
            dialogue = players[com_input.lower()].dialogue
            for i in dialogue["art"]:
                print(i)
            delay_print(dialogue["start"][0], "\n")
            delay_print("*" * 5, "Game Starting", "*" * 5)
            game_map = create_game_map()
            current_area = game_map[kingdom.key]
            plr["map"].append(kingdom.key)
            last_event = -1
            while True:
                delay_print("\n" + ("*" * 48))
                event_type = create_event(plr, current_area, last_event)
                current_event = new_event(event_type, plr, game_map, current_area)

                if current_event is not None:
                    if event_type == 0:
                        current_area = game_map[current_event]

                last_event = event_type
                game_state = check_game_state(plr, event_type, current_event)
                if game_state != 0:
                    break
        else:
            continue

        break  # This break should only be reached when the game is finished.
    print()
    delay_print("*" * 8, "YOU {}!".format(game_states[game_state]).upper(), "*" * 8)


# The main game loop.
if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    intro()
    tell_story()
    show_instructions()
    while True:
        show_player_types()
        game()
        while True:
            delay_print("\n")
            com_in = print_command("Restart? yes/no")  # Has an option to restart
            com_val = handle_command(bool_command, com_in, None, None, None)
            if com_val is False:
                delay_print("Exiting the game...")
                time.sleep(0.8)
                sys.exit()
            if com_val is True:
                delay_print("." * 12, "Creating new Game!", "." * 12)
                break
