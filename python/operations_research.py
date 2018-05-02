from ortools.constraint_solver import pywrapcp
import FlexibleJobShopData as fjsd


class TaskAlternative():
    def __init__(self, j):
        solver = pywrapcp.Solver("flexible_jobshop")
        self.job_id = j
        self.alternative_variable = solver.IntVar()
        self.intervals = solver.IntervalVar()


def FlexibleJobshop(data):
    solver = pywrapcp.Solver("flexible_jobshop")
    machine_count = data.machine_count
    job_count = data.job_count
    horizon = data.horizon
    all_jobs = range(0, job_count)
    all_machines = range(0, machine_count)

    print(data.debug_string())
    # ----- Creates all Intervals and vars -----
    jobs_to_tasks = []
    machines_to_tasks = []

    # Creates all individual interval variables (jobs)
    for job_id in all_jobs:
        tasks = data.tasks_of_job(job_id)
        all_tasks = range(0, len(tasks))

        for task_id in all_tasks:
            task = tasks[task_id]
            all_machines = range(0, len(task.machines))
            # TODO: CHECK_EQ(job_id, task.job_id);
            jobs_to_tasks[job_id].append(job_id)
            optional = True if len(task.machines) > 1 else False
            active_variables = []

            # For every possible machine that can be assigned to this task
            for alt in all_machines:
                machine_id = task.machines[alt]
                duration = task.duration[alt]
                name = '{}{}{}{}{}'.format(
                    task.job_id,
                    task_id,
                    alt,
                    machine_id,
                    duration
                )
                interval = solver.FixedDurationIntervalVar(
                    0,
                    horizon,
                    duration,
                    optional,
                    name
                )
                jobs_to_tasks[job_id][-1].intervals.append(interval)
                machines_to_tasks[machine_id].append(interval)
                if optional:
                    # TODO: active_variables.push_back(interval->PerformedExpr()->Var());
            alternative_name = '{}{}'.format(job_id, task_id)
            alt_var = solver.IntVar(0, len(task.machines-1, alternative_name)
            job_to_tasks[job_id].alternative_variable=alt_var
            if optional:
                # solver.AddConstraint(solver.MakeMapDomain(alt_var, active_variables));

    # Creates precedences inside, add conjunctive contraints.
    for i, j in zip(all_jobs, range(0, len(jobs_to_tasks[i]) - 1)):
        task_alt1=jobs_to_tasks[i][j]
        task_alt2=jobs_to_tasks[i][j+1]
        for alt1, alt2 in zip(len(task_alt1.intervals), len(task_alt2.intervals)):
            t1=task_alt1.intervals[alt1]
            t2=task_alt2.intervals[alt2]
            solver.Add(t2.StartsAfterEnd(t1))

    # Collect alternative variables.
    all_alternative_variables=[]
    for i, j in zip(all_jobs, range(0, len(jobs_to_tasks[i]) - 1)):
        all_alternative_variables=jobs_to_tasks[i][j].alternative_variable
        # TODO : if (!alternative_variable->Bound())
        # all_alternative_variables.append(alternative_variable)

    # Adds disjunctive constraints on unary resources, and creates
    # sequence variables. A sequence variable is a dedicated variable
    # whose job is to sequence interval variables.

    all_sequences=[]  # SequenceVar vector
    for machine_id in range(0, machine_count):
        name='Machine {}'.format(machine_id)
        disj_ct=solver.DisjunctiveConstraint(
            machines_to_tasks[machine_id], name)
        all_sequences.append(disj_ct.SequenceVar())
        solver.Add(disj_ct)

    # Creates array of end_times of jobs.
    all_ends=[]
    for i in range(0, len(job_count)):
        task_alt=jobs_to_tasks[job_id][-1]
        for j in range(0, len(task_alt)):
            t=task_alt.intervals[j]
            all_ends.append(t)

    # Objective: minimize the makespan (maximum end times of all tasks) of the problem.
    obj_var=solver.Max(all_ends)
    obj_mon=solver.Minimize(obj_var, 1)

    # ----- Search monitors and decision builder -----
    alternative_phase=solver.Phase(
        all_alternative_variables, solver.CHOOSE_MIN_SIZE, solver.ASSIGN_MIN_VALUE)
    sequence_phase=solver.Phase(all_sequences, solver.SEQUENCE_DEFAULT)
    obj_phase=solver.Phase(
        obj_var, solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE)

    # The main decision builder (ranks all tasks, then fixes the objective_variable).
    main_phase=solver.Compose(alternative_phase, sequence_phase, obj_phase)

    # Create the solution collector.
    collector=solver.LastSolutionCollector()
    collector.AddObjective(obj_var)
    collector.Add(all_alternative_variables)
    collector.Add(all_sequences)

    # Search log
    kLogFrequency=1000000
    search_log=solver.SearchLog(kLogFrequency, obj_mon)
    # TODO: limit

    # Search.
    if (solver.Solve(main_phase, search_log, obj_mon, limit, collector))
        for m in all_machines:
            seq=all_sequences[m]
            print('{}: '.format(seq.name))
