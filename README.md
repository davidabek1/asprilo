# ASPRILO
ASPRILO, an intra-logistics benchmark suite for answer set programming https://asprilo.github.io/
see also github repository https://github.com/potassco/asprilo

This project aims to extend ASPRILO solver (using CLINGO) with MAPF family solvers, 
starting from M family problems (only moving toward shelves in the warehouse),
future work would be to confront A B C family problems by reducing it to MAPF problem,
and solving with MAPF solvers.

## Getting Started

* While ASPRILO states sometimes being able to be installed on Windows platform, 
  we have found it can be installed on Linux only (some commands exists only on Linux platform).
* Read carefully asprilo site and install the generator and vizualizer.
* Install dotnet core, in order to be able to run the MAPF solvers DLLs.
* create asprilo folder under users home directory, and clone this files and folders into it.
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
  solvers: A*+OD+ID, EPEA*, ICTS+ID, CBS
  - create solvers_results.csv file with all documented results.
## Running a Demo

