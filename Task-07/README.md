# Task 07 — Berry Broker Discord Bot

> **Berry Broker — A Pirate Economy Discord Bot inspired by One Piece**

The **Berry Broker** is a modular Discord bot built using `discord.py` and SQLite. It features a complete pirate-themed economy where players earn, transfer, spend, and raid Berries to compete for a spot on the **Worst Generation** leaderboard.

---

## Overview

Every server member is treated as a pirate starting with a wallet of **500 Berries**. Players can claim daily rewards, buy items from a shop, inspect their inventory, raid rivals, track transaction logs, and fetch character data dynamically via an external One Piece API.

### Key Architecture
- **Framework:** `discord.py` with modular **Cogs** architecture.
- **Database:** Local **SQLite3** database for reliable state persistence.
- **Data Serialization:** External JSON configuration for shop items.
- **Asynchronous HTTP:** `aiohttp` for non-blocking API consumption.

---

## Features & Commands

| Command | Description |
| :--- | :--- |
| `!bounty` | Check your current Berry wallet balance. |
| `!setsail` | Claim **300 Berries** daily (24-hour cooldown). |
| `!trade @user <amount>` | Transfer Berries directly to another pirate. |
| `!raid @user` | Attempt a chance-based raid to steal ~20% of a target's wallet. |
| `!worstgeneration` | Display the top 5 richest pirates on the server. |
| `!shop` | Browse available items from the store. |
| `!buy <item>` | Purchase an item using your Berries. |
| `!inventory` | View your owned items and active statuses. |
| `!history` | View your recent transaction history. |
| `!logpose` | Fetch random One Piece character & Devil Fruit details from an API. |

---

## Economy & Mechanics

### Starting Capital & Daily Allowance
New pirates automatically register upon first interaction and receive an initial **500 Berries**. Running `!setsail` grants **+300 Berries** once every 24 hours.

```text
Initial Wallet:    500 Berries
Daily Reward:     +300 Berries (!setsail)
```

### Direct Trading
Pirates can transfer wealth using `!trade @user <amount>`. Every transfer updates both wallets and records a double-entry item in each pirate's ledger.

### High-Stakes Raiding
Running `!raid @user` triggers a chance-based mechanic:
- **Success Rate:** 50%
- **Reward:** ~20% of the target's current wallet balance
- **Risk:** Failure results in a lost raid opportunity.

---

## 🛒 Shop & Inventory

Shop items are managed in `data/shop.json` for easy updates without changing core application code.

### Available Shop Items
| Item | Price | Description |
| :--- | :--- | :--- |
| 🧭 **Log Pose** | 300 Berries | Navigation tool for grand line adventures |
| 🐌 **Den Den Mushi** | 500 Berries | Transponder snail for communications |
| 🗺️ **Treasure Map** | 750 Berries | Map leading to hidden loot |
| 🪨 **Sea Prism Stone** | 1,000 Berries | Rare mineral that weakens Devil Fruit users |
| 🍈 **Devil Fruit Box** | 1,500 Berries | Mysterious box containing unknown powers |

Purchased items persist in the SQLite database (`inventory` table) across bot reboots.

---

## Transaction History

All financial activity—including daily claims, trades, shop purchases, and raids—is recorded in the transaction ledger and viewable via `!history`:

```text
📜 Pirate Ledger

TRADE — -50 Berries
Sent 50 Berries to @Sid

BUY — -300 Berries
Bought Log Pose

DAILY — +300 Berries
Claimed daily Berries
```

---

## One Piece API Integration

The `!logpose` command consumes an external REST API asynchronously to output rich character data card outputs:

```text
🧭 LOG POSE ACTIVATED!

🏴‍☠️ Pirate: Trébol
💰 Bounty: 99.000.000
👥 Crew: Don Quixote's crew
🍈 Devil Fruit: Poisse-Poisse fruit
✨ Power: The eater's body can generate mucus at will.
```

---

## Database Design

The bot uses SQLite (`database/berry.db`) containing three core tables:

```text
database/berry.db
├── users
│   ├── user_id (PRIMARY KEY)
│   ├── wallet (INTEGER)
│   └── last_daily (TIMESTAMP)
│
├── inventory
│   ├── id (PRIMARY KEY)
│   ├── user_id (FOREIGN KEY)
│   ├── item_name (TEXT)
│   ├── quantity (INTEGER)
│   └── active (BOOLEAN)
│
└── history
    ├── id (PRIMARY KEY)
    ├── user_id (FOREIGN KEY)
    ├── action (TEXT)
    ├── amount (INTEGER)
    ├── description (TEXT)
    └── created_at (TIMESTAMP)
```

---

## Project Structure

```text
DankMemerBot/
│
├── bot.py                # Main bot entry point & Cog loading
├── config.py             # Configuration and environment variables
├── database.py           # SQLite connection and helper queries
├── test_api.py           # Verification script for One Piece API
├── .gitignore            # Git exclusion rules
│
├── cogs/                 # Command modules (Discord Cogs)
│   ├── economy.py        # !bounty, !setsail, !trade, !raid, !worstgeneration
│   ├── fun.py            # Additional fun/meme commands
│   ├── history.py        # !history
│   ├── onepiece.py       # !logpose (REST API integration)
│   └── shop.py           # !shop, !buy, !inventory
│
├── data/
│   └── shop.json         # Configurable shop catalogue
│
└── database/
    └── berry.db          # Local SQLite storage file
```

---

## Requirements & Dependencies

- **Python 3.8+**
- **Libraries:**
  - `discord.py` (Discord API wrapper)
  - `aiohttp` (Async HTTP requests for the One Piece API)
- A registered **Discord Bot Application** and token.

---

## Installation & Setup

1. **Clone the repository and enter the directory:**
   ```bash
   cd Task-07/DankMemerBot
   ```

2. **Create and activate a virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install required dependencies:**
   ```bash
   pip install discord.py aiohttp
   ```

4. **Set your Discord Bot Token environment variable:**
   - **PowerShell:**
     ```powershell
     $env:DISCORD_TOKEN="YOUR_BOT_TOKEN_HERE"
     ```
   - **Linux / macOS:**
     ```bash
     export DISCORD_TOKEN="YOUR_BOT_TOKEN_HERE"
     ```

5. **Start the bot:**
   ```bash
   python bot.py
   ```

---

## Security & Best Practices

- **Token Safety:** Sensitive secrets are managed via `os.getenv("DISCORD_TOKEN")` and are never committed in source control.
- **Git Hygiene:** Local databases (`database/*.db`), cached bytecode (`__pycache__`), and virtual environments (`venv/`) are excluded using `.gitignore`.

---

## Summary

The **Berry Broker** bot delivers a complete pirate-themed Discord economy experience. By combining relational storage in SQLite, asynchronous external API fetching, clean Cog modularity, and event-driven commands, it serves as a robust example of modern `discord.py` application architecture.

*Earn Berries. Build your bounty. Raid your rivals. Claim your spot in the Worst Generation!* 🏴‍☠️
