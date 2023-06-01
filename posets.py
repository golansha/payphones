import ast


def put_i_in_place_j_and_shift(solution,i,j):
    result = [a if a<i else a+1 for a in solution]
    result.insert(j,i)
    return str(result)

def extendSolution(solution):
    solution1 = ast.literal_eval(solution)
    for i in range(1,len(solution1)+2):
        for j in range(len(solution1)+1):
            yield put_i_in_place_j_and_shift(solution1,i,j)
def check_poset(length,subSolutions,extendedSolutions,outputFile):
    allChildren =set()
    for solution in subSolutions:
        children =set()
        for extendedSolution in extendSolution(solution):
            if extendedSolution in extendedSolutions and extendedSolution not in children:
                children.add(extendedSolution)
                allChildren.add(extendedSolution)
                outputFile.write(f'{solution}, {extendedSolution}\n')
    if (len(allChildren) == len(extendedSolutions)):
        print(f'all permutations of size {length+2} have parents')
    else: print(f'The following permutations of size {length+2 } have no parent: {extendedSolutions.difference(allChildren)}')
solutions = []
for i in range(1,10):
    inputFile = open(f'output/phones_kings_{i}.txt')
    solutions.append({line.strip() for line in inputFile})
for i in range(8):
    outputFile = open(f'output/phones_kings_children_{i+1}.txt','w')
    check_poset(i,solutions[i],solutions[i+1],outputFile)