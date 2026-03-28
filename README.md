# ♟️ Chess Royale AI

A Python-based Chess game with an AI opponent powered by the Stockfish engine. This project combines game logic, a graphical interface using Pygame, and an external chess engine to create an interactive chess-playing experience.

---

## 🚀 Features

* ♟️ Fully functional chess game
* 🤖 AI opponent using Stockfish
* 🎮 Graphical interface built with Pygame
* 🔄 Move validation and game rules implemented
* 🧠 Basic AI integration for smart moves

---

## 🛠️ Tech Stack

* Python
* Pygame
* Stockfish (external chess engine)

---

## 📂 Project Structure

```
Chess_Royale_AI/
│
├── ChessMain.py        # Main game loop
├── ChessEngine.py      # Game logic and rules
├── aibot.py            # AI integration with Stockfish
├── images/             # Chess piece images
├── .gitignore
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository

```
git clone https://github.com/karina202330/Chess_Royale_AI.git
cd Chess_Royale_AI
```

### 2. Install dependencies

```
pip install pygame
```

### 3. Download Stockfish

* Go to: https://stockfishchess.org/download/
* Download the Windows version
* Extract the `.exe` file

### 4. Add Stockfish to project

Place the downloaded file in the root folder:

```
Chess_Royale_AI/
└── stockfish-windows-x86-64-avx2.exe
```

---

## ▶️ Run the Game

```
python ChessMain.py
```

---

## 🧠 How AI Works

* The game uses the Stockfish engine to calculate optimal moves.
* The Python script communicates with Stockfish via subprocess.
* Based on the current board position, Stockfish returns the best move.

---

## 📸 Future Improvements

* Add difficulty levels
* Improve UI/UX
* Add multiplayer mode
* Highlight possible moves
* Add game history and undo feature

---

## 🙌 Acknowledgements

* Stockfish Chess Engine
* Pygame Library

---

## 📌 Author

**Karina Kesur**
GitHub: https://github.com/karina202330

---

⭐ If you like this project, consider giving it a star!
