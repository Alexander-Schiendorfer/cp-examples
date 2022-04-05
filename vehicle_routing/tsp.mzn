% The alldifferent (permutation-based) model of TSP
int: n_locations;
set of int: Locations = 1..n_locations;
array[Locations] of string: loc_names :: add_to_output;

array[Locations, Locations] of int: distances;
array[Locations, Locations] of int: durations;
int: max_length;

% get the maximum length entry of the distance metric 
% to set up a domain
int: max_dist = max(i, j in Locations)(distances[i,j]);

% the main set of decision variables -> a permutation of the locations
% tour[1] = t means that the first stop of our tour is t
array[Locations] of var Locations: tour :: add_to_output;

array[Locations] of var 1..max_dist: tour_distances :: add_to_output;

% since we gotta visit all the places -> easiest to use alldifferent
include "alldifferent.mzn";
constraint alldifferent(tour);

% tie tour_distances to tour 
constraint forall(i in 1..n_locations)(
  tour_distances[i] = distances[tour[i], tour[i mod n_locations + 1]]
);

var 0..n_locations*max_dist: tour_length :: add_to_output;
constraint tour_length = sum(tour_distances);
constraint tour_length <= max_length;

solve minimize tour_length;