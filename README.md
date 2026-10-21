
# Expense Tracker 💰

A personal expense-tracking application built with Python, Flet, and SQLite.

## Features

- Track income and expenses
- Categorize transactions
- Calculate your balance automatically
- Store transactions locally using SQLite
- View transaction history
- Delete transactions
- Validate transaction amounts

## Technologies

- Python 3.15
- Flet
- SQLite
- Git and GitHub

## Requirements

- Python installed on Windows
- Git (optional, for contributing)

## Installation on Windows

1. Clone this repository or download the source code.
2. Open PowerShell in the project folder.
3. Create a virtual environment:

   ```powershell
   python -m venv .venv
   ```

4. Activate the virtual environment:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Install Flet:

   ```powershell
   python -m pip install flet
   ```

6. Start the application:

   ```powershell
   python app.py
   ```

## Data and Privacy

Transaction records are stored locally in `expenses.db`.
The database is excluded from Git version control.

## Current Status

The dashboard, transaction entry, SQLite storage,
income and expense totals, and deletion functionality
are implemented.

## Future Improvements

- Edit existing transactions
- Monthly spending charts
- Search and filter transactions
- Automated tests
- Android APK packaging

## Author

Sujal — B.Tech Computer Science Engineering student
