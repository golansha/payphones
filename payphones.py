from math import isinf

""" 
finds the set of cells for which the closest occupied cell is most distant
Parameters
arr: array
    The current cell assignment
neighbor_left: array
    For each cell, what is its closest neighbor on the left
neighbor_right: array
    For each cell, what is its closest neighbor on the right
places: iterable
    A filter on the potential cells to examine
"""
def findMaxDistanceSet(arr, neighbor_left, neighbor_right, places):
    farthest = []
    maximal_distance = 0
    for i in places:
        if arr[i] != -1:
            continue
        distance = min(i - neighbor_left[i], neighbor_right[i] - i)
        if distance == maximal_distance:
            farthest.append(i)
        if distance > maximal_distance:
            maximal_distance = distance
            farthest = [i]
    return farthest

""" 
finds the cells belonging to the longest interval/s
Parameters
arr: array
    The current cell assignment
neighbor_left: array
    For each cell, what is its closest neighbor on the left
neighbor_right: array
    For each cell, what is its closest neighbor on the right
"""
def find_max_interval(arr, neighbor_left, neighbor_right):
    result = []
    max_interval_size = 0
    for i in range(len(arr)):
        if arr[i] != -1: continue
        left = max(-1, neighbor_left[i])
        right = min(len(arr), neighbor_right[i])
        interval = right - left
        if interval == max_interval_size:
            result.append(i)
        if interval > max_interval_size:
            max_interval_size = interval
            result = [i]
    return result

""" 
counts the number of payphones permutations
Parameters
arr: array
    The current cell assignment
neighbor_left: array
    For each cell, what is its closest neighbor on the left
neighbor_right: array
    For each cell, what is its closest neighbor on the right
nth: int
    The number of occupied cells
preferEdges: bool
    indicates whether a payphone user prefers not to be sandwiched (relevant for p3 and p4)
preferLongInterval: bool
    indicates whether a payphone user prefers long intervals (relevant for p2 and p4)


"""
def p1_rec(arr, neighbor_left, neighbor_right, nth, preferEdges, preferLongInterval):
    # Base case
    if nth == len(arr):
        return 1

    # Find the set of cells that are equivalent candidates for the next user
    if nth == 0:
        candidates = range(len(arr))
    elif preferEdges and (arr[0] == -1 or arr[-1] == -1):
        candidates = [0, len(arr) - 1]
    elif preferLongInterval:
        candidates = find_max_interval(arr, neighbor_left, neighbor_right)
    else:
        candidates = range(len(arr))
    result = 0
    preferred = findMaxDistanceSet(arr, neighbor_left, neighbor_right, candidates)

    # Assign the next user and call recursively
    for i in preferred:
        # Assign an option
        arr[i] = nth
        left = max(-1, neighbor_left[i])
        right = min(len(arr), neighbor_right[i])
        for j in range(left + 1, i):
            neighbor_right[j] = i
        for j in range(i + 1, right):
            neighbor_left[j] = i

        # Find the number of options for the next users
        result += p1_rec(arr, neighbor_left, neighbor_right, nth + 1, preferEdges, preferLongInterval)

        # Reverse the last option
        for j in range(left + 1, i):
            neighbor_right[j] = neighbor_right[i]
        for j in range(i + 1, right):
            neighbor_left[j] = neighbor_left[i]
        arr[i] = -1

    return result


def p1(n, preferEdges, preferLongInterval):
    return p1_rec([-1] * n, [float('-inf')] * n, [float('inf')] * n, 0, preferEdges, preferLongInterval)


for i in range(11):
    print(f'p4({i}) = {p1(i, True, True)}')
