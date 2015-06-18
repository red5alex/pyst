__author__ = 'are'

"""
JCO1 - (JCO2MAT) -> MAT1  (calibration)
JCO2 - (JCO2MAT) -> MAT2  (prognosis)

get all observation rows
get all prognosis rows

export all selected observations from calibration (JROW2MAT)
export all selected observations from prognosis (JROW2MAT)

implement option to rename observations (required if prognosis and calibration model use the
same observations

bound all rows together (MATJOINC) -> MAT3

MAT3 - (MAT2JCO) -> MAT3

"""