#! /usr/bin/env python
# coding: utf-8
 
# generator-1.py, a simple python dungeon generator by
# James Spencer <jamessp [at] gmail.com>.

# To the extent possible under law, the person who associated CC0 with
# pathfinder.py has waived all copyright and related or neighboring rights
# to pathfinder.py.

# You should have received a copy of the CC0 legalcode along with this
# work. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
 
#from __future__ import print_function
import random

import dungeon as dn

import sys
 
CHARACTER_TILES = {'stone': ' ',
                   'floor': '.',
                   'wall': '#'}
 
 
class Adapter():
    def __init__(self, maze, robots, width, height, N):
        self.robots = robots
        self.maze = maze
        self.width=width
        self.height=height
        self.N=N

 
    def gen_map(self):
        lp_file = ''
        s = maze.split('\n')
        node_id = 1
        X = Y = 0
        S = robots
        occupied={}
        for row, line in enumerate(s):
            Y = max(Y,row)
            for col, tile in enumerate(line):
                X = max(X,col)
                occupied[(col,row)]=True
                if tile == '0':
                    #print('0', sep='', end='', flush=True)
                    lp_file+=f'init(object(node,{node_id}),value(at,({col+1},{row+1}))).\n'
                    node_id+=1
                    occupied[(col,row)]=False
                #if tile == '1':
                #    print('1', sep='', end='', flush=True)
                    
                #print(tile)
            #print('\n', sep='', end='', flush=True)

        print(lp_file)

        
        header = ''
        header = '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n'
        header +=f'% Grid Size X:                      {X}\n'
        header +=f'% Grid Size Y:                      {Y}\n'
        header +=f'% Number of Nodes:                  {node_id-1}\n'
        header +=f'% Number of Highway Nodes:          0\n'
        header +=f'% Number of Robots:                 {S}\n'
        header +=f'% Number of Shelves:                {S}\n'
        header +=f'% Number of Picking Stations:       0\n'
        header +=f'% Number of Products:               0\n'
        header +=f'% Number of Product Units in Total: 0\n'
        header +=f'% Number of Orders:                 0\n'
        header +='%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n\n'
        header +='#program base.\n\n'
        header +='% init\n'



        






        asprilo_file = header + lp_file

        freeNodes = node_id-1

        #robots
        left = S
        robot_id = 1
        while left > 0:
            if freeNodes==0:
                return
            #print (random.randint(0, 5))
            rand_x = random.randint(0, X-1)
            rand_y = random.randint(0, Y-1)
            if occupied[(rand_x,rand_y)]==True:
                #print(f'{rand_x},{rand_y} is occupied!')
                #left-=1
                continue                
            asprilo_file+=f'init(object(robot,{robot_id}),value(at,({rand_x+1},{rand_y+1}))).\n'
            robot_id+=1
            occupied[(rand_x,rand_y)]=True
            left-=1
            freeNodes-=1


        #shelves
        left = S
        shelf_id = 1
        while left > 0:
            if freeNodes==0:
                return
            #print (random.randint(0, 5))
            rand_x = random.randint(0, X-1)
            rand_y = random.randint(0, Y-1)

            if occupied[(rand_x,rand_y)]==True:
                #print(f'{rand_x},{rand_y} is occupied!')
                #left-=1
                continue                
            asprilo_file+=f'init(object(shelf,{shelf_id}),value(at,({rand_x+1},{rand_y+1}))).\n'
            asprilo_file+=f'init(object(product,{shelf_id}),value(on,({shelf_id},1))).\n'
            asprilo_file+=f'init(object(order,{shelf_id}),value(pickingStation,1)).\n'
            asprilo_file+=f'init(object(order,{shelf_id}),value(line,({shelf_id},1))).\n'
            shelf_id+=1
            occupied[(rand_x,rand_y)]=True
            left-=1
            freeNodes-=1

        #picking station
        left = 1
        while left > 0:
            if freeNodes==0:
                return
            #print (random.randint(0, 5))
            rand_x = random.randint(0, X-1)
            rand_y = random.randint(0, Y-1)
            if occupied[(rand_x,rand_y)]==True:
                #print(f'{rand_x},{rand_y} is occupied!')
                #left-=1
                continue                
            asprilo_file+=f'init(object(pickingStation,1),value(at,({rand_x+1},{rand_y+1}))).\n'
            #shelf_id+=1
            occupied[(rand_x,rand_y)]=True
            left-=1    
            freeNodes-=1

        assignments = 1
        asprilo_file_assigned = ''
        #assignments
        for a in range(0,assignments):
            asprilo_file_assigned = asprilo_file
            shuffled_s = list(range(1,S+1))
            random.shuffle(shuffled_s)
            for i in range(0,S):
                asprilo_file_assigned+=f'assign(robot({i+1}),shelf({shuffled_s[i]}),station(1)).\n'







        print(asprilo_file_assigned)


        file_name = f'generatedInstances/x{self.width}_y{self.height}_n{node_id-1}_r{self.robots}_N{self.N:03d}.lp'
        text_file = open(file_name, "w")

        text_file.write(asprilo_file_assigned)

        text_file.close()


def printUsage():
    #help = 'usage: gen.py [X] [Y] [Robots/Shelves] [iterations] [assaignments] [batchs size]\n'
    help = 'usage: gen.py [X] [Y] [Robots/Shelves] [max rooms] [min room] [max room] [batchs size]\n'
    help += 'example: gen.py 15 10 5 4 2 3\n'
    help.join('  -h    desplay help')
    print(help)

def checkargs():
    if len(sys.argv) != 8:
        printUsage()
        sys.exit()

 
if __name__ == '__main__':
    checkargs()
    X = int(sys.argv[1])
    Y = int(sys.argv[2])
    robots = int(sys.argv[3])
    max_rooms = int(sys.argv[4])
    min_room_size = int(sys.argv[5])
    max_room_size = int(sys.argv[6])
    batch_size = int(sys.argv[7])

    gen = dn.Generator(width=X, height=Y, max_rooms=max_rooms, min_room_xy=min_room_size,
                 max_room_xy=max_room_size, rooms_overlap=False, random_connections=1,
                 random_spurs=3)    
    #gen = dn.Generator(width=16, height=16, max_rooms=5, min_room_xy=3, max_room_xy=5, rooms_overlap=False, random_connections=1,random_spurs=3)
    gen.gen_level()
    maze = gen.gen_tiles_level()
    for n in range(1,batch_size+1):    
        myadapter = Adapter(maze, robots, width=X, height=Y, N=n)
        myadapter.gen_map()
        #print(maze)
