* Description: Extracts the text of web-novels articles/chapters to a TXT or SSML file to be used in a text-to-speech program or service.
* Supported Sites
  * Royal Road
  * WordPress sites
  * to add more

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
