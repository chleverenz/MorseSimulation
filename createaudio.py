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

def append_silence(duration_milliseconds=500, noisefraction = 0.1, volume = 1.0):
    """
    Adding silence is easy - we add zeros to the end of our array
    """
    num_samples = duration_milliseconds * (sample_rate / 1000.0)
    if noisefraction > 1.0:
        noisefraction = 1.0
    for x in range(int(num_samples)): 
        val = 0
        if(noisefraction > 0.0):
            val = random.random() * noisefraction * volume
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
        if noisefraction > 0.0:
            val = (val * (1.0 - noisefraction)) + ((random.random() - 0.5) * noisefraction * volume);
        audio.append(val)
    return


def save_wav(file_name, alreadyconverted = False):
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
        if alreadyconverted:
            wav_file.writeframes(struct.pack('h', sample))
        else:
            wav_file.writeframes(struct.pack('h', int( sample * 32767.0 )))

    wav_file.close()

    return

def save_adc(file_name):
    # Open up a wav file
    adc_file= open(file_name,"w")

    for sample in audio:
        adc_file.write(str(int(sample * 32767.0)) + "\n")

    adc_file.close()

    return

OUTFILECOMMANDLINE = ["--outbase","-o"]
CREATEWAVFROMADCCOMMANDLINE = ["--adc2wav","-a2w"]
FILECOMMANDLINE = ["--file","-f"]
SILENCENOISECOMMANDLINE = ["--silentnoise","-siln"]
SIGNALNOISECOMMANDLINE = ["--signalnoise","-sign"]
FREQUENCYCOMMANDLINE = ["--frequency","-freq","-p"]
VOLUMECOMMANDLINE = ["--volume","-vol","-v"]
DEFAULTOUTFILEBASE = "example"
HELPCOMMANDLINE = ["--help","-h","-?"]

DEFAULTSILENCENOISE = 0.0
DEFAULTFREQENCY = 440
DEFAULTVOLUME = 0.25

HELPDELIMITER = " or "
HELPINDENTION = "  "

def givehelp():
    print("Creates a morse audiofile from a timingfile")
    print("Usage: " + sys.argv[0] + " with parameters:")
    print(HELPINDENTION + HELPDELIMITER.join(FILECOMMANDLINE) + " <filename> : filename to read timing/adcvalues from")
    print(HELPINDENTION + HELPDELIMITER.join(OUTFILECOMMANDLINE) + ": basename for outputfiles (default: " + DEFAULTOUTFILEBASE +")")
    print(HELPINDENTION + HELPDELIMITER.join(SILENCENOISECOMMANDLINE) + ": noisefraction in silence (default: " + str(DEFAULTSILENCENOISE) +")")
    print(HELPINDENTION + HELPDELIMITER.join(SIGNALNOISECOMMANDLINE) + ": noisefraction in signal (default: " + str(DEFAULTSILENCENOISE) +")")
    print(HELPINDENTION + HELPDELIMITER.join(FREQUENCYCOMMANDLINE) + ": freqency for signal (default: " + str(DEFAULTFREQENCY) +")")
    print(HELPINDENTION + HELPDELIMITER.join(VOLUMECOMMANDLINE) + ": outputvolume (default: " + str(DEFAULTVOLUME) +")")
    print(HELPINDENTION + HELPDELIMITER.join(CREATEWAVFROMADCCOMMANDLINE) + ": just create wav from adc file")
    print(HELPINDENTION + HELPDELIMITER.join(HELPCOMMANDLINE) + ": this text :-)")

def main():
    args = sys.argv[1:]
    arglen = len(args)
    
    helpalreadygiven = False
    filenameapplied = False

    if arglen == 0:
        givehelp()
        helpalreadygiven = True

    volume = DEFAULTVOLUME
    frequency = DEFAULTFREQENCY
    silencenoise = DEFAULTSILENCENOISE
    signalnoise = silencenoise
    #infilename = "example.timing"
    infilename = ""
    outputfilebase = DEFAULTOUTFILEBASE
    adc2wav = False

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
                filenameapplied = True
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
                print("Error: no argument for volume given")
        elif cmd in CREATEWAVFROMADCCOMMANDLINE:
            adc2wav = True
        elif cmd in HELPCOMMANDLINE:
            if not helpalreadygiven:
                givehelp()
                helpalreadygiven = True
        else:
            print("unknown parameter " + cmd)
            if not helpalreadygiven:
                givehelp()
                helpalreadygiven = True
    
    filenameapplied = infilename != ""

    if exists(infilename) and filenameapplied:
        adot = "."
        outputparts = outputfilebase.split(adot)
        if len(outputparts) > 1:
            outputfilebase = adot.join(outputparts[:-1])
        outputfile = outputfilebase + ".wav"
        outputfileadc = outputfilebase + ".adc"
        if adc2wav:
            print(f"converting file {infilename} to {outputfile}")
            global audio
            infile = open(infilename,"r")
            audio = list(map(lambda e: int(e),infile.readlines()))
            infile.close()
            save_wav(outputfile, alreadyconverted=True)
        else:
            print(f"converting file {infilename} to {outputfile} and {outputfileadc}")
            #print("converting file " + infilename + " to " + outputfile)

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
                        append_silence(duration_milliseconds= abs(t), noisefraction=silencenoise, volume = volume)
                save_wav(outputfile)
                save_adc(outputfileadc)
    else:
        if filenameapplied:
            print(f"file {infilename} not found")
        else:
            print(f"no inputfile given")

if __name__ == "__main__":
    main()
