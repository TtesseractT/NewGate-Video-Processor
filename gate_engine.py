#-------------------------------------------------------------------#
# Name: Gated Video Editor                                          #
#-------------------------------------------------------------------#
# Author: SABIAN HIBBS                                              #
# License: MIT                                                      #
# Version: 2.0                                                      #
#-------------------------------------------------------------------#

from audiotsm import phasevocoder
from audiotsm.io.wav import WavReader, WavWriter
from scipy.io import wavfile
import re, subprocess, math, shutil, numpy as np
from utils import (getMaxVolume, copyFrame, createPath, TEMP_FOLDER)
from cli import (frameRate, SAMPLE_RATE, SILENT_THRESHOLD, FRAME_SPREADAGE,
                 NEW_SPEED, INPUT_FILE, FRAME_QUALITY, OUTPUT_FILE, AUDIO_FADE_ENVELOPE_SIZE,
                 INP_F_TOTAL)

try:
    createPath(TEMP_FOLDER)  # Create a temporary folder
    print(f'Total Number of Frames In Video: {INP_F_TOTAL}')

    # Use FFmpeg to extract frames from the input video
    command = f'ffmpeg -loglevel error -stats -i {INPUT_FILE} -qscale:v {FRAME_QUALITY} {TEMP_FOLDER}/frame%06d.jpg -hide_banner'
    subprocess.call(command, shell=True)

    # Use FFmpeg to extract audio from the input video
    command = "ffmpeg -loglevel error -stats -i " + INPUT_FILE + " -ab 160k -ac 2 -ar " + str(
        SAMPLE_RATE) + " -vn " + TEMP_FOLDER + "/audio.wav"
    subprocess.call(command, shell=True)

    command = "ffmpeg  -loglevel error -stats -i " + TEMP_FOLDER + "/input.mp4 2>&1"
    f = open(TEMP_FOLDER + "/params.txt", "w")
    subprocess.call(command, shell=True, stdout=f)

    # Get the audio data and properties
    sampleRate, audioData = wavfile.read(TEMP_FOLDER + "/audio.wav")
    audioSampleCount = audioData.shape[0]
    maxAudioVolume = getMaxVolume(audioData)

    # Get the frame rate of the video from FFmpeg output
    f = open(TEMP_FOLDER + "/params.txt", 'r+')
    pre_params = f.read()
    f.close()
    params = pre_params.split('\n')
    for line in params:
        m = re.search('Stream #.*Video.* ([0-9]*) fps', line)
        if m is not None:
            frameRate = float(m.group(1))

    samplesPerFrame = sampleRate / frameRate
    audioFrameCount = int(math.ceil(audioSampleCount / samplesPerFrame))
    hasLoudAudio = np.zeros((audioFrameCount))

    # Find audio frames with sound above the silent threshold
    for i in range(audioFrameCount):
        start = int(i * samplesPerFrame)
        end = min(int((i + 1) * samplesPerFrame), audioSampleCount)
        audiochunks = audioData[start:end]
        maxchunksVolume = float(getMaxVolume(audiochunks)) / maxAudioVolume
        if maxchunksVolume >= SILENT_THRESHOLD:
            hasLoudAudio[i] = 1

    chunks = [[0, 0, 0]]
    shouldIncludeFrame = np.zeros((audioFrameCount))

    # Divide audio frames into chunks based on the presence of sound
    for i in range(audioFrameCount):
        start = int(max(0, i - FRAME_SPREADAGE))
        end = int(min(audioFrameCount, i + 1 + FRAME_SPREADAGE))
        shouldIncludeFrame[i] = np.max(hasLoudAudio[start:end])
        if (i >= 1 and shouldIncludeFrame[i] != shouldIncludeFrame[i - 1]):
            # If the frame has changed, add the previous chunk's end frame to the list
            chunks.append([chunks[-1][1], i, shouldIncludeFrame[i - 1]])

    chunks.append([chunks[-1][1], audioFrameCount, shouldIncludeFrame[i - 1]])
    chunks = chunks[1:]
    outputAudioData = np.zeros((0, audioData.shape[1]))
    outputPointer = 0
    lastExistingFrame = None

    # Alter the speed of each chunk and process the frames
    for chunk in chunks:

        audioChunk = audioData[int(chunk[0] * samplesPerFrame):int(chunk[1] * samplesPerFrame)]
        sFile = TEMP_FOLDER + "/tempStart.wav"
        eFile = TEMP_FOLDER + "/tempEnd.wav"
        wavfile.write(sFile, SAMPLE_RATE, audioChunk)

        with WavReader(sFile) as reader:
            with WavWriter(eFile, reader.channels, reader.samplerate) as writer:
                tsm = phasevocoder(reader.channels, speed=NEW_SPEED[int(chunk[2])])
                tsm.run(reader, writer)

        _, alteredAudioData = wavfile.read(eFile)
        leng = alteredAudioData.shape[0]
        endPointer = outputPointer + leng
        outputAudioData = np.concatenate((outputAudioData, alteredAudioData / maxAudioVolume))

        if leng < AUDIO_FADE_ENVELOPE_SIZE:
            outputAudioData[outputPointer:endPointer] = 0
        else:
            premask = np.arange(AUDIO_FADE_ENVELOPE_SIZE) / AUDIO_FADE_ENVELOPE_SIZE
            mask = np.repeat(premask[:, np.newaxis], 2, axis=1)  # Repeat for stereo
            outputAudioData[outputPointer:outputPointer + AUDIO_FADE_ENVELOPE_SIZE] *= mask
            outputAudioData[endPointer - AUDIO_FADE_ENVELOPE_SIZE:endPointer] *= 1 - mask
        startOutputFrame = int(math.ceil(outputPointer / samplesPerFrame))
        endOutputFrame = int(math.ceil(endPointer / samplesPerFrame))

        for outputFrame in range(startOutputFrame, endOutputFrame):
            inputFrame = int(chunk[0] + NEW_SPEED[int(chunk[2])] * (outputFrame - startOutputFrame))
            didItWork = copyFrame(inputFrame, outputFrame)
            if didItWork:
                lastExistingFrame = inputFrame
            else:
                copyFrame(lastExistingFrame, outputFrame)
        outputPointer = endPointer

    wavfile.write(TEMP_FOLDER + "/audioNew.wav", SAMPLE_RATE, outputAudioData)

    # Combine the altered frames and audio into the output file using FFmpeg
    command = "ffmpeg -loglevel error -stats -framerate " + str(frameRate) + " -i " + TEMP_FOLDER + "/newFrame%06d.jpg -i " + TEMP_FOLDER + "/audioNew.wav -strict -2 " + OUTPUT_FILE
    subprocess.call(command, shell=True)
except:
    shutil.rmtree(TEMP_FOLDER)
    raise

# Remove the temporary folder
shutil.rmtree(TEMP_FOLDER)
