# GuessMe - A Number Guessing Game

This is a fun, simple number guessing game built using [Flet](https://flet.dev/), a Python web framework. The game challenges the player to guess a random number between 1 and 100, while maintaining a consecutive score and tracking high scores.

## Features
- **Consecutive Scoring**: The game keeps track of how many correct guesses you can make in a row.
- **High Score Tracking**: Achieve a high score and save your name to the leaderboard!
- **Lives System**: You have 5 lives. Incorrect guesses reduce your lives, and the game resets when you run out.
- **Hints**: Receive helpful hints on whether to guess higher or lower after each incorrect guess.
- **Randomized Target Number**: After each correct guess, a new number is randomly selected.

## Requirements
- Python >= 3.12
- Flet >= 24.1

## Running the Game
To start the game, simply run the main Python file:
```bash
python main.py
```
## Game Interface
1. Input your guesses in the `TextField`.
2. Click `Guess!` to submit your guess.
3. The game will provide hints whether your guess is too high or too low.
4. The consecutive score and high score will be displayed on the screen.
5. Once the game ends (when your lives `❤️` reach 0), your high score can be saved.

## Contributing
Feel free to fork the repository, submit issues, or make pull requests if you'd like to contribute to the game!