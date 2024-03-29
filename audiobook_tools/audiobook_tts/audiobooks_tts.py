#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W


###########################################################################
#
# Audiobook TTS (text to speech) - 
#
#   Description:
#       Interface to online and locally installed tts services to convert txt/ssml file to mp3 file
#
#   Author: Zef the Tinker
#
#   Date: 2022 07
#
#   License: GPLv3
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
#       -abreviations are prononced fully, sometimes incorrectly
#           ie. Miss is pronounced as Missisipi for voicerss
#
#   Non-featurs:
#       -no inteligent checks to see if settings are valid for tts service
#           ie invalid voices
#       -no ssml error checking (maybe use bs4)
#
#   Cloud/Online TTS services
#
#       VoiceRSS
#           http://www.voicerss.org/api/ 
#       Google Cloud Text-to=Speech (not implimented yet)
#           Install: pip install google-cloud-texttospeech
#           https://googleapis.dev/python/texttospeech/latest/index.html
#       Google translate tts (not cloud):
#           https://pypi.org/project/gTTS/
#           install:  pip install gTTS
#       Amazon Polly: (not implimented yet)
#           Install: pip install boto3
#           import boto3
#       Microsoft Azure Text-to-Speech:
#           Install: pip install azure-cognitiveservices-speech
#
#   Offline/Local applications
#       pyttsx3 (not implimented):
#           Install: pip install pyttsx3
#       mimic3 (not implimented):
#       Coqui TTS:
#           install: pip install TTS
#           notes: doesn't support SSML
#           https://github.com/thorstenMueller/Thorsten-Voice/issues/22
#   Requirments:
#       - python3
#       - "appdirs" module; Install: pip install appdirs
#       - "configparser" module; Install: pip install configparser
#       - "requests" module; Install: pip install requests
#       - modules for specific services, see above
#
#   TODO:
#       fix config priority
#       fix voicerss call
#       check if profiles actually work
#       add post retries
#
############################################################################





############################################################################
# Configure
# 
#  global DEBUG
#  global TEST

#DEBUG=1
#TEST=0

# number of char to send to service (smaller has less errors)
#  POST_CHAR_LIMIT = 1500






#############################################################################
# Code
#

# API selector
#from APIs.api_select import tts_conversion

# debug
import pprint


# tts
#  import voicerss_tts

# system stuff
import os
import sys

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
# try:
#     from appdirs import *
# except:
#     print("Error: module 'appdirs' not installed")
#     print("Install: pip install appdirs")
#     exit(1)
# try:
#     import configparser
#     config_file = configparser.ConfigParser()
# except:
#     print("Error: module 'configparser' not installed")
#     print("Install: pip install configparser")
#     # exit(1)

# web grab
try:
    import requests
except:
    print("Error: module 'requests' not installed")
    print("Install: pip install requests")
    exit(1)

# load external file for APIs
#  from tts_service_APIs import *






