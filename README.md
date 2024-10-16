# NFL DFS Brute-Force Optimizer
Optimize highest projected NFL DraftKings Classic format competition lineups.  

## Requirements

- Python 3.9 or later
- `numpy` and `pandas` Python packages

## Usage

### Step 1: Install Required Packages

Ensure you have the required packages installed before running the optimizer:
`pip install numpy pandas`

### Step 2: Download DraftKings Salaries

- Navigate to the DraftKings lineup building screen for your competition.
- Click the "Export to CSV" button to download the player salaries.
- Move the downloaded CSV file to this project's source directory.

### Step 3: Prepare Your Projections File

Prepare a CSV file containing player projections with the following columns:
- `Position`
- `Name`
- `Team`
- `Fpts` (projected fantasy points)
- `Ownership` (projected ownership percentage)

Place the projections CSV in the source directory.

### Step 4: Update Directories in optimizer.py

Open `optimizer.py` and update the file paths in the `__main__` function:
```
salariesDir = 'path_to_your_salaries_csv'
projDir = 'path_to_your_projections_csv'
```

Ensure the paths point to your salary and projection CSV files.

### Step 5: Configure the Partial Lineup and Exclusions

In the `__main__` function of `optimizer.py`, configure the following:
- `remainingPosList`: A list of positions you want to optimize (e.g., ['RB', 'RB', 'WR', 'FLEX]).
- `remainingSal`: The remaining salary you have left to spend (e.g., 28300).
- `excludedNames`: A list of player names you want to exclude from the optimization (e.g., players already in your partial lineup).

Example:
```
remainingPosList = ["RB", "RB", "WR", "WR", "FLEX"]
remainingSal = 33600
excludedNames = ["Amari Cooper", "Ezekiel Elliott", "Michael Gallup", "Tyler Lockett"]
```

### Step 6: Run the Optimizer

Run the optimizer with the following command:
`python optimizer.py`

The optimizer will print the top projected lineups to the console. To display less lineups, change the `numLineups` argument in `optimize()`

