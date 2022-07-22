ab-tts

Description:
   Essentially a wrapper for mimic3 optimized for aubiobook encoding.

Requirements
* *mimic3 - https://github.com/mycroftAI/mimic3
***** mimic3-voices - https://github.com/MycroftAI/mimic3-voices

Voices(en)
******* Male (British/deep) -    en_UK/apope_low -       (ok, slow, recomended speed 0.9)
* Male (American)    -     en_US/cmu-arctic_low -  (ok, recomended speed 1.0)
* Male (American/deep) -   en_US/hifi-tts_low -    (not-great, deep voice, recomended speed 1.1)
* Female (Ameican) -       en_US/ljspeech_low -    (not-great, clipped, recomended speed 0.9)
* Male (American) -        en_US/m-ailabs_low -    (not-great, recomended speed 1.1)
* Female (American) -      en_US/vctk_low -        (bad, very fast, recomended speed 1.7)


=Test command=
head -n 20 test.txt |mimic3 --voice "en_US/vctk_low"  --length-scale 1  |ffmpeg -y -i - out.mp3


=bash script equivelent=

<pre>
#!/bin/env bash

NAME=$(echo $1 |sed 's/\.txt$/.mp3/')

echo $NAME

cat "$1" | mimic3 --voice "en_US/ljspeech_low" --length-scale 0.9 | ffmpeg -y -i - "$NAME"
</pre>

=Alterative TTS engines=
examples/samples of various engins can be found here https://synesthesiam.github.io/opentts
* marytts - sounds wobbly between words
* espeak - robotic voices
* festival - robotic voices
* CMU Flite (festival-lite) - https://github.com/festvox/flite - robotic, but less than most

