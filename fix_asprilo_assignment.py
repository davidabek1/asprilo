import sys
import os


def printUsage():
    help = 'usage: ' + sys.argv[0] +' [asprilo-file.lp>]\n'
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
            

    #print (f'X = {X}, Y = {Y}')
            
    return robots, shelves, X, Y, nodes



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
    print("asprilo fix assaignments")
 
    checkargs()
    fName = sys.argv[1]
    file_dir, _ = os.path.split(fName)
    #fName = 'x19_y9_n171_r6_s45_ps3_pr180_u540_o12_N1.lp'
    #fName = 'x11_y6_n66_r3_s12_ps2_pr5_u50_o3_N001.lp'
    txtfile = loadFile(fName)
    #agents_file, map_file =
    robots, shelves, X, Y,  nodes = parse(txtfile)

    #print(robots)
    assign(fName, robots, shelves)





        

if __name__== "__main__":
    main()
    sys.exit()
