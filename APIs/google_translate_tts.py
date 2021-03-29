########################################################################
#
#   File for various online/cloud TTS APIs
#
#   Global variables:
#       config['preferred']['tts_service']
#       config['preferred']['voice']
#       config['preferred']['locale']
#       config['preferred']['audio_format']
#       config['preferred']['audio_settings']
#       config['preferred']['input_format']
#       config['preferred']['key']
#       config['preferred']['url_parameters']
#       config['preferred']['gtts_lang']
#       config['preferred']['gtts_tld']
#       config['preferred']['delay_between_requests']
#
#       config['DEBUG']['debug']
#
#
########################################################################




########################################################################
# Google Translate TTS
#
def get_tts_audio(text, config, args):
    """
    Parameters
     tl: language
     ie: txt encoding, ex. utf.8
     q:  text to translate
    slow?
    lang check?
    unoffical
    tld: top-level domain (adds accent) ex. com, ca, co.uk, com.au
    """

    # imports API
    from gtts import gTTS
    from io import BytesIO # for bytes instead of file
    import re # regex
    import pprint # debuging
    import requests # for sending request to server
    import time # for sleep

    # Enable/Disable debug
    DEBUG = config['DEBUG']['debug']

    if args.gtts_lang:
        LANG_in    = args.gtts_lang
    else:
        LANG_in    = config['google_translate_tts']['lang']

    if args.gtts_tld :
        TLD_in    = args.gtts_tld
    else:
        TLD_in   = config['google_translate_tts']['tld']

    if config['google_translate_tts']['slow']:
        if config['google_translate_tts']['slow'] == 'True':
            SLOW_in = True
        else:
            SLOW_in = False
    else:
        SLOW_in = False


    if re.search('ssml', config['preferred']['input_format'], re.IGNORECASE):
        print("  Warning: Google Translate TTS does not support SSML, and will sound weird.")
     
    # Allows writing to varable instead of file 
    mp3_fp = BytesIO()

    tts = gTTS(text, lang=LANG_in, tld=TLD_in, slow=SLOW_in)

    tts.write_to_fp(mp3_fp)

    response = mp3_fp.getvalue()#tts_audio.read1()


    return response
 # End: google_translate_tts

