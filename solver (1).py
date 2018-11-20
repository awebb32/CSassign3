import sys
from satispy import CnfFromString
from satispy.solver import Minisat

if(len(sys.argv) < 2):
    print("No argument supplied. Argument must be the path to the expression file.")
    sys.exit()
elif(len(sys.argv) > 2):
    print("Too many arguments supplied. The only argument should be the path to the execution file.")
    sys.exit()

expressions = []
try:
    path = str(sys.argv[len(sys.argv)-1])
    expfile = open(path,'r')
    expressions = expfile.readlines()
except FileNotFoundError:
    print("Error: File not found.")
    sys.exit(1)
except:
    print("Error: A problem has occured while opening the expression file.")
    sys.exit(1)

expr = "({})".format(expressions[0].rstrip())
for i in range(1, len(expressions)):
    expr += " & ({})".format(expressions[i].rstrip())

print("\nAttempting to solve: " + expr)

count = 0
while True:

    expression = None
    solution = None
    symbols = []
    try:
        expression, symbols = CnfFromString.create(expr)
        solver= Minisat()

        solution = solver.solve(expression)
    except:
        print("Error: Expression file could not be parsed. Please check variable names and operator symbols:\n-NOT: -(unary)\n-AND: &\n-OR: |\n-XOR: ^\n-IMPLICATION: >>")
        sys.exit(1)

    if solution.success:
        if count == 0: print ("\nThe expression is satisfiable with:")
        print("\n--{}:".format(count+1))

        bools = []
        keys = []
        for variable in symbols.keys():
            print("{}: {}".format(variable, solution[symbols[variable]]))
            keys.append(variable)
            bools.append(solution[symbols[variable]])

        if bools[0]:
            removeForm =  "-(" + keys[0]
        else:
            removeForm = "-(-({})".format(keys[0])

        for j in range(1, len(keys)):
            if bools[j]:
                removeForm += " & " + keys[j]
            else:
                removeForm += " & -({})".format(keys[j])
        removeForm += ")"

    else:
        if count == 0: print ("\nThe expression cannot be satisfied.")
        break;
    expr += " & " + removeForm
    count += 1
