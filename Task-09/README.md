# One Piece Memory Matcher

A One Piece themed memory matching game built with **Flutter**.

The goal is simple: flip cards, find all matching character pairs, and complete the game with the highest possible score in the least amount of time.

---

## Features

-  16-card memory matching board
-  8 One Piece characters with matching pairs
-  Custom character artwork and card-back artwork
-  Real-time game timer
-  Move counter
-  Score system
-  Persistent best score
-  Dark mode
-  Light mode
-  Theme and best score persistence using `shared_preferences`
-  New Game button
-  Card flip and match animations
-  Responsive layout
-  Supports Flutter Web and Desktop

---

## How to Play

1. Start a new game.
2. Click any card to reveal the character.
3. Click another card to reveal it.
4. If the two cards match, they remain revealed.
5. If they don't match, both cards are flipped back.
6. Continue until all pairs are matched.
7. Complete the board with as few moves and as little time as possible.

---

## Scoring System

The game uses a simple scoring system:

### Correct Match

Every correct pair:
```text
+100 points
```

### Incorrect Match

Every incorrect pair:
```text
-15 points
```
*The score cannot become negative from incorrect matches.*

### Completion Bonuses

When all pairs are matched, the final score receives:

**Time Bonus:**
```text
500 - (seconds × 5)
```

**Move Bonus:**
```text
500 - (moves × 20)
```

*Both bonuses have a minimum value of 0.*

Therefore:
```text
Final Score = Match Score + Time Bonus + Move Bonus
```

---

## Characters

The current game contains eight characters:

- Monkey D. Luffy
- Roronoa Zoro
- Nami
- Sanji
- Tony Tony Chopper
- Nico Robin
- Usopp
- Portgas D. Ace

Each character appears twice, creating a total of:
```text
8 pairs = 16 cards
```

---

## Technologies Used

- **Flutter**
- **Dart**
- **Material 3**
- **Shared Preferences**

### Packages

```yaml
dependencies:
  shared_preferences: ^2.5.5
```

`shared_preferences` is used to persist:
- Best score
- Dark/light theme preference

---

## Project Structure

```text
one_piece_memory_matcher/
│
├── assets/
│   └── cards/
│       ├── ace.png
│       ├── card_back.png
│       ├── chopper.png
│       ├── luffy.png
│       ├── nami.png
│       ├── robin.png
│       ├── sanji.png
│       ├── usopp.png
│       └── zoro.png
│
├── lib/
│   └── main.dart
│
├── pubspec.yaml
└── README.md
```

---

## Running the Project

Make sure Flutter is installed and configured.

1. Fetch dependencies:
   ```bash
   flutter pub get
   ```

2. Run the application on Edge (Web):
   ```bash
   flutter run -d edge
   ```

3. Or run it on a supported desktop device (e.g. Windows):
   ```bash
   flutter run -d windows
   ```

---

##  Code Quality

The project was checked using Flutter's static analyzer:

```bash
flutter analyze
```

**Expected result:**
```text
No issues found!
```

---

##  Persistent Data

The application uses `shared_preferences` to store user preferences locally.

Currently persisted data includes:
- `bestScore`
- `darkMode`

This means the user's best score and selected theme remain available after restarting the application.

---

## Design

The interface follows a dark pirate/adventure inspired visual style with:

- Gold accent colors
- Rounded cards
- Custom One Piece artwork
- Animated card interactions
- Responsive 4 × 4 game board
- Light and dark themes
- Clear game statistics

The layout is designed so that the complete game board remains visible without unnecessary scrolling on supported screen sizes.

---

## Game Logic

The game creates two copies of every character:

```dart
final shuffled = [
  ..._characters,
  ..._characters,
];
```

The cards are then randomly shuffled before every new game.

Two cards are temporarily revealed during each turn. After a short delay:
- Matching cards are permanently revealed.
- Non-matching cards are hidden again.
- The move counter is increased.
- The score is updated.

The game ends automatically when every card has been matched.

---

## Best Score

After completing a game, the final score is compared against the stored best score.

If the new score is higher, **"NEW BEST SCORE!"** is displayed and the score is saved locally.

---

## Future Improvements

Possible future improvements include:

- Multiple difficulty levels
- Additional One Piece characters
- Sound effects and background music
- More board sizes
- Leaderboards
- Game statistics and history
- Different scoring modes
- Custom animations
- Mobile-specific UI optimization

---

## Author

**Siddharth S**  

---
