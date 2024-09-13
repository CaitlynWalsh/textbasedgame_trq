# The Royal Quest: A Text-Based Game

Reccomended to run the game with the "Run" batch file to disable warnings.
This game was created for my "Introduction to Scripting" class for my IT certification at Southern New Hampshire University.

## Story Summary:

Inside the Game’s world, there are two kingdoms. One, the world’s bustling and rich Kingdom in which the player will start in. The other is in land far away across the Forbidden Sea, and through the Volcanic Islands of dragons. Yet despite the distance, this kingdom is wreaking havoc across the game’s world. The Royal King knows that the world has a tainted future, and has no choice but to assign the player a royal quest: to travel across the Forbidden Sea, enter the Dark Castle, and defeat The Shadow Lord once and for all.

## Game Map:

The map shown on the next page visualizes the world’s areas, and where they are located.

![image](https://github.com/user-attachments/assets/83595bb6-ba96-4675-bbf4-453e4acc8e2e)

## Game Objects and Events:
•	Items:

In the game, Items are part of a named tuple called “Item”, which store the item’s dictionary key, their display name in the game, and optional required items the player must have in order to obtain the item. Items are game objects that can be taken and stored in a player’s inventory.

•	Entities:

Entities are living beings in the game which can interact with each other. They derive from a named tuple named “Entity”, which takes the entity’s dictionary key, their display name, their max health, their attack damage, their magic damage, their swiftness, accuracy, and a dictionary containing the optional dialogue of the entity.
Health, Attack, Magic, Swift, and Accuracy stats affect a battle’s outcome within the game. Attack damage and Magic damage are the amount of health taken away from the opposing entity during a battle move, and an entity’s Accuracy and their opponent’s Swiftness will be calculated to determine the opponent’s chance to dodge battle moves.
Entities are created into a modifiable dictionary once the game initializes a new entity through a function, so their health and stats can be changed if needed.

•	Areas (Rooms):

Areas are a physical space to travel to within the game. Areas are created using a named tuple called “Area”, and require the dictionary key, the display name, an optional Entity, an optional Item, and a dictionary containing the area’s narrations for storytelling.
The game’s map creates a new instance of each area and turns them into a modifiable room using a function, as well as storing the keys of the rooms adjacent to it. That way, the game will know where the player can move to depending on the direction they travel. The game will also initialize new Entities and Items within that room.

•	Commands:

Commands are certain inputs players can choose from to communicate and progress through the game. Such as moving through the world, saying yes or no, battle commands, and so on. Commands are created by a named tuple called “Command”, which takes the command’s display name and a list of possible prompts for that command. 
Main commands are commands that can be executed during any point of the game, and have no impact on the gameplay. Main commands are only for game information, such as a player’s stats, their inventory or current health, their partner’s stats, or displaying the player’s personal map, and where areas they have discovered are located in the game.
Commands are executed through a function that takes in the command type, and the player’s input, as well as other necessary game objects. The input of the player is then determined if it matches any possible prompts for that command type. For example, if the player types “yes” or “no” for a Boolean command, it will execute properly. But if the player types something other than “yes” or “no”, it will not execute properly, and will prompt the player to enter a proper input.

•	Events:

Events are important functions within the game that control the game’s story progression and flow. Such events are moving between areas, picking up items, narrating the story, using items, the final battle, etc.
The game chooses an event by the context of the game’s last event, and the current location of the player. Event types are represented by integers, and the game creates a new event based on the integer. Events return values that affect certain variables within the game, such as changing the player’s current room, or removing an item from an area’s dictionary once the player has taken it. 
Events can also affect the ending of the game by changing the game’s state, an integer that represents if the game is still active, or has ended somehow, and if the player has won the game, lost the game, or has died by losing all their health. 

## Gameplay:

In the very beginning before the gameplay, the game will print out the title, the story of the game, and the instructions of the game, as well as the proper commands. Then, the player is prompted to choose their type. Player types include the Knight, Mage, Archer, and the Warrior type. Each type has its own storytelling, and affects other elements of the game such the player’s stats. Once chosen, the player will start in the Kingdom, and the game will narrate the story and prompt events moving forward.
Events depend on the area, including if the area has an entity or an item. If the area is undiscovered and newly traveled to by the player, the narration event will fire, and narrate the area’s story. The narration for a particular room is only printed once. If the area has both an entity and an item, the entity’s dialogue is printed before the player is prompted to take the area’s item. If all the possible events for the area are fired, then the move event will be chosen, and will let the player move between areas.
Certain areas require multiple items to unlock their item, and other areas require items to enter other rooms. For example, In the Stony Peaks, an entity named the Elder Mage will only give the player a Magical Orb if the player’s inventory contains the Magic Lily from the Deepwoods, and the Pearly Stone within the Steep Hills. Another example is the Forbidden Sea, which requires the Abandoned Boat from the Lost Shore to enter.
Each item has their own use within the game, and some will even help the player during the final battle with The Shadow Lord.

## Game Areas:

•	Kingdom:

No Entity. 
No Item.
Starting area of the game.

### •	Castle:

Entity: The Royal King.

Item: The Heavenly Sword.

The Heavenly Sword can be used once to deal immense damage to The Shadow Lord.

### •	Dungeon:

Entity: Royal Guard

Item: Dungeon Key

Dungeon key can be used in this area to unlock a companion for the player.

### •	Kingstown:

Entity: Old Townslady

Item: Food Basket

Food basket is reusable, and will regain random amount of health of the player and the companion when used in battle.

### •	Deepwoods:

No Entity.

Item: Magic Lily

Used to unlock Magical Orb from Elder Mage.

### •	Steep Hills:

No Entity.

Item: Pearly Stone

Used to unlock the Magical Orb from Elder Mage.

### •	Stony Peaks:

Entity: Elder Mage.

Item: Magical Orb

Magical Orb is used to fast-travel to areas the player has already been, and to randomly increase magic damage during a battle move.

### •	Lost Shore:

No Entity.

Item: Abandoned Boat

Abandoned Boat is used to travel across the Forbidden Sea.

### •	Forbidden Sea

No Entity.

Item: Ancient Potion

Ancient Potion can be used once to regain all of the player’s and companion’s health during the final battle. 

### •	Volcanic Islands:

No Entity.

Item: Dragon Egg

Dragon Egg can be hatched during battle, and create a new Entity called Baby Dragon, that can deal a small amount of damage to The Shadow Lord every round.

### •	Shadow Lands:

Entity: Empty Knight

Item: Ominous Key

Ominous Key is used to enter the Dark Castle.

### •	Dark Castle

Entity: The Shadow Lord

No Item.

The final battle. 

All the items in the world play a crucial role in defeating the main villain of the game: The Shadow Lord. If one item is not collected, there will be no way to win the game.

