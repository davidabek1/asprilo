import sys
import os


def printUsage():
    help = 'usage: ' + sys.argv[0] +' [asprilo-file.plan>]\n'
    help.join('  -h    display help')
    print(help)

def checkargs():
    if len(sys.argv) != 2:
        printUsage()
        sys.exit([1])

def loadFile(fName):
    #if os.path.exists(fName):
        res = []
        try:
            with open(fName, 'rb') as f:
                for line in f:
                    tmp = line.decode("utf-8").split('. ')
                    for ind in tmp:
                        print(ind)
                        res.append(ind)
                return res
        except (IOError, OSError) as e:
            print(e)
            sys.exit([1])


def parse(txtfile):
    #print(txtfile)
    X = Y = 0
    robots = []
    shelves = []
    nodes = []
    steps=0
    for  i, line in enumerate(txtfile):
        #print(line)
        #if 'Grid Size X' in line:
        #    X = (int)(line.split(' ')[-1])
            
        #    print(f'X = {X}')
        #if 'Grid Size Y' in line:
        #    Y = (int)(line.split(' ')[-1])
        #    print(f'Y = {Y}')


        if 'init(object(robot' in line:
            #print(line)
            split = line.split(',')
            left = split[-2].replace("(", "")
            right = split[-1].replace(")", "").replace(".", "")
            robots.append((int(left)-1,int(right)-1))
            #print(f'robot id {len(robots)} : ({left},{right})')

        if 'init(object(shelf' in line:
            split = line.split(',')
            left = split[-2].replace("(", "")
            right = split[-1].replace(")", "").replace(".", "")
            shelves.append((str(int(left)-1),str(int(right)-1)))
            #print(f'shelves id {len(shelves)} : ({left},{right})')

        if 'init(object(node' in line:
            split = line.split(',')
            left = split[-2].replace("(", "")
            right = split[-1].replace(")", "").replace(".", "")
            nodes.append(((int)(left)-1,(int)(right)-1))
            #print(f'node id {len(nodes)} : ({left},{right})')
            X = max(X,(int)(left))
            Y = max(Y,(int)(right))
            
        if 'occurs(object(robot' in line:
            clean = line.replace("(", "").replace(")", "").replace(".", "")
            split = clean.split(',')
            robot_id = split[1]
            left = (int)(split[3])
            right = (int)(split[4])
            step = (int)(split[5])
            #plan.append(((int)(left)-1,(int)(right)-1))
            print(f'robot {robot_id} move x:{left} y:{right} step:{step}')
            steps = max(steps,step)


    print (f'max step: {steps}')
            
    return robots, shelves, X, Y, nodes, steps

def getPlan(txtfile, robots, max_step):
    #occurs(object(robot,4),action(move,(-1,0)),9).
    plan = {}
    for robot, location in enumerate(robots):
        for step in range(0,max_step+1):
            plan[(step,robot)]=location
            print(location)



    for  i, line in enumerate(txtfile):
        #print(line)
        if 'occurs(object(robot' in line:
            clean = line.replace("(", "").replace(")", "").replace(".", "")
            split = clean.split(',')
            robot_id = (int)(split[1])
            left = (int)(split[3])
            right = (int)(split[4])
            step = (int)(split[5])
            #plan.append(((int)(left)-1,(int)(right)-1))
            for i in range(step,max_step+1):
                plan[(i,robot_id-1)]=(plan[(step-1,robot_id-1)][0] + left,plan[(step-1,robot_id-1)][1] + right)
            print(f'robot {robot_id-1} move x:{left} y:{right} step:{step} {plan[(step,robot_id-1)]}')
    #print(plan)

    line=''
    for step in range(0,max_step+1):
        line += f'{step} |'
        for robot, location in enumerate(robots):
            move = plan[(step,robot)]
            #print(move)
            #reversed
            line+=f'({(int)(move[1])},{(int)(move[0])})|'
            #print(f'plan[(step,robot)]=location
        line+='\n'
        print(line)
 


def assign(fName, robots, shelves):
    try:
        with open(fName, 'a') as f:
            for i, robot in enumerate(robots):
                newline = f'assign(robot({i+1}),shelf({i+1}),station(1)).\n'
                f.write(newline)
    except (IOError, OSError) as e:
        print(e)
        sys.exit([1])
    
def main():
    print("asprilo to eli")
 
    checkargs()
    fName = sys.argv[1]
    file_dir, _ = os.path.split(fName)
    txtfile = loadFile(fName)
    
    robots, shelves, X, Y,  nodes, steps = parse(txtfile)
    plan = getPlan(txtfile, robots, steps)
    #print(robots)
    #assign(fName, robots, shelves)





        

if __name__== "__main__":
    main()
    sys.exit()
