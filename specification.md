# Polish Notation Calculator
## Only binary operands
	+ 1 1 -> 2
	(+ 1 -1) -> 0
    / -2 (+ 1 1) -> -1
    - (+ 1 1) (* 1 1) -> 1
## Multiple operands
	+ 1 1 1 1 -> 4
	(- 1 1 1 1) -> -2
    * 1 (- 2 1 1) 0 (/ 4 2) -> 0
## Redundant Brackets
	1 -> 1
    (1) -> 1
    (((1))) -> 1
    ((+ (+ 1 ((1))) ((1)))) -> 1
## Variable in global environment
	predefined env: {
        x: 1,
        y: 0,
        z: -1
    }
    
    x -> 1
    (y) -> 0
    (z) -> -1
    + x 1 -> 2
    + x y -> 1
    + x y z -> 0
## Variable and reassignment in global environment
	predefined env: {
        x: 1,
        y: 0,
        z: -1
    }
    
    + x 1 -> 2
    + x y -> 1
    + x y z -> 0
    = x 10 + x x z -> 21
    = x 10 = y 10 = z 10 + x y z -> 30
## Variable and reassignment in scoped environment, aka shadow variable feature
	predefined env: {
        x: 1,
        y: 0,
        z: -1
    }
    
    +   x (= y 1000 (= y 10 + x y)) z y -> 11
    ### 1                     1 10 -1 0 -> 11
## Handle unresolved variable
	predefined env: {
        x: 1,
        y: 0,
        z: -1
    }
    
    + x y z -> 0
    + (+ x 1) (+ a 1) -> + a 3 | + 3 a