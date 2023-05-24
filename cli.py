#-------------------------------------------------------------------#
# Name: Gated Video Editor                                          #
#-------------------------------------------------------------------#
# Author: SABIAN HIBBS                                              #
# License: MIT                                                      #
# Version: 2.0                                                      #
#-------------------------------------------------------------------#

import os, subprocess, argparse

# Create an argument parser and provide descriptions for the arguments
parser = argparse.ArgumentParser(description='Check Documentation for more info.')
parser.add_argument('--input_file', type=str)  # Path to the input file
parser.add_argument('--output_file', type=str)  # Path to the output file
parser.add_argument('--silent_threshold', type=float, default=0.03)  # Threshold for considering frames as silent
parser.add_argument('--sounded_speed', type=float, default=1.00)  # Speed for sounded frames
parser.add_argument('--silent_speed', type=float, default=9999999)  # Speed for silent frames
parser.add_argument('--frame_margin', type=float, default=1)  # Number of adjacent frames to include for context
parser.add_argument('--sample_rate', type=float, default=44100)  # Sample rate of audio
parser.add_argument('--frame_rate', type=float, default=30)  # Frame rate of video
parser.add_argument('--frame_quality', type=int, default=1)  # Quality of extracted frames
args = parser.parse_args()

SAMPLE_RATE = args.sample_rate  # Assign the sample rate from arguments to a variable
SILENT_THRESHOLD = args.silent_threshold  # Assign the silent threshold from arguments to a variable
FRAME_SPREADAGE = args.frame_margin  # Assign the frame margin from arguments to a variable
NEW_SPEED = [args.silent_speed, args.sounded_speed]  # Assign the speed values from arguments to a list
INPUT_FILE = args.input_file  # Assign the input file path from arguments to a variable
FRAME_QUALITY = args.frame_quality  # Assign the frame quality from arguments to a variable
AUDIO_FADE_ENVELOPE_SIZE = 400  # Size of the audio fade envelope
INP_F_TOTAL = 0  # Initialize the total number of frames

assert INPUT_FILE != None, "No input file specified."  # Check if input file is provided

# Use ffprobe to extract the frame rate of the input file
probe = subprocess.run(['ffprobe', '-v', '0', '-of', 'csv=p=0', '-select_streams', 'v:0', '-show_entries',
                        'stream=avg_frame_rate', INPUT_FILE], capture_output=True, text=True)
num, denom = probe.stdout.strip().split('/')
frameRate = float(num) / float(denom)

# Use ffprobe to extract the total number of frames in the input file
ffprobe_output = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries',
                                 'stream=nb_frames', '-of', 'default=nokey=1:noprint_wrappers=1', INPUT_FILE],
                                capture_output=True, text=True)
INP_F_TOTAL = int(ffprobe_output.stdout.strip())

# Determine the output file name based on the input file name
if args.output_file:
    OUTPUT_FILE = args.output_file  # Use the provided output file path
else:
    filename, extension = os.path.splitext(args.input_file)
    OUTPUT_FILE = filename + '_Output' + extension
