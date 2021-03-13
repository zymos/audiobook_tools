########################################################################
#
#   File for various online/cloud TTS APIs
#
#   Global variables:
#      config['VOICE'], 
#       config['LOCALE']
#	config['AUDIO_FORMAT']
#	config['AUDIO_SETTINGS']
#	config['INPUT_FORMAT']
#	config['KEY']) 
#
########################################################################

#  from online_tty import *
import re # regex
import pprint # debuging
import requests # for sending request to server


#############################################################################
#   TTS Service Selection
#       Uses config file or args to select which servies is used
#       Ex: google_translate_tts, google_cloud_tts, voicerss
#

def tts_service_selection(text, config):

    #  pprint.pprint(config)

    if( config['GENERAL']['tts_service'] == 'voicerss' ):
        response = voicerss_tts(text, config);
    # elif( config['GENERAL']['tts_service'] == 'example_tts' ):
    #   response = example_tts(text, config)    
    else:
        # Default
        print("Using default(local) service")
        response = local_tts(text, config);
        #  response = ''

    return response
# End: tts_service_selection()







###########################################################################
#
#   VoiceRSS API
#
###########################################################################
#
#   API Format (example):
#       http://api.voicerss.org/?key=1234567890QWERTY&hl=en-us&c=MP3&src=Hello
#
# Settings:
#   key -  Mandatory
#       The API key
#   src -  Mandatory
#       The textual content for converting to speech (length limited by 100KB).
#   hl -  Mandatory
#       The textual content language. Allows values: see Languages.
#   v -  Optional
#       The speech voice. Allows values: see Voices. 
#       Default value: depends on a language.
#   r -  Optional
#       The speech rate (speed). Allows values: from -10 (slowest speed) up 
#       to 10 (fastest speed). Default value: 0 (normal speed).
#   c - Optional
#       The speech audio codec. Allows values: see Audio Codecs. 
#       Default value: WAV.
#   f -  Optional
#       The speech audio formats. Allows values: see Audio Formats. 
#       Default value: 8khz_8bit_mono.
#   ssml - Optional
#      The SSML textual content format (see SSML documentation). 
#       Allows values: true and false. Default value: false.
#   b64 - Optional
#       Defines output as a Base64 string format (for an internet browser playing)
#       Allows values: true and false. Default value: false.
#
def voicerss_tts(text_in, config):
    
    # Enable/Disable debug
    DEBUG = 0
 
    print(" Using Voice RSS TTS service")

    # Set SSML true/false
    if( config['VOICERSS']['input_format'] == 'ssml' ):
        is_ssml = 'true'
    else:
        is_ssml = 'false'

    # Arguments to send to server
    VOICE_in            = config['VOICERSS']['voice']
    LOCALE_in           = config['VOICERSS']['locale']
    AUDIO_FORMAT_in     = config['VOICERSS']['audio_format']
    AUDIO_SETTINGS_in   = config['VOICERSS']['audio_settings']
    INPUT_FORMAT_in     = config['VOICERSS']['input_format']
    KEY_in              = config['VOICERSS']['key']

    # codec/format (needs capitalized)
    AUDIO_FORMAT_in = AUDIO_FORMAT_in.capitalize()

    # Create the url
    url_sans_text = "http://api.voicerss.org/?key=" + KEY_in + "&hl=" + LOCALE_in + "&c=" + AUDIO_FORMAT_in + "&f=" + AUDIO_SETTINGS_in + "&src=" 
    url = url_sans_text + text_in

    # Debug stuff
    if DEBUG:
        print(VOICE_in, LOCALE_in, AUDIO_FORMAT_in, AUDIO_SETTINGS_in, INPUT_FORMAT_in, KEY_in)
        print(text_in)
        print(url)


    # Send request to server
    try:
        response = requests.get(url) 
    except:
        # requests module failed
        print('Error: tts conversion request failed')
        print("URL (without text): " + url_sans_text)
        exit(1)

    # Check for errors
    if( re.search('ERROR', response.text, re.IGNORECASE) ):
        print("Error response text: " + response.text)
        print("URL (without text): " + url_sans_text)
        exit(1)
    elif( int(response.status_code) >= 400 ):
        print("Error: HTTP response status code: " + str(response.status_code))
        print("Error response text: " + response.text)
        print("URL (without text): " + url_sans_text)
        exit(1)

    # Success
    if DEBUG: print('Convertion success.')


    # return response (audio out, binary)
    return response.content 
# End: voicerss_tts()

