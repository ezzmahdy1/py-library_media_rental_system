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


## Requirements
```
rich
```

## Project structure

- `Item` (base class) → `Book`, `DVD`, `Game`
- `Member` (base class) → `Student`, `Staff`, `Vip`


## What I learned

This project was my introduction to:
- **Object-oriented design in Python (inheritance, class hierarchies)**.
- **Learned database fundamentals the hard way.** Building my own read/parse/write logic with regex meant handling schema, keys, and consistency by hand.
- **First real taste of system design.** Deciding how items, members, and fees relate to each other, and keeping one consistent pattern across every feature.
- Regex for parsing custom data formats.
- Building a robust text-based UI with input validation.
- Packaging a Python script into a distributable executable.

## License

Feel free to use or adapt this project for learning purposes.
