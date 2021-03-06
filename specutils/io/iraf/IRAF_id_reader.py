import re
import numpy as np

#	image	sample_id_J[*,93]
imre = re.compile('^\s*image\s*.*\[[0-9*]*,([0-9]*)\]')
#	features	65
featre = re.compile('^\s*features\s*([0-9]*)')
#	function spline3
splinere = re.compile("^\s*function\s*spline")
blankre = re.compile("^\s*(#.*)?$")
# data line:
# 20.24 14832.9644     14833.   4.0 1 1 0.62
# should be:
#datare = re.compile("^(\s+[0-9\.]+){6,7}")
# but that doesn't work.
datare = re.compile("^"+"(\s+[0-9\.]+)"*7+"?")

def IRAF_identify_reader(fn):
    """
    Read a file generated by the IRAF identify task

    Returns
    -------
    idlines : dict
        A dictionary with indices corresponding to the Y-index of the line
        where each entry contains the X coordinates of each fitted position.
        This is useful for overplotting on an image to see where the lines were
        extracted.
    sections: dict
        A dictionary again indexed by the Y-value of the fitted line containing
        all lines from the id file corresponding to said Y-value.
    """
    idlines = {}
    sections = {}
    with open(fn) as of:
        section = []
        for line in of:
            section.append(line)
            if imre.search(line):
                ypos = int(imre.search(line).groups()[0])
            elif blankre.search(line):
                ypos = None
                sections[line] = section
                section = []
            elif featre.search(line):
                nlines = int(featre.search(line).groups()[0])
                arr = np.empty(nlines)
                idlines[ypos] = arr
                counter = 0
            elif splinere.search(line):
                if counter != nlines:
                    raise ValueError("Did not find the expected number of lines")
            elif datare.search(line):
                data = datare.search(line).groups()
                xpos = data[0]
                arr[counter] = xpos
                counter += 1

    return idlines, sections
