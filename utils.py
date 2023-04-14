#-------------------------------------------------------------------#
# Name: Gated Video Editor                                          #
#-------------------------------------------------------------------#
# Description: A Python tool that allows you to alter the playback  #
# speed of a video while preserving the audio pitch, using the      #
# phase vocoder time-scale modification algorithm. The program      #
# first analyzes the audio track of the input video to identify     #
# loud audio segments, and then divides the video into chunks based #
# on these segments. For each chunk, the program applies the        #
# time-scale modification algorithm to the audio track, and         #
# generates new video frames at the altered speed. The resulting    #
# output video has the same pitch as the original, but plays at a   #
# different speed.                                                  #
#-------------------------------------------------------------------#
# Author: SABIAN HIBBS                                              #
# License: MIT                                                      #
# Version: 2.0                                                      #
#-------------------------------------------------------------------#

import os, numpy as np
from shutil import copyfile, rmtree

TEMP_FOLDER = "TEMP"

def getMaxVolume(s):
    maxv = float(np.max(s))
    minv = float(np.min(s))
    return max(maxv,-minv)

def copyFrame(inputFrame,outputFrame):
    src = TEMP_FOLDER+"/frame{:06d}".format(inputFrame+1)+".jpg"
    dst = TEMP_FOLDER+"/newFrame{:06d}".format(outputFrame+1)+".jpg"
    if not os.path.isfile(src):
        return False
    copyfile(src, dst)
    if (outputFrame+1) % 1000 == 0:
        print(str(outputFrame+1)+" time-altered frames saved.")
    return True


def inputToOutputFilename(filename):
    dotIndex = filename.rfind(".")
    return filename[:dotIndex]+"_ALTERED"+filename[dotIndex:]

def createPath(s):
    try:  
        os.mkdir(s)
    except OSError:  
        assert False, "Creation of the directory %s failed. Temp folder already exists?"

def deletePath(s): # Dangerous!
    try:  
        rmtree(s,ignore_errors=False)
    except OSError:  
        print ("Deletion of the directory %s failed" % s)
        print(OSError)