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
    return maximal_distance, farthest

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
        interval = right - left - 1
        if(isinf(neighbor_right[i]) or isinf(neighbor_left[i])): interval = interval*2-1
        if interval == max_interval_size:
            result.append(i)
        if interval > max_interval_size:
            max_interval_size = interval
            result = [i]
    return max_interval_size, result

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
        # print(arr)
        return 1

    # Find the set of cells that are equivalent candidates for the next user
    if nth == 0:
        candidates = range(len(arr))
    # elif preferEdges and (arr[0] == -1 or arr[-1] == -1):
    #     candidates = [0, len(arr) - 1]
    elif preferLongInterval:
        max_interval_size, candidates = find_max_interval(arr, neighbor_left, neighbor_right)
    else:
        candidates = range(len(arr))
    result = 0
    maximal_distance, preferred = findMaxDistanceSet(arr, neighbor_left, neighbor_right, candidates)
    # if (maximal_distance == 1) and (arr[0] == -1 or arr[-1] == -1) and preferEdges:
    #     maximal_distance, preferred = findMaxDistanceSet(arr, neighbor_left, neighbor_right, [0, len(arr) - 1])
    edgesVacant = (arr[0] == -1 or arr[-1] == -1)
    # Assign the next user and call recursively
    for i in preferred:
        # Assign an option
        sandwiched = (neighbor_left[i]==i-1) and (neighbor_right[i]==i+1)
        if (preferEdges and sandwiched and edgesVacant): continue
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

def p(n,i):
    if i==1:
        return p1(n,False,False)
    if i==2:
        return p1(n,False,True)
    if i==3:
        return p1(n,True,False)
    if i==4:
        return p1(n,True,True)
def p1(n, preferEdges, preferLongInterval):
    return p1_rec([-1] * n, [float('-inf')] * n, [float('inf')] * n, 0, preferEdges, preferLongInterval)
# print("sequences for p1:")
# print(f'A total of {p1(7,False,False)} sequences')
print("sequences for p2:")
print(f'A total of {p1(5,True,True)} sequences')
# print("sequences for p3:")
# print(f'A total of {p1(7,True,False)} sequences')
# print("sequences for p4:")
# print(f'A total of {p1(7,True,True)} sequences')
for j in range(1,5):
    for i in range(11):
         print(f'p{j}({i}) = {p(i,j)}')
