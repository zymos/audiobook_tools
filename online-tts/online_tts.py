#!/usr/bin/python
# -*- coding: utf-8 -*-

###########################################################################
#
# Online TTS (text to speech) - 
#
#   Description:
#       Interface to online tts servies to convert txt/ssml file to mp3 file
#
#   Author: Zef the Tinker
#
#   Date: 2021 03
#
#   License: GPLv3
#
#   Requirments:
#       python configparser
#
#   
#   Notes:
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



############################################################################
# Configure
# 

DEBUG=0
TEST=0

# number of char to send to service (smaller has less errors)
POST_CHAR_LIMIT = 1000


#############################################################################
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
config_file = configparser.ConfigParser()

# web grab
import requests

# load external file for APIs
from tts_service_APIs import *




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








##########################################
# Config file
#
def load_config():
    
    # Get config file location

    global config

    config = {}

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


    config = {s:dict(cfg.items(s)) for s in cfg.sections()}
    #  # voice
    #  if( args.voice ):
        #  config['VOICE'] = args.voice
    #  elif( cfg['GENERAL']['VOICE'] ):
        #  config['VOICE'] = cfg['GENERAL']['VOICE']
    #  else:
        #  config['VOICE'] = VOICE

    #  # locale
    #  config['LOCALE'] = cfg['GENERAL']['LOCALE']
    #  config['KEY'] = cfg['GENERAL']['KEY']
    #  config['INPUT_FORMAT'] = cfg['GENERAL']['INPUT_FORMAT']
    #  config['AUDIO_FORMAT'] = cfg['GENERAL']['AUDIO_FORMAT']
    #  config['AUDIO_SETTINGS'] = cfg['GENERAL']['AUDIO_SETTINGS']
    #  #  config['VOICE'] = cfg['GENERAL']['voice']

    #  return config
# End load_config






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
        

#######################################
#   Check if file is binary
#   
#       Used to ignore all non-text files
#       Usful when using wildcards in command line
#
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




###################################
# Get total char count for all the files loaded
#   to display when your TTS service has char limit
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
# End: get_char_count_forall_files




###################################
# Split text into chunks
#   to avoid errors in long conversions
#   and service char limits
#
# TO FIX: add <speak> tag to each txt chunk
def split_file_into_text_chunks(filename):
        print("Filename:", filename)
        # Open file
        try:
            fin=open(filename, 'r')
        except:
            # failed but no need to exit
            print("Error: Could not open file!")

        # read first line
        ebook_txt_line = fin.readline()

        # initialize
        total_char_cnt=0
        chunk_cnt=0
        char_cnt=0
        ebook_txt_chunks=[''] * 1000
        # Read books lines, seperates into chunks of text
        # read first line
        ebook_txt_line = fin.readline()
        while ebook_txt_line:
            #counts chars for post, splits into chunks
            if char_cnt >  POST_CHAR_LIMIT:
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
        return (ebook_txt_chunks, total_char_cnt, chunk_cnt)
# End: split_file_into_text_chunks(


################################
# Process each chunk of text
#
def process_chunks(ebook_txt_chunks):

        # setup temp dir
        tmp_dir = tempfile.mkdtemp() #tmp dir to store mp3 chunks
        if DEBUG: print("Temp folder: ", tmp_dir)


        # Send request to service
        cnt=0
        audio_data= b'' # bytes
        for chunk in ebook_txt_chunks:
            #  print "************************************************"
            #  print chunk
            #  print "================================================"

            # if text empty or contains no alpha numeric char, skips
            if (not re.search('[a-zA-Z0-9]', chunk)): continue      

            cnt = cnt + 1
            print("    >Chunk:", cnt) # print a dot showing progress

            # to avoid clobbering servers
            time.sleep(1) 

            # actually send the data
            if(not TEST):
                response = tts_service_selection(chunk, config)

                # join the mp3 fragments together
                # temp mp3 file has errors, needs re-encode
                audio_data = audio_data + response        
            else:
                # blank in test mode
                audio_data = ''
        
        # Write TMP mp3 file of joined chunks
        filename_tmp_audio = os.path.join(tmp_dir, 'joined-out.mp3')
        if(not TEST):
            f = open(filename_tmp_audio, 'wb')
            f.write(audio_data)
            f.close()
        
        # returns filename for re-encoding
        return filename_tmp_audio
# End: process_chunks




################################
# FFMPEG: re-encode audio
#   merged audio chunks have 
#   errors, need re-encode
def ffmpeg_reencode(filename_orig, filename_tmp_audio):

        # Set Output file name
        filename_output_audio = re.sub("\.....?", "." + args.format, filename_orig)

        # ffmpeg command for re-encoding
        ffmpeg_cmd = ['ffmpeg',
                '-y',
                '-i', filename_tmp_audio,
                '-b:a', args.bitrate,
                '-ar', args.samplerate,
                filename_output_audio]

        if DEBUG:
            print(" Temp audio file: " + filename_tmp_audio)
            pprint.pprint(ffmpeg_cmd)

        # Run ffmpeg command
        print("  Joining audio chunks.")
        if(not TEST):
            proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            # print ffmpeg output
            ffmpeg_out = proc.communicate()
            if DEBUG: print( ffmpeg_out)

        print("Output file: ", filename_output_audio)
# End: ffmpeg_reencode()





#######################################
# Main funcion
#
def main():

    # Get CLI args
    # make args global for easy
    global args
    args = parse_args()

    # generate config settings
    load_config()

    # get list of files inputed
    file_list = get_file_list(args.EBOOK)
    
    # Get total char count for all files
    # in case your service has limits
    print("Total of", get_char_count_forall_files(file_list) , "charactors in ", len(file_list), "file(s)")

    # Run for each file inputed
    for filename in file_list:
        
        # open file and split into text chunks
        (ebook_txt_chunks, total_char_cnt, chunk_cnt) = split_file_into_text_chunks(filename)

        # Sends chunks of text to audio and merging
        print("  Coverting to audio:", str(total_char_cnt) , " charators, seperated in", str(chunk_cnt + 1), "chunks.")
        filename_tmp_audio = process_chunks(ebook_txt_chunks)

        # re-encode broken audiofile
        ffmpeg_reencode(filename, filename_tmp_audio)

    # End for each file
# End: main()


#################################
# Start it up
if __name__ == "__main__":
   main()
