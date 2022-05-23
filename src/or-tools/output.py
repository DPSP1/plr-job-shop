
from ortools.sat.python.cp_model import CpSolverSolutionCallback, OPTIMAL, FEASIBLE

from constants import TASK_MACHINE, TASK_DURATION, TASK, START_VAR, PRESENCES_VAR

class IntermediateSolutionPrinter(CpSolverSolutionCallback):
    """Print intermediate solutions"""
    def __init__(self):
        CpSolverSolutionCallback.__init__(self)
        self.__solution_count = 0

    def on_solution_callback(self):
        """Called at each new solution"""
        print(f'Solution {self.__solution_count}, time = {self.WallTime()} s, objective = {self.ObjectiveValue()}')
        self.__solution_count += 1

def print_statistics(solver, status):
    # Solver Statistics
    print('--------------------------------')
    print('           Statistics           ')
    print('--------------------------------')
    print(f'  - conflicts: {solver.NumConflicts()}')
    print(f'  - branches : {solver.NumBranches()}')
    print(f'  - wall time: {solver.WallTime():8f} s')
    print('--------------------------------')
    print(f'  Solve status: {solver.StatusName(status)}')
    print(f'  Optimal objective value: {solver.ObjectiveValue()}')
    print('--------------------------------')
    
def print_results(solver, status, jobs, makespan):
    # Print the results
    if status == OPTIMAL or status == FEASIBLE:
        print('Found a Solution')
        # Print Solution
        print_optimal_solution(solver, jobs, makespan)
    else:
        print('No Solution Found')

def print_optimal_solution(solver, jobs, makespan):    
    # Print Final Solution
    for job, info in jobs.items():
        task      = info[         TASK]
        start     = info[    START_VAR]
        presences = info[PRESENCES_VAR]

        (machine, duration) = (-1, -1)
        for (alt_task, presence) in zip(task, presences):
            if solver.Value(presence):
                duration = alt_task[TASK_DURATION]
                machine  = alt_task[TASK_MACHINE ]
                break
        print(f'Job {job}: starts at {solver.Value(start)} (machine {machine}, duration {duration})')
    
    print(f'Objective Function: {solver.Value(makespan)}')
