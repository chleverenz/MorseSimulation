#!/usr/bin/python 
import morsecodes as mc
import sys
from os.path import exists

#how many milliseconds for a dot?
DOTMILLIS = 100
TIMINGS = [
    (mc.DITOUT, 1)
    , (mc.DAHOUT, 3)
    , (mc.DOTSPACE, -1)
    , (mc.CHARSPACE, -3)
    , (mc.WORDSPACE, -6)
    , (mc.NEWLINESPACE, -6)
]

EXTENSION = ".timing"
DEFAULTOUTFILEBASE = "outputwav"
FILECOMMANDLINE = ["--file","-f"]
HELPCOMMANDLINE = ["--help","-h","-?"]
OUTFILECOMMANDLINE = ["--outbase","-o"]
HELPDELIMITER = " or "
HELPINDENTION = "  "

def givehelp():
    print("Creates timingfile from tokenfile")
    print("Usage: " + sys.argv[0] + " with parameters:")
    print(HELPINDENTION + HELPDELIMITER.join(FILECOMMANDLINE) + " <filename> : filenmane to read text from")
    print(HELPINDENTION + HELPDELIMITER.join(OUTFILECOMMANDLINE) + ": basename for outputfiles (default: " + DEFAULTOUTFILEBASE +")")
    print(HELPINDENTION + HELPDELIMITER.join(HELPCOMMANDLINE) + ": this text :-)")


def main():
    args = sys.argv[1:]
    arglen = len(args)
    text = ""
    outputfilebase = DEFAULTOUTFILEBASE
    helpalreadygiven = False
    timing = {}
    for i in range(len(TIMINGS)):
        entry = TIMINGS[i]
        timing[entry[0]] = entry[1]
    i = 0
    while i < arglen:
        cmd = args[i].lower()
        i += 1
        if cmd in FILECOMMANDLINE:
            if arglen > i:
                filetoread = args[i]
                if outputfilebase == DEFAULTOUTFILEBASE:
                    outputfilebase = filetoread
                if(exists(filetoread)):
                    file = open(filetoread, "r")
                    text = file.read()
                    file.close()
                else:
                    print("file " + filetoread + " does not exist")
                i += 1
            else:
                print("Error: no argument for filename given")
        elif cmd in HELPCOMMANDLINE:
            if not helpalreadygiven:
                givehelp()
                helpalreadygiven = True
        elif cmd in OUTFILECOMMANDLINE:
            if arglen > i:
                i = i + 1
                outputfilebase = args[i]
            else:
                print("Error: no argument for outfilebase given")
        else:
            print("unknown parameter " + cmd)
            if not helpalreadygiven:
                givehelp()
                helpalreadygiven = True
        if text != "":
            adot = "."
            outputparts = outputfilebase.split(adot)
            if len(outputparts) > 1:
                outputfilebase = adot.join(outputparts[:-1])

            outfile = open(outputfilebase + EXTENSION, "wt")
            for i in range(len(text)):
                c = text[i]
                if c in timing:
                    t = timing[c] * DOTMILLIS
                    outfile.write(str(t) + "\n")
            outfile.close()

if __name__ == "__main__":
    main()
