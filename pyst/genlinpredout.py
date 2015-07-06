__author__ = 'are'

class SupcalcResult:
    def __init__(self):
        self.SolnSpaceSize = None
        self.NullSpaceSize = None

class ParameterAnalysis:
    def __init__(self):
        self.supcalc = SupcalcResult()
        self.parameters = []
        self.identifiability = {}
        self.relErrVarReduction = {}
        self.relUncertVarReduction = {}

    def parseFromString(self, text):
        for l in text.split("\n"):
            if "Number of dimensions of calibration solution space" in l:
                self.supcalc.SolnSpaceSize = int(l.split()[-1].strip())
                continue
            if "Number of dimensions of calibration null space" in l:
                self.supcalc.NullSpaceSize = int(l.split()[-1].strip())

            if len(l.split()) == 4\
                    and not "---------------" in l\
                    and not " Identifiability " in l:
                parname, ident, varred, uncred = l.split()
                self.parameters.append(parname)
                self.identifiability[parname] = float(ident)
                self.relErrVarReduction[parname] = float(varred)
                self.relUncertVarReduction[parname] = float(uncred)

class Predvar1Result:
    def __init__(self):
        self.nameOfPrediction = None
        self.preCalTotalErrorVariance = None
        self.postCalTotalErrorVariance = None

        self.SingularValueIndices = []
        self.NullSpaceTerm = {}
        self.SolnSpaceTerm = {}
        self.TotalVariance = {}

    def parseFromString(self, text):
        state = None
        for l in text.split("\n"):
            if "PREDVAR1 analysis for prediction" in l:
                self.nameOfPrediction = l.split()[-2].strip('\"')
                continue

            if len(l.split()) == 5\
                    and not "Sing_val" in l\
                    and not "index" in l\
                    and not "--------" in l\
                    and not "Total" in l:
                svindex, nsterm, ssterm, totvar, totstdev = l.split()
                self.SingularValueIndices.append(int(svindex))
                self.NullSpaceTerm[svindex] = float(nsterm)
                self.SolnSpaceTerm[svindex] = float(ssterm)
                self.TotalVariance[svindex] = float(totvar)

            if "Pre-calibration:-" in l or "Post-calibration:-" in l:
                state = l.strip()

            if "Total error variance" in l:
                var = float(l.split()[-1].strip())
                if state == "Pre-calibration:-":
                    self.preCalTotalErrorVariance = var
                elif state == "Post-calibration:-":
                    self.postCalTotalErrorVariance = var
                else:
                    raise ValueError("Parse Error: Pre-Cal / Postcal keyword not found")

            if "Minimum error variance occurs at singular value number" in l:
                self.svOfMinVar = int(l.split()[-1].strip("."))

class Predunc1Result:
    def __init__(self):
        self.preCalTotalUncertaintyVariance = None
        self.postCalTotalUncertaintyVariance = None

    def parseFromString(self, text):
        state = None
        for l in text.split("\n"):
            if "PREDUNC1 analysis for prediction" in l:
                self.nameOfPrediction = l.split()[-2].strip('\"')
                continue

            if "Pre-calibration:-" in l or "Post-calibration:-" in l:
                state = l.strip()

            if "Total uncertainty variance" in l:
                var = float(l.split()[-1].strip())
                if state == "Pre-calibration:-":
                    self.preCalTotalUncertaintyVariance = var
                elif state == "Post-calibration:-":
                    self.postCalTotalUncertaintyVariance = var
                else:
                    raise ValueError("Parse Error: Pre-Cal / Postcal keyword not found")

class Predvar4Result:
    def __init__(self):
        self.nameOfPrediction = None
        self.description = "Contributions to predictive error variance"
        self.parameters = []
        self.preCalContrib = {}
        self.postCalContrib = {}

    def parseFromString(self, text):
        for l in text.split("\n"):

            if "PREDVAR4 analysis for prediction" in l:
                self.nameOfPrediction = l.split()[-2].strip('\"')
                continue

            if len(l.split()) == 3\
                    and not "Parameter" in l\
                    and not "---------" in l:
                parname, preCalContrib, postCalContrib = l.split()
                self.parameters.append(parname)
                self.preCalContrib[parname] = float(preCalContrib)
                self.postCalContrib[parname] = float(postCalContrib)

class Predunc4Result:
    def __init__(self):
        self.nameOfPrediction = None
        self.description = "Contributions to predictive uncertainty variance"
        self.parameters = []
        self.preCalContrib = {}
        self.postCalContrib = {}

    def parseFromString(self, text):
        for l in text.split("\n"):
            if "PREDUNC4 analysis for prediction" in l:
                self.nameOfPrediction = l.split()[-2].strip('\"')
                continue

            if len(l.split()) == 3\
                    and not "Parameter" in l\
                    and not "---------" in l:
                parname, preCalContrib, postCalContrib = l.split()
                self.parameters.append(parname)
                self.preCalContrib[parname] = float(preCalContrib)
                self.postCalContrib[parname] = float(postCalContrib)

