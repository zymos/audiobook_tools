"""
########################################################################
#
#   MS Azure cloud TTS API
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
"""

###########################################################################
#
#   Microsoft Azure Text-to-Speech
#
###########################################################################
def get_tts_audio(text, config, args):
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

    import re # regex
    import pprint # debuging
    import requests # for sending request to server
    import time # for sleep
    import urllib.parse

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
    DEBUG = config['ARGS']['debug']

    # Modifying ssml file
    #   ssml requires voices set,
    #   and is the only place to alter speaking rate
    if input_format == 'txt' and not speaking_rate == "1.0":
        print("    Warning: MS Azure in TXT mode, does not support changes in speaking rate")

    # clean up ssml for errors and such
    # ms azure is very picky
    if input_format == 'ssml':
        try:
            from audiobook_tools.common.text_conversion import clean_ssml
        except:
            print("loading text_conversion failed")
        text = clean_ssml(text, voice, speaking_rate)

    #print(type(text))
    #  text = urllib.parse.quote(text)

    if DEBUG:
        print("000000000000000000 text to ms_azure 0000000000000000000000000000")
        print(text   )
        print("0000000000000000 text to ms azure end 0000000000000000000")
#  <prosody pitch="value" contour="value" range="value" rate="value" duration="value" volume="value"></prosody>

    #exit()
    #  text = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="string"><voice name="en-US-AriaRUS"><prosody rate="1.0">Hello, my name is poop.</prosody></voice></speak>'

    # server stuff
    speech_config = speechsdk.SpeechConfig(subscription=key, region=server_region)
    # voice
    speech_config.speech_synthesis_voice_name = voice
    # audio settings
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat[audio_settings])

    speech_config.set_property_by_name("SpeechServiceResponse_Synthesis_WordBoundaryEnabled", "false")

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
