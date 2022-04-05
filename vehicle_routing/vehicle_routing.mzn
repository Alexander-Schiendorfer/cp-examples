 % A student-project matching
include "../simple_diversity_mixin.mzn";
include "vehicle_routing_core.mzn";

%----------------------------------------------------------------------------
% connecting the model hook from the diversity mixin to this model
diversity_variables_of_interest = startOfVisit; % all other variables depend on this assignment   