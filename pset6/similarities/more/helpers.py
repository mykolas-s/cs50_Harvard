from enum import Enum


class Operation(Enum):
    """Operations"""

    DELETED = 1
    INSERTED = 2
    SUBSTITUTED = 3

    def __str__(self):
        return str(self.name.lower())


def distances(a, b):
    """Calculate edit distance from a to b"""
    # set up 2D list - matrix. Add values for base cases
    cost = [[(0, None) for x in range(len(b) + 1)] for y in range(len(a) + 1)]

    for i in range(1, len(a) + 1):
        cost[i][0] = (i, Operation.DELETED)
    for j in range(1, len(b) + 1):
        cost[0][j] = (j, Operation.INSERTED)

    # calculate cost for other steps and add the cost to the matrix
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cdel, _ = cost[i - 1][j]
            cins, _ = cost[i][j - 1]
            csub, _ = cost[i - 1][j - 1]
            cdel += 1
            cins += 1
            if (a[i - 1] != b[j - 1]):
                csub += 1
            if (cdel < cins and cdel < csub):
                cost[i][j] = (cdel, Operation.DELETED)
            elif (cins < cdel and cins < csub):
                cost[i][j] = (cins, Operation.INSERTED)
            else:
                cost[i][j] = (csub, Operation.SUBSTITUTED)
    return cost