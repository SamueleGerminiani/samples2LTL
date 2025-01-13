from smtEncoding.dagSATEncoding import DagSATEncoding
from z3 import *
import sys
import pdb
import traceback
import logging
from utils.SimpleTree import Formula
import time

def get_models(finalDepth, traces, startValue, step, encoder, maxNumModels=1, templateMode=0, timeout=600):
    results = []
    i = startValue
    fg = encoder(i, traces)
    fg.encodeFormula(True, templateMode) 
    start = time.time()
    while i <= finalDepth:
        #print depth
        if time.time() - start > timeout:
            logging.error("Timeout reached, stopping...")
            break

        if len(results) >= maxNumModels:
            logging.info("Reached max number of formulas, stopping...")
            break

        logging.info("depth {}".format(i))
        solverRes = fg.solver.check()
        if not solverRes == sat:
            logging.debug("not sat for i = {}".format(i))
            i += step
            fg = encoder(i, traces)
            fg.encodeFormula(True, templateMode)
        else:
            solverModel = fg.solver.model()
            formula = fg.reconstructWholeFormula(solverModel)
            logging.info("found formula {}".format(formula.prettyPrint()))
            #print("found formula {}".format(formula))
            try:
                formula = Formula.normalize(formula)
            except Exception as e:
                logging.error("error normalizing formula, continue...")
                logging.error(e)
                logging.error(traceback.format_exc())
                continue
            logging.info("normalized formula {}".format(formula))
            if formula not in results:
                results.append(formula)

            #prevent current result from being found again
            block = []
            # pdb.set_trace()
            # print(m)
            infVariables = fg.getInformativeVariables()

            logging.debug("informative variables of the model:")
            for v in infVariables:
                logging.debug((v, solverModel[v]))
            logging.debug("===========================")
            for d in solverModel:
                # d is a declaration
                if d.arity() > 0:
                    raise Z3Exception("uninterpreted functions are not supported")
                # create a constant from declaration
                c = d()
                if is_array(c) or c.sort().kind() == Z3_UNINTERPRETED_SORT:
                    raise Z3Exception("arrays and uninterpreted sorts are not supported")
                block.append(c != solverModel[d])
            fg.solver.add(Or(block))

    return results


        
    
