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


#  from online_tty import *
import re # regex
import pprint # debuging
import requests # for sending request to server
import time # for sleep

#############################################################################
#   TTS Service Selection
#

def tts_service_selection(text, config, args):
    """
    Uses config file or args to select which servies is used
    Ex: google_translate_tts, google_cloud_tts, voicerss
    """
    #  pprint.pprint(config)

    if( config['preferred']['tts_service'] == 'voicerss' ):
        response = voicerss_tts(text, config, args);
    elif( config['preferred']['tts_service'] == 'google_translate_tts' ):
         response = google_translate_tts(text, config, args)    
    elif( config['preferred']['tts_service'] == 'offine_tts' ):
         response = offine_tts(text, config, args)    
    elif( config['preferred']['tts_service'] == 'ms_azure_tts' ):
         response = ms_azure_tts(text, config, args)    



    # elif( config['GENERAL']['tts_service'] == 'example_tts' ):
    #   response = example_tts(text, config, args)    
    else:
        print("TTS service incorrectly set")
        exit(1)

    return response
# End: tts_service_selection()


##########################################################################
# 
# Local
#
#########################################################################
#  def offline_tts(text, config, args):

    #  # not working

    #  #  filename_output_audio = re.sub("\.....?", "." + args.format, filename)
    #  filename = config['INPUT']['filename']
    #  file_out = config['OUTPUT']['filename']

    #  print("Filename:", filename)
    #  print("Filename out:", file_out)

    #  # Open file
    #  try:
        #  fin=open(filename, 'r')
    #  except:
        #  # failed but no need to exit
        #  print("Error: Could not open file!")
        #  return

    #  text=fin.read()
    #  fin.close()

    #  import pyttsx3
    #  engine = pyttsx3.init() # object creation
    #  import traceback

    #  #  print(text)
    #  try:
        #  engine.save_to_file(text, file_out)
    #  except:
        #  traceback.print_exc()

    #  engine.runAndWait()

    #  return b"" # makes it the same format as all the others



###########################################################################
#
#   Microsoft Azure Text-to-Speech
#
###########################################################################
def ms_azure_tts(text, config, args):
    """
    Install: pip install azure-cognitiveservices-speech

    List of voices/locale
 	https://docs.microsoft.com/azure/cognitive-services/speech-service/language-support

    Other settings:
 	https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/rest-text-to-speech

    server_region = westus
    voice = en-US-AriaRUS
    key =
    locale = Female
    audio_settings = audio-16khz-64kbitrate-mono-mp3
    gender = en-US
    id = ???????????
    """
    


    # import ms azure tts api
    try:
        import azure.cognitiveservices.speech as speechsdk
    except ImportError:
        print("""
        Importing the Speech SDK for Python failed.
        azure.cognitiveservices.
        Install: pip install azure-cognitiveservices-speech
        """)
        import sys
        sys.exit(1)


    #  print(text)
    #  print("00000000000000000000000000000000000000000000000000000000000")

    # alter text
    #   change rate
    #   <prosody rate="+30.00%"></prosody> or decimal
    input_format    = config['preferred']['input_format']
    voice           = config['preferred']['voice']
    key             = config['preferred']['key']
    server_region   = config['ms_azure_tts']['server_region']
    #  https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechsynthesisoutputformat?view=azure-python
    audio_settings  = config['preferred']['audio_settings']
    speaking_rate   = config['preferred']['speaking_rate']

    # Modifying ssml file 
    #   ssml requires voices set, 
    #   and is the only place to alter speaking rate
    if input_format == 'txt' && not speaking_rate == "1.0":
        print("    Warning: MS Azure in TXT mode, does not support changes in speaking rate")
    elif input_format = 'ssml':
        # SSML, adding basic tags if needed
        # remove <speak> tags, will add later
        text = re.sub('<\/?speak[^>]+>', '', text)
        text = re.sub('<\/speak>', '', text)
        text = text.strip()

        # add <prosody ...> tag if needed, otherwise assume corrent
        if not re.search('<prosody ', text):
            print("    Adding <prosody> tag.")
            text = '<prosody rate="' + speaking_rate + '">' + text + '</prosody>'
        
        # add <voice ...> tag if needed, otherwise assume corrent
        if not re.search('<voice ', text):
            print("    Adding <voice> tag")
            text = '<voice name="' + voice + '">' + text + '</voice>'

        # adding the <speak> tag
        text = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="string">' + text + '</speak>'