#################################################
# Parse Arguments
#
def parse_args():
    """
    CLI Arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('EBOOK', nargs='+', type=str, help='ebook txt file')
    # only mp3s are supported currently
    parser.add_argument('--bitrate', type=str, help='audio encoding bitrate', choices=["32k","48k","64k","96k","128k","196k"])
    parser.add_argument('--samplerate', type=str, help='audio encoding samplerate', choices=[16000,22050,44100,48000])
    parser.add_argument('--output-format', type=str, help='audio encoding format', choices=["mp3", "wav", "ogg", "m4b"])
    parser.add_argument('--input-format', type=str, help='format sent to TTS service', choices=["txt","ssml","json-txt","json-ssml"])
    parser.add_argument('--key', type=str, help='tts serices\'s key, auth code, auth file')
    parser.add_argument('--locale', type=str, help='example: en-us, en-au,')
    parser.add_argument('--voice', type=str, help='voice')
    parser.add_argument('--gender', type=str, help='')
    #  parser.add_argument('--url_parameters', type=str, help='this will be attached to url after question mark') # remove
    #  parser.add_argument('--audio_settings', type=str, help='')
    parser.add_argument('--tts-service', type=str, help='tts service to use. ie google_translate_tts, voicerss, google_cloud_tts(unimplemented), amazone_polly(unimplemented')
    #  parser.add_argument('--config-file', type=str, help='config file location')
    parser.add_argument('--profile', type=str, help='profile to use, set in config file')
    parser.add_argument('--debug', help='debug mode, more output', action="store_true")
    parser.add_argument('--remove-all-bad-chars', help=r'remove problematic charactors, that can change speech. [, ], (, ), *, /, \, "', action="store_true")
    parser.add_argument('--remove-bad-char', type=str, help=r'remove problematic charactors, that can change speech, comman seperated. b=brackets, q=double_quotes, p=parentheses, a=asterisks, s=forward/back_slashs. example --remove-bad-char="b,a,q"')
    parser.add_argument('--test', help='test mode, no writing data', action="store_true")
    #  parser.add_argument('--', type=str, help='', choices=[""], default="")

    parser.add_argument('--remove-non-ascii-chars', help='Removes non-ASCII charators, ie standard english chars only', action="store_true")
    parser.add_argument('--remove-non-latin1-chars', help='Removes non-latin1 charators. ie no Arabic/Chinese/Japanese/etc', action="store_true")
    #  parser.add_argument('-a', '--speak-asterisk', help='Speaks out asterisk[*] (off by default)', action="store_true")
    #  parser.add_argument('-q', '--dont-remove-quotes', help='Leave quotes in place and may or may not be spoken (off by default)', action="store_true")
    
    args = parser.parse_args()
    
    return args
#  End: parse_args 












#########################################################
# Get file list
#

def get_file_list(list_in):
    """
    get file list
    """
    file_list = []
    for filename in list_in:
        # Ignore binary files
        if filename == '': # ignore blanks
            continue
        elif not os.path.isfile(filename):
            print("Warning (file not found): ", filename)
            continue
        elif is_binary(filename) : #ignore binary files
            if DEBUG:
                print("  File", filename)
                print("     is binary, ignoring.")
            continue
        # add the file to list
        file_list.append(filename)

    return file_list
# End: get_file_list




#########################################################
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
# End: is_binary



########################################################
# Get total char count for all the files loaded
#   to display when your TTS service has char limit
def get_char_count_forall_files(file_list):
    """
    Get total char count for all the files loaded
    to display when your TTS service has char limit  
    """
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



#########################################################
# Open file
#
def open_text_file(filename):
    """
    Open a file
    """
    print("Converting filename:", filename)

    # Open file
    try:
        fin=open(filename, 'r')
    except:
        # failed but no need to exit
        print("Error: Could not open file!")

    text=fin.read()
    fin.close()

    return text # return the text



#########################################################
# Split text into chunks
#   to avoid errors in long conversions
#   and service char limits
#
def split_file_into_text_chunks(filename):
        """
        Split text into chunks
        to avoid errors in long conversions
        and service char limits
        """
        # read first line
        #  ebook_txt_line = fin.readline()

        # initialize
        total_char_cnt=0
        chunk_cnt=0
        char_cnt=0
        #  ebook_txt_chunks=[''] * 1000
        ebook_txt_chunks = [''] # one line array
        # Read books lines, seperates into chunks of text

        # read first line
        #  ebook_txt_line = fin.readline()
        content = open_text_file(filename).splitlines()
            
        # debug
        #if config['ARGS']['debug']:
        #    print("-------------------------------------------------")
        
        #print(content)
        #  process each line in file
        for ebook_txt_line in content:

            # Clean up text
            #  ebook_txt_line = clean_text(ebook_txt_line)
            #print(ebook_txt_line)
            # remove html tags if txt
            if( config['preferred']['input_format'] == 'txt'):
                ebook_txt_line = re.sub('<[^>]+>', '', ebook_txt_line)
            elif( config['preferred']['input_format'] == 'ssml'):
                #remove <speak> tags, will add later
                ebook_txt_line = re.sub(r'<\?speak>', '', ebook_txt_line)
                    

            #counts chars for post, splits into chunks, increment
            if (char_cnt + len(ebook_txt_line) ) >  float(config['preferred']['max_charactors']) * 0.95:
                if config['ARGS']['debug']:
                    print("  > chunk:",chunk_cnt,", char count:",char_cnt) 
                ebook_txt_chunks.append('')
                chunk_cnt = chunk_cnt + 1
                char_cnt = 0

            # increment current char cnt for chunk
            char_cnt = char_cnt + len(ebook_txt_line)
            total_char_cnt = total_char_cnt + len(ebook_txt_line)
            
            # add text to chunk (maybe add newline instead of just space
            ebook_txt_chunks[chunk_cnt] = ebook_txt_chunks[chunk_cnt] + " " + ebook_txt_line
            #read next line
            #  ebook_txt_line = fin.readline()


        # debug
        #if config['ARGS']['debug']:
        #    print("-------------------------------------------------")

        # close file
        #  fin.close()
        
        # clean the text for each chunk
        x = 0
        for chunk in ebook_txt_chunks:
            #print(chunk)
            from audiobook_tools.common.text_conversion import clean_text
            
            ebook_txt_chunks[x] = clean_text(chunk, config)
            x +=1

        # add <speak> tag to each chunk for ssml
        if(config['preferred']['input_format'] == 'ssml'):
            x=0
            for chunk in ebook_txt_chunks:
                ebook_txt_chunks[x] = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="string">\n' + chunk + "\n</speak>\n"
                x += 1

        return (ebook_txt_chunks, total_char_cnt, chunk_cnt)
# End: split_file_into_text_chunks(







#############################################################################
#   TTS Service Selection
#

def tts_api_selection(text):
    """
    Uses config file or args to select which servies is used
    Ex: google_translate_tts, google_cloud_tts, voicerss
    """
    import importlib
    
    api = config['preferred']['tts_service']
    api_module = 'APIs.' + api

    if DEBUG: print("using api", api)

    # load specific API module
    try:
        selected_api = importlib.import_module(api_module)
    except:
        print("Error: ", api, "(api) not found in folder 'APIs'")
        exit(1)

    # Call API to post text and get audio responce        
    tts_audio_output = selected_api.get_tts_audio(text, config, args)
    
    return tts_audio_output
# End: tts_service_selection()



################################################
# Process each chunk of text
#
def process_chunks(ebook_txt_chunks):
        """
        process the each chunk of text
        """


        # Send request to service
        cnt=0
        audio_data= b'' # binary
        tts_audio_data = b''

        for chunk in ebook_txt_chunks:
            #  print "************************************************"
            #  print chunk
            #  print "================================================"

            # if text empty or contains no alpha numeric char, skips
            if (not re.search('[a-zA-Z0-9]', chunk)): continue      

            cnt = cnt + 1
            #  print("         >Chunk:", cnt) # print a dot showing progress
            print(".", end="", flush=True)

            if DEBUG:
                filename_tmp = os.path.join(config['TMP']['tmp_dir'], str(cnt) 
                + ".txt")
                print(  "\nWriting tmp file:", filename_tmp)
                fp = open(filename_tmp, "w")
                fp.write(chunk)
                fp.close()
                #print("----------------File Chunk (begin)------------------")
                #print(chunk)
                #print("----------------File chunk (end)--------------------")

            # actually send the data
            if(not TEST):
                tts_audio_data = tts_api_selection(chunk)
                if DEBUG:
                    filename_tmp = os.path.join(config['TMP']['tmp_dir'], str(cnt) + ".mp3")
                    print(  "\nWriting tmp mp3 file:", filename_tmp)
                    fp = open(filename_tmp, "wb")
                    fp.write(tts_audio_data)
                    fp.close()
                    print("\nTTS Chunk size: " + str(sys.getsizeof(tts_audio_data)) + "bytes")
                # join the mp3 fragments together
                # temp mp3 file has errors, needs re-encode
                if sys.getsizeof(tts_audio_data) < 1000: # if the audio is 1kB 
                    print("Error: audio chunk is too small and is likely broken. Check file for errors.")

                audio_data = audio_data + tts_audio_data        
            else:
                # blank in test mode
                audio_data = b''

        print("") # prints new line
        
        if(DEBUG):
            print("Writing joined-audio tmp file:", filename_tmp)
            filename_tmp_audio = os.path.join(tmp_dir, 'joined-out.mp3')
            if(not TEST):
                f = open(filename_tmp_audio, 'wb')
                f.write(audio_data)
                f.close()
        
        #  Write TMP mp3 file of joined chunks 
        #   TODO: ideally i would keep this as binary str and pipe to ffmpeg
       
              
        # returns audio variable
        return audio_data
# End: process_chunks






###############################################
# FFMPEG: re-encode audio
#  
def ffmpeg_reencode(filename_orig, audio_data):
        """
        calls ffmpeg for reenconde
        merged audio chunks have 
        errors, need re-encode
        """

        # output filename
        filename_output_audio = config['OUTPUT']['filename']

        # ffmpeg command for re-encoding
        ffmpeg_cmd = ['ffmpeg',
                '-hide_banner',
                '-loglevel', 'error',
                '-y',
                '-i', '-']

        ffmpeg_cmd += ['-b:a', config['preferred']['bitrate'] ]
        ffmpeg_cmd += ['-ar', config['preferred']['samplerate'] ]

        if config['preferred']['output_format'] == 'ogg':
            ffmpeg_cmd += ['-c:a', 'libvorbis']

        ffmpeg_cmd += [filename_output_audio]

        if DEBUG:
            print("\tFFMPEG reencode command: ")
            pprint.pprint(ffmpeg_cmd)

        # Run ffmpeg command
        print("\tJoining audio chunks.")
        if(not TEST):
            #  proc = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
             # re-en
            #  ffmpeg_command = ['ffmpeg', '-i', '-'] + ['-f'] + ['mp3'] + ['pipe:']
            proc = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            ffmpeg_out, ffmpeg_stderr = proc.communicate(input=audio_data) # pipe wav info ffmpeg; outputs mp3 and stderr


            # print ffmpeg output
            #  ffmpeg_out = proc.communicate()
            if DEBUG: 
                #  print( ffmpeg_out)
                print("---------------------------ffmpeg joining chunks----------------------")
                print("--- notes on ffmpeg stderr, 'Heading missing.....Error while decoding stream.....Invalid data found....' is normal, and causes no problems")
                print('ffmpeg stderr: ' + str(ffmpeg_stderr))
                print("-------------------------ffmeg joining chunks (end)-------------------")

        print("\tOutput file: ", filename_output_audio)
# End: ffmpeg_reencode()







#######################################
# Process each file
#
def process_file(filename):
        """
        process file
        """

        # store the filename to variable
        config['INPUT']['filename'] = filename
        #  print(config['INPUT']['filename'])

        # FIXME current only supports mp3
        #  config['preferred']['format'] = 'mp3'

        # output filename (without invalid chars)
        config['OUTPUT']['filename'] = re.sub(r"\.....?$", ".", filename) + config['preferred']['output_format']
        config['OUTPUT']['filename'] = re.sub(r"[\?:\"\|\*\\><]", ".", config['OUTPUT']['filename'] ) # remove invalid chars

        #  print(config['OUTPUT']['filename'])
        # Run the python TTS module instead of online services
        #  if config['GENERAL']['tts_service'] == 'offline_tts':
            
            #  text = open_text_file(filename)
            # Set Output file name
            #  offline_tts(text, config, args)
            #  return
            
        # open file and split into text chunks
        (ebook_txt_chunks, total_char_cnt, chunk_cnt) = split_file_into_text_chunks(filename)

        # Sends chunks of text to audio and merging
        if(chunk_cnt == 0):
            chunk_cnt += 1
        print("\tProcessing:", str(total_char_cnt) , "chars, in", str(chunk_cnt), "chunks.", end="", flush=True)
        audio_data = process_chunks(ebook_txt_chunks)

        # re-encode broken audiofile
        ffmpeg_reencode(filename, audio_data)
# End: process_file()

   


########################################
# Clean up 
#
def clean_up():
    """
    Clean up temp files
    """
    #  if config['preferred']['debug']:
    #      print("Not deleting tmp folder", config['TMP']['tmp_dir'])
    #  else:
    #      print("Removing temp files")
    #      os.rmdir(config['TMP']['tmp_dir'])

    # TODO change to os module
    import shutil

    if DEBUG: print("Deleting tmp dir")
    if os.path.isdir(config['TMP']['tmp_dir']):
        shutil.rmtree(config['TMP']['tmp_dir'])

# End: clean_up())






#######################################
# Main funcion
#
def main():
    """
    Main function for online-tts.py
    """
    #  print("main")
    # Get CLI args
    # make args global for easy
    global args
    args = parse_args()

    # setup temp dir
    global tmp_dir
    tmp_dir = tempfile.mkdtemp() #tmp dir to store mp3 chunks

    # generate config settings
    global config
    from audiobook_tools.common.load_config import load_config
    config = load_config("audiobook-tts.conf", args, tmp_dir)

    # enable DEBUG (to be reimplemented)
    global DEBUG
    global TEST
    if config['preferred']['debug']:
        DEBUG = 1
    else:
        DEBUG = 0
    if config['preferred']['test']:
        TEST = 1
    else:
        TEST = 0


    # get list of files inputed
    file_list = get_file_list(args.EBOOK)
    
    print("Using TTS service:", config['preferred']['tts_service'])

    # Get total char count for all files
    # in case your service has limits
    print("Total of", get_char_count_forall_files(file_list) , "charactors in ", len(file_list), "file(s)")

    if DEBUG: print("   Temp folder: ", tmp_dir)

    # Run for each file inputed
    for filename in file_list:
        process_file(filename)
   

    # remove temp files
    clean_up()

    print("done.")
    exit()
    # End for each file
# End: main()


#################################
# Start it up
if __name__ == "__main__":
   main()
