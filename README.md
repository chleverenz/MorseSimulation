# MorseSimulation
Some tools for generating morsecode in order to be usable as input for morsedecoders

The idea is to have some helpers to cerate files that can later be used
for reconstructing morsestuff. This sounds a little bit weired but is a commen
practise in physics: you simulate something and try to find your signal back.

As there are different things to to, currently theer are three tools:

- createditdah.py creates a so called tokenfile, a plaintextfile (well, input = output :-) and a morsefile 
    with dashes and dots

```bash
python3 createditdah.py -f example.txt -to -p -m
```

- createtiming.py creates a timingfile from a tokenfile. The main thing is to cerate teh length og the appearance of
    a signal or the absence of it. Signal is denoted as a positive number, pause as a negavite number

```bash
python3 createtiming.py -f example.token
```

- createaudio.py  creates an audio from a timingfile. it will create a wavfile with thge provided timing which is 
    interprted as millisecinds. You can set the frequency, the noise and the volume for example. This wavfile could be 
    the input to the final reconstruction. As text and timing is available, the quality could be tested :-)

```bash
python3 createaudio.py -f example.timing
```
