# Four-in-a-Row

A terminal Four-in-a-Row (Connect-4 style) game with an AI opponent built on **Minimax search with Alpha-Beta pruning** and a hand-designed, window-based evaluation function.

---

## 1. The Game

- **Board:** 6 rows × 7 columns. Pieces drop to the lowest empty cell of the chosen column.
- **Goal:** Be the first to line up **four pieces** horizontally, vertically or diagonally.
- **Draw:** The board fills up and nobody has four in a row.
- **Players:** Player 1 is **Green (G)** and moves first. Player 2 is **Red (R)**.

### Game Modes

| Mode | Description |
|---|---|
| Human vs Human | Two players take turns entering columns (1–7) |
| Human vs Agent | Play against the AI at a chosen difficulty |
| Agent vs Agent | Two AIs play each other, possibly at different difficulties |

### Difficulty Levels

| Level | Search depth passed to Minimax | Effective look-ahead* |
|---|---|---|
| Easy | 0 | 1 ply (judges the next move with the heuristic only) |
| Medium | 2 | 3 plies |
| Hard | 4 | 5 plies |

\*`best_move` plays one candidate move before calling Minimax, so the look-ahead is the depth + 1.

---

## 2. Approach

```
Board state ──► best_move() ──► try each column (centre first)
                                      │
                                      ▼
                          minimax() with alpha-beta
                                      │
               win/loss/draw? ── yes ─► terminal score
                     │ no
               depth == 0? ── yes ─► evaluate()  (heuristic)
                     │ no
                     └──► recurse on each valid column
```

### 2.1 Board Representation and Windows
- The board is a 6×7 grid holding `0` (empty), `"G"` or `"R"`. Row 0 is the top row.
- At game start, every possible line of four cells (a **window**) is generated once:

| Direction | Windows |
|---|---|
| Horizontal | 24 |
| Vertical | 21 |
| Diagonal ↘ | 12 |
| Diagonal ↙ | 12 |
| **Total** | **69** |

The same window list is used both for **win detection** and for **evaluation**.

### 2.2 Evaluation Function (Heuristic)
Each window is scored from Red's point of view. Red maximises the score and Green minimises it.

| Window contents | Score |
|---|---|
| Both colours present | 0 (can never be completed) |
| 1 piece of one colour, rest empty | ±1 |
| 2 pieces of one colour, rest empty | ±10 |
| 3 pieces of one colour, rest empty | ±100 ÷ (1 + gap) |

- **Gap penalty:** `gap` is the number of empty cells **below** the missing cell of a 3-piece window. A threat that can be played right now counts in full. A threat that needs other pieces underneath it first counts for less.
- The sign is **+ for Red** and **− for Green**.

### 2.3 Minimax with Alpha-Beta Pruning
- **Minimax** looks ahead over both players' moves, assuming the opponent always plays its best reply.
- **Alpha-Beta pruning** skips branches that cannot change the final decision. This reduces the work without changing the chosen move.
- **Terminal scores:**
  - Red win: `+1,000,000 + depth`
  - Green win: `−1,000,000 − depth`
  - Draw: `0`

  Adding the remaining depth makes the agent **prefer faster wins and delay losses**.

### 2.4 Move Ordering
At the root, columns are tried in the order **4, 3, 5, 2, 6, 1, 7**, centre first. Centre columns belong to the most windows, so trying them first usually finds strong moves early and makes pruning more effective.

### 2.5 Playing as Either Colour
`best_move(board, level, symbol)` lets the agent play as either colour:
- **Red** picks the move with the **highest** score.
- **Green** picks the move with the **lowest** score.

---

## 3. Experiments and Development

| # | What we tried / changed | Result |
|---|---|---|
| 1 | Core engine: Human vs Agent at a fixed depth of 4 (`main.py`) | Working AI opponent |
| 2 | Invalid input handling | Bad input no longer crashes the game |
| 3 | Difficulty levels (Easy / Medium / Hard) via search depth | Strength can be adjusted |
| 4 | Multiple game modes (Human / Agent for each player) | Human vs Human, Human vs Agent and Agent vs Agent all supported |
| 5 | Fix: window list was not cleared between games | Each new game starts clean |
| 6 | Easy depth set to 0 | Easy is now a clearly weaker, 1-ply heuristic player |
| 7 | Agent vs Agent mode with a 1 s delay per move | AI matches can be watched move by move |

### Sample Agent vs Agent Game: Easy (Green) vs Hard (Red)
Recorded in `final_nb.ipynb`:

- **Easy** greedily built a horizontal line along the bottom row (columns 2–4).
- **Hard** blocked it at column 1, then built in the centre.
- **Hard (Red) won in 7 moves** (14 plies total) with a diagonal ↘ from column 2 to column 5.

Final board:

```
. . . . . . .
. . . . . . .
. R R R . . .
. G R G . . .
. G G R . . .
R G G G R . .
1 2 3 4 5 6 7
```

This shows that deeper search (5 plies) both **blocks** the opponent's threats and **sets up its own** winning lines.

---

## 4. How to Run

**Requirements:** Python 3 (no external libraries).

**Latest version (all modes and levels): `final_nb.ipynb`**
1. Open the notebook in Jupyter or VS Code and run all cells.
2. Answer the prompts:
   - Player 1 / Player 2: `Human` or `Agent`
   - Agent level: `Easy`, `Medium` or `Hard`
3. Humans enter a column number from **1 to 7**.

**Original version (Human vs Agent, Hard only): `main.py`**
```bash
python main.py
```

> The prompts are case-sensitive: type `Human`, `Agent`, `Easy`, etc. exactly as shown.

---

## 5. Project Structure

```
Four-in-a-Row/
├── final_nb.ipynb   # Latest version: modes, difficulty levels, Agent vs Agent
├── main.py          # Initial version: Human vs Agent, fixed depth
└── README.md
```

---

## 6. Limitations and Future Work

- **Move ordering inside the tree:** centre-first ordering is only used at the root. Using it at every level would allow more pruning.
- **Deterministic agents:** the same position always produces the same move. Random tie-breaking would add variety.
- **Transposition table:** caching positions already evaluated would allow deeper search in the same time.
- **Interface:** a graphical version (e.g. Pygame) instead of a terminal board.
