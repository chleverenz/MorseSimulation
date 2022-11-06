#!/usr/bin/python 
# based on : www.daniweb.com/code/snippet263775.html
import math
import wave
import struct
import random
import sys
from os.path import exists


# Audio will contain a long list of samples (i.e. floating point numbers describing the
# waveform).  If you were working with a very long sound you'd want to stream this to
# disk instead of buffering it all in memory list this.  But most sounds will fit in 
# memory.
audio = []
#sample_rate = 44100.0
sample_rate = 8000.0

def append_silence(duration_milliseconds=500, noisefraction = 0.1):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = duration_milliseconds * (sample_rate / 1000.0)
    if noisefraction > 1.0:
        noisefraction = 1.0
    for x in range(int(num_samples)): 
        val = 0
        if(noisefraction > 0.0):
            val = random.random() * noisefraction
        audio.append(val)
    return

def append_sinewave(
        freq=440.0, 
        duration_milliseconds=500, 
        volume=1.0,
        noisefraction = 0.1):
    """
    The sine wave generated here is the standard beep.  If you want something
    more aggresive you could try a square or saw tooth waveform.   Though there
    are some rather complicated issues with making high quality square and
    sawtooth waves... which we won't address here :) 
    """ 
    if noisefraction > 1.0:
        noisefraction = 1.0

    global audio # using global variables isn't cool.

    num_samples = duration_milliseconds * (sample_rate / 1000.0)

    for x in range(int(num_samples)):
        val = volume * math.sin(2 * math.pi * freq * ( x / sample_rate ))
        if noisefraction > 1.0:
            val = (val * (1.0 - noisefraction)) + (random.random() * noisefraction);
        audio.append(val)
    return


def save_wav(file_name):
    # Open up a wav file
    wav_file=wave.open(file_name,"w")

    # wav params
    nchannels = 1

    sampwidth = 2

    # 44100 is the industry standard sample rate - CD quality.  If you need to
    # save on file size you can adjust it downwards. The standard for low quality
    # is 8000 or 8kHz.
    nframes = len(audio)
    comptype = "NONE"
    compname = "not compressed"
    wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

    # WAV files here are using short, 16 bit, signed integers for the 
    # sample size.  So we multiply the floating point data we have by 32767, the
    # maximum value for a short integer.  NOTE: It is theortically possible to
    # use the floating point -1.0 to 1.0 data directly in a WAV file but not
    # obvious how to do that using the wave module in python.
    for sample in audio:
        wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

    return

OUTFILECOMMANDLINE = ["--outbase","-o"]
FILECOMMANDLINE = ["--file","-f"]
SILENCENOISECOMMANDLINE = ["--silentnoise","-siln"]
SIGNALNOISECOMMANDLINE = ["--signalnoise","-sign"]
FREQUENCYCOMMANDLINE = ["--frequency","-freq","-p"]
VOLUMECOMMANDLINE = ["--volume","-vol","-v"]
DEFAULTOUTFILEBASE = "example"

def main():
    args = sys.argv[1:]
    arglen = len(args)

    volume = 0.25
    frequency = 440.0
    silencenoise = 0.0
    signalnoise = silencenoise
    infilename = "example.timing"
    outputfilebase = DEFAULTOUTFILEBASE

    i = 0
    while i < arglen:
        cmd = args[i].lower()
        i += 1
        if cmd in OUTFILECOMMANDLINE:
            if arglen > i:
                outputfilebase = args[i]
                i = i + 1
            else:
                print("Error: no argument for outfilebase given")
        elif cmd in FILECOMMANDLINE:
            if arglen > i:
                infilename = args[i]
                i = i + 1
                if outputfilebase == DEFAULTOUTFILEBASE:
                    outputfilebase = infilename
            else:
                print("Error: no argument for infilename given")
        elif cmd in SILENCENOISECOMMANDLINE:
            if arglen > i:
                silencenoise = float(args[i])
                i = i + 1
                if silencenoise > 1.0:
                    silencenoise = 1.0
            else:
                print("Error: no argument for silencenoise given")
        elif cmd in SIGNALNOISECOMMANDLINE:
            if arglen > i:
                signalnoise = float(args[i])
                i = i + 1
                if signalnoise > 1.0:
                    signalnoise = 1.0
            else:
                print("Error: no argument for signalnoise given")
        elif cmd in FREQUENCYCOMMANDLINE:
            if arglen > i:
                frequency = float(args[i])
                i = i + 1
            else:
                print("Error: no argument for frequency given")
        elif cmd in VOLUMECOMMANDLINE:
            if arglen > i:
                volume = float(args[i])
                i = i + 1
                if volume > 1.0:
                    volume = 1.0
            else:
                print("Error: no argument for frequency given")
        else:
            print("command " + cmd + " not known")

    if exists(infilename):
        infile = open(infilename,"r")
        lines = infile.readlines()
        infile.close()
        linecout = len(lines)
        if linecout > 0:
            for i in range(linecout):
                t = int(lines[i])
                if t > 0:
                    append_sinewave(volume=volume, duration_milliseconds= t, freq=frequency, noisefraction=signalnoise)
                else:
                    append_silence(duration_milliseconds= abs(t), noisefraction=silencenoise)
            adot = "."
            outputparts = outputfilebase.split(adot)
            if len(outputparts) > 1:
                outputfilebase = adot.join(outputparts[:-1])
            save_wav(outputfilebase + ".wav")
    else:
        print("file " + infilename + " not found")

if __name__ == "__main__":
    main()
