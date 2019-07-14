import sys
import os


def printUsage():
    help = 'usage: parser.py [asprilo.lp>]\n'
    help.join('  -h    display help')
    print(help)


def checkargs():
    if len(sys.argv) != 2:
        printUsage()
        sys.exit([1])


def loadFile(fName):
        res = []
        try:
            with open(fName, 'rb') as f:
                for line in f:
                    tmp = line.decode("utf-8").strip()
                    res.append(tmp)
                return res
        except (IOError, OSError) as e:
            print(e)
            sys.exit([1])


def parse(txtfile):
    X = Y = 0
    robots = []
    shelves = []
    nodes = []
    robot2shelf = {}
    for i, line in enumerate(txtfile):
        if 'init(object(robot' in line and 'value(at' in line:
            split = line.split(',')
            left = split[-2].replace("(", "")
            right = split[-1].replace(")", "").replace(".", "")
            robots.append((str(int(left)-1),str(int(right)-1)))
            # print(f'robot id {len(robots)} : ({left},{right})')

        if 'init(object(shelf' in line:
            split = line.split(',')
            left = split[-2].replace("(", "")
            right = split[-1].replace(")", "").replace(".", "")
            shelves.append((str(int(left)-1),str(int(right)-1)))
            # print(f'shelves id {len(shelves)} : ({left},{right})')

        if 'init(object(node' in line:
            split = line.split(',')
            left = split[-2].replace("(", "")
            right = split[-1].replace(")", "").replace(".", "")
            nodes.append((int(left)-1, int(right)-1))
            # print(f'node id {len(nodes)} : ({left},{right})')
            X = max(X, int(left))
            Y = max(Y, int(right))

        if 'assign(robot(' in line:
            split = line.split(',')
            robot = split[0].replace("assign(", "").replace("robot(", "").replace(")", "")
            shelf = split[1].replace("shelf(", "").replace(")", "")
            robot2shelf[robot] = shelf

            

    # print (f'X = {X}, Y = {Y}')
            
    return robots, shelves, X, Y, nodes, robot2shelf


def gen(robots, shelves, X, Y, nodes, robot2shelf, file_dir):

    agents_file = f'{len(robots)}\n'

    for i, line in enumerate(robots):
        # handle cases where assign rules are not present, defaulting to robot 1..x assigned to shelf 1..x
        if len(robot2shelf) > 0:
            shelf = int(robot2shelf[str(i+1)])-1  # +1/-1 to convert actual object to location in list
        else:
            shelf = i
        agents_file += shelves[shelf][1] + ',' + shelves[shelf][0] + ',' + line[1] + ',' + line[0] + '\n'
    # print(agents_file)

    maze = f'{Y},{X}\n'
    for row in range(0, Y):
        for col in range(0, X):
            if (col, row) in nodes:
                # free space
                maze += '0'
            else:
                # obstacle
                maze += '1'

            # end of line?
            if col == X-1:
                maze += '\n'

    # print(maze)
    # writing agents file
    text_file = open(os.path.join(file_dir, "agents.agents"), "w")

    text_file.write(agents_file)

    text_file.close()
    # writing map file
    text_file = open(os.path.join(file_dir, "maze.map"), "w")

    text_file.write(maze)

    text_file.close()


def main(fName):
    print("asprilo parser")

    file_dir, _ = os.path.split(fName)
    txtfile = loadFile(fName)
    robots, shelves, X, Y,  nodes, robot2shelf = parse(txtfile)

    gen(robots, shelves, X, Y, nodes, robot2shelf, file_dir)


def from_asprilo_from_viz(content):
    print("asprilo parser to MAPF map and agents")
    robots, shelves, X, Y, nodes, robot2shelf = parse(content)
    gen(robots, shelves, X, Y, nodes, robot2shelf, '')

    # plan = ''
    # for l in content:
    #     plan += l
    # with open('viz.asp','w') as f:
    #     f.write(plan)


if __name__ == "__main__":
    checkargs()
    main(sys.argv[1])
    sys.exit()
