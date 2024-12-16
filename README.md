# Video Game Database Application - Final CPSC408 Project

## Authors

- **Kendra Manz**
- **Mason Pennell**
- **Samantha Mondragon Landeros**
- **Teresa Wong**

---
## Overview
This is an interactive application that manages a Video Game database. The project includes functionalities to **create, update, delete, search, and export data** while using MySQL for the backend database. The schema and data are initialized based on the provided CSV files and a pre-defined Entity-Relationship diagram.

---

## Features

### 1. Game Search (`1_Game-Search.py`)
- Search for games by:
  - Title (prefix-based search)
  - Developer and Publisher (via radio buttons)
  - Minimum rating (slider input)
- Query involves subqueries for efficient filtering.

### 2. Store Search (`2_Store_Search.py`)
- Search for stores by their location.
- Displays matching records in a table.

### 3. User Creation (`3_Create.py`)
- Create new users with:
  - Name
  - Password
- User IDs are auto-incremented.
- View all users after insertion.

### 4. Delete Game (`4_Delete.py`)
- Mark a game as deleted (soft delete using `isDeleted` flag).
- Aggregate query displays the total number of games.
- Supports transaction management for reliability.

### 5. Export Data (`5_Export.py`)
- Export CSV files (`developer.csv`, `game.csv`, etc.) for all tables.
- Downloadable buttons are dynamically generated.

### 6. Update Game (`6_Update.py`)
- Update attributes of a game (title, genre, rating) using buttons.
- Ensures real-time updates with validation.

### 7. Database Initialization (`Hello.py`)
- Creates the required MySQL tables (`game`, `developer`, `publisher`, `store`, `user`) if they don't already exist.
- Populates tables from the provided CSV files.
- Includes:
  - Database views 
  - Placeholder support for future extensions.

### Helper Functions (`helper.py`)
- Includes utility functions to:
  - Clean and process CSV data.
  - Convert string inputs to proper data types.
  - Nicely format outputs.

---

## ER Diagram

The database structure is based on the our Entity-Relationship Diagram

---

## Project Structure

```plaintext
├── data/
│   ├── developer.csv
│   ├── game.csv
│   ├── publisher.csv
│   ├── store.csv
│   └── user.csv
├── pages/
│   ├── 1_Game-Search.py
│   ├── 2_Store_Search.py
│   ├── 3_Create.py
│   ├── 3_Create.py
│   ├── 5_Export.py
│   └── 6_Update.py
├── Hello.py
├── helper.py
├── image.jpg
└── .gitignore
```

---

## Instructions

- **Python**
- **MySQL Server**
- **Streamlit** (install via `pip3 install streamlit`)
- **MySQL** connector for Python (`pip3 install mysql-connector-python`)
- **Pandas** pip3 (install via ` pip3 install pandas`)
- **Change password at lines 9, 18, and 120 in ```Hello.py```**
- Run **streamlit run Hello.py** in terminal

---

## How to Use

- **Navigation**: Use the Streamlit navigation sidebar or launch specific scripts to perform actions (e.g., search, create, delete, update).
- **Interactivity**: Provide inputs via text boxes, sliders, radio buttons, and buttons.
- **Data Export**: Use the **Export** section to download table data in CSV format.

---

## Notes

- **Soft Deletes**: Deleted games are marked with `isDeleted = 1`. Toggle the "Show deleted games" option in the Delete Game script to view them.
- **Views**: Use the `GameView` for a joined and cleaner view of the game data.

---

