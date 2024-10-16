import pandas as pd


class Projections:
    def __init__(self, salariesDir, projDir):
        # Create Data DF from DK Salaries CSV
        salary_cols = ["Position", "Name", "Salary", "TeamAbbrev"]  # Columns from DK Salaries CSV that we actually want to use
        self.data = pd.read_csv(salariesDir, usecols=salary_cols)
        self.data.rename(columns={'TeamAbbrev': 'Team'}, inplace=True)

        # Read in Projections
        projCols = ["Position", "Name", "Team", "Fpts", "Ownership"]
        projections = pd.read_csv(projDir, usecols=projCols)
        projDSTRows = projections.loc[projections["Position"] == "DST"]
        projDST = projDSTRows.drop(columns=["Name"])

        projDSTData = self.data.merge(projDST)
        self.data = self.data.merge(projections)
        self.data = pd.concat([self.data, projDSTData])








