#!/usr/bin/python2
# -*- coding: utf-8 -*-

###########################################################################
#
# Voice RSS text to speech - txt file to mp3 file
#
#   Author: Zef the Tinker
#   Date: 2021 03
#   License: GPLv3
#
# Notes:
#
#   Free subscription: 350 daily requests (100kb/request)
# 
#   Optimize:
#   ideally it would go
#   text -> text segments -> cloud tts -> mp3 segment strings -> 
#   concate mp3 string -> ffmpeg -> output valid single mp3 file
#
#   but im too stupid to figure out piping variables to ffmpeg, so it goes
#
#   Current Operation
#       text -> text segments -> cloud tts -> mp3 segment strings -> 
#       concate mp3 string -> temp mp3(saved with errors due to concate) ->
#       temp mp3 -> ffmpeg -> output valid single mp3 file
# 
#   Reference:
#       http://www.voicerss.org/api/ - API, Options - Voices/formats/etc
#
#
#   Bugs:
#       abreviations are prononced fully, sometimes incorrectly
#       Miss is pronounced as Missisipi
#
#
#   Cloud/Online TTS services
#
#       VoiceRSS
#           http://www.voicerss.org/api/ 
#       Google Cloud Text-to=Speech
#           pip install google-cloud-texttospeech
#           https://googleapis.dev/python/texttospeech/latest/index.html
#
#       Google translate tts (not cloud):
#           https://pypi.org/project/gTTS/
#           install:  pip install gTTS
#
#       Amazon Polly:
#           pip install boto3
#           import boto3
#
#   Offline
#       local (offline):
#           pip install pyttsx3

#
############################################################################



#######################################################
# Configure
# 

DEBUG=0
TEST=0


VOICE='Amy' # Amy, Mary, Linda ...
LOCALE='en-us' # locale must match voice
CHARACTOR_LIMIT=10000
POST_CHAR_LIMIT=1000 #max number of charators to send for each convertion
INPUT_FORMAT='txt'
TTS_FORMAT='mp3'
TTS_AUDIO_SETTINGS='16khz_16bit_stereo'




#######################################
# Code
#

# debug
import pprint

# tts
import voicerss_tts

# system stuff
import os

# command line args
import argparse

# temp file directory
import tempfile

#  import sys
import subprocess

# regex
import re

# for sleep
import time

# for loading config files
from appdirs import *
import configparser
#  from configparser import ConfigParser


config_file = configparser.ConfigParser()


######################################
# CLI Arguments
#
def parse_args():
    # CLI Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('EBOOK', nargs='+', type=str, help='ebook txt file')
    parser.add_argument('--bitrate', type=str, help='audio encoding bitrate', choices=["32k","48k","64k","96k","128k","196k"], default="64k")
    parser.add_argument('--samplerate', type=str, help='audio encoding samplerate', choices=[16000,22050,48000], default="22050")
    parser.add_argument('--format', type=str, help='audio encoding format', choices=["mp3", "wav", "ogg"], default="mp3")
    parser.add_argument('--input-format', type=str, help='format sent to TTS service', choices=["txt","ssml","json-txt","json-ssml"])
    parser.add_argument('--key', type=str, help='key, auth code, auth file')
    parser.add_argument('--locale', type=str, help='example: en-us, en-au,')
    parser.add_argument('--voice', type=str, help='voice')
    #  parser.add_argument('--', type=str, help='', choices=[""], default="")
    #  parser.add_argument('--', type=str, help='', choices=[""], default="")
    #  parser.add_argument('--', type=str, help='', choices=[""], default="")
    #  parser.add_argument('--', type=str, help='', choices=[""], default="")
    #  parser.add_argument('--', type=str, help='', choices=[""], default="")
    #  parser.add_argument('--', type=str, help='', choices=[""], default="")
    #  parser.add_argument('--', type=str, help='', choices=[""], default="")
    #  parser.add_argument('--', type=str, help='', choices=[""], default="")


# all ffmpeg vars should strings even numbers

#  parser.add_argument('-a', '--speak-asterisk', help='Speaks out asterisk[*] (off by default)', action="store_true")
#  parser.add_argument('-q', '--dont-remove-quotes', help='Leave quotes in place and may or may not be spoken (off by default)', action="store_true")
    args = parser.parse_args()
    
    return args








