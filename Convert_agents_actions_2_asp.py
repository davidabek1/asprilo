#!/usr/bin/env python
# coding: utf-8

import sys
from ast import literal_eval
import os


def print_usage():
    print('usage: asprilo_parser.py "solver_outcome.plan"')


def checkargs():
    if len(sys.argv) != 2:
        print_usage()
        sys.exit([1])


def loadfile(filename):
    with open (filename) as f:
        agents_actions = f.readlines()
    return agents_actions


def convert_from_solver_2_asp(agents_actions):
    asprilo_plan = []
    robots_prev_location = agents_actions[0].strip().split('|')[1:-1]
    for step_idx,agents_actions_line in enumerate(agents_actions[1:]):
        robots_cur_location = agents_actions_line.strip().split('|')[1:-1]
        for r_idx,r_loc in enumerate(robots_cur_location):
            move_y = literal_eval(r_loc)[0]-literal_eval(robots_prev_location[r_idx])[0]
            move_x = literal_eval(r_loc)[1]-literal_eval(robots_prev_location[r_idx])[1]
            if move_x != 0 or move_y != 0:
                # if both values are zero, robot is not moving
                # and we will not create an action for it.
                command = 'occurs(object(robot,{}),action(move,({},{})),{}).'.format(r_idx+1,move_x,move_y,step_idx+1)
                asprilo_plan.append(command)
        robots_prev_location = robots_cur_location
    return asprilo_plan


def write_plan_to_file(asprilo_plan, file_dir):
    plan = ''
    for l in asprilo_plan:
        plan += l+'\n'
    with open(os.path.join(file_dir, "asprilo_m_outcome.plan"), 'w') as f:
        f.write(plan)


def main(filename):
    file_dir, _ = os.path.split(filename)
    agents_actions = loadfile(filename)
    asprilo_plan = convert_from_solver_2_asp(agents_actions)
    write_plan_to_file(asprilo_plan, file_dir)


def convert_actions_from_viz(content):
    asprilo_plan = convert_from_solver_2_asp(content)
    return asprilo_plan


if __name__ == "__main__":
    checkargs()
    main(sys.argv[1])
    sys.exit()


