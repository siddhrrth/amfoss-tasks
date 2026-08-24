# 🏴‍☠️ Logbook of the Grand Line

## Task 02 — Prologue

### Captain's Log

This logbook records every flag, cipher fragment, transmission code,
keyword, command, and important discovery found during the Terminal Voyage.

---

## Level 1 — Awakening at Loguetown Reef

### Discovery

AWAKENING_SIGNATURE: ONE_PIECE{GITO_GITO_NO_AWAKENING}

The genuine Devil Fruit was found at:

sector_C/devil_fruit_6.txt

### Method

I first inspected `eat.sh` to understand how it identifies the genuine fruit.
The script checks whether the supplied file is executable using the `-x`
file test.

I then searched all four storage sectors for executable regular files using:

find sector_A sector_B sector_C sector_D -type f -executable -print

This revealed:

sector_C/devil_fruit_6.txt

I passed this file to the provided eating script:

./eat.sh sector_C/devil_fruit_6.txt

The script successfully awakened the Gito Gito no Mi and revealed the
AWAKENING_SIGNATURE.

### Screenshot

![Level 01](image.png)

---

## Level 2 — The Two Faces of Whiskey Peak

### Objective

Recover the Executive Transmission Code hidden within the alternate history of Whiskey Peak.

### Discovery

EXECUTIVE TRANSMISSION CODE:

`BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}`

### Method

I first inspected the visible files in the Whiskey Peak directory:

```bash
cd ~/Terminal-Voyage-User-Edition/GrandLine/Whiskey_Peak
ls -lah
cat feast_manifest.txt
```

The visible manifest contained:

```text
Item 01: 50 Barrels of Bink's Sake
Item 02: Roasted Sea King Meat
```

There was no transmission code in the visible timeline.

The Level 2 description mentioned that Whiskey Peak had another hidden history. Since the repository uses Git, I inspected the Git history:

```bash
git log --all --oneline --decorate --graph
```

This revealed a separate branch:

```text
bc5aff3 (origin/whiskey_peak_investigation) Level 2: Implemented
```

I then inspected the Whiskey Peak manifest from this alternate timeline without switching branches:

```bash
git show origin/whiskey_peak_investigation:GrandLine/Whiskey_Peak/feast_manifest.txt
```

The alternate version contained:

```text
Item 01: 50 Barrels of Sleep Powder Infused Sake
Item 02: Roasted Sea King Meat
```

This confirmed that the branch contained the hidden history mentioned in the challenge.

Next, I inspected the Level 2 implementation commit:

```bash
git show --stat bc5aff3
```

This revealed a hidden script:

```text
GrandLine/Whiskey_Peak/.baroque_works_cache/unlock_vault.sh
```

I inspected the script directly from the Git commit:

```bash
git show bc5aff3:GrandLine/Whiskey_Peak/.baroque_works_cache/unlock_vault.sh
```

The script required the `AWAKENING_SIGNATURE` obtained in Level 1. It calculated the SHA-256 hash of the signature and compared it with a target hash.

I extracted the historical script and executed it using the Level 1 signature:

```bash
git show bc5aff3:GrandLine/Whiskey_Peak/.baroque_works_cache/unlock_vault.sh > /tmp/unlock_vault.sh
chmod +x /tmp/unlock_vault.sh
AWAKENING_SIGNATURE='ONE_PIECE{GITO_GITO_NO_AWAKENING}' /tmp/unlock_vault.sh
```

The vault successfully authenticated the Devil Fruit signature and generated two transmission logs:

```text
marine_intercept.log
bounty_hunter_feed.log
```

The script instructed me to compare the two files using `diff`.

I therefore ran:

```bash
diff marine_intercept.log bounty_hunter_feed.log
```

The output showed that line 42 differed:

```text
42c42
< LOG_STREAM_ENTRY_SECURE_NODE_042_VALID
---
> BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}
```

The altered line contained the Executive Transmission Code.

### Screenshot

![Level 02](![Level 02](image-1.png))

---

## Level 3 — The Wax Labyrinth of Little Garden

### Objective
Locate the authentic Baroque Works Executive Report among the decoy logs in the Wax Jungle using the broadcast representation of the Level 2 Executive Transmission Code.

### Discovery
- **EXECUTIVE TRANSMISSION CODE:** `BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}`
- **BROADCAST IDENTIFIER (SECURITY_TAG):** `QkFST1FVRV9ESUFMe1NQTElUX1RJTUVMSU5FX01JU0RJUkVDVElPTn0K`
- **GENUINE REPORT:** `GrandLine/Wax_Jungle/sector_beta/outpost/watchtower/storage/archive/agent_manifest.log`
- **PONEGLYPH_FRAGMENT_I:** `KjY2MjF4bW0lKzYqNyBsIS0vbTAtJTcnL`

### Method
1. Inspected the file tree of the `origin/little_garden` branch (`ee6f464`) using `git ls-tree -r ee6f464 GrandLine/Wax_Jungle`.
2. Encoded the Level 2 transmission code into Base64 (`echo 'BAROQUE_DIAL{SPLIT_TIMELINE_MISDIRECTION}' | base64`), yielding `QkFST1FVRV9ESUFMe1NQTElUX1RJTUVMSU5FX01JU0RJUkVDVElPTn0K`.
3. Inspected `GrandLine/Wax_Jungle/sector_beta/outpost/watchtower/storage/archive/agent_manifest.log` directly via `git show`.
4. Verified that the `SECURITY_TAG` matched the broadcast code and extracted `PONEGLYPH_FRAGMENT_I`.

### Screenshot
![Level 03](image-2.png)
## Level 4 — The Camouflaged Blueprints of Water 7

### Objective
Identify the disguised blueprint by determining its true file nature
and recover Cipher Fragment 2.

### Discovery
Pending.

### Method
Pending.

### Screenshot
Pending.

---

## Level 5 — The Buster Call Timeline Recovery

### Objective
Travel backward through the timeline, recover the surviving records,
and reconstruct the Poneglyph inscription.

### Discovery
Pending.

### Method
Pending.

### Screenshot
Pending.

---

## Level 6

### Objective
To be discovered.

### Discovery
Pending.

### Method
Pending.

### Screenshot
Pending.