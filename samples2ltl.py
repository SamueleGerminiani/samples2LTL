import pdb
from z3 import *
import argparse
from smtEncoding.dagSATEncoding import DagSATEncoding
import os
from solverRuns import run_solver, run_dt_solver
from utils.Traces import Trace, ExperimentTraces
from multiprocessing import Process, Queue
import logging

def helper(m, d, vars):
    tt = { k : m[vars[k]] for k in vars if k[0] == d }
    return tt



 
def main():
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--traces", dest="tracesFileName", default="traces/dummy.trace")
    parser.add_argument("--max_depth", dest="maxDepth", default='8')
    parser.add_argument("--start_depth", dest="startDepth", default='1')
    parser.add_argument("--max_num_formulas", dest="numFormulas", default='1')
    parser.add_argument("--max_trace_length", dest="max_samples", default='10000')
    parser.add_argument("--iteration_step", dest="iterationStep", default='1')
    parser.add_argument("--test_dt_method", dest="testDtMethod", default=False, action='store_true')
    parser.add_argument("--test_sat_method", dest="testSatMethod", default=False, action='store_true')
    parser.add_argument("--timeout", dest="timeout", default=600, help="timeout in seconds")
    parser.add_argument("--log", dest="loglevel", default="INFO")
    parser.add_argument("--dump_to", dest="dumpTo", default="out.txt")
    parser.add_argument("--force_always_implication", dest="forceAlwaysImplication", default=False)
    parser.add_argument("--force_always", dest="forceAlways", default=False)
    args,unknown = parser.parse_known_args()
    tracesFileName = args.tracesFileName
    
    
    """
    traces is 
     - list of different recorded values (traces)
     - each trace is a list of recordings at time units (time points)
     - each time point is a list of variable values (x1,..., xk) 
    """
    
    numeric_level = args.loglevel.upper()
    logging.basicConfig(level=numeric_level)

    
    maxDepth = int(args.maxDepth)
    numFormulas = int(args.numFormulas)
    startDepth = int(args.startDepth)
    traces = ExperimentTraces()
    iterationStep = int(args.iterationStep)
    finalDepth = int(args.maxDepth)
    traces.readTracesFromFile(tracesFileName, int(args.max_samples))
    timeout = int(args.timeout)
    dumpTo = args.dumpTo
    forceAlwaysImplication = args.forceAlwaysImplication
    forceAlways = args.forceAlways
    templateMode=0

    if forceAlwaysImplication:
        templateMode=2
    elif forceAlways:
        templateMode=1
        

    #debug
    #print(traces)

    if args.testSatMethod == True:
        [formulas, timePassed] = run_solver(finalDepth=maxDepth, traces=traces, maxNumOfFormulas = numFormulas, startValue=startDepth, step=iterationStep, templateMode=templateMode, timeout=timeout)
        logging.info("formulas: "+str([f.prettyPrint(f) for f in formulas])+", timePassed: "+str(timePassed))
        with open(dumpTo, "w") as f:
            #dump one formula per line
            for formula in formulas:
                pp=formula.prettyPrint()
                if pp != "true":
                   f.write(pp+"\n")
        
    
   # if args.testDtMethod == True:
   #     
   #     [timePassed, numAtoms, numPrimitives] = run_dt_solver(traces=traces)
   #     logging.info("timePassed: {0}, numAtoms: {1}, numPrimitives: {2}".format(str(timePassed), str(numAtoms), str(numPrimitives)))
        
    

            

if __name__ == "__main__":
    main()

