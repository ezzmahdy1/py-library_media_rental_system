# Library / Media Rental System

A console-based rental management system built in Python. It manages a catalog of books, DVDs, and games, tracks member accounts and borrowing, and automatically calculates late fees — all backed by a simple text-file database and a clean terminal UI powered by [`rich`](https://github.com/Textualize/rich).

> 🐣 **This is my first Python project.** I built it to learn object-oriented design, file I/O, and regex-based parsing from the ground up — feedback and suggestions are very welcome.

## Features

### Item management
- Add, remove, update, and search items across three types: **Books**, **DVDs**, and **Games**
- Each item type has its own loan period and late fee rate (e.g. books: 14 days / £5 per day late; DVDs: 7 days / £20 per day; games: 30 days / £50 per day)
- Search by title, ID, or creator, with an optional filter for items currently available in store
- Tracks total copies vs. copies currently checked out

### Member management
- Three membership tiers with different borrowing limits: **Student** (3 items), **Staff** (5 items), **VIP** (10 items)
- Add, remove, and update member records
- Checkout and return items, with automatic validation against borrowing limits and item availability
- Members are automatically suspended if their confirmed fees exceed a threshold
- Search members by name or ID

### Fees
- Automatic calculation of late fees based on how long an item has been checked out
- Separate tracking of confirmed (payable) fees vs. running/accruing fees
- Dedicated flow for members to pay down pending fees

### Data persistence
- All items and members are stored in human-readable `.txt` files (`items.txt`, `members.txt`)
- Custom regex-based parser reads and writes structured records without needing a database engine
- Data files are created automatically on first run if they don't already exist

### Interface
- Clean, styled terminal menus and tables via `rich`
- Input validation on every user-facing prompt, with clear error messages for invalid IDs, malformed entries, and out-of-range actions

## Tech stack

- **Python 3**
- [`rich`](https://pypi.org/project/rich/) — terminal styling, panels, and tables
- `re` — regex-based parsing of the text-file database
- `datetime` — date tracking for loans and fee calculation

## Getting started

### Requirements
```
pip install rich
```

### Run it
```
python library_system.py
```

On first run, `items.txt` and `members.txt` will be created automatically in the same folder.

### Build a standalone executable (optional)
This project can be packaged into a single Windows `.exe` with [PyInstaller](https://pyinstaller.org/), so it can run without a Python installation:
```
pip install pyinstaller
pyinstaller --onefile --console library_system.py
```
The executable will be in the generated `dist/` folder.

## Project structure

- `Item` (base class) → `Book`, `DVD`, `Game`
- `Member` (base class) → `Student`, `Staff`, `Vip`
- Each menu action follows a consistent pattern: **read from file → validate input → apply action → write back to file**

## Known limitations

- Uses flat text files rather than a real database, so it isn't designed for concurrent/multi-user use
- Titles or creator names containing `"` or `.` can break the regex parser
- No authentication — anyone running the program has full access

These were conscious trade-offs for a learning project focused on OOP and file handling rather than production deployment.

## What I learned

This project was my introduction to:
- Object-oriented design in Python (inheritance, `super()`, class hierarchies)
- Reading and writing structured data to plain text files
- Regex for parsing custom data formats
- Building a robust text-based UI with input validation
- Packaging a Python script into a distributable executable

## License

Feel free to use or adapt this project for learning purposes.
