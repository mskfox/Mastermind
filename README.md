# Mastermind

This is a graphical implementation of the classic Mastermind game using Python
and Pygame. The game allows you to guess a secret colour code through multiple
attempts, receiving hints on how many colours and positions are correct.

## Table of Contents

- [Installation](#installation)
- [Running the Game](#running-the-game)
- [Game Description](#game-description)
- [Contributing](#contributing)
- [License](#license)

## Installation

Before running the game, ensure you have Python installed on your system. To
install the necessary dependencies, use the `requirements.txt` file provided in
the repository. You can install the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Running the Game

- `-fps`: Sets the frame rate of the game (default is 30).

## Game Description

### Objective

The objective of Mastermind is to guess a secret code consisting of a sequence
of colours. You have multiple attempts to guess the code, and after each guess,
you receive feedback indicating how many colours are correct and in the correct
position (white hints) and how many colours are correct but in the wrong
position (red hints).

### How to Play

1. **Select a colour**: Click on a colour from the toolbar on the right to select it.
2. **Place the colour**: Click on the slots in the current row to place the
selected colour.
3. **Submit Guess**: Once all slots in the current row are filled, the game will
provide feedback with hints.
4. **Hints**:
   - White hints indicate a correct colour in the correct position.
   - Red hints indicate a correct colour in the wrong position.
5. **Repeat**: Repeat the process until you guess the correct sequence or run out of attempts.

Toggle between dark and light themes by clicking the sun/moon button at the
bottom right.

## Contributing

We welcome contributions to the project! If you would like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes.
4. Submit a pull request with a description of your changes.

### Coding Standards

- Follow PEP 8 coding standards.
- Write clear and concise commit messages.
- Include comments and docstrings for better code understanding.

### Repo Activity

![Alt](https://repobeats.axiom.co/api/embed/b86a851650fff4ac693ab829f0a2d54b7ea228d9.svg "Repobeats analytics image")

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to reach out with any questions or suggestions. Enjoy playing Mastermind!