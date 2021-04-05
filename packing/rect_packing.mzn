% Use this editor as a MiniZinc scratch book
int: n; % number of squares
set of int: SQUARE = 1..n; 
array[SQUARE] of int: widths;
array[SQUARE] of int: heights; 

%widths = [i | i in SQUARE];
%heights = [i | i in SQUARE]; 

int: maxl = sum(i in SQUARE) (max(widths[i], heights[i]));
int: mina = sum(i in SQUARE) (widths[i]*heights[i]);
int: min_height_square = max(heights);
int: min_width_square = max(widths);

var min_height_square..maxl: height;
var min_width_square..maxl: width; 

var mina .. n*maxl: area ;
constraint area = height*width;

% where is square i placed in terms of x and y?
array[SQUARE] of var 0..maxl: x;
array[SQUARE] of var 0..maxl: y; 

% squares need to fit into the rectangle

constraint forall(s in SQUARE) (x[s] + widths[s] <= width);
constraint forall(s in SQUARE) (y[s] + heights[s] <= height);

% squares should not overlap

constraint forall(s1, s2 in SQUARE where s1 < s2) (
  x[s1] + widths[s1] <= x[s2] \/
  x[s2] + widths[s2] <= x[s1] \/
  y[s1] + heights[s1] <= y[s2] \/ 
  y[s2] + heights[s2] <= y[s1]
);

%constraint x = array1d(1..11, [0, 0, 0, 6, 0, 0, 4, 9, 7, 10, 0]);
%constraint y = array1d(1..11, [9, 4, 0, 5, 3, 6, 0, 0, 0, 0, 8]);

solve 
:: int_search([area, height, width], input_order, indomain_min, complete)
minimize area;