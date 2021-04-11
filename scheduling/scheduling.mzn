% Use this editor as a MiniZinc scratch book
int: lastT;
set of int: TIME = 0..lastT;

enum JOBS;
int: nTasks;
set of int: TASKS = 1..nTasks;

array[JOBS,TASKS] of int: dur;

% actual decision variables
array[JOBS,TASKS] of var TIME: start;
array[JOBS,TASKS] of var TIME: end;
constraint forall(j in JOBS, t in TASKS)(
  end[j,t] = start[j,t] + dur[j,t]
);

% machines 
int: nMachines;
set of int: MACHINES = 1..nMachines;
array[JOBS,TASKS] of MACHINES: taskToMach;

constraint 
  forall(j1, j2 in JOBS, t1, t2 in TASKS where 
                  j1 != j2
               /\ taskToMach[j1, t1] = taskToMach[j2, t2]) (
                  end[j1, t1] <= start[j2, t2] \/
                  end[j2, t2] <= start[j1, t1]
                 ); 

% precedences 
constraint forall(j in JOBS, t in 1..max(TASKS)-1) (
  end[j,t] <= start[j,t+1]
);

% objective 
var TIME: makespan; 
constraint makespan = max(j in JOBS, t in TASKS)(end[j,t]);
