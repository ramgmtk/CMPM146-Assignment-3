Programming Assignment 3: MCTS
Team Members: Rammohan Ramanathan, Emmanuel Butor

Description of Modified MCTS:
Modified MCTS differs from our Vanilla MCTS by its rollout strategy. 
While Vanilla simulates turns with random moves at each step to reach a finished board state, Modified makes educated guesses using a heuristic.

The rollout strategy is that instead of choosing a random move: 
1. Select at most 5 moves randomly at each step.
2. Of those 5 moves check which moves result in the next game state returning a point to either player. (e.g. they win the sub game inside the big game)
3a. Modified then selects moves that, for 1 step in a future, result in one of the nine tic tac toe games finishing.
3b. If a none of the 5 moves result in a finished sub game, return the first randomly selected move.
4. Keep simulating until a finished board state is reached, much like Vanilla.

The heuristic that is being used places weight on moves that on the next turn will result in the respective player gaining a point, or minimizing the point gap with the opponent.
At each step the weight is based on whose turn it would be for that move.
This means that the rollout assumes both players want to place moves that immediately result in them gaining a point during the next turn, or minimizing the opponents point gains.
This heurstic is very similar to what is used in the rollouts done by rollout_bot, but a prime differentiating factor is how moves are selected.
The number 5 is not chosen arbitrarily but rather, 5 moves cover the majority of spaces on a tic tac toe board.
Meaning we do not need to evaluate every possible move, but having at least five means the bot will cover enough ground to see if one moves results in them winning, or blocking an opponent.

