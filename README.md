# Multi-Game Platform (Uni Project)

## Description:

First Game: "Des chiffres et des lettres" is a popular TV game show consisting of several rounds:

First Game: "Le Mot Le Plus Long" is a web implementation of the classic game where players try to form the longest word from a set of letters. The project is written in Python and uses the Flask framework for web interface management. This project also includes a local version that allows playing from the terminal, connected to online players.

Second Game: "Le compte est bon" is a game where players have 6 numbers and basic operations such as addition, subtraction, multiplication, and division. Players must use each number at most once to form, through successive operations, a number that comes as close as possible to the target number.

Second Game:
"Opti'Mot" is an interactive online word game that challenges players to form words from letters arranged in a vertical column. The project is also written in Python and uses the Flask framework for web interface management. Real-time communication between the server and clients is handled by Socket.IO, allowing players to interact instantly and share game updates without reloading the page. The user interface is created with HTML, CSS, and JavaScript, providing a visually pleasing and responsive experience. The game also uses a dictionary file (ODS9.txt) to validate words proposed by players. Thanks to this architecture, OptiMot offers a smooth and engaging gaming experience.

Third Game:
"BananaGrams" is also a word game played on a board with 144 tiles. Three game modes are available:

- Banana Solitaire: Play alone. You receive a draw of 21 letters and your goal is to form horizontal and vertical words connected to each other. You can draw a letter if you are stuck.
- Chrono Banana: Play with multiple players. The first one to finish their grid wins.
- Banana Café: Play with multiple players on a shared grid. The first player to place all their letters wins. Exchanging one tile for three is possible.
  
## Features:
- **Player Managment :**A `Joueur` class models players and their parameters..
- **Game Mechanics :** All functions related to game logic are grouped in the `Jeu.py` file containing the JeuMotPlusLong, JeuOptiMot, JeuBanana, JeuLeCompteEstBon classes.
- **Web Version:** The `serveur.py`file manages connections, Flask routes, and HTML templates.
- **Local Version :** The `Jeu_Local.py`file allows a player to participate in the game from the terminal while playing against players connected via the web interface or other terminals.

## Project Structure:

```
.
├── Joueur.py       # Class to model players
├── Jeu.py          # Main functions for Le Mot Le Plus Long
├── Jeu_OptiMot.py  # Main functions for Opti'Mot
├── serveur.py      # Flask server managing the web interface and connections
├── Jeu_Local.py    # Terminal interface to play on the server from the terminal
├── templates/      # HTML files for the user interface
└── README.md       # Project documentation
```

## Required Installations

## Usage:
```bash
pip install -r requirements.txt
```

### Web Version:
1. Start the server:
   ```bash
   python serveur.py
   ```

2. Access the game from your browser at the server address:
   Example: [http://192.168.1.43:8888/](http://192.168.1.43:8888/)


### Local Version:
1. Start the server:
   ```bash
   python serveur.py
   ```
2. Run the `Jeu_Local.py`file in another terminal:
   ```bash
   python Jeu_Local.py
   ```

3.Enter the server IP address. Example: `192.168.1.43`

4. Follow the instructions in the terminal to play

## Functionality

### `Joueur.py` file:
The file contains the `Joueur` class, which models the properties and behaviors of players, such as their name, score, proposals,...

### `Jeu.py` file:
The `jeu.py` file groups all the main functionalities necessary for the smooth running of the different games offered. It includes key classes and methods that ensure the management of each game stage, such as the random generation of letters from a tile bag, drawing letters for players, finding the longest word (motMax) in some variants, comparing words submitted by players to validate their authenticity and compliance with the dictionary, score management, including awarding points based on player performance, and saving player proposals, allowing tracking of moves made.

This file also contains the JeuBanane class, which centralizes the logic of the three versions of the Bananagrams game: Banana Solitaire, Banane Café, Chrono Banana.
These three versions have been integrated into a single class because they rely on similar mechanisms, such as letter management, word validation, and board verification. This allows code sharing while preserving the specificity of each variant.

### Flask Server `serveur.py`:
This file manages:
- Route management (e.g., displaying the home page, displaying the board, managing letter draw buttons, and displaying player rankings).
- Calls to different functions in the Jeu.py and Jeu_OptiMot.py files
- Rendering HTML templates for the user interface.

Note: the Opti'Mot game is a work in progress, the file includes registration to connect to the game with a maximum number of players but it is not yet playable.

### `Jeu_Local.py` file:
This file allows playing from the terminal by connecting to the server, the player can join the same game as other web players. It also allows communication with the server to synchronize game actions.

### `Jeu_OptiMot.py` file:
This file groups some main functions of the game, such as distributing cards to players and on the board, placing letters in the board columns to form words, checking the validity of the written word, covering letters, and the ability to discard and draw one or more cards.


### `bananaSolver.py` file:
This file contains a bananaSolver(tirage) function that takes a string of letters as input and generates a grid as a list of lists. Each cell in this grid represents either a letter from the draw or an empty cell (indicated by a '.'). The goal of this function is to find a letter arrangement that respects the game rules while being as optimal as possible. To test the performance of this solution, time measurements will be taken on draws of various sizes. The project is organized independently and contains a requirements.txt file listing the necessary dependencies for running the solver. This code has been designed to be easily integrated into a test environment to validate its efficiency.




