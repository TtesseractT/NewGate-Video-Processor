#-------------------------------------------------------------------#
# Name: Gated Video Editor                                          #
#-------------------------------------------------------------------#
# Author: SABIAN HIBBS                                              #
# License: MIT                                                      #
# Version: 2.0                                                      #
#-------------------------------------------------------------------#

import os, numpy as np
from shutil import copyfile, rmtree

TEMP_FOLDER = "TEMP"

# Calculate the maximum volume of an audio signal
def getMaxVolume(s):
    maxv = float(np.max(s))
    minv = float(np.min(s))
    return max(maxv, -minv)

# Copy a frame from the input directory to the output directory
def copyFrame(inputFrame, outputFrame):
    src = TEMP_FOLDER + "/frame{:06d}".format(inputFrame + 1) + ".jpg"
    dst = TEMP_FOLDER + "/newFrame{:06d}".format(outputFrame + 1) + ".jpg"
    if not os.path.isfile(src):
        return False
    copyfile(src, dst)
    if (outputFrame + 1) % 1000 == 0:
        print(str(outputFrame + 1) + " time-altered frames saved.")
    return True

# Convert an input file name to an output file name
def inputToOutputFilename(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex] + "_ALTERED" + filename[dotIndex:]

# Create a directory if it doesn't exist
def createPath(s):
    try:
        os.mkdir(s)
    except OSError:
        assert False, "Creation of the directory %s failed. Temp folder already exists?" % s

# Delete a directory and its contents
def deletePath(s):
    try:
        rmtree(s, ignore_errors=False)
    except OSError:
        print("Deletion of the directory %s failed" % s)
        print(OSError)
