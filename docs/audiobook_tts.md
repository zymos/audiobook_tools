# audiobook-tts

## Description:
   Text to Speech (TTS) program which interfaces with TTS software or online/cloud TTS services, and is optimized for audiobooks and web-novels

## Usage
<pre>
usage: online-tts [-h] [--bitrate {32k,48k,64k,96k,128k,196k}]
                  [--samplerate {16000,22050,44100,48000}] [--format {mp3,wav,ogg}]
                  [--input-format {txt,ssml,json-txt,json-ssml}] [--key KEY]
                  [--locale LOCALE] [--voice VOICE] [--gender GENDER]
                  [--url_parameters URL_PARAMETERS]
                  [--audio_settings AUDIO_SETTINGS] [--gtts-lang GTTS_LANG]
                  [--gtts-tld GTTS_TLD] [--tts-service TTS_SERVICE]
                  [--profile PROFILE] [--keep-asterisk] [--keep-quotes]
                  [--keep-problematic-chars] [--debug] [--test]
                  EBOOK [EBOOK ...]

positional arguments:
  EBOOK                 ebook txt file

optional arguments:
  -h, --help            show this help message and exit
  --bitrate {32k,48k,64k,96k,128k,196k}
                        audio encoding bitrate
  --samplerate {16000,22050,44100,48000}
                        audio encoding samplerate
  --format {mp3,wav,ogg}
                        audio encoding format
  --input-format {txt,ssml,json-txt,json-ssml}
                        format sent to TTS service
  --key KEY             key, auth code, auth file
  --locale LOCALE       example: en-us, en-au,
  --voice VOICE         voice
  --gender GENDER
  --url_parameters URL_PARAMETERS
                        this will be attached to url after question mark
  --audio_settings AUDIO_SETTINGS
  --gtts-lang GTTS_LANG
                        language for google-translate-tts
  --gtts-tld GTTS_TLD   top-level-domain for google-tanslate-tts accents
  --tts-service TTS_SERVICE
                        tts service to use. ie google_translate_tts, voicerss,
                        google_cloud_tts(unimplemented), amazone_polly(unimplemented
  --profile PROFILE     profile to use, set in config file
  --keep-asterisk       Some TTS servers speak out "asterisk", by default they are
                        removed
  --keep-quotes         Some TTS servers speak out "quote", by default they are
                        removed
  --keep-problematic-chars
                        don\'t remove problematic charactors, that are often spoken
                        [\"\\\/*]
  --debug               debug mode, more output
  --test                test mode, no writing data
</pre>

## Requirements:
- python3
- ffmpeg
- account for online services (optional)
- mimic3 (optional)
- python-gtts (optional, for google_translate_tts)


### Mimic3 TTS (software)
Quality varies depending on voices. 'en_UK/apope_low' is the best, it sounds natural but flat and unemotional.

Requirements
- *mimic3 - https://github.com/mycroftAI/mimic3
-**** mimic3-voices - https://github.com/MycroftAI/mimic3-voices

Voices(en)
-****** Male (British)     - en_UK/apope_low -       
      (good, lite british accent, dep voice, realistic voice but flat, recomended speed 0.9)
- Male (American)    - en_US/cmu-arctic_low -  (ok, recomended speed 1.0)
- Male (American)    - en_US/hifi-tts_low -    (not-great, deep voice, recomended speed 1.1)
- Female (Ameican)   - en_US/ljspeech_low -    (not-great, clipped, recomended speed 0.9)
- Male (American)    - en_US/m-ailabs_low -    (not-great, recomended speed 1.1)
- Female (American)  - en_US/vctk_low -        (bad, very fast)

### VoiceRSS TTS (online service)
Free limited service or paid full service.  Voice quality is average (between robotic and natural).


### MS Azure TTS (online serice)
requires a subsciption or free testing period


### Google Translate TTS
This is not Google cloud TTS, it uses Google translate's option for TTS output. Voice quality is robotic.

Requirements
- python gtts module


## Alterative (unimplemented) TTS engines
I have not created APIs for these serices yet, but you can add you own in the APIs folder, then add to config file. Examples/samples of various engins can be found here https://synesthesiam.github.io/opentts

- marytts (software) - pitch warbles between words
- espeak (software) - robotic voices
- festival (software) - robotic voices
- CMU Flite/festival-lite (software) - https://github.com/festvox/flite - robotic, but less than some
- Amazon Polly - Quality is better than average.  I don't have an account.
- IBM Cloud -  https://cloud.ibm.com/catalog/services/text-to-speech - I don't have an account
- Coqui TTS - sounds great in a single phrases, but has intermiten odd pauses and slowed words when reading chapters
- Google Cloud TTS - their deep-learning TTS is the best I've heard, the standard TTS is better than average.  I don't have an account.

