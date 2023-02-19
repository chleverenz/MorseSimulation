# MorseSimulation

Some tools for generating morsecode in order to be usable as input for morsedecoders

The idea is to have some helpers to create files that can later be used
for reconstructing morsestuff. This sounds a little bit weired but is a commen
practise in physics: you simulate something and try to find your signal back.

As there are different things to do, currently there are three tools:

- createditdah.py creates a so called tokenfile, a plaintextfile (well, input = output :-) and a morsefile
    with dashes and dots

    The definition in the tokenfile is:

        - DITOUT = "D" # short
        - DAHOUT = "L" # long
        - DOTSPACE = "S" # space between shorts and longs
        - CHARSPACE = "C" # character boundary
        - WORDSPACE = "W" # word boundary
        - NEWLINESPACE = "N" # newline boundary

    ```bash
    python3 createditdah.py -f example.txt -to -p -m
    ```



- createtiming.py creates a timingfile from a tokenfile. The main thing is to create the length of the appearance of
    a signal or the absence of it. Signal is denoted as a positive number, pause as a negative number

    ```bash
    python3 createtiming.py -f example.token
    ```

- createaudio.py  creates an audio from a timingfile. It will create a wavfile with the provided timing which is
    interpreted as/in milliseconds. You can set the frequency, the noise and the volume for example. This wavfile could be the input to the final reconstruction. As text and timing is available, the quality could be tested :-)

    ```bash
    python3 createaudio.py -f example.timing
    ```

Currently, everything is more or less static and there is no jitter or something on the timing. But i think: start
simple and make it more challenging later is not a bad idea :-)

The format and content of the files is quite simple. Just generate some and look at them and the code (which is also
simple as i am not a python expert :-) )

