|||| PROJECT9 PickMushrooms Game
|||| Fengshi Teng
|||| Nov 18, 2024

README

This program is written in Jack as part of the NAND2Tetris course.
It implements a game called PickMushrooms, where the player controls a rabbit
to collect mushrooms while avoiding poisonous ones. The game is designed for
the Hack computer architecture and uses object-oriented programming concepts in
Jack language.

The project includes several .jack files that define the game’s core logic, 
graphics, and utility classes.

How to Run the Program

	1 Decompress the provided .zip file containing the Jack files.
	2 Compile the .jack files into .vm code.
	3 Load the compiled .vm files into the Hack virtual machine.
	4 Run the program and follow the on-screen instructions.

Game Objective

	• Win Condition:
	Collect 5 good mushrooms to win.
	• Lose Condition:
	Touch a poisonous (black) mushroom.
	• Controls:
	Use the arrow keys on the keyboard to move the rabbit.

Features
	1 Object-Oriented Design:
	• The game uses Jack’s class-based structure to manage objects like th
 	  rabbit, mushrooms, and game logic.
	• Each object has its own properties and methods for drawing, erasing,
	  and updating its state.
	2 Random Mushroom Generation:
	• Mushrooms are dynamically created with randomized positions and statuses
	  (poisonous or good).
	3 Collision Detection:
	  The game checks for collisions between the rabbit and mushrooms to
	  update the score or trigger a loss condition.
	4 Interactive Gameplay:
	  Real-time movement using the keyboard.
	  The game displays text instructions and dynamically updates the screen
	  based on player input.

Workflow
	1 Game Initialization:
	  The game starts with instructions displayed on the screen.
	  Players can press any key to start.
	2 Gameplay Loop:
	  The rabbit moves based on player input.
	  The game dynamically updates mushrooms' positions and statuses.
	  Collision detection is performed on each frame.
	3 Game End:
	  If the player collects 5 good mushrooms, a “You Win!” message is
	  displayed.
	  If the rabbit touches a poisonous mushroom, the game ends with a 
	  “Game Over” message.

Enjoy playing PickMushrooms!