# alexiaventuratexasholdemICS33
This was my final project for the intermediate Python programming class I took at UCI (called ICS 33). I created a Texas Hold 'Em game that a human can play with bot players. This game can be played through a simple GUI and the bot players make decisions based on the game environment.

The information in this project's README file is below:

# README file for Alexia Ventura's ICS 33 Project Program, implementing both Option 1 (GUI) and Option 2 (smarter bots).

Version of Python used for this project: Python 3.8.2

Source used for Markdown language (I was told in office hours to use this for the README file):
https://www.markdownguide.org/basic-syntax/

# File Names

texasholdemgameUI.py (contains the code for creating the GUI)

Project_Alexia_Ventura.py (contains the code that creates players and the deck of cards, checks
for winners and best-possible hands, and adjusts players' status and money during the game based
on their choices)

# Summary Of The Program

The purpose of this program is to create a Texas Hold 'Em game that is played in a GUI
and has smarter bot players (meaning that their decisions are influenced by the conditions
of the game).

# Important Notes For The User

I requested an extension and Lu approved it. Because Brooke told me to submit a screenshot
of the email confirming the extension approval, I included it in my zip file. The screenshot
name is "ICS 33 Project Extension Request Screenshot".

Option 1 (creating a GUI) was the primary option I chose to implement, especially because it
was the one I worked on first. I added Option 2 (smarter bot players) in to attempt to improve
my program and get some extra credit.

There may be occasional bugs that cause the program to not work, specifically
when interacting with the GUI. It is very infrequent, however. I noticed that sometimes there's
a specific bug with clicking the Check button, which prevents the game from continuing because
the window won't update correctly. If that or any similar bug happens, just try restarting the
program from the command line. Having trouble with the GUI, from my own testing, is rare.

Also note that when you try to submit a value that is not acceptable (a number of bots or
a money amount that is invalid), nothing should happen when you click the submit button. If
you have the shell or Command Prompt open, you may see an AssertionError, which means the
program is working correctly. (However, the user isn't supposed to be looking at it because
this program uses a GUI) If you submitted an invalid value, change the value so it's valid and 
then resubmit. The instructions for running this program will explain what values are valid.

# How Bot Players Are Smarter

The names of the functions used for creating these smarter bots are: decision_criteria, 
bot_bet, bot_logic. They are in the Project_Alexia_Ventura.py file.

decision_criteria has the conditions for what causes a bot to fold, bot_bet is used to
pass in the correct arguments for bot_logic, and bot_logic adjusts the bot's money amount 
depending on their hand and which round they're playing in.

Bots are smarter because their decisions depend on the hand they have and how many players are
still playing in Round 2. Comments in the smart bot functions go into more detail about what
specifically happens to avoid making this README too long, as well as to make it easier to
see what code corresponds with what makes the bot smarter. In general, bots bet more money the
better their hand is. For high cards specifically, they may cause the bot to fold or check in Round
1, or bet in Round 2 depending on how many players are continuing to play. This follows what a human
player would probably do: if they have a potentially good hand in Round 1, they check to see whether
their hand may be better in Round 2. They fold if they think their hand isn't going to improve in the
game. They bet much more money with a royal flush than a pair.

On the GUI, the human user will only see whether the bot players folded or not. They will not see
the bot players' cards nor how much money they bet (if any) until the end of the game, where the
bot players' final adjusted money amounts and their hands (if they didn't fold in Round 2) are 
displayed.

# How To Run This Program

(Note that Round 1 shows the first three community cards, Round 2 shows the last two community cards)

IMPORTANT: Make sure you download the texasholdemgameUI.py and Project_Alexia_Ventura.py files, and
put them in the same folder! This is because although texasholdemgameUI.py is the file you'll run directly,
this file also uses code from Project_Alexia_Ventura.py.

1) Run the texasholdemgameUI.py file program with a command line (after locating the
correct directory, type "python texasholdemgameUI.py" without the quotation marks).
A window with a green background should show up with the following displayed: a "How 
many bot players do you want to play with?" label, a text box, and a "Submit Number of 
Bots" button). Expand the window to help with seeing everything on it.

2) In the text box, type in a integer between 2 and 4 inclusive for the number of bots.
This was a condition set for minimum and maximum bot players to make the labels easier to
display on the GUI window, as well as to avoid making the game too overwhelming for the
human player. Click the "Submit Number of Bots" button. (If you click the "Submit Number
of Bots" button and nothing happens on the GUI window, it is probably an error with your
input; just try again with a correct input.)

3) If you submitted correct input for the number of bots, you should see the following:
labels showing all players' starting money amounts for the game, the player ID(s) of the
bot player(s), the first three community cards, your player's information (player ID,
two cards combined with the three community cards for readability, and best rank from
that 5-card hand), and which bot players decided to not fold in Round 1 (indicated 
by "These bot players chose to continue in Round 1"). You should also see
the question about whether you want to bet, fold, or check, with the buttons displayed
to make these choices.

4) If you choose to bet, you will see the question "How much do you want to bet?" You
can't bet less than $1, can only bet in integer amounts, and can't bet more money than
what you have. If you choose to check, your money amount won't change and the game continues
including you. If you fold, the rest of the game happens without you.

5) Once you make your decision in Round 1, the last two community cards will be displayed
for Round 2. Just like in Round 1, the bot players who want to fold will, and the human
player again will be asked to bet their chosen amount of money (as long as it is valid) 
or fold.

6) The prize money, the winner(s), information about the bot players who didn't fold in
Round 2, and the new amounts of money for each player will be displayed to conclude Round 2.
The bot player information includes the 7 cards (5 community cards and the player's 2 cards)
used to figure out the bot player's best rank, and the rank that was determined to be the best.

7) The human player will be asked if they want to play again with the same players or
start over, with the buttons for each choice. If the human player chooses "Play With
Same Players," the current window will close and a new one will open, showing the same
content again as before except the players' starting money will be the same as the
previous game's. If the human player chooses "Start Over," the current window will close
and a new one will open, but the human player will be asked to choose a new number of bot
players, and the history of any previous games will be erased.

8) To completely stop playing any Texas Hold 'Em games, click the "X" button at the top
right-hand corner of the window.
