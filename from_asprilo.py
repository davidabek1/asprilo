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
    #if os.path.exists(fName):
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
    #print(txtfile)
    X = Y = 0
    robots = []
    shelves = []
    nodes = []
    for  i, line in enumerate(txtfile):
        #print(line)
        #if 'Grid Size X' in line:
        #    X = (int)(line.split(' ')[-1])
            
        #    print(f'X = {X}')
        #if 'Grid Size Y' in line:
        #    Y = (int)(line.split(' ')[-1])
        #    print(f'Y = {Y}')


        if 'init(object(robot' in line:
            split = line.split(',')
            left = split[-2].replace("(", "")
            right = split[-1].replace(")", "").replace(".", "")
            robots.append((str(int(left)-1),str(int(right)-1)))
            print(f'robot id {len(robots)} : ({left},{right})')

        if 'init(object(shelf' in line:
            split = line.split(',')
            left = split[-2].replace("(", "")
            right = split[-1].replace(")", "").replace(".", "")
            shelves.append((str(int(left)-1),str(int(right)-1)))
            print(f'shelves id {len(shelves)} : ({left},{right})')

        if 'init(object(node' in line:
            split = line.split(',')
            left = split[-2].replace("(", "")
            right = split[-1].replace(")", "").replace(".", "")
            nodes.append(((int)(left)-1,(int)(right)-1))
            print(f'node id {len(nodes)} : ({left},{right})')
            X = max(X,(int)(left))
            Y = max(Y,(int)(right))
            

    print (f'X = {X}, Y = {Y}')
            
    return robots, shelves, X, Y, nodes

def gen(robots, shelves, X, Y, nodes, file_dir):

    agents_file = f'{len(robots)}\n'

    for i, line in enumerate(robots):
        #print(f'ans is {line}')
        agents_file += shelves[i][1] + ',' + shelves[i][0] + ',' + line[1] + ',' + line[0] + '\n'
    print(agents_file)

    maze = f'{Y},{X}\n'
    for row in range(0, Y):
        for col in range(0,X):
            if ((col,row)) in nodes:
                #free space
                maze+='0'
            else:
                #obstacle
                maze+='1'

            #end of line?
            if col != X-1:
                maze+=','
            else:
                maze+='\n'
    print(maze)


    text_file = open(file_dir+'/'+"agents.agents", "w")

    text_file.write(agents_file)

    text_file.close()


    text_file = open(file_dir+'/'+"maze.map", "w")

    text_file.write(maze)

    text_file.close()


    
    
def main():
    print("asprilo parser")
    #print('This is the name of the script: ', sys.argv[0])
    #print('Number of arguments: ', len(sys.argv))
    #print('The arguments are: ' , str(sys.argv))

    checkargs()
    fName = sys.argv[1]
    file_dir, _ = os.path.split(fName)
    #fName = 'x19_y9_n171_r6_s45_ps3_pr180_u540_o12_N1.lp'
    #fName = 'x11_y6_n66_r3_s12_ps2_pr5_u50_o3_N001.lp'
    txtfile = loadFile(fName)
    #agents_file, map_file =
    robots, shelves, X, Y,  nodes = parse(txtfile)

    gen(robots, shelves, X, Y, nodes, file_dir)
    #print(robots)






        

if __name__== "__main__":
    main()
    sys.exit()