class Predvar5SubtractResult:
    def __init__(self):
        self.nameOfPrediction = None
        self.description = "Increases in predictive error variance incurred through loss of observations"
        self.Observations = []
        self.VarianceIncrease = {}

    def parseFromString(self, text):
        for l in text.split("\n"):
            if "for prediction" in l:
                self.nameOfPrediction = l.split()[-2].strip('\"')
                continue

            if len(l.split()) == 2\
                    and not "Observation" in l\
                    and not "---------" in l:
                observation, varIncrease = l.split()
                self.Observations.append(observation)
                self.VarianceIncrease[observation] = float(varIncrease)

class Predunc5SubtractResult:
    def __init__(self):
        self.nameOfPrediction = None
        self.description = "Increases in predictive uncertainty variance incurred through loss of observations"
        self.Observations = []
        self.VarianceIncrease = {}

    def parseFromString(self, text):
        for l in text.split("\n"):
            if "for prediction" in l:
                self.nameOfPrediction = l.split()[-2].strip('\"')
                continue

            if len(l.split()) == 2\
                    and not "Observation" in l\
                    and not "---------" in l:
                observation, varIncrease = l.split()
                self.Observations.append(observation)
                self.VarianceIncrease[observation] = float(varIncrease)

class Predvar5AdditionResult:
    def __init__(self):
        self.nameOfPrediction = None
        self.description = "Decreases in pre-calibration predictive error variance incurred through addition of observations"
        self.Observations = []
        self.VarianceIncrease = {}

    def parseFromString(self, text):
        for l in text.split("\n"):
            if "for prediction" in l:
                self.nameOfPrediction = l.split()[-2].strip('\"')
                continue

            if len(l.split()) == 2\
                    and not "Observation" in l\
                    and not "---------" in l:
                observation, varIncrease = l.split()
                self.Observations.append(observation)
                self.VarianceIncrease[observation] = float(varIncrease)

class Predunc5AdditionResult:
    def __init__(self):
        self.nameOfPrediction = None
        self.description = "Decreases in pre-calibration predictive uncertainty variance incurred through addition of observations"
        self.Observations = []
        self.VarianceIncrease = {}

    def parseFromString(self, text):
        for l in text.split("\n"):
            if "for prediction" in l:
                self.nameOfPrediction = l.split()[-2].strip('\"')
                continue

            if len(l.split()) == 2\
                    and not "Observation" in l\
                    and not "---------" in l:
                observation, varIncrease = l.split()
                self.Observations.append(observation)
                self.VarianceIncrease[observation] = float(varIncrease)

class GenlinpredOutFile:
    def __init__(self, filename):
        self.blocks = {}
        self.parse(filename)
        if "ANALYSIS OF PARAMETERS" in self.blocks.keys():
            self.parameterUncertainty = ParameterAnalysis()
            self.parameterUncertainty.parseFromString(self.blocks["ANALYSIS OF PARAMETERS"])
        if "PREDVAR1 analysis" in self.blocks.keys():
            self.predvar1 = Predvar1Result()
            self.predvar1.parseFromString(self.blocks["PREDVAR1 analysis"])
        if "PREDUNC1 analysis" in self.blocks.keys():
            self.predunc1 = Predunc1Result()
            self.predunc1.parseFromString(self.blocks["PREDUNC1 analysis"])
        if "PREDVAR4 analysis" in self.blocks.keys():
            self.predvar4 = Predvar4Result()
            self.predvar4.parseFromString(self.blocks["PREDVAR4 analysis"])
        if "PREDUNC4 analysis" in self.blocks.keys():
            self.predunc4 = Predunc4Result()
            self.predunc4.parseFromString(self.blocks["PREDUNC4 analysis"])
        if "PREDVAR5 observation subtraction" in self.blocks.keys():
            self.predvar5subtract = Predvar5SubtractResult()
            self.predvar5subtract.parseFromString(self.blocks["PREDVAR5 observation subtraction"])
        if "PREDUNC5 observation subtraction" in self.blocks.keys():
            self.predunc5subtract = Predunc5SubtractResult()
            self.predunc5subtract.parseFromString(self.blocks["PREDUNC5 observation subtraction"])
        if "PREDVAR5 observation addition" in self.blocks.keys():
            self.predvar5add = Predvar5SubtractResult()
            self.predvar5add.parseFromString(self.blocks["PREDVAR5 observation addition"])
        if "PREDUNC5 observation addition" in self.blocks.keys():
            self.predunc5add = Predunc5SubtractResult()
            self.predunc5add.parseFromString(self.blocks["PREDUNC5 observation addition"])

    def parse(self, filename):
        readable_blocks = ["ANALYSIS DETAILS",
                                "ANALYSIS OF PARAMETERS",
                                "PREDVAR1 analysis",
                                "PREDUNC1 analysis",
                                "PREDVAR4 analysis",
                                "PREDUNC4 analysis",
                                "PREDVAR5 observation subtraction",
                                "PREDUNC5 observation subtraction",
                                "PREDVAR5 observation addition",
                                "PREDUNC5 observation addition"]
        self.available_blocks = []
        self.blocks={"None": ""}
        f = open(filename)
        current_block = "None"
        lines = f.readlines()
        for line in lines:
            for keyword in readable_blocks:
                if keyword in line:
                    current_block = keyword
                    self.available_blocks.append(current_block)
                    self.blocks[current_block] = ""
            self.blocks[current_block] += line
        f.close()
