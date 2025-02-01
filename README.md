# Variable Neighborhood Search for Red-Blue Separating Set on Graphs

The content of this repository contains code for variable neighborhood search, brute-force and greedy algorithms for minimal red-blue separating set on Graphs.

## Content
+ graphs - random generated red-blue colored graph instances;
+ greedy - results of running greedy algorithm;
+ bruteforce - results of running brute-force algorithm
+ vns - results of running vns algorithm
+ k_sens - results of running vns algorithm with different values  of k
+ src - source code

## Requirements
+ Python3
+ Networkx

## Usage 
To create instances or run a certain algorithm on __num_instances__ graphs with __n__ number of nodes and __p__ probability of edge creation use the following command.

```
python3 rbss.py -a action -ip input_path -op output_path -i num_instance -n num_nodes -p edge_prob
```
where
| parameter  | value |
|----------- |-------|
| -a     | generate, bruteforce, vns, greedy |
| -ip | absolute or relative path to the input directory. In case of generate this parameter can be excluded. |
| -op | absolute or relative path to the output directory. In case of generate this parameter can be excluded. |
| -i | number of instances to generate or test. |
| -n | number of nodes to create or search to test. |
| -p | probability of edge creation or search to test.|

To test all alredy generated instances with default number of nodes and probabilities use:
```
python3 vns_call.py
```
or
```
python3 greedy_call.py
```