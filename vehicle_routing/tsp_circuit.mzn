% The circuit-based TSP model
% Takes cities and next[c] for every city
int: n_locations;
set of int: Locations = 1..n_locations;

array[Locations, Locations] of int: distances;
array[Locations, Locations] of int: durations;

int: max_length;

% get the maximum length entry of the distance metric 
% to set up a domain
int: max_dist = max(i, j in Locations)(distances[i,j]);

% the main set of decision variables -> for city c, give me its successor
array[Locations] of var Locations: next;

array[Locations] of var 1..max_dist: tour_distances;

constraint forall(l in Locations) (tour_distances[l] = distances[l, next[l]]);

% constrain the tour represented by next to be a circuit
include "circuit.mzn";

constraint circuit(next);
var 0..n_locations*max_dist: tour_length;
constraint tour_length = sum(tour_distances);
constraint tour_length <= max_length;

solve minimize tour_length;