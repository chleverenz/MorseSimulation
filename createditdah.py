#!/usr/bin/python 
import morsecodes as mc
import sys
from os.path import exists

EMPTYSTRING = ""
EXAMPLETEXT = "The quick brown Fox jumps over the lazy dog. 1234567890"
DEFAULTOUTFILEBASE = "exampleoutput"

HELPDELIMITER = " or "
HELPINDENTION = "  "
EXAMPLECOMMANDLINE = ["--example","-e"]
HELPCOMMANDLINE = ["--help","-h","-?"]
TEXTCOMMANDLINE = ["--text","-t"]
OUTFILECOMMANDLINE = ["--outbase","-o"]
QUIETCOMMANDLINE = ["--quiet","-q"]
FILECOMMANDLINE = ["--file","-f"]
TOKENOUTCOMMANDLINE = ["--token","-to"]
TOKENFILEEXTENSION = ".token"
PLAINOUTCOMMANDLINE = ["--plain","-p"]
PLAINFILEEXTENSION = ".plain"
MORSEOUTCOMMANDLINE = ["--morse","-m"]
MORSEFILEEXTENSION = ".morse"

def givehelp():
    print("Creates some parseable morsecode from text")
    print("Usage: " + sys.argv[0] + " with parameters:")
    print(HELPINDENTION + HELPDELIMITER.join(FILECOMMANDLINE) + " <filename> : filenmane to read text from")
    print(HELPINDENTION + HELPDELIMITER.join(TEXTCOMMANDLINE) + " <text>: text to be transformed")
    print(HELPINDENTION + HELPDELIMITER.join(EXAMPLECOMMANDLINE) + ": dumps some code with the exampletext: " + EXAMPLETEXT)
    print(HELPINDENTION + HELPDELIMITER.join(QUIETCOMMANDLINE) + ": do not write to console")
    print(HELPINDENTION + HELPDELIMITER.join(OUTFILECOMMANDLINE) + ": basename for outputfiles (default: " + DEFAULTOUTFILEBASE +")")
    print(HELPINDENTION + HELPDELIMITER.join(TOKENOUTCOMMANDLINE) + ": write to tokenfile (" + TOKENFILEEXTENSION +")")
    print(HELPINDENTION + HELPDELIMITER.join(PLAINOUTCOMMANDLINE) + ": write to plain file ("+ PLAINFILEEXTENSION+")")
    print(HELPINDENTION + HELPDELIMITER.join(MORSEOUTCOMMANDLINE) + ": write to morsefile (" + MORSEFILEEXTENSION + ")")
    print(HELPINDENTION + HELPDELIMITER.join(HELPCOMMANDLINE) + ": this text :-)")

def dumpmorse(thetext = "", toConsole = True, tokenFile = None, morseFile = None, plainFile = None):
    morsetext = mc.getmorse(thetext) 
    outfiles = [morseFile, tokenFile, plainFile]
    morselen = len(morsetext)
    deli = (mc.CHARSPACES,mc.CHARSPACE, mc.EMPTYSTRING)
    for i in range(morselen):
        if toConsole:
            print(morsetext[i],)
        for f in range(len(outfiles)):
            if outfiles[f] != None:
                outfiles[f].write(morsetext[i][f])
        # if this or next character already produces a pause, no characterpause :-)
        if i < morselen - 1 and morsetext[i + 1][1] not in mc.SPACEPRODUCERS and morsetext[i][1] not in mc.SPACEPRODUCERS:
            if toConsole:
                print(deli)
            for f in range(len(outfiles)):
                if outfiles[f] != None:
                    outfiles[f].write(deli[f])

def main():
    args = sys.argv[1:]
    arglen = len(args)
    helpalreadygiven = False
    text = EMPTYSTRING
    outputfilebase = DEFAULTOUTFILEBASE
    toconsole = True
    toTokenfile = False
    toPlainfile = False
    toMorsefile = False
    i = 0
    while i < arglen:
        cmd = args[i].lower()
        i += 1
        if cmd in EXAMPLECOMMANDLINE:
            text = EXAMPLETEXT
        elif cmd in TEXTCOMMANDLINE:
            if arglen > i:
                text = args[i]
                i += 1
            else:
                print("Error: no argument for text given")
        elif cmd in FILECOMMANDLINE:
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
        elif cmd in QUIETCOMMANDLINE:
            toconsole = False
        elif cmd in TOKENOUTCOMMANDLINE:
            toTokenfile = True
        elif cmd in PLAINOUTCOMMANDLINE:
            toPlainfile = True
        elif cmd in MORSEOUTCOMMANDLINE:
            toMorsefile = True
        else:
            print("unknown parameter " + cmd)
            if not helpalreadygiven:
                givehelp()
                helpalreadygiven = True

    if text == EMPTYSTRING:
        print ("no text or file given, do not know, what to do :-)")
        if not helpalreadygiven:
            givehelp()
            helpalreadygiven = True
    else:
        tokenFile = None
        morseFile = None
        plainFile = None
        createmode = "wt"
        adot = "."
        outputparts = outputfilebase.split(adot)
        if len(outputparts) > 1:
            outputfilebase = adot.join(outputparts[:-1])
        if toTokenfile:
            tokenFile = open(outputfilebase + TOKENFILEEXTENSION,createmode)
        if toPlainfile:
            plainFile = open(outputfilebase + PLAINFILEEXTENSION,createmode)
        if toMorsefile:
            morseFile = open(outputfilebase + MORSEFILEEXTENSION,createmode)
        if text != EMPTYSTRING:
            dumpmorse(thetext = text , toConsole = toconsole, tokenFile = tokenFile, morseFile = morseFile, plainFile = plainFile)
            if tokenFile != None:
                tokenFile.close()
            if morseFile != None:
                morseFile.close()
            if plainFile != None:
                plainFile.close()

if __name__ == "__main__":
    main()