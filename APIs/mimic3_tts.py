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
    #  import ffmpeg


    # Enable/Disable debug
    DEBUG = config['DEBUG']['debug']

    # ensure mimic3 is installed
    if(not which('mimic3')):
       print('Error: mimic3 is not install.')
       exit

    VOICE_in = config['preferred']['voice']
    #  RATE = config['preferred']['read_rate']
    #  AUDIO_FORMAT_in = config['preferred']['format'] # mp3
    AUDIO_SETTINGS_in = config['preferred']['audio_settings']
    INPUT_FORMAT_in = config['preferred']['input_format'] # txt/ssml
    READ_SPEED = config['preferred']['read_speed']
    #  text = "this is a test"
    

    # Create ffmpeg and mimic3 commands
    mimic3_command_param = []
    ffmpeg_command_param = []

    if(VOICE_in):
        mimic3_command_param += ["--voice"] + [VOICE_in]

    # set and correct ssml
    if(INPUT_FORMAT_in == 'ssml'):
        mimic3_command_param += ["--ssml"]
        try:
            from audiobook_tools.common.text_conversion import clean_ssml
        except:
            print("loading text_conversion failed")
        # clean ssml for errors
        text_in = clean_ssml(text_in, VOICE_in, READ_SPEED)


    #  if(AUDIO_FORMAT_in):
        #  ffmpeg_format = AUDIO_FORMAT_in
    #  else:
        #  ffmpeg_format = 'mp3'

    # change reading speed/rate
    if(READ_SPEED and not float(READ_SPEED) == 1 ):
        mimic3_command_param += ['--length-scale'] + [READ_SPEED]

    # set file format for ffmpeg to pipe currently only mp3 works
    ffmpeg_format = 'mp3' # keep mp3 format no matter what final format
    ffmpeg_bitrate = '128k' # overdo bitrate no matter what the final format

    # mimic3 command
    mimic3_command = ["mimic3"] + mimic3_command_param + ['--stdout']
    #  ffmpeg command
    ffmpeg_command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', '-']
    ffmpeg_command += ["-b:a", ffmpeg_bitrate]
    ffmpeg_command += ['-f', ffmpeg_format, 'pipe:']


    if DEBUG:
        print("[------------------------mimic3 API-------------------------]")
        print(" Using mimic3 TTS application")
        print(VOICE_in, READ_SPEED)
        print("-----------------------------TEXT----------------------------")
        print(text_in)
        print("--------------------------Commands---------------------------")
        print(mimic3_command)
        print(ffmpeg_command)


    # Execute mimic command, with stdout as mimic3_wav_out
    p1 = subprocess.Popen(mimic3_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    mimic3_wav_out, mimic3_stderr = p1.communicate(input=text_in.encode()) # pipe in text to mimic3, outputs wav and stderr

    #Execute ffmpeg with mimic3's stdout piped in and output to ffmpeg3_mp3_out
    p2 = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ffmpeg_mp3_out, ffmpeg_stderr = p2.communicate(input=mimic3_wav_out) # pipe wav info ffmpeg; outputs mp3 and stderr


    #  audio_out = p2.stdout
    #  audio_out = b''

    ###############
    # Debug stuff
    if DEBUG:
        print('----------stdout size (binary audio)-----------------------')
        print("mimic3: " + str(sys.getsizeof(mimic3_wav_out)) + " bytes")
        print("ffmpeg: " + str(sys.getsizeof(ffmpeg_mp3_out)) + " bytes")
        print("---------------------STDERR-------------------------------")
        print("---mimic3 STDERR---")
        print(str(mimic3_stderr))
        print("---FFMPEG STDERR---")
        print(str(ffmpeg_stderr))    
        print("-------------------mimic3 API (end)------------------------")
   
    return ffmpeg_mp3_out
