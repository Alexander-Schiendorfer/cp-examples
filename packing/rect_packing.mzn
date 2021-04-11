% Use this editor as a MiniZinc scratch book
int: n; % number of shapes
set of int: SHAPES = 1..n; 
array[SHAPES] of int: widths;
array[SHAPES] of int: heights; 

int: max_width_square = sum(i in SHAPES) (widths[i]);
int: max_height_square = sum(i in SHAPES) (heights[i]);

int: min_height_square = max(heights);
int: min_width_square = max(widths);
int: minArea = sum(i in SHAPES) (widths[i]*heights[i]);
int: maxArea = max_width_square*max_height_square;

var min_height_square..max_height_square: sq_height;
var min_width_square..max_width_square: sq_width; 

var minArea .. maxArea: area ;
constraint area = sq_height * sq_width;

% where is square i placed in terms of x and y?
array[SHAPES] of var 0..max_width_square: x;
array[SHAPES] of var 0..max_height_square: y; 

% squares need to fit into the rectangle

constraint forall(s in SHAPES) (x[s] + widths[s] <= sq_width);
constraint forall(s in SHAPES) (y[s] + heights[s] <= sq_height);

% squares should not overlap

constraint forall(s1, s2 in SHAPES where s1 != s2) (
  x[s1] + widths[s1] <= x[s2] \/
  x[s2] + widths[s2] <= x[s1] \/
  y[s1] + heights[s1] <= y[s2] \/ 
  y[s2] + heights[s2] <= y[s1]
);

solve 
:: int_search([area, sq_height, sq_width], input_order, indomain_min, complete)
minimize area;