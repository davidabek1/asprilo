# SOLVER DEEP DIVE 

## What have changed for correct installation

when following installation of ASPRILO with:

```
conda install asprilo-visualizer -c potassco -c potassco/label/dev
```

besides python required packages, ASPRILO is adding 3 script files in the python bin folder: viz, viz-solver, viz-simulator
<br>and is putting an egg file in the site-packages folder called: visualizer-0.2.2-py3.7.egg, 
based on current version.

Intervene with ASPRILO solver happens in 2 places:
* changing the script file viz-solver to include reference of newly similar to egg folder called visualizer022py37MAPFext
relevant changed reference is:
```
from visualizer022py37MAPFext.solver import main
```

* changing solver.py to allow running different solvers based on the relevant command in the vizualizer, 
by adding new classes for each solver:
```
# overrides the solve function and on_data

# astar solver
class SolverAstar(Solver):

# cbs solver (withBypass)
class SolverCbs(Solver):

# EPEA solver
class SolverEpea(Solver):

# ICTS solver
class SolverICTS(Solver):

# macbs solver
class SolverMacbs(Solver):

# modern cbs solver
class SolverCbsh(Solver):
```

MAPF solvers are counting on 2 python files:
* [from_asprilo.py](https://github.com/davidabek1/asprilo/blob/master/from_asprilo.py) - to convert ASP rules into map and agents files (maze.map, agents.agents)
* [Convert_agents_actions_2_asp.py](https://github.com/davidabek1/asprilo/blob/master/Convert_agents_actions_2_asp.py) - to convert solved by MAPF solution into ASP rules

## Invoking relevant solver

First running the vizualizer by command viz in the asprilo folder (~/asprilo).

From the vizualizer the way to invoke the solvers is by first intialize solver from the Network menu,
<br>each solver has its invocation command.
<br>The parts of the command are: 
* ./viz-solver - this will invoke the script from current folder and not from the installed script in python bin folder
* --port - this parameter is telling the listener where to expect the instance, (5000 by default)
* -m - this parameter will invoke the relevant solver class (ASPRILO variants are default, incremental, interactive)
* -e - this parameter will provide the relevant encodings for ASPRILO, and either MAKESPAN or SUM of costs goal for the MAPF solvers.

<br>Example invokation for each solver:
* ASPRILO
```./viz-solver --port 5000 -m incremental -e ~/asprilo/encodings/m/encoding.ilp```
* A* with ID with OD, goal MAKESPAN
```./viz-solver --port 5000 -m astar -e MAKESPAN```
  - for goal Sum of Costs
```./viz-solver --port 5000 -m astar -e SUM```
* CBS with Bypass with Cardinal Lookahead, goal MAKESPAN
```./viz-solver --port 5000 -m cbs -e MAKESPAN```
* EPEA* with ID, goal Sum of Costs
```./viz-solver --port 5000 -m epea -e SUM```
* ICTS with ID, goal Sum of Costs
```./viz-solver --port 5000 -m icts -e SUM```
* maCBS over A* with OD 20 with Bypass with Cardinal Lookahead, goal MAKESPAN
<br>```./viz-solver --port 5000 -m macbs -e MAKESPAN```
* modern CBS (Hueristic CBS)
```./viz-solver --port 5000 -m cbsh -e SUM```
