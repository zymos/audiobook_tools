########################################################################
#
#   File for various online/cloud TTS API
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


#  from online_tty import *



###########################################################################
#
#   VoiceRSS API
#
###########################################################################
def get_tts_audio(text_in, config, args):
    """
     API Format (example):
         http://api.voicerss.org/?key=1234567890QWERTY&hl=en-us&c=MP3&src=Hello

    Settings:
     key -  Mandatory
         The API key
     src -  Mandatory
         The textual content for converting to speech (length limited by 100KB).
     hl -  Mandatory
         The textual content language. Allows values: see Languages.
     v -  Optional
         The speech voice. Allows values: see Voices.
         Default value: depends on a language.
     r -  Optional
         The speech rate (speed). Allows values: from -10 (slowest speed) up
         to 10 (fastest speed). Default value: 0 (normal speed).
     c - Optional
         The speech audio codec. Allows values: see Audio Codecs.
         Default value: WAV.
     f -  Optional
         The speech audio formats. Allows values: see Audio Formats.
         Default value: 8khz_8bit_mono.
     ssml - Optional
        The SSML textual content format (see SSML documentation).
         Allows values: true and false. Default value: false.
     b64 - Optional
         Defines output as a Base64 string format (for an internet browser playing)
         Allows values: true and false. Default value: false.
    """
    import re # regex
    import pprint # debuging
    import requests # for sending request to server
    import time # for sleep
    
    try:
        from audiobook_tools.common.basic_url_request import basic_url_request
    except:
        print("Error: loading basic url request")
        exit(1)
    
    # Enable/Disable debug
    DEBUG = config['DEBUG']['debug']


    ###############
    # get prefered parameter
    VOICE_in = config['preferred']['voice']
    LOCALE_in = config['preferred']['locale']
    AUDIO_FORMAT_in = config['preferred']['audio_format']
    AUDIO_SETTINGS_in = config['preferred']['audio_settings']
    INPUT_FORMAT_in = config['preferred']['input_format']
    KEY_in = config['preferred']['key']
    URL_PARAMETERS = config['preferred']['url_parameters']


    ######################
    # alterations required by voicer

    # codec/format (needs capitalized)
    AUDIO_FORMAT_in = AUDIO_FORMAT_in.capitalize()

    # Set SSML true/false
    if( INPUT_FORMAT_in == 'ssml' ):
        is_ssml = 'true'
    else:
        is_ssml = 'false'


    ################
    # Create the url
    url_sans_text = "http://api.voicerss.org/?key=" + KEY_in + "&hl=" + LOCALE_in + "&c=" + AUDIO_FORMAT_in + "&f=" + AUDIO_SETTINGS_in + "&src="
    url = url_sans_text + text_in


    ###############
    # Debug stuff
    if DEBUG:
        print("-----------------------------------------------------------")
        print(" Using Voice RSS TTS service")
        print(VOICE_in, LOCALE_in, AUDIO_FORMAT_in, AUDIO_SETTINGS_in, INPUT_FORMAT_in, KEY_in)
        print("----------------------------TEXT---------------------------")
        print(text_in)
        print("----------------------------URL---------------------------")
        print(url)
        print("----------------------------------------------------------")
        #  print(text_in)
        #  print("----------------------------------------------------------")


    ############
    # Send the request and get the audio
    try:
        audio = basic_url_request(url)
    except:
        print("Error: calling basic_url_request failed")
        exit(1)
        
    return audio
# End: voicerss_tts()
