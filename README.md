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
    <br>master branch is following original asprilo installation while adding support for incremental solve,
    <br>while working with vizualizer, see issue #31 on their git site.
    <br>using this branch asprilo is solving only anonymous problems, while MAPF solvers are given default assignment
    <br>(e.g. first robot to first shelf, second robot to second shelf... )
  - assignments branch is handling Running the tests section
    <br>create asprilo folder under users home directory, and clone this files and folders into it.
    <br>assignments branch has added support of assign rules to the encodings, so asprilo will solve non-anonymous problems
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
  - run asprilo solver against each problem and document solution and time 
    (keep assignment of robots to shelves)
  - translate the prolbem into MAPF problem by generating agents file and map file
  - run dotnet solvers and document solutions steps and time
  solvers: A*+OD+ID, EPEA*, ICTS+ID, CBS, CBS modern (CBSH), MACBS over A*
  - create solvers_results.csv file with all documented results.
## Running a Demo


