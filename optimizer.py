from projections import Projections
import collections
import numpy as np


# Iterates through projections, and removes players who have projections lower than somebody cheaper than them
def cleanProj(data):
    sorted_data = data.sort_values("Salary")
    maxes = collections.defaultdict(int)
    # NOTE: Iterating thorugh rows in pandas apparently slow. Possibly faster solution in different route (should be
    # relatively inconsequential to run-time for any NFL slate)
    indices = []
    for index, row in sorted_data.iterrows():
        currProj = row["Fpts"]
        currPos = row["Position"]
        if currProj > maxes[currPos]:
            maxes[currPos] = currProj
            indices.append(index)
    result = sorted_data[sorted_data.index.isin(indices)]
    return result


# Takes in a list of names and removes them from the dataframe
def removePlayers(data, exclusionNames):
    for currName in exclusionNames:
        data.drop(data.index[data["Name"] == currName], inplace=True)


# Returns a tuple with the position indices you'll need for meshgrid
def getPosIndices(clean_data, posList):
    qbInds = clean_data[clean_data["Position"] == "QB"].index.tolist()
    rbInds = clean_data[clean_data["Position"] == "RB"].index.tolist()
    wrInds = clean_data[clean_data["Position"] == "WR"].index.tolist()
    teInds = clean_data[clean_data["Position"] == "TE"].index.tolist()
    dstInds = clean_data[clean_data["Position"] == "DST"].index.tolist()
    flexInds = rbInds + teInds + wrInds

    result = ()
    for pos in posList:
        if pos == "QB":
            result += (qbInds,)
        elif pos == "RB":
            result += (rbInds,)
        elif pos == "WR":
            result += (wrInds,)
        elif pos == "TE":
            result += (teInds,)
        elif pos == "DST":
            result += (dstInds,)
        else:
            result += (flexInds,)
    return result


# Uses numpy vectorization to quickly brute-force calculate the projection score of every combination of
# players. Prints out the top numLineups lineups
def optimize(numRemainingPos, remainingPosList, remainingSal, excludedNames, numLineups, salariesDir, projDir):
    proj = Projections(salariesDir, projDir)
    data = proj.data
    clean_data = cleanProj(data)
    removePlayers(clean_data, excludedNames)
    clean_data.reset_index(drop=True, inplace=True)
    posIndicies = getPosIndices(clean_data, remainingPosList)

    # Get matrix of all combinations of Player Identities
    indexCombinations = np.array(np.meshgrid(*posIndicies)).T.reshape(-1, numRemainingPos)
    rangeSeries = np.array(range(indexCombinations.shape[0]))
    rangeMatrix = np.repeat(rangeSeries, numRemainingPos).reshape(-1, numRemainingPos)
    rangeMatrixMult = rangeMatrix * len(clean_data)
    indexIncrements = (rangeMatrixMult + indexCombinations).reshape(-1)
    playerIdentities = np.zeros(indexCombinations.shape[0] * len(clean_data))
    np.add.at(playerIdentities, indexIncrements, 1)
    playerIdentities = playerIdentities.reshape(-1, len(clean_data))

    # Get matrix of projections
    pointProjections = clean_data["Fpts"].to_numpy(copy=True)
    pointProjMatrix = np.repeat(pointProjections.reshape(1, -1), indexCombinations.shape[0], axis=0)
    salaries = clean_data["Salary"].to_numpy(copy=True)
    salaryMatrix = np.repeat(salaries.reshape(1, -1), indexCombinations.shape[0], axis=0)

    # Create masks for salary and duplicate (no more than 1 of each player) restraints
    lineupSalMatrix = salaryMatrix * playerIdentities
    lineupSalTotals = np.sum(lineupSalMatrix, axis=1)
    salMask = np.where(lineupSalTotals <= remainingSal, 1, 0)
    maxOccurrenceArray = np.amax(playerIdentities, axis=1)
    dupeMask = np.where(maxOccurrenceArray > 1, 0, 1)

    # Apply masks to projection totals
    lineupProjMatrix = pointProjMatrix * playerIdentities
    lineupProjTotals = np.sum(lineupProjMatrix, axis=1) * salMask * dupeMask
    lineupOrder = np.argsort(lineupProjTotals)
    playerNames = clean_data["Name"]
    lineupNum = numLineups
    for lineupInd in lineupOrder[-lineupNum:]:
        print("Lineup " + str(lineupNum) + ":")
        lineupPlayerIndices = np.argsort(playerIdentities[lineupInd, :])[-numRemainingPos:]
        for playerIndex in lineupPlayerIndices:
            print(playerNames[playerIndex])
        print(str(lineupProjTotals[lineupInd]) + " Fpts")
        print("\n")
        lineupNum -= 1


if __name__ == "__main__":
    remainingPosList = ["RB", "RB", "WR", "WR", "FLEX"]
    numRemainingPos = len(remainingPosList)
    remainingSal = 33600
    excludedNames = ["Amari Cooper", "Ezekiel Elliott", "Michael Gallup", "Tyler Lockett"]
    salariesDir = "wk16_salaries.csv"
    projDir = "wk16_projections.csv"
    optimize(numRemainingPos, remainingPosList, remainingSal, excludedNames, 100, salariesDir, projDir)


