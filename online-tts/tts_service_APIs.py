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

def tts_service_selection(text, config, args):

    #  pprint.pprint(config)

    if( config['GENERAL']['tts_service'] == 'voicerss' ):
        response = voicerss_tts(text, config, args);
    elif( config['GENERAL']['tts_service'] == 'google_translate_tts' ):
         response = google_translate_tts(text, config, args)    
    elif( config['GENERAL']['tts_service'] == 'offine_tts' ):
         response = offine_tts(text, config, args)    



    # elif( config['GENERAL']['tts_service'] == 'example_tts' ):
    #   response = example_tts(text, config, args)    
    else:
        # Default
        #  print("Using default(local) service")
        response = offline_tts(text, config, args)
        #  response = ''

    return response
# End: tts_service_selection()


##########################################################################
# 
# Local
#
#########################################################################
def offline_tts(text, config, args):

    # not working

    #  filename_output_audio = re.sub("\.....?", "." + args.format, filename)
    filename = config['INPUT']['filename']
    file_out = config['OUTPUT']['filename']

    print("Filename:", filename)
    print("Filename out:", file_out)

    # Open file
    try:
        fin=open(filename, 'r')
    except:
        # failed but no need to exit
        print("Error: Could not open file!")
        return

    text=fin.read()
    fin.close()

    import pyttsx3
    engine = pyttsx3.init() # object creation
    import traceback

    #  print(text)
    try:
        engine.save_to_file(text, file_out)
    except:
        traceback.print_exc()

    engine.runAndWait()

    return b"" # makes it the same format as all the others




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
def voicerss_tts(text_in, config, args):
    
    # Enable/Disable debug
    DEBUG = 0

    if DEBUG: print(" Using Voice RSS TTS service")

    VOICE_in=''
    LOCALE_in=''
    AUDIO_FORMAT_in=''
    AUDIO_SETTINGS_in='' 
    INPUT_FORMAT_in=''
    KEY_in=''
    URL_PARAMETERS=''

    # Arguments to send to server
    # OVERRIDE is overridden from commandline args
    if args.voice:
        VOICE_in    = args.voice
    else:
        VOICE_in    = config['voicerss']['voice']

    if args.locale :
        LOCALE_in    = args.locale
    else:
        LOCALE_in   = config['voicerss']['locale']

    if args.format:
        AUDIO_FORMAT_in = args.format
    else:
        AUDIO_FORMAT_in = config['voicerss']['audio_format']

    if args.audio_settings:
        AUDIO_SETTINGS_in   = args.audio_settings
    else:
        AUDIO_SETTINGS_in   = config['voicerss']['audio_settings']

    if args.input_format:
        INPUT_FORMAT_in = args.input_format
    else:
        INPUT_FORMAT_in = config['voicerss']['input_format']

    if args.key:
        KEY_in  = args.key
    else:
        KEY_in  = config['voicerss']['key']

    if args.url_parameters:
        URL_PARAMETERS_in   = args.url_parameters


    # codec/format (needs capitalized)
    AUDIO_FORMAT_in = AUDIO_FORMAT_in.capitalize()

    # Set SSML true/false
    if( INPUT_FORMAT_in == 'ssml' ):
        is_ssml = 'true'
    else:
        is_ssml = 'false'



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






########################################################################
# Google Translate TTS
#
def google_translate_tts(text, config, args):
    # Parameters
    #   tl: language
    #   ie: txt encoding, ex. utf.8
    #   q:  text to translate
    # slow?
    # lang check?
    # unoffical
    # tld: top-level domain (adds accent) ex. com, ca, co.uk, com.au
    
    #  from gtts import gTTS
    from gtts import gTTS
    from io import BytesIO

 
        # OVERRIDE is overridden from commandline args


    DEBUG = 1

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


    if re.search('ssml', args.input_format, re.IGNORECASE):
        print("  Warning: Google Translate TTS does not support SSML, and will sound weird.")
    #  # Create the url
    #  url_sans_text = "https://translate.google." + TLD_in + "/translate_tts?ie=UTF-8&&tl=" + LANG_in + "&q=" 
    #  url = url_sans_text + text

    #  # Debug stuff
    #  if DEBUG:
        #  import pprint
        #  print(LANG_in, TLD_in, )
        #  print(gtts.lang.tts_langs())
        #  print(text)
        #  print(url)

    #  tts_audio = BytesIO()

    # process tts
    #  try:
    #  tts = gTTS('hello', lang=LANG_in, tld=TLD_in, slow=SLOW_in)
    #  tts.save('hello.mp3')
    #  except:
        #  print(infer_msg(tts))
 #  write to file object
    #  tts.write_to_fp(tts_audio)
    
    mp3_fp = BytesIO()

    tts = gTTS(text, lang=LANG_in, tld=TLD_in, slow=SLOW_in)

    tts.write_to_fp(mp3_fp)
    #  if DEBUG:
        #  print(type(mp3_fp))
        #  print(mp3_fp.getvalue())

           # convert to bytes
    #  response = tts_audio.read1()
#  print(tts_audio.read1())

        #  print(type(tts))

        #  print(type(response))
        #  pprint.pprint(response)
    
    # convert to bytes
    response = mp3_fp.getvalue()#tts_audio.read1()


    return response
    #tts_audio.read1()
    #  print(type(tts))



    #  # Send request to server
    #  try:
        #  response = requests.get(url) 
    #  except:
        #  # requests module failed
        #  print('Error: tts conversion request failed')
        #  print("URL (without text): " + url_sans_text)
        #  exit(1)

    #  # Check for errors
    #  if( re.search('ERROR', response.text, re.IGNORECASE) ):
        #  print("Error response text: " + response.text)
        #  print("URL (without text): " + url_sans_text)
        #  exit(1)
    #  elif( int(response.status_code) >= 400 ):
        #  print("Error: HTTP response status code: " + str(response.status_code))
        #  print("Error response text: " + response.text)
        #  print("URL (without text): " + url_sans_text)
        #  exit(1)

    #  # Success
    #  if DEBUG: print('Convertion success.')


    #  # return response (audio out, binary)
    #  return response.content 

    # creats a bytes file object to dump into


# End: google_translate_tts
