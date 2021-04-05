% Use this editor as a MiniZinc scratch book
int: n; % number of squares
set of int: SQUARE = 1..n; 

int: maxl = sum(i in SQUARE) (i);
int: mina = sum(i in SQUARE) (i*i);
var n..maxl: height;
var n..maxl: width; 

var mina .. n*maxl: area ;
constraint area = height*width;

% where is square i placed in terms of x and y?
array[SQUARE] of var 0..maxl: x;
array[SQUARE] of var 0..maxl: y; 

% squares need to fit into the rectangle

constraint forall(s in SQUARE) (x[s] + s <= width);
constraint forall(s in SQUARE) (y[s] + s <= height);

% squares should not overlap

constraint forall(s1, s2 in SQUARE where s1 < s2) (
  x[s1] + s1 <= x[s2] \/
  x[s2] + s2 <= x[s1] \/
  y[s1] + s1 <= y[s2] \/ 
  y[s2] + s2 <= y[s1]
);

solve 
:: int_search([area, height, width], input_order, indomain_min, complete)
minimize area;