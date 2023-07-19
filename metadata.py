import json
import sys

with open('master.json') as master_file:
    data = json.load(master_file)
    count = len(data)
print (len(sys.argv))
if len(sys.argv) == 3:
    n1 = sys.argv[1]
    n2 = sys.argv[2]
    print(n1)
    print(n2)
    if n1.isnumeric() == False:
        print("Error: First parameter is not number")
        exit()
    elif n2.isnumeric() == False:
        print("Error: Second parameter is not number")
        exit()
    n1 = int(n1)
    n2 = int(n2)

    if n1 > n2:
        print("Error: n1 > n2")
        exit()
    elif n2 > count:
        print("Error: n2 > count")
        exit()
    
    n2 = n2 + 1

    with open('metadata.json', 'w') as outfile:
        json.dump(data[n1:n2], outfile)
else:
    print("Error: Over paramter count")
