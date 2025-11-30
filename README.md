# 🧠 Minesweeper AI

An AI agent that plays the classic **Minesweeper** game using propositional logic, knowledge-based inference, and constraint satisfaction techniques.

This project is part of **CS50's Introduction to Artificial Intelligence with Python** and showcases reasoning under uncertainty, structured knowledge representation, and algorithmic problem-solving.

---

## 📁 Project Structure

```
minesweeper/
├── assets/                 
├── minesweeper.py          # Game logic + AI implementation
├── runner.py               # CLI runner to play or observe AI
├── requirements.txt        # Dependencies
└── test_minesweeper.py     # Debugging tool
```

---

## 🚀 Overview

The project contains:

- A full **Minesweeper game engine**
- A **Sentence** class representing logical constraints
- A **MinesweeperAI** class that infers safe moves and mines
- A **runner script** to observe the AI playing
- **Unit tests** verifying state updates and inference correctness

The AI deduces information logically rather than guessing randomly.

---

## 🧩 How the AI Works

### 1. Knowledge Representation  
The AI stores logical constraints as sentences.  
Each sentence looks like:

```
{(x1, y1), (x2, y2), (x3, y3)} = 2
```

Meaning:  
> *Exactly 2 of these cells contain mines.*

### 2. Inference  
The AI infers:

- **Known mines** if `len(cells) == count`
- **Known safe cells** if `count == 0`
- **New sentences** when an existing sentence is a subset of another

Example:

```
{A, B, C} = 2  
{A, B}    = 1
-------------
{C}       = 1   → C is a mine
```

### 3. Knowledge Updating  
When the AI clicks a safe cell:

1. Records the move  
2. Marks it as safe  
3. Creates a new logical sentence from its neighbors  
4. Updates all sentences  
5. Applies inference until no new information can be derived  

### 4. Choosing Moves  
The agent will always choose:

- A **safe move**, if one is known  
- Otherwise a **random unplayed cell**

---

## ▶️ Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the game:

```bash
python runner.py
```

You can modify the board size or number of mines inside `runner.py`.

---

## 🧪 Testing

> **Note:** The `test_minesweeper.py` file is not a formal unit test suite.  
> It is a debugging tool I created to visualize game states and AI decisions directly in the terminal using ASCII rendering.  
> It allows me to run controlled scenarios with fixed parameters without using `runner.py`, making it easier to inspect and verify the AI’s logic during development.

---

## 🧠 Skills Demonstrated

This project demonstrates:

- **Python OOP**
- **Logical inference & propositional logic**
- **Constraint satisfaction**
- **Game state modeling**
- **Algorithm design**
- **Testing and debugging**

---

## 📌 Possible Future Enhancements


- Add  **Unit tests for core logic**  
- Add a **probability-based AI** for the guessing stage  
- Add logs showing the inference process step-by-step  

---

## 🏷 License

This project is open-source and available under the MIT License.
