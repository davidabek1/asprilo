# ASPRILO
ASPRILO, an intra-logistics benchmark suite for answer set programming https://asprilo.github.io/
<br>see also github repository https://github.com/potassco/asprilo

This project aims to extend ASPRILO solver (using CLINGO) with MAPF family solvers, 
starting from M family problems (only moving toward shelves in the warehouse),
future work would be to confront A B C family problems by reducing it to MAPF problem,
and solving with MAPF solvers.

## Getting Started

* While ASPRILO states sometimes being able to be installed on Windows platform, 
  we have found it can be installed on Linux only (some commands exists only on Linux platform).
* Read carefully asprilo site and install the generator and vizualizer.
* Install dotnet core, in order to be able to run the MAPF solvers DLLs.
* Branches in current git:
  - master branch is handling Running Demo section
    <br>create asprilo folder under users home directory, and clone this files and folders into it.
    <br>master branch is following original ASPRILO installation while adding support for incremental solve,
    <br>while working with vizualizer, see issue #31 on their git site: https://github.com/potassco/asprilo/issues/31
    <br>using this branch ASPRILO is solving only anonymous problems, while MAPF solvers are given default assignment
    <br>(e.g. first robot to first shelf, second robot to second shelf... )
  - assignments branch is handling Running the tests section
    <br>create asprilo folder under users home directory, and clone this files and folders into it.
    <br>assignments branch has added support of assign rules to the encodings, so ASPRILO will solve non-anonymous problems
## Running the tests

### Generating logistic M problems

* update generate_problems.py file with your home directory
* run generate_problems.py
* problems will be generated into generatedInstances folder
* problems are spanning robots in the warehouse from 5 to 80 steping 5, 
  - it is a medium size grid warehouse of 15X12
  - quantity of robots is equal to number of shelves to number of products to number of orders 
    to number of total units.
    
### Running solvers and documenting results

* open asprilo_solver.py and update your home directory
* run asprilo_solver.py
  - it will run through all generated problems in generatedInstances folder
  - run ASPRILO solver against each problem and document solution and time 
    (keep assignment of robots to shelves)
  - translate the prolbem into MAPF problem by generating agents file and map file
  - run dotnet solvers and document solutions steps and time
  solvers: A*+OD+ID, EPEA*, ICTS+ID, CBS, CBS modern (CBSH), MACBS over A*
  - create solvers_results.csv file with all documented results.
## Running a Demo

The ability of using the vizualizer to examine instances, and examine solvers solutions visually, has tremendous impact.
<br>As this extended capability allowing the researcher easily compare and debug sovlers solutions.

### Demo Movie

open viz_demo.mp4 to see example functionality of the vizualizer working with the different solvers including(in the movie by order of appearence): 
* ASPRILO solving anonymous and MAKESPAN goal
* A*+OD+ID solving non-anonymous (default assignment), goal MAKESPAN and Sum of Costs
* CBS solver exists only for MAKESPAN variant, so the solver solves when asking for MAKESPAN goal, and shows a message of non existent solver, when asking for Sum of Costs variant.

### Vizualizer workflow

The vizualizer is communicating with the attached solver over configured port (5000 by default), 
<br>transmitting an instance problem, and expecting a plan solved by the solver, to show the solution in the vizualizer.
<br>The workflow goes through this steps:
* initiate the solver that will work on the instance problem
* the solver opens a port listener and is waiting for incoming instance
* incoming instance is forwarded to initiated solver
  - with MAPF solvers, we changed the workflow to first convert ASP plan to MAPF format (map and agents files)
  - run a sub process triggering the .NET Dlls with the created files
  - on success, coverting back the solution to ASP format plan
* on solver success, plan is communicated back to the vizualizer for examining.

<br> extended information on the changes is in [SOLVER.md](https://github.com/davidabek1/asprilo/blob/master/SOLVER%20DEEP%20DIVE.md)


## Authors

* **Eli Boyarski**
* **David Abekasis**
* **Nir Zagdanski**

## License

This project has no license

## Acknowledgments

* We thank Dr.Roni Stern for the guidance and interesting lectures of Multi Agents Systems


