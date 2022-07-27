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
    AUDIO_FORMAT_in = config['preferred']['format'] # mp3
    AUDIO_SETTINGS_in = config['preferred']['audio_settings']
    INPUT_FORMAT_in = config['preferred']['input_format'] # txt/ssml

    #  text = "this is a test"
    
    mimic3_command_param = []
    ffmpeg_command_param = []
    if(VOICE_in):
        mimic3_command_param += ["--voice"] + [VOICE_in]

    if(INPUT_FORMAT_in == 'ssml'):
        mimic3_command_param += ["--ssml"]

    #  if(AUDIO_FORMAT_in):
        #  ffmpeg_format = AUDIO_FORMAT_in
    #  else:
        #  ffmpeg_format = 'mp3'


    #  if(RATE):
        #  mimic3_command_param += " --lendth-scale " + RATE + " "

    # set file format for ffmpeg to pipe currently only mp3 works
    ffmpeg_format = 'mp3'


    mimic3_command = ["mimic3"] + mimic3_command_param + ['-stdout']
    #  mimic3_command = "ls"
    ffmpeg_command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', '-'] + ['-f'] + [ffmpeg_format] + ['pipe:']
    #  ffmpeg_command = ['ffmpeg', '-i', '-'] + ffmpeg_command_param + ['xoxox.mp3']
    #  ffmpeg_command += ['-']
    #  f=open('pythonout.wav', 'w+b')
    p1 = subprocess.Popen(mimic3_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    mimic3_wav_out, mimic3_stderr = p1.communicate(input=text_in.encode()) # pipe in text to mimic3, outputs wav and stderr
    #  p1.wait()
    #  f.close()
    #  audio_out, _ = (ffmpeg
    #                  .input('pipe:', format='pcm_s16le', ac=1)
    #                  .output('-', format=ffmpeg_format)
    #                  .overwrite_output()
    #                  .run(capture_stdout=True)
    #  )
    #  f=open('pytest.mp3', 'w+b')
    p2 = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ffmpeg_mp3_out, ffmpeg_stderr = p2.communicate(input=mimic3_wav_out) # pipe wav info ffmpeg; outputs mp3 and stderr

    if DEBUG: 
        #  print( ffmpeg_out)
        print('ffmpeg stderr: ' +str(ffmpeg_stderr))

    #  p2.wait()
    #  f.close()
    #  p2 = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=10**8)
    #  ffmpeg_mp3_out = p2.communicate(input=mimic3_wav_out)[0]


    #  audio_out = p2.stdout
    audio_out = ffmpeg_mp3_out
    #  audio_out = b''


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
