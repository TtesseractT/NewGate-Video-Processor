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

import os, subprocess, argparse

parser = argparse.ArgumentParser(description='Check Documentation for more info.')
parser.add_argument('--input_file', type=str)
parser.add_argument('--output_file', type=str)
parser.add_argument('--silent_threshold', type=float, default=0.03)
parser.add_argument('--sounded_speed', type=float, default=1.00)
parser.add_argument('--silent_speed', type=float, default=9999999)
parser.add_argument('--frame_margin', type=float, default=1)
parser.add_argument('--sample_rate', type=float, default=44100)
parser.add_argument('--frame_rate', type=float, default=30)
parser.add_argument('--frame_quality', type=int, default=1)
args = parser.parse_args()

SAMPLE_RATE = args.sample_rate
SILENT_THRESHOLD = args.silent_threshold
FRAME_SPREADAGE = args.frame_margin
NEW_SPEED = [args.silent_speed, args.sounded_speed]
INPUT_FILE = args.input_file
FRAME_QUALITY = args.frame_quality
AUDIO_FADE_ENVELOPE_SIZE = 400
INP_F_TOTAL = 0
assert INPUT_FILE != None , "No input file specified."
    
# Use ffprobe to extract the frame rate
probe = subprocess.run(['ffprobe', '-v', '0', '-of', 'csv=p=0', '-select_streams', 'v:0', '-show_entries', 'stream=avg_frame_rate', INPUT_FILE], capture_output=True, text=True)
num, denom = probe.stdout.strip().split('/')
frameRate = float(num) / float(denom)

# Use ffprobe to extract the total number of frames
ffprobe_output = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=nb_frames', '-of', 'default=nokey=1:noprint_wrappers=1', INPUT_FILE], capture_output=True, text=True)
INP_F_TOTAL = int(ffprobe_output.stdout.strip())

if args.output_file:
    OUTPUT_FILE = args.output_file
else:
    filename, extension = os.path.splitext(args.input_file)
    OUTPUT_FILE = filename + '_Output' + extension

