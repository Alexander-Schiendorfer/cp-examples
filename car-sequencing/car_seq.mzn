% Car sequencing for discrete optimization

int: nCarConfigs; int: nOptions;

set of int: Slots = 1..nSlots;
set of int: Options = 1..nOptions;
set of int: CarConfigs = 1..nCarConfigs;

array[CarConfigs] of int: demand;
int: nCars = sum(c in CarConfigs) (demand[c]) ;
array[CarConfigs,Options] of 0..1: requires;

 % how many of each car type are required
int: nSlots = nCars; % that is quite optimistic, we could need breaks ... but let's keep it simple

% for each option,
% within per_slots slots, only at_most may require that option
array[Options] of int: at_most;
array[Options] of int: per_slots;


% ----------------------- 
% now for the actual decisions

% map every slot to a CarType
array[Slots] of var CarConfigs: line;
array[Slots,Options] of var bool: setup;

% setup[o,s] = true means that option o is needed in slot s

% now for the actual constraints to make sure everything works out nicely

% we produce what is ordered
constraint forall(c in CarConfigs) (
  count(line, c) = demand[c]
);

% tie the setup variables to the requires matrix 
constraint forall (s in Slots, o in Options) (
  setup[s,o] = requires[line[s],o]
);

% now for the actual sequence constraints 
constraint forall (o in Options, 
                   s in 1..nSlots - per_slots[o] + 1) 
      ( sum(s_ in s .. (s + per_slots[o]-1) ) (setup[s_,o]) 
        <= at_most[o]);
      
% solve satisfy;
