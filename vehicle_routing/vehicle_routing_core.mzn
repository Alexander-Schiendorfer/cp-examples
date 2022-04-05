% Use this editor as a MiniZinc scratch book
include "globals.mzn";

int: n_locations;

set of int: Locations = 1 .. n_locations;
Locations: head_quarters;

array[Locations,Locations] of int: distances;
array[Locations,Locations] of int: durations;

% Realistically, we have more than one route -> also costs
% array[Locations, Locations, Time, RouteId, Density] of int: distances;
% array[Locations, Locations, Time, RouteId, Density] of int: co2costs;

array[Locations] of int: durationOfVisit;
array[Locations] of int: siteOpens;
array[Locations] of int: siteCloses;

int: n_vehicles;
set of int: Vehicles = 1..n_vehicles;

array[Vehicles, Locations] of var Locations: next;

include "subcircuit.mzn";

constraint forall(v in Vehicles) (subcircuit([next[v, s] | s in Locations]));
%constraint arrivalTime[2] > 15;
% each site should only belong to one vehicle
array[Vehicles] of var set of Locations: covered_by;
constraint forall(v in Vehicles, s in Locations) ( s in covered_by[v] <-> (next[v, s] != s \/ s = head_quarters) );

%constraint covered_by[1] = {1};
%constraint covered_by[2] = {1,2,3,4,5};

array[Locations] of var Vehicles: location_belongs_to_vehicle;

% constraint int_set_channel(location_belongs_to_vehicle, covered_by);
% needed a modified variant to account for HQ
constraint forall(l in Locations, v in Vehicles) (l in covered_by[v] <-> (location_belongs_to_vehicle[l] = v \/ l = head_quarters) );
                        
% the sites that belong to a subcircuit
% time business 

array[Locations] of var 0..infinity: arrivalTime;
constraint arrivalTime[head_quarters] = 0;

constraint forall(v in Vehicles) ( arrivalTime[next[v,head_quarters]] = durations[head_quarters, next[v, head_quarters]]);
constraint forall (v in Vehicles, i in covered_by[v] where i != head_quarters /\ next[v, i] != head_quarters) (
 arrivalTime[next[v, i]] = arrivalTime[i] + durations[i,next[v,i]]
);

array[Vehicles] of var 0..infinity: latest_arrival;
constraint forall(v in Vehicles) (latest_arrival[v] = max(l in covered_by[v])(arrivalTime[l]));
%constraint forall (i in covered_by[2] where i != head_quarters /\ next[2, i] != head_quarters) (
% arrivalTime[next[2, i]] = arrivalTime[i] + durations[i,next[2,i]]
%);

var 0..infinity: tour_end;
constraint tour_end = max(v in Vehicles)(latest_arrival[v]);

solve 
%:: int_search(arrivalTime, input_order, indomain_max)
%:: int_search(next, input_order, indomain_min)
 minimize tour_end;