#  <prosody pitch="value" contour="value" range="value" rate="value" duration="value" volume="value"></prosody>

    #  print(text)
    #  exit()
    #  text = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="string"><voice name="en-US-AriaRUS"><prosody rate="1.0">Hello, my name is poop.</prosody></voice></speak>'

    # server stuff
    speech_config = speechsdk.SpeechConfig(subscription=key, region=server_region)
    # voice
    speech_config.speech_synthesis_voice_name = voice
    # audio settings
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat[audio_settings])
    
    speech_config.set_property_by_name("SpeechServiceResponse_Synthesis_WordBoundaryEnabled", "false");

    # sets config and audio output
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # get audio response for input=txt/ssml
    if input_format == 'ssml':
        result = speech_synthesizer.speak_ssml_async(text).get()
    else:
        result = speech_synthesizer.speak_text_async(text).get()
    
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        if config['DEBUG']['debug']: print("Success: Speech synthesis")
        #  stream = speechsdk.AudioDataStream(result)
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Error: Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error: MS Azure TTS Error details: {}".format(cancellation_details.error_details))
            exit(1)

    # response to bytes data
    audio_data = result.audio_data

    # close up everything
    del result
    del speech_synthesizer

    return audio_data
# End: ms_azure_tts()




###########################################################################
#
#   VoiceRSS API
#
###########################################################################
def voicerss_tts(text_in, config, args):
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

    # Enable/Disable debug
    DEBUG = config['DEBUG']['debug']


    ###############
    # get prefered parameters
    VOICE_in = config['preferred']['voice']
    LOCALE_in = config['preferred']['locale']
    AUDIO_FORMAT_in = config['preferred']['audio_format']
    AUDIO_SETTINGS_in = config['preferred']['audio_settings']
    INPUT_FORMAT_in = config['preferred']['input_format']
    KEY_in = config['preferred']['key']
    URL_PARAMETERS = config['preferred']['url_parameters']


    ######################
    # alterations required by voicerss

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
    audio = basic_url_request(url)

    return audio
# End: voicerss_tts()






########################################################################
# Google Translate TTS
#
def google_translate_tts(text, config, args):
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



#####################################
# Function for general url requests
#
def basic_url_request(url):
    """
    Input: full url with all paramerters and text
    Output: audio data (byte)


    TODO seperate para, headers
    """
    

    trys = 1
    # try a couple of times
    while 1:
        # Send request to server
        set = 0
        try:
            response = requests.get(url) 
        except:
            # requests module failed
            print('Error: tts conversion request failed')
            #  print("URL (without text): " + url_sans_text)
            print("Trying again(" + str(trys) + ")")
            set = 1
            trys += 1

        # Check for errors
        if( re.search('ERROR', response.text, re.IGNORECASE) ):
            print("Error response text: ")
            print("  ", response.text)
            print("URL (without text): " + url)
            print("Trying again(" + str(trys) + ")")
            set = 1
            trys += 1
        elif( int(response.status_code) >= 400 ):
            print("Error: HTTP response status code: "+str(response.status_code))
            print("Error response code:",  response.status_code)
            #  print( response.text)
            #  print("URL (without text): " + url_sans_text)
            print("Trying again(" + str(trys) + ")")
            set = 1
            trys += 1

        # everything is ok
        if not set:
            break

        # Give up after 3 tries, and exit
        if trys >= int(config['preferred']['max_retries']) + 1:
            print("Conversion failed, exiting.")
            exit(1)

        time.sleep(config['preferred']['delay_between_requests']) # dont clobber
    # End of try loop


    # return response (audio out, binary)
    return response.content 
# End: basic_url_request()
