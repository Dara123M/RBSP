#!/usr/bin/python3
import os
import sys
PARAMS = {
    "NUM_INSTANCES" : "10", #10
    "NUM_NODES" : "", #10
    "PROB_EDGE" : "", #0.01
    "TO_EXECUTE" : "generate",
    "OUTPUT_DIR_PATH" : "",
    "INPUT_DIR_PATH" : "graphs/"
}

def error(msg):
    print(msg)
    exit(1)



def extractParameters(args):
    parameters = {}
    prev_key = ""
    for a in args:
        if a[0] == "-" and not a.isnumeric():
            prev_key = a
        elif prev_key != "":
            parameters[prev_key] = a
        
    return parameters

    
def validateParameters(parameters):
   for k, v in parameters.items():
        if not k in ("-a", "-ip", "-op", "-i", "-n", "-p"):
            error("""
            Invalid parameters:
            -a => action
            -ip => input path
            -op => output path
            -i => number of instances
            -n => number of nodes
            -p => edge probability
            """)

def evaluateParametersToExec(parameters):

    if "-a" in parameters.keys():
        PARAMS["TO_EXECUTE"] = parameters['-a']
    else: 
        PARAMS["TO_EXECUTE"] = "generate"
    
    if "-ip" in parameters.keys():
        PARAMS["INPUT_DIR_PATH"] = parameters['-ip']
    else:
        PARAMS["INPUT_DIR_PATH"] = "graphs/"
    
    
    if "-op" in parameters.keys() and (PARAMS["TO_EXECUTE"] == 'vns' or PARAMS["TO_EXECUTE"] == 'bruteforce'):
        PARAMS["OUTPUT_DIR_PATH"] = parameters['-op']
    else:
        PARAMS["OUTPUT_DIR_PATH"] = ""
    
    if "-i" in parameters.keys():
        PARAMS["NUM_INSTANCES"] = parameters["-i"]
    else:
        NUM_INSTANCES = "10"
    
    if "-n" in parameters.keys():
        PARAMS["NUM_NODES"] = parameters['-n']
    else:
        PARAMS["NUM_NODES"] = ""
    
    if "-p" in parameters.keys():
        PARAMS["PROB_EDGE"] = parameters['-p']
    else:
        PARAMS["PROB_EDGE"] = ""
    
        
#python3 exec call generate
#python3 exec -a generate -ip input_path -i instance -n nodes -p prob
#python3 exec -a bruteforce -ip input_path -op output_path_path -n nodes -p prob
#python3 exec -a vns -ip input_path -op output_path -n nodes -p prob
def main():    
    #print(sys.argv)
    if len(sys.argv) > 1 and sys.argv[1] != "-a":
        error("First parameter must be -a followed by an action [generate, vns, bruteforce]")
    
    parameters = {}    
    if len(sys.argv) > 2 and not sys.argv[2] in ("bruteforce", "generate", "vns"):
        error("Second parameter mus be an action [generate, vns,  bruteforce]")
    
    parameters = extractParameters(sys.argv[1:])

    validateParameters(parameters)
    
    evaluateParametersToExec(parameters)
    
    exec_str = f"python3 {PARAMS["TO_EXECUTE"]:s}.py {PARAMS["INPUT_DIR_PATH"]:s} {PARAMS["OUTPUT_DIR_PATH"]:s} {PARAMS["NUM_INSTANCES"]:s} {PARAMS["NUM_NODES"]:s} {PARAMS["PROB_EDGE"]:s}"
 
    status = os.system(exec_str)
    if status == 0:
        print("Finished succesfully")
    else:
        print("Exited with error")
    
    exit(status)   

    
    
if __name__=='__main__':
    main()

    
