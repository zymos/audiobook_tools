# -*- coding: utf-8 -*-


###########################################################################
#   mimic3 TTS API
#
def get_tts_audio(text_in, config, args):

    """
    """
    from pathlib import Path
    import sys
    from shutil import which
    import subprocess

    # Enable/Disable debug
    DEBUG = config['DEBUG']['debug']

    # ensure mimic3 is installed
    if(not which('mimic3')):
       print('Error: mimic3 is not install.')
       exit

    VOICE_in = config['preferred']['voice']
    #  RATE = config['preferred']['read_rate']
    AUDIO_FORMAT_in = config['preferred']['audio_format']
    AUDIO_SETTINGS_in = config['preferred']['audio_settings']
    INPUT_FORMAT_in = config['preferred']['input_format']

    #  text = "this is a test"
    
    mimic3_command_param = []
    ffmpeg_command_param = []
    if(VOICE_in):
        mimic3_command_param += ["--voice"] + [VOICE_in]

    if(INPUT_FORMAT_in == 'ssml'):
        mimic3_command_param += ["--ssml"]

    if(AUDIO_FORMAT_in):
        ffmpeg_command_param += ['-format', AUDIO_FORMAT_in]
    else:
        ffmpeg_command_param += ['-format', 'mp3']


    #  if(RATE):
        #  command_param += " --lendth-scale " + RATE + " "

    mimic3_command = ["mimic3"] + mimic3_command_param
    #  mimic3_command = "ls"
    ffmpeg_command = ['ffmpeg', '-i', '-'] + ffmpeg_command_param
    ffmpeg_command += ['-']

    p1 = subprocess.Popen(mimic3_command + ['|'] + ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out = p1.communicate(input=text_in.encode())[0] # pipe in text to mimic3

    audio_out = out
    ###############
    # Debug stuff
    if DEBUG:
        print("-----------------------------------------------------------")
        print(" Using mimic3 TTS application")
        print(VOICE_in, AUDIO_FORMAT_in, AUDIO_SETTINGS_in)
        print("----------------------------TEXT---------------------------")
        print(text_in)
        print("------------------------Command---------------------------")
        print(mimic3_command)
        print(ffmpeg_command)
        print("----------------------------------------------------------")
    

    return audio_out