############################
# Config file
#
def load_config_file():
    

    # Format:
    #
    # [tt

    # Get config file location
    appname = "audiobook-tools"
    appauthor = "audiobook-tools"
    config_file = os.path.join(user_config_dir(appname, appauthor), "audiobook-tools.conf")

    #  print("Config file:", config_file)

    # read config file
    if os.path.isfile(config_file):  
        print("Config file:", config_file)
        cfg = configparser.ConfigParser()
        cfg.read(config_file)
    else:
        print("Config file not found.")
        exit()

    config = {}

    # service
    config['SERVICE'] = cfg['TTY_SERVICE']['SERVICE']
    
    # voice
    if( args.voice ):
        config['VOICE'] = args.voice
    elif( cfg['GENERAL']['VOICE'] ):
        config['VOICE'] = cfg['GENERAL']['VOICE']
    else:
        config['VOICE'] = VOICE

    # locale
    config['LOCALE'] = cfg['GENERAL']['LOCALE']
    config['KEY'] = cfg['GENERAL']['KEY']
    config['INPUT_FORMAT'] = cfg['GENERAL']['INPUT_FORMAT']
    config['AUDIO_FORMAT'] = cfg['GENERAL']['AUDIO_FORMAT']
    config['AUDIO_SETTINGS'] = cfg['GENERAL']['AUDIO_SETTINGS']
    #  config['VOICE'] = cfg['GENERAL']['voice']

    return config




#######################################
# Get file list
#

def get_file_list(list_in):

    file_list = []
    for filename in list_in:
        # Ignore binary files
        if( is_binary(filename) ):
            print("  File is binary, ignoring.")
            continue
        # add the file to list
        file_list.append(filename)

    return file_list
        


# Used to ignore all non-text files
def is_binary(filename):
    """ 
    Return true if the given filename appears to be binary.
    File is considered to be binary if it contains a NULL byte.
    FIXME: This approach incorrectly reports UTF-16 as binary.
    """
    with open(filename, 'rb') as f:
        for block in f:
            if b'\0' in block:
                return True
    return False



# Get total char count for all the files loaded
def get_char_count_forall_files(file_list):

    total_cnt = 0
    for filename in file_list:
        f = open(filename, 'r')
        #  txt = f.read()
        #  print(txt)
        cnt = len(f.read())
        total_cnt += cnt
        #  print(
        #  if DEBUG: print("Length: ", cnt)        
        f.close()

    return total_cnt





#######################################
# VoiceRSS
#


def voicerss(text_in, VOICE_in, LOCALE_in, AUDIO_FORMAT_in, AUDIO_SETTINGS_in, INPUT_FORMAT_in, KEY_in):
    
    print(VOICE_in, LOCALE_in, AUDIO_FORMAT_in, AUDIO_SETTINGS_in, INPUT_FORMAT_in, KEY_in)
    if( INPUT_FORMAT == 'ssml' ):
        is_ssml = 'true'
    else:
        is_ssml = 'false'

    voice = voicerss_tts.speech({
            'key': KEY_in,
            'hl': LOCALE_in,
            #  'v': VOICE_in,
            'src': text_in,
            #  'r': '0',
            #  'c': AUDIO_FORMAT_in,
            #  'f': AUDIO_SETTINGS_in,
            #  'ssml': is_ssml,
            #  'b64': 'false'
        })

    # check for error
    if voice['error']:
        print("Error by VoiceRSS detected while converting chunk")
        print("Error: " + voice['error'])
        exit(1)

    return voice['responce']


