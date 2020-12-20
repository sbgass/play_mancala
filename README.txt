How to Run the Program: 

This program was written in python 3 and takes two input arguments to run. The game board prints to the terminal in each turn. 

The inputs are the player types and can be any of the following: human, random, minimax, alphabeta. 

For example, running the following command from the program's directory will start a new game between a human player as player one and a minimax player as player two: 

"python3 mancala.py human minimax"

Player Options: 
"Human" players require user input to play moves. 
"Random" computer players will play random moves in each turn. 
"Minimax" computer players use a fixed-depth MiniMax algorithm with a utility function to choose the best move in each turn. 
"Alphabeta" computer players use a the AlphaBeta pruning extension to the MiniMax algorithm to search to a greater depth. These players are, therefore, harder to beat than minimax. 




