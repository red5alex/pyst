__author__ = 'are'

import subprocess
import os
import shutil

def genlinpred(
        pstfile,
        workdir=None,
        paruncsource="bounds",
        paruncfile=None,
        weightfactor=1.,
        prediction_par=None,
        prediction_obs=None,
        jcofile=None,
        outfilename="genlinpred.out"):

    if workdir is not None:
        os.chdir(workdir)

    responsefilename = "genlinpred.in"
    responsefile = open(responsefilename, "w")

    responsefile.write("\n")    # Enter name of responsefile (None)
    responsefile.write("f\n")   # abbreviated or full input? (full)

    if not os.path.isfile(pstfile):
        raise FileNotFoundError("file " + pstfile + " does not exist")
    responsefile.write(pstfile + "\n")  # PEST control file

    if paruncsource == "bounds":
        responsefile.write("b\n")  # bounds or uncertainty file for parameter uncertainties? (bounds)
    else:
        if paruncfile is None:
            raise Exception("uncertainty file nominated, but no UNC file path given")
        responsefile.write("u\n")  # bounds or uncertainty file for parameter uncertainties? (bounds)
        raise Exception("uncertainty file not implemeted yet!")
        #TODO: implement uncertainty file

    responsefile.write("n\n")  # are weights the inverse of measurement uncertainty? (no)
    responsefile.write(str(weightfactor) + "\n")  # factor to make weights inverse of measurement noise
    responsefile.write(outfilename + "\n")  # GENLINPRED output file
    responsefile.write("y\n")  # perform global parameter estimability analysis?
    responsefile.write("y\n")  # compute parameter identifiabilities?
    responsefile.write("y\n")  # compute relative parameter error reduction?
    responsefile.write("y\n")  # use SUPCALC to estimate solution space dimensionality?
    responsefile.write("y\n")  # compute relative parameter uncertainty reduction?
    responsefile.write("y\n")  # perform comprehensive analysis of prediction or parameter?

    #  Analyse error/uncertainty of an entity:
    runPredictiveAnalysis = False
    if prediction_obs is not None:
        if jcofile is None:
            raise Exception("observation type prediction requested, but no JCO file path given")
        else:
            responsefile.write(prediction_obs + "\n")  # name of prediction or parameter to analyze
            responsefile.write(jcofile+"\n") # file to read predictive sensitivies or "p" for parameter
            runPredictiveAnalysis = True
    elif prediction_par is not None:
        responsefile.write(prediction_par + "\n")   # name of prediction or parameter to analyze
        responsefile.write("p\n")  # file to read predictive sensitivies or "p" for parameter
        runPredictiveAnalysis = True

    if runPredictiveAnalysis:
        responsefile.write("y\n")  # compute solution/null space contributions to predictive error?
        responsefile.write("y\n")  # compute predictive uncertainty?
        responsefile.write("y\n")  # compute parameter contributions to parameter or predictive error?
        responsefile.write("y\n")  # compute parameter contributions to uncertainty?
        responsefile.write("i\n")  # for individual parameters or parameter groups?
        responsefile.write("y\n")  # compute observation worth with respect to error?
        responsefile.write("y\n")  # compute observation worth with respect to uncertainty?
        responsefile.write("i\n")  # for individual observations or for observation groups?
        responsefile.write("n\n")  # over-ride SUPCALC calculation of solution space dimensions?

    responsefile.close()

    # call GENLINPRED using responsefile as input
    responsefile = open(responsefilename)
    subprocess.call(["genlinpred.exe"], stdin=responsefile)
    responsefile.close()
