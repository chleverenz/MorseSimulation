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
    , ":" : "---..."
    , ";" : "-.-.-."
    , "/" : "-..-."
    , "-" : "-....-"
    , "ar" : ".-.-."
    , "sk" : "...-.-"
    , "hh" : "........"
}
DITSYM = "."
DAHSYM = "-"
DITOUT = "D"
DAHOUT = "L"
DOTSPACE = "DS"
CHARSPACE = "CS"
WORDSPACE = "WS"

def getsinglemorse(str = ""):
    if str != "" and str.lower() in CODES:
        return CODES[str.lower()]
    else:
        return ""

def getmorse(str = ""):
    retval = ""
    if str != "":
        for  i in range(len(str)):
            retval += getsinglemorse(str[i]) + " "
    return retval

def main():
    print("to be used as an import")

if __name__ == "__main__":
    main()