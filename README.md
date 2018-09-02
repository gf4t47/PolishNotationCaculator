# Polish Notation Calculator
## Description
You will implement a polish notation calculator, signature as:
```python
def calculate(expression: str, env: Dict[str, int]) -> int
eg:
    assert 1 == calculate("/ (* (+ 1 1 1) (- 4 2)) 4", {})
```
NOTICE that "/" stands for integer division

## Features
You calculator should support the below features as much as possible, the feature list is in difficulty increased order.
1. single numbers `1 -> 1`, only support single factor, operator must operate on at least tow operands
2. binary operands `+ 1 1 -> 2`
3. multiple operands `+ 1 1 1 1 -> 4`
4. redundant brackets `((+ (((1))) 1)) -> 2`, `(((2))) -> 2`
5. predefined global variables:
    ``` python
    def calculate(expression: str, env: Dict[str, int]) -> int
    eg:
        env = { "x": 1, "y": 0 }

        assert 0 == calculate("y", env)
        assert 1 == calculate("+ x y", env)
    ```
6. variable syntax is multiple characters in alphabet, case sensitive:
    ```
    env: { "IamAlongVariable": 1, "iamalongvariable": -1 }
    + IamAlongVariable 1 -> 2
    ```
7. variable reassignment, "= var val" could be used to as reassignment statement, it's always a binary expression and always before real calculate expression:
    ```
    env: { "x": 1, "y": 1 }
    = x -1 + x y -> 0
    ### reassign x to -1 first, then [x: -1] + [y: 1] -> 0
    ```
8. multiple reassignments in one or multiple expression:
    ```
    env: { "x": 1, "y": 1 }
    = x 0 + x y -> 1
    = x 0 = y 0 + x y -> 0
    + (= x -1 x) (= y -1 y) -> -2
    ```
9. right part of the reassignment could be another variable:
    ```
    env: { "x": 1, "y": 0 }
    = x y + x y -> 0
    ```
10. right part of the reassignment could be a expression:
    ```
    env: { "x": 1, "y": 0 }
    = x (* 2 2) + x y -> 4
    = x (* 2 y) + x y -> 0
    ```
11. scoped enviroment(aka variable shadowing), internal reassignment could overwrite the outside one, but the variable will recover once it's out of the internal scope
    ```
	env: { x: 1, y: 0, z: -1 }
      + x (= y 1000 (= y 10 + x y)) z y -> 11
    ### 1                     1 10 -1 0 -> 11
    ### see each varible value as above, notice that inside the first brackets, y is assigned to 1000 but it's never be calculated.
    ```
12. variable can assigned to itself now, since the calculator support scoped enviroment:
    ```
    env: { x: 1, y: 0, z: -1 }
    + x ( = x (+ x 1) x ) -> 3
    ```
13. handle unresolved variable, return a simplified version of expression(string) if there are variables can't be resolved:
    ```
    env: { x: 1, y: 0, z: -1 }
    + (+ x 1) (+ a 1) -> + a 3 | + 3 a
    ```
We are not leetcode, you don't have to implement all those features to get scored, try your best :)