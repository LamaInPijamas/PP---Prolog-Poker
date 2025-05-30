# 🃏 Poker Game

## About

This is a **Poker game** that uses **Prolog** for the main logic like *generating the deck, shuffling, dealing cards, drawing cards, and hand evaluation*.  
You have to download Prolog yourself — I don’t care how, good luck.

You **must run the code from the `Core` directory**, because Prolog is a dumb, picky beast and throws errors otherwise.

For communication between Python and Prolog, we use a Python class called `Core` (in the `Core` directory), along with the `pyswip` library.  
The `Core` class is the foundation for building various game variants — check the `Variants` directory for examples.

There's also an **MCCFR AI algorithm** (currently broken) in the `AI` directory that uses PyTorch.  
To see how variants work, check `Example.py`.  
`Run.py` is for a Rails website (*I have no clue how Rails works. I only write Prolog and Python. Ask **LamasPajamas***).

---

## ✅ TODO

- [ ] Repair [`MCCFR.py`](./AI/MCCFR.py) — *Daynlight*
- [ ] Write [`Run.py`](./Run.py) — *LamasPajamas*
- [ ] Check for bugs
- [ ] Fix “no cards in deck” draw issue
- [ ] Implement payment system (I want some money ❤️)

---

## 🛠️ Installation

1. Install **Shity Prolog** from their [shiny site](https://www.swi-prolog.org/download/stable). Good luck.
2. Install **Python** from the [official site](https://www.python.org/downloads/).
3. Run the build script in `.Scripts` (it’ll create a virtual environment and install dependencies from `requirements.txt`).
4. Congrats, it’s installed. Now head to the [Usage](#usage-section-you-lazy-ass).

---

## 🚀 Usage

### More Important Stuff

- The `Core` class takes these parameters: `players`, `rounds`, `max_draw`  
  - **players**: List of players (1 to 10)  
  - **rounds**: Number of loops. For example, 2 rounds with players A and B means: A draws → B draws → A draws → B draws → end game.  
  - **max_draw**: Max number of cards a player can draw in one round.

- **MCCFR**: I’ll write about this after I fix it. It’s kinda dead right now.

### Less Important Stuff

- You can create your own poker variant based on the ones in `Variants`. Just understand how `Core` works — **read the code**, it's short, I swear.
- If you're lazy, just use an existing variant from the `Variants` directory and run `Example.py`.
- If you're **LamasPajamas**, run `.Scripts/Run.sh` — it’ll launch `Run.py` with Core and Prolog working.  
  (`Run.py` should handle the Rails stuff.)

---

## ✨ Features

### `Core` class

- **reset()**: Resets the game, creates a new deck, and deals new cards.
- **evaluate()**: Ends the game and returns a list of points.
- **draw(playerID, cardIndexesList)**: Draws new cards, replacing the given indexes.
- **getPlayersInfo()**: Returns info about all players and their current hands.

### `MCCFR` (WIP)

- Still broken. Will document after fixing.

---

## 📦 Dependencies

### Prolog

- `pyswip`

### MCCFR

- `torch`
- `matplotlib`

### Other

- `tqdm`
