__author__ = 'are'

import subprocess

"""These are bindings to the PEST Matrix Manipulation programs. See Addenum to PEST Manual, p 230 for implementation
"""

def jco2jco(casename1, casename2):
    """
    JCO2JCO reads a PEST control file (featuring base parameters) and its corresponding JCO file (normally computed
    through running PEST with NOPTMAX set to -1 or 1). It then reads a second PEST control file in which some or all of
    the same parameters and observations are cited. Some of these parameters may be tied or fixed or have different log
    transformation status in the second PEST control file. JCO2JCO calculates a JCO file for the second PEST control
    file on the basis of derivatives recorded in the first JCO file.
    See PEST manual v5, p 8 -26; PEST Addendum section 3.1
    :param casename1:the name of an existing PEST control file for which a complimentary JCO file exists
    :param casename2:PEST control file for which it is desired that a JCO file be written
    :return:
    """


def cov2cor():
    print("requires implementation. Syntax see addendum to PEST manual.")


def covcond():
    print("requires implementation. Syntax see addendum to PEST manual.")


def jco2mat(jcofile, matfile):
    """JCO2MAT reads a PEST-produced Jacobian matrix file.
    It re-writes the matrix contained therein in the same matrix file format as that employed by other utility
    programs documented herein. The Jacobian matrix is then amenable to manipulation using these utilities.

    :param jcofile: is the name of a Jacobian matrix file
    :param matfile: is the name of the matrix file to which the Jacobian matrix is to be written
    :return:
    """
    subprocess.call(["jco2mat", jcofile, matfile])


def jrow2mat(jcofile, obsname, matfile):
    """JROW2MAT extracts a row of a Jacobian matrix from a PEST unformatted “Jacobian matrix file” and writes that row
    as a 1×NPAR matrix to a standard matrix file, where NPAR is the number of (adjustable) parameters featured in the
    Jacobian matrix file. Note that the expected extension for a Jacobian matrix file is “.jco”.

    :param jcofile:is the name of a Jacobian matrix file,
    :param obsname:is the name of an observation or prior information item featured in that file,
    :param matfile:is the name of the matrix file to which the 1×NPAR matrix is to be written
    :return:
    """
    subprocess.call(["jrow2mat", jcofile, obsname, matfile])


def jrow2vec(jcofile, obsname, matfile):
    """
    JROW2VEC performs the same function as JROW2MAT followed by MATTRANS. That is, it extracts a user-nominated row
    from a Jacobian matrix. However instead of writing the extracted row in the form of a row matrix, it writes it as a
    column matrix. Thus, if desired, the extracted set of observation or predictive sensitivities is immediately usable
    by MATQUAD for evaluation of predictive error variance.
    :param jcofile:is the name of a Jacobian matrix file
    :param obsname:is the name of an observation or prior information item featured in that file,
    :param matfile:is the name of the matrix file to which the NPAR×1 matrix is to be written.
    :return:
    """
    subprocess.call(["jrow2vec", jcofile, obsname, matfile])


def mat2jco(matfile, jcofile):
    """
    MAT2JCO carries out the inverse of the operation carried out by JCO2MAT. It reads a matrix file and re-writes the
    matrix contained therein as a binary Jacobian matrix (i.e. JCO) file.
    MAT2JCO can be useful for transporting Jacobian matrices between different computing platforms. For example a binary
    JCO file produced on a UNIX platform may not be readable by the version of PEST running on a PC because of the fact
    that the UNIX and PC versions of PEST will necessarily have been compiled using different compilers. To overcome this
    problem, the binary JCO file can be translated to ASCII matrix file format on the UNIX machine; the matrix file can
    then be transferred to the PC; re-translation to binary JCO format can then be effected using the MAT2JCO utility.
    :param matfile:is the name of the matrix file
    :param jcofile:is a binary Jacobian matrix file
    :return:
    """
    subprocess.call(["mat2jco", matfile, jcofile])


def mat2srf():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matadd():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matcolex():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matdiag():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matdiff():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matinvp():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matjoinc():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matjoind():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matjoinr():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matorder():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matprod():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matquad():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matrow():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matsmul():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matspec():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matsvd():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matsym():
    print("requires implementation. Syntax see addendum to PEST manual.")


def mattrans():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matxtxi():
    print("requires implementation. Syntax see addendum to PEST manual.")


def matxtxix():
    print("requires implementation. Syntax see addendum to PEST manual.")


def pest2vec():
    print("requires implementation. Syntax see addendum to PEST manual.")


def vec2pest():
    print("requires implementation. Syntax see addendum to PEST manual.")


def velog():
    print("requires implementation. Syntax see addendum to PEST manual.")