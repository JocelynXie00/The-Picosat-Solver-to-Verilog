# Picosat Solver from verilog

## testbench example
```
iverilog -o sl2out sl2test.v
./sl2out
```
For other testbench in this problem, they are named as xxxtest.v, where xxx is the module name.

## Solver 
The solver would use the picosat, executable file
```
python solver.py xxx.v [#steps] [#targetstate]
```

## script 
```
python script.py
```
All script task is done here. Change the functionality by cancelling comments.

