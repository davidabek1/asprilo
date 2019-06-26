import os
import subprocess
import glob
import csv
import time
import collections
from ast import literal_eval


os.chdir('/home/david/asprilo/')
problems = glob.glob('generatedInstances/*.lp')


def write_line(filename, dict, is_first=False):
    dict = collections.OrderedDict(sorted(dict.items()))
    with open(filename, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=',', lineterminator='\n', fieldnames=dict.keys())
        if is_first:
            writer.writeheader()
        writer.writerow(dict)

def find_max_steps(content):
    init_plan = []
    nodes = []
    agents = {}
    grid_X = grid_Y = 0
    parse_content = content.split('.')
    steps = parse_content[-2].split(',')[-1].strip(')')
    for line in parse_content:
        if 'init(' in line:
            init_plan.append(line+'.')
        if 'init(object(robot' in line:
            line_split = line.split(',')
            robot_id = line_split[1].strip(')')
            X = line_split[-2].strip('(')
            Y = line_split[-1].strip(')')
            agents[robot_id] = ['({},{})'.format(X,Y),'({},{})'.format(X,Y)]
        if 'occurs(object(robot' in line:
            line_split = line.split(',')
            robot_id = line_split[1].strip(')')
            move_X = line_split[-3].strip('(')
            move_Y = line_split[-2].strip(')')
            new_X = literal_eval(agents[robot_id][1])[0] + int(move_X)
            new_Y = literal_eval(agents[robot_id][1])[1] + int(move_Y)
            agents[robot_id][1] = '({},{})'.format(new_X,new_Y)
        if 'init(object(node' in line:
            line_split = line.split(',')
            X = line_split[-2].strip('(')
            Y = line_split[-1].strip(')')
            nodes.append(((int)(X)-1,(int)(Y)-1))
            grid_X = max(grid_X,(int)(X))
            grid_Y = max(grid_Y,(int)(Y))

    return steps, agents, grid_X,grid_Y, nodes, init_plan

#init(object(robot,1),value(at,(1,1))).
#occurs(object(robot,5),action(move,(1,0)),9).


def gen_agents_file(agents, filename):
    file_content = '{}\n'.format(len(agents))
    for key in sorted(agents):
        source_tuple = literal_eval(agents[key][0])
        target_tuple = literal_eval(agents[key][1])
        # agents file expect to start from target to source
        # agents file locations start from 0,0
        # agents file uses rows by columns (opposite from asprilo of X[cols],Y[rows])
        file_content += str(target_tuple[1]-1) + ',' + str(target_tuple[0]-1) + ',' \
                        + str(source_tuple[1]-1) + ',' + str(source_tuple[0]-1) + '\n'
    with open(filename, 'w') as f:
        f.write(file_content)


def gen_map_file(grid_X, grid_Y, nodes, filename):
    file_content = '{},{}\n'.format(grid_Y,grid_X)
    for row in range(0, grid_Y):
        for col in range(0, grid_X):
            if ((col, row)) in nodes:
                #free space
                file_content += '0'
            else:
                #obstacle
                file_content += '1'

            # end of line?
            if col != grid_X-1:
                file_content += ','
            else:
                file_content += '\n'

    with open(filename, 'w') as f:
        f.write(file_content)


def gen_init_instance(init_plan, filename):
    file_content = ''
    for line in init_plan:
        file_content += line + '\n'
    with open(filename, 'w') as f:
        f.write(file_content)


def gen_a_star_plan(a_star_plan, filename):
    max_steps = a_star_plan.count('\n')
    with open(filename, 'w') as f:
        f.write(a_star_plan)
    return max_steps


def gen_epea_plan(epea_plan, filename):
    max_steps = epea_plan.count('\n')
    with open(filename, 'w') as f:
        f.write(epea_plan)
    return max_steps


def gen_icts_plan(icts_plan, filename):
    max_steps = icts_plan.count('\n')
    with open(filename, 'w') as f:
        f.write(icts_plan)
    return max_steps


def gen_cbs_plan(cbs_plan, filename):
    max_steps = cbs_plan.count('\n')
    with open(filename, 'w') as f:
        f.write(cbs_plan)
    return max_steps


def prob_order(x):
    r_loc = x.find('_r')
    r_no = x[r_loc+2:r_loc+4]
    r_no = r_no.strip('_')
    N_loc = x.find('_N')
    N_no = x[N_loc+2:N_loc+5]
    return int(r_no+N_no)


problems = sorted(problems, key=prob_order)
is_first = True
for p in problems:
    start_time = time.time()
    content = subprocess.run('clingo encodings/m/encoding.ilp {} --outf=0 -V0 --out-atomf=%s. | head -n1'.format(p),stdout=subprocess.PIPE,shell=True)
    solve_time = time.time() - start_time
    solver_output = content.stdout.decode('utf-8')
    solver_success = not(content.returncode)
    plan_file = p[:-2]+'plan'
    if solver_success:
        with open(plan_file, 'w') as f:
            f.write(solver_output)
        max_steps, agents, grid_X, grid_Y, nodes, init_plan = find_max_steps(solver_output)
        gen_agents_file(agents, p[:-2]+'agents')
        gen_map_file(grid_X, grid_Y, nodes, p[:-2]+'map')
        gen_init_instance(init_plan, p[:-2]+'init')
        #a_star
        start_time = time.time()
        content = subprocess.run('dotnet solvers/A_Star_WithOD_WithID.dll {} {}'.format(p[:-2]+'map',p[:-2]+'agents'),stdout=subprocess.PIPE,shell=True)
        a_star_time = time.time() - start_time
        a_star_output = content.stdout.decode('utf-8')
        a_star_plan_file = p[:-2]+'astar'
        astar_steps = gen_a_star_plan(a_star_output,a_star_plan_file)
        #EPEAstarWithID
        start_time = time.time()
        content = subprocess.run('dotnet solvers/EPEAstarWithID.dll {} {}'.format(p[:-2]+'map',p[:-2]+'agents'),stdout=subprocess.PIPE,shell=True)
        epea_time = time.time() - start_time
        epea_output = content.stdout.decode('utf-8')
        epea_plan_file = p[:-2]+'epea'
        epea_steps = gen_epea_plan(epea_output,epea_plan_file)
        #ICTS_WithID
        start_time = time.time()
        content = subprocess.run('dotnet solvers/ICTS_WithID.dll {} {}'.format(p[:-2]+'map',p[:-2]+'agents'),stdout=subprocess.PIPE,shell=True)
        icts_time = time.time() - start_time
        icts_output = content.stdout.decode('utf-8')
        icts_plan_file = p[:-2]+'icts'
        icts_steps = gen_icts_plan(icts_output,icts_plan_file)
        #modern-cbs
        start_time = time.time()
        content = subprocess.run('dotnet solvers/modern-cbs.dll {} {}'.format(p[:-2]+'map',p[:-2]+'agents'),stdout=subprocess.PIPE,shell=True)
        cbs_time = time.time() - start_time
        cbs_output = content.stdout.decode('utf-8')
        cbs_plan_file = p[:-2]+'cbs'
        cbs_steps = gen_cbs_plan(cbs_output,cbs_plan_file)
    test_scores = {'problem_file': p, 'asp_time': solve_time, 'asp_steps': max_steps \
                   ,'astar_time': a_star_time, 'astar_steps': astar_steps \
                   ,'epea_time': epea_time, 'epea_steps': epea_steps \
                   ,'icts_time': icts_time, 'icts_steps': icts_steps \
                   ,'cbs_time': cbs_time, 'cbs_steps': cbs_steps}
    write_line('solvers_results.csv',test_scores,is_first)
    is_first=False