#######################################
# Main funcion
#
def main():

    global args
    # get inpout args
    args = parse_args()


    config = load_config_file()
    #  if(not TEST):
        #  print("setting:", TEST)
    #  else:
        #  print "no"
    #  exit()
    
    pprint.pprint(config)

    #####################
    # get the text
    #  print("Opening: " + os.path.abspath(args.EBOOK))

    # Initialize
    tmp_dir = tempfile.mkdtemp() #tmp dir to store mp3 chunks

    if DEBUG: print("Temp folder: ", tmp_dir)


    # get list of input files
    file_list = get_file_list(args.EBOOK)
    
    # Get total char count for all files, to check if you going to overwelm
    #  all_files_char_cnt = get_char_count_forall_files(file_list)
    print("Total of", get_char_count_forall_files(file_list) , "charactors in ", len(file_list))


    #  pprint.pprint(args.EBOOK)

    
    for filename in file_list:
    
        print("Filename:", filename)


        # Open file
        try:
            fin=open(filename, 'r')
        except:
            print("Error: Could not open file!")

        # read first line
        ebook_txt_line = fin.readline()

        total_char_cnt=0
        chunk_cnt=0
        char_cnt=0

        ebook_txt_chunks=[''] * 1000
        
        #  print(" bbbbb", len(ebook_txt_chunks))

        #while book has lines
        while ebook_txt_line:
            #  if DEBUG: 
                #  print("  >", filename)
                #  print("   >chunk count ", chunk_cnt, "; char_cnt: ", char_cnt)
            if char_cnt >  POST_CHAR_LIMIT: #counts chars for post, splits into chunks
                chunk_cnt = chunk_cnt + 1
                char_cnt = 0
            # increment current char cnt for chunk
            char_cnt = char_cnt + len(ebook_txt_line)
            total_char_cnt = total_char_cnt + len(ebook_txt_line)
            # add text to chunk
            ebook_txt_chunks[chunk_cnt] = ebook_txt_chunks[chunk_cnt] + ebook_txt_line
            #read next line
            ebook_txt_line = fin.readline()

        # close file
        fin.close()

        print("  Coverting to audio:", str(total_char_cnt) , " charators, seperated in", str(chunk_cnt + 1), "chunks.")
        #  print("  Converting text chunks to audio.")


        #####################
        # request the speech
        cnt=0
        mp3_data=''
        for chunk in ebook_txt_chunks:
            


           
            #  print "************************************************"
            #  print chunk
            #  print "================================================"
            if (not re.search('[a-zA-Z0-9]', chunk)): continue # if text empty or contains no alpha numeric char, skips
            # send the text to VoiceRSS and get mp3

            #  VOICE='Amy' # Amy, Mary, Linda ...
            #  LOCALE='en-us'
            #  KEY='f46e67af78d74976833caaaed05b9719'
            #  CHARACTOR_LIMIT=10000
            #  POST_CHAR_LIMIT=1000 #max number of charators to send for each convertion
            #  INPUT_FORMAT='SSML'
            #  TTS_FORMAT='mp3'
            #  TTS_AUDIO_SETTINGS='16khz_16bit_stereo'
            
            cnt = cnt + 1
            print("    >Chunk:", cnt) # print a dot showing progress
            time.sleep(1) # to avoid clobbering servers
      
# voicerss(text_in, voice, locale, audio_format, audio_settings, input_format, key):

            if(not TEST):
    
                response = voicerss(chunk, config['VOICE'], config['LOCALE'], config['AUDIO_FORMAT'], config['AUDIO_SETTINGS'], config['INPUT_FORMAT'], config['KEY']) 

                # join the mp3 fragments together
                mp3_data = mp3_data + response        # write mp3_data to file (temp mp3 file, needs re-encode)

          
            else:
                mp3_data = ''


        
        # Write TMP mp3 file
        tmp_mp3 = os.path.join(tmp_dir, 'joined-out.mp3')
        #  if DEBUG: print("writing ,", str(cnt) + '-joined-out.mp3')
        if(not TEST):
            f = open(tmp_mp3, 'w')
            f.write(mp3_data)
            f.close()


        # Set Output file name
        output_mp3_name = re.sub("\.....?", "." + args.format, filename)


        # ffmpeg command for re-encoding
        ffmpeg_cmd = ['ffmpeg',
                '-y',
                '-i', tmp_mp3,
                '-b:a', args.bitrate,
                '-ar', args.samplerate,
                output_mp3_name]

        if DEBUG:
            print " temp file: " + tmp_mp3
            pprint.pprint(ffmpeg_cmd)


        # Run ffmpeg command
        print("  Joining audio chunks.")
        if(not TEST):
            proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            # print ffmpeg output
            ffmpeg_out = proc.communicate()
            if DEBUG: print ffmpeg_out

        print("Output file: ", output_mp3_name)

        # Clean up
        #  ebook_txt_chunks.clear()

#  if res:
            #  print "Error: ffmpeg failed"
            #  print " -> " + ffmpeg_cmd
            #  exit(1)

#  try:
            #  except:
                #  print("Error: failure output file write, "  str(chunk) + 'out.mp3')
#  import subprocess
#  from subprocess import Popen, PIPE, STDOUT
#  cmd_out = ['ffmpeg',
                #  '-y',
                #  '-i', '-',
                #  'out.mp3']

#  proc = Popen([cmd_out], stdin=PIPE)
#  pipe.stdin.close()
#  (output, err) = p.communicate(input=mp3_data)
#  p_status = p.wait()
#  print "Command output: " + output

#  exit()
#  if(DEBUG):  
            #  pprint.pprint(voice['error'])
            #  print(type(voice['error']))

# check if failed
#  if(voice['error'] is None):
            #  print("success")
            #  print(voice['response'])
#  else:
            #  print("Error detected: " + voice['error'])
            #  exit(1)


####################
# Output the file




#################################
# Start it up
if __name__ == "__main__":
   main()
