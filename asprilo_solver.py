import os
import subprocess
import glob
import csv
import time
import collections
from ast import literal_eval


#os.chdir('/home/david/asprilo/')
os.chdir('/home/zeged/mygits/asprilo/')
problems = glob.glob('generatedInstances/*.lp')
print(f'found {len(problems)} problems')

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
                file_content += ''
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

def gen_macbs_plan(macbs_plan, filename):
    max_steps = macbs_plan.count('\n')
    with open(filename, 'w') as f:
        f.write(macbs_plan)
    return max_steps

def gen_macbs_cl_plan(macbs_cl_plan, filename):
    max_steps = macbs_cl_plan.count('\n')
    with open(filename, 'w') as f:
        f.write(macbs_cl_plan)
    return max_steps

def prob_order(x):
    r_loc = x.find('_r')
    r_no = x[r_loc+2:r_loc+4]
    r_no = r_no.strip('_')
    N_loc = x.find('_N')
    N_no = x[N_loc+2:N_loc+5]
    return int(r_no+N_no)



astar_fail = False
astar_fail_counter = 0

macbs_fail = False
macbs_fail_counter = 0

icts_fail = False
icts_fail_counter = 0

cbs_fail = False
cbs_fail_counter = 0

fail_limit = 5

problems = sorted(problems, key=prob_order)
is_first = True
for p in problems:
    print(p)
    if astar_fail and macbs_fail and icts_fail and cbs_fail  :
        print('asprilo win')
        break

    start_time = time.time()
    content = subprocess.run('clingo encodings/m/encoding.ilp {} --outf=0 -V0 --out-atomf=%s.  | head -n1'.format(p),stdout=subprocess.PIPE,shell=True)
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
        print('a_star')
        if astar_fail:
            a_star_time = 'skip'
            astar_steps = 'NA'
            print('astar skip')

        else:
            start_time = time.time()
            content = subprocess.run('dotnet solvers/A_Star_WithOD_WithID-MAKESPAN.dll {} {}'.format( p[:-2]+'map', p[:-2] + 'agents') ,stdout=subprocess.PIPE,shell=True)
            a_star_time = time.time() - start_time
            a_star_output = content.stdout.decode('utf-8')
            a_star_plan_file = p[:-2]+'astar'
            astar_steps = gen_a_star_plan(a_star_output,a_star_plan_file) - 1
            if a_star_time > 280 or astar_steps < 3:
                astar_fail_counter += 1
                print(f'astar fail {astar_fail_counter}')
                astar_steps = 'NA'
                a_star_time = 'timeout'
                if astar_fail_counter == fail_limit : astar_fail = True
            else : astar_fail_counter = 0
                



        print('macbs-over-astarwithod-20-withBypass-withCardinalLookahead-MAKESPAN')
        #macbs-over-astarwithod-20-withBypass-withCardinalLookahead-MAKESPAN
        if macbs_fail:
            macbs_time = 'skip'
            macbs_steps = 'NA'
            print('macbs skip')

        else:
            start_time = time.time()
            content = subprocess.run('dotnet solvers/macbs-over-astarwithod-20-withBypass-withCardinalLookahead-MAKESPAN.dll {} {}'.format(p[:-2]+'map',p[:-2]+'agents'),stdout=subprocess.PIPE,shell=True)
            macbs_time = time.time() - start_time
            macbs_output = content.stdout.decode('utf-8')
            macbs_plan_file = p[:-2]+'cbs'
            macbs_steps = gen_macbs_plan(macbs_output,macbs_plan_file) -1
            if macbs_time > 280 or macbs_steps < 3:
                macbs_fail_counter += 1
                print(f'macbs fail {macbs_fail_counter}')
                macbs_steps = 'NA'
                macbs_time = 'timeout'
                if macbs_fail_counter == fail_limit : macbs_fail = True
            else:  macbs_fail_counter = 0




        print('ICTS_WithID-experimental-MAKESPAN')
        #ICTS_WithID-experimental-MAKESPAN
        if icts_fail:
            icts_time = 'skip'
            icts_steps = 'NA'
            print('icts skip')

        else:
            start_time = time.time()
            content = subprocess.run('dotnet solvers/ICTS_WithID-experimental-MAKESPAN.dll {} {}'.format(p[:-2]+'map',p[:-2]+'agents'),stdout=subprocess.PIPE,shell=True)
            icts_time = time.time() - start_time
            icts_output = content.stdout.decode('utf-8')
            icts_plan_file = p[:-2]+'cbs'
            icts_steps = gen_icts_plan(icts_output,icts_plan_file) -1
            duration = icts_time
            if icts_steps < 3 :
                print(f'icts fail')
                icts_time = 'fail'
                icts_steps = 'NA'
            if duration > 280:
                icts_fail_counter += 1
                print(f'icts timeout {icts_fail_counter}')
                icts_time = 'timeout'
                icts_steps = 'NA'
            else:
                icts_fail_counter = 0
            if icts_fail_counter == fail_limit : icts_fail = True







        print('cbs-withBypass-withCardinalLookahead-MAKESPAN')
        #cbs-withBypass-withCardinalLookahead-MAKESPAN
        if cbs_fail:
            cbs_time = 'skip'
            cbs_steps = 'NA'
            print('cbs skip')

        else:
            start_time = time.time()
            content = subprocess.run('dotnet solvers/cbs-withBypass-withCardinalLookahead-MAKESPAN.dll {} {}'.format(p[:-2]+'map',p[:-2]+'agents'),stdout=subprocess.PIPE,shell=True)
            cbs_time = time.time() - start_time
            cbs_output = content.stdout.decode('utf-8')
            cbs_plan_file = p[:-2]+'cbs'
            cbs_steps = gen_cbs_plan(cbs_output,cbs_plan_file) -1
            if cbs_time > 280 or cbs_steps < 3:
                cbs_fail_counter += 1
                print(f'cbs fail {cbs_fail_counter}')
                cbs_steps = 'NA'
                cbs_time = 'timeout'
                if cbs_fail_counter == fail_limit : cbs_fail = True
            else:  cbs_fail_counter = 0




    test_scores = {'problem_file': p, 'asp_time': solve_time, 'asp_steps': max_steps \
                   ,'astar_time': a_star_time, 'astar_steps': astar_steps \
                   ,'macbs_time': macbs_time, 'macbs_steps': macbs_steps \
                   ,'icts_time': icts_time, 'icts_steps': icts_steps \
                   ,'cbs_time': cbs_time, 'cbs_steps': cbs_steps}
    write_line('solvers_results.csv',test_scores,is_first)
    is_first=False


