from math import isinf

def modn(i,n):
    if isinf(i):return i
    return (i+n)%n

def checkKings(arr):
    for i in range(len(arr)-1):
        if (abs(arr[i]-arr[(i+1)%len(arr)])==1): return False
    return True
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
        distance = min(modn(i - neighbor_left[i],len(arr)), modn(neighbor_right[i] - i,len(arr)))
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
        interval = (right - left - 1+len(arr))%len(arr)
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
def c1_rec(arr, neighbor_left, neighbor_right, nth, preferEdges, preferLongInterval,outputFile):
    # Base case
    if nth == len(arr):
        if not checkKings(arr): return 0
        outputFile.write(f'{str(arr)}\n')
        return 1

    # Find the set of cells that are equivalent candidates for the next user
    if nth == 0:
        candidates = range(len(arr))
        maximal_distance, preferred = float('inf'), candidates
    # elif preferEdges and (arr[0] == -1 or arr[-1] == -1):
    #     candidates = [0, len(arr) - 1]
    else:
        if preferLongInterval:
            max_interval_size, candidates = find_max_interval(arr, neighbor_left, neighbor_right)
        else:
            candidates = range(len(arr))
        maximal_distance, preferred = findMaxDistanceSet(arr, neighbor_left, neighbor_right, candidates)
    # if (maximal_distance == 1) and (arr[0] == -1 or arr[-1] == -1) and preferEdges:
    #     maximal_distance, preferred = findMaxDistanceSet(arr, neighbor_left, neighbor_right, [0, len(arr) - 1])
    result = 0
    edgesVacant = (arr[0] == -1 or arr[-1] == -1)
    # Assign the next user and call recursively
    for i in preferred:
        # Assign an option
        sandwiched = (neighbor_left[i]==i-1) and (neighbor_right[i]==i+1)
        if (preferEdges and sandwiched and edgesVacant): continue
        arr[i] = nth+1
        left = max(-1, neighbor_left[i])
        right = min(len(arr), neighbor_right[i])
        j = (left+1)
        while (j % len(arr)) != i:
            neighbor_right[j % len(arr)] = i
            j = (j+1)%len(arr)
        j = i+1
        while (j % len(arr)) != right%len(arr):
            neighbor_left[j % len(arr)] = i
            j = j+1


        # Find the number of options for the next users
        result += c1_rec(arr, neighbor_left, neighbor_right, nth + 1, preferEdges, preferLongInterval,outputFile)

        # Reverse the last option
        j = left+1
        while (j % len(arr)) != i:
            neighbor_right[j % len(arr)] = neighbor_right[i]
            j = (j + 1)
        j = (i+1)
        while (j % len(arr)) != right%len(arr):
            neighbor_left[j % len(arr)] = neighbor_left[i]
            j = j + 1
        arr[i] = -1

    return result

def c(n,i,circular,outputFile):
    if i==1:
        return c1(n,False,False, circular,outputFile)
    if i==2:
        return c1(n,False,True, circular,outputFile)
    if i==3:
        return c1(n,True,False, circular,outputFile)
    if i==4:
        return c1(n,True,True, circular,outputFile)
def c1(n, preferEdges, preferLongInterval,circular,outputFile):
    if circular:
        input = [-1] * n
        input[0]=0
        return n*c1_rec(input, [0]*n, [0]*n, 1, preferEdges, preferLongInterval,outputFile)
    else:
        return c1_rec([-1] * n, [float('-inf')] * n, [float('inf')] * n, 0, preferEdges, preferLongInterval,outputFile)
# print("sequences for p1:")
# print(f'A total of {p1(7,False,False)} sequences')
# print("sequences for p2:")
# print(f'A total of {p1(5,True,True)} sequences')
# print("sequences for p3:")
# print(f'A total of {p1(7,True,False)} sequences')
# print("sequences for p4:")
# print(f'A total of {p1(7,True,True)} sequences')
# for j in range(1,3):
#     for i in range(1,11):
#          print(f'c{j}({i}) = {c(i,j,True)}')
for j in range(1,2):
    for i in range(1,10):
        outputFile = open(f'output/phones_kings_{i}.txt', 'w')
        print(f'p{j}({i}) = {c(i,j,False,outputFile)}')
        outputFile.close()
