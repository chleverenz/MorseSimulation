# how are the characters in the codetable are made of?
DITSYM = "."
DAHSYM = "-"
# a list of recognized morsecodes, do not use spaces in morsecodes, only DITSYM and DAHSYM as defined
CODES = {
    "a" : ".-"
    , "b" : "-..."
    , "c" : "-.-."
    , "d" : "-.."
    , "e" : "."
    , "f" : "..-."
    , "g" : "--."
    , "h" : "...."
    , "i" : ".."
    , "j" : ".---"
    , "k" : "-.-"
    , "l" : ".-.."
    , "m" : "--"
    , "n" : "-."
    , "o" : "---"
    , "p" : ".--."
    , "q" : "--.-"
    , "r" : ".-."
    , "s" : "..."
    , "t" : "-"
    , "u" : "..-"
    , "v" : "...-"
    , "w" : ".--"
    , "x" : "-..-"
    , "y" : "-.--"
    , "z" : "--.."
    , "0" : "-----"
    , "1" : ".-----"
    , "2" : "..---"
    , "3" : "...--"
    , "4" : "....-"
    , "5" : "....."
    , "6" : "-...."
    , "7" : "--..."
    , "8" : "---.."
    , "9" : "----."
    , "." : ".-.-.-"
    , "," : "--..--"
    , "?" : "..--.."
    , ":" : "---..."
    , ";" : "-.-.-."
    , "/" : "-..-."
    , "-" : "-....-"
    , "ar" : ".-.-."
    , "sk" : "...-.-"
    , "hh" : "........"
    , "\b" : "........"
}
# the constants which are used pro producing outputs
EMPTYSTRING = ""
#how should charactes go to a special textfile (one character only for the ease of use and all should be diffrent of course)
DITOUT = "D" # short
DAHOUT = "L" # long
DOTSPACE = "S" # space between shorts and longs
CHARSPACE = "C" # character boundary
WORDSPACE = "W" # word boundary
NEWLINESPACE = "N" # newline boundary
# how many spaces should go for the actula morsecode?
CHARSPACES = " "
WORDSPACES = "  "
NEWLINESPACES = "   "
# special codes which are handled in a special way like space, newline, carriage returns tabs and so on
SPECIALCODES = {
    "\n" : (NEWLINESPACES, NEWLINESPACE)
    , "\r" : (NEWLINESPACES, NEWLINESPACE)
    , "\f" : (NEWLINESPACES, NEWLINESPACE)
    , "\t" : (WORDSPACES, WORDSPACE)
    , " " : (WORDSPACES, WORDSPACE)
}
# which charaters already produce a pause?
SPACEPRODUCERS = [
    NEWLINESPACE
    , WORDSPACE
    , CHARSPACE
    , "\b"
]

# get code for a single character, returns a tuple with the code, the shortcode for file and the parsed character
def getsinglemorse(str = EMPTYSTRING):
    retval = (EMPTYSTRING,EMPTYSTRING)
    if str in SPECIALCODES:
        retval = SPECIALCODES[str]
    else:
        if str != EMPTYSTRING and str.lower() in CODES:
            themorse = CODES[str.lower()];
            thetoken = EMPTYSTRING
            morselen = len(themorse)
            for i in range(morselen):
                if(themorse[i] == DITSYM):
                    thetoken += DITOUT
                else:
                    thetoken += DAHOUT
                if i < morselen - 1:
                    thetoken += DOTSPACE
            retval = (themorse,thetoken)
        else:
            retval = (EMPTYSTRING,EMPTYSTRING)
    return (retval[0], retval[1],str.lower())

#get the morsecode for a string for convinience, does not handle multicharatercodes... :-)
def getmorse(str = EMPTYSTRING):
    retval = []
    if str != EMPTYSTRING:
        for  i in range(len(str)):
            thecode = getsinglemorse(str[i])
            retval += (thecode,)
    return retval

def main():
    print("to be used as an import")

if __name__ == "__main__":
    main()