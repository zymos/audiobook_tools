#!/usr/bin/env python3
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
#       -abreviations are prononced fully, sometimes incorrectly
#           ie. Miss is pronounced as Missisipi for voicerss
#
#   Non-featurs:
#       -no inteligent checks to see if settings are valid for tts service
#           ie invalid voices
#       -no ssml error checking
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
#      Offline
#           local (offline) (not implimented):
#           Install: pip install pyttsx3
#
#   Requirments:
#       python3
#       "appdirs" module
#            Install: pip install appdirs
#       "configparser" module
#           Install: pip install configparser
#       "requests" module
#           Install: pip install requests
#       modules for specific services, see above
#
#   TODO:
#       fix config priority
#       fix voicerss call
#       check if profiles actually work
#
############################################################################


############################################################################
# Configure
# 
#  global DEBUG
#  global TEST

DEBUG=1
TEST=0

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
try:
    from appdirs import *
except:
    print("Error: module 'appdirs' not installed")
    print("Install: pip install appdirs")
    exit(1)
try:
    import configparser
    config_file = configparser.ConfigParser()
except:
    print("Error: module 'configparser' not installed")
    print("Install: pip install configparser")
    exit(1)

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
# CLI Arguments
#
def parse_args():
    """
    CLI Arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('EBOOK', nargs='+', type=str, help='ebook txt file')
    parser.add_argument('--bitrate', type=str, help='audio encoding bitrate', choices=["32k","48k","64k","96k","128k","196k"], default="64k")
    parser.add_argument('--samplerate', type=str, help='audio encoding samplerate', choices=[16000,22050,44100,48000], default="22050")
    parser.add_argument('--format', type=str, help='audio encoding format', choices=["mp3", "wav", "ogg"], default="mp3")
    parser.add_argument('--input-format', type=str, help='format sent to TTS service', choices=["txt","ssml","json-txt","json-ssml"])
    parser.add_argument('--key', type=str, help='key, auth code, auth file')
    parser.add_argument('--locale', type=str, help='example: en-us, en-au,')
    parser.add_argument('--voice', type=str, help='voice')
    parser.add_argument('--gender', type=str, help='')
    parser.add_argument('--url_parameters', type=str, help='this will be attached to url after question mark')
    parser.add_argument('--audio_settings', type=str, help='')
    parser.add_argument('--gtts-lang', type=str, help='language for google-translate-tts')
    parser.add_argument('--gtts-tld', type=str, help='top-level-domain for google-tanslate-tts accents')
    parser.add_argument('--tts-service', type=str, help='tts service to use. ie google_translate_tts, voicerss, google_cloud_tts(unimplemented), amazone_polly(unimplemented')
    #  parser.add_argument('--config-file', type=str, help='config file location')
    parser.add_argument('--profile', type=str, help='profile to use, set in config file')
    parser.add_argument('--dont_remove_asterisk', help='Some TTS servers speak out "asterisk", by default they are removed', action="store_true")
    parser.add_argument('--dont_remove_quotes', help='Some TTS servers speak out "quote", by default they are removed', action="store_true")
    #  parser.add_argument('--', type=str, help='', choices=[""], default="")

    #  parser.add_argument('-a', '--speak-asterisk', help='Speaks out asterisk[*] (off by default)', action="store_true")
    #  parser.add_argument('-q', '--dont-remove-quotes', help='Leave quotes in place and may or may not be spoken (off by default)', action="store_true")
    
    args = parser.parse_args()
    
    return args
#  End: parse_args 







##################################################
# Config file
#
def load_config():
    """
    Get config file location
    priority is [CLI args] - > [local config] -> [default config]
    """

    global config
    config = {}

    # set app name and gets config location
    appname = "audiobook-tools"
    appauthor = "audiobook-tools"
    config_file = os.path.join(user_config_dir(appname, appauthor), "online-tts.conf")
    default_config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "online-tts.conf")
 
    # read config file
    cfg_found = 0
    cfg_default_found = 0
    if os.path.isfile(config_file):  
        print("Local config file:", config_file)
        cfg = configparser.ConfigParser()
        cfg.read(config_file)
        cfg_found = 1
    if os.path.isfile(default_config_file):
        print("Default config file:", default_config_file)
        cfg_default = configparser.ConfigParser()
        cfg_default.read(default_config_file)
        cfg_default_found = 1
    if cfg_found == 0 and cfg_default_found == 0:
        print("Config file not found.")
        print(" Not:", config_file)
        print(" Not:", default_config_file)
        exit(1)


    # create dictionary (from default config)
    config = {s:dict(cfg_default.items(s)) for s in cfg_default.sections()}  

    # overwrite config var's defaults using local config
    if cfg_found:
        for s in cfg.sections():
            for op in cfg.items(s):
                print(s, " --- ", op[0], " === ", op[1])
                print(type(s), " --- ", type(op[0]), " === ", type(op[1]))
                #config[s][op[0]] = op[1]
    #config = {s:dict(cfg.items(s)) for s in cfg.sections()}
    exit()
    # TODO FIX check is setting in config exists befor setting see above
    # Add args to config var for conveonce of a single var
    config.update({'ARGS': {'set': 1}})
    for setting in vars(args):
        print(vars(args)[setting])
        #config['ARGS'].update(setting:vars(args)[setting])

    # Set Prefered settings

    #  Overrides via commandline
    #  voice
    #  config.update({'preferred':{'voice': ''}})
    #  if( args.voice ):
        #  config['preferred']['voice'] = args.voice
    #  elif config[config['GENERAL']['tts_service']].get('voice') is not None:
        #  config['preferred']['voice'] = config[config['GENERAL']['tts_service']]['voice'] 

    #print(config[config['GENERAL']['tts_service']])
    if config.get(config['GENERAL']['tts_service']) is None :
        print("Error: tts serivce \"" + config['GENERAL']['tts_service'] + 
        "\" is set in config, yet the section does not exist.  Fix the [GENERAL] \"tts_service\" setting, or add a new section named \"" +
        config['GENERAL']['tts_service'] , "\" an create a file in 'APIs' folder named \"" + config['GENERAL']['tts_service'] + ".py\"")
        exit(1)

    ####################
    # Preferred Settings
    
    # create the 'preferred' key
    config.update({'preferred':{'preferrences': 1}})

    # TTS Service
    if args.profile :
        if config[args.profile].get('tts_service') is not None:
            config['preferred']['tts_service'] = config[args.profile]['tts_service']
        else:
            config['preferred']['tts_service'] =  config['GENERAL']['tts_service']
    else:
        config['preferred']['tts_service'] =  config['GENERAL']['tts_service']


    # Preferred vars 
    # if DEBUG: print("pref vars")
    preferred_vars = ('voice', 'profile', 'locale', 'gender', 'key', 'input_format', 'audio_format', 'audio_settings', 'gtts_lang', 'gtts_tld', 'url_parameters', 'delay_between_requests', 'max_charactors','speaking_rate')
    # go through each setting
    for setting in preferred_vars:
        config['preferred'].update({setting: ''}) 
        if DEBUG: print("Config settings:", setting)
        if setting in vars(args).keys(): # var exists
            if vars(args)[setting]: # var is set
                if DEBUG: print("vars",vars(args)[setting] )
                config['preferred'][setting] = vars(args)[setting]
            elif config[config['GENERAL']['tts_service']].get(setting) is not None:
                config['preferred'][setting] = config[config['GENERAL']['tts_service']][setting] 
        elif config[config['GENERAL']['tts_service']].get(setting) is not None:
            config['preferred'][setting] = config[config['GENERAL']['tts_service']][setting] 
            #  print("asdasdasdasda", setting)
    
    # set some hard defaults
    if config['preferred']['max_charactors'] == '':
        config['preferred']['max_charactors'] = 1000

    # Debugging and testing
    config.update({'DEBUG':{'debug': False}})
    config['DEBUG'].update({'test': False})
    if DEBUG:
        config['DEBUG']['debug'] = True
    if TEST:
        config['DEBUG']['test'] = True

    #  pprint.pprint(vars(args)[profile])
    #  if( args.key ):
        #  config.update({'OVERRIDE':{'key': args.key}}) 
    #  elif config[config['GENERAL']['tts_service']]['key']:
        #  config.update({'preferred':{'key': config[config['GENERAL']['tts_service']]['key']}}) 
    #  else:
        #  config.update({'preferred':{'key': ''}}) 
    # input format
    #  config['preferred'].update({'input_format': ''}) 
    #  if( args.input_format ):
        #  config['preferred']['input_format'] = args.input_format
    #  elif config[config['GENERAL']['tts_service']].get('input_format') is not None:
        #  config['preferred']['input_format'] = config[config['GENERAL']['tts_service']]['input_format'] 


    #  if( args.input_format ):
        #  config.update({'OVERRIDE':{'input_format': args.input_format}}) 
        #  #  config['OVERRIDE']['input_format'] = args.input_format
    #  # PROFILE
    #  if( args.profile ):
        #  config.update({'OVERRIDE':{'profile': args.profile}}) 
    #  # URL_PARAMETERS
    #  if( args.url_parameters ):
        #  config.update({'OVERRIDE':{'url_parameters': args.url_parameters}}) 

    # Places to store variables
    config.update({'INPUT':{'filename': ''}}) 
    config.update({'INPUT':{'text': ''}}) 
    config.update({'INPUT':{'text_ssml': ''}}) 
    config.update({'INPUT':{'text_chunk': ''}}) 
    config.update({'OUTPUT':{'filename': ''}}) 
    config.update({'TMP':{'tmp_dir': tmp_dir}})

    if DEBUG: 
        print("------------------------config------------------------")
        pprint.pprint(config)
        print("------------------------------------------------------")
    #  return config
# End load_config






#########################################################
# Get file list
#

def get_file_list(list_in):

    file_list = []
    for filename in list_in:
        # Ignore binary files
        if filename == '': # ignore blanks
            continue
        elif not os.path.isfile(filename):
            print("Warning (file not found): ", filename)
            continue
        elif( is_binary(filename) ): #ignore binary files
            print("  File is binary, ignoring.")
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
    print("  Filename:", filename)

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
        #if config['DEBUG']['debug']:
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
                ebook_txt_line = re.sub('<\?speak>', '', ebook_txt_line)
                    

            #counts chars for post, splits into chunks, increment
            if (char_cnt + len(ebook_txt_line) ) >  float(config['preferred']['max_charactors']) * 0.95:
                if config['DEBUG']['debug']:
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
        #if config['DEBUG']['debug']:
        #    print("-------------------------------------------------")

        # close file
        #  fin.close()
        
        # clean the text for each chunk
        x = 0
        for chunk in ebook_txt_chunks:
            #print(chunk)
            try:
                from audiobook_tools.common.text_conversion import clean_text
            except:
                print("error loading audiobook_tools python files")
            ebook_txt_chunks[x] = clean_text(chunk, args.dont_remove_asterisk, args.dont_remove_quotes, config['preferred']['input_format'])
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
    
    print("api", api)

    try:
        selected_api = importlib.import_module('audiobook_tools.APIs.' + api)
    except:
        print("Error: ", api, "(api) not found in folder 'APIs'")
        
    response = selected_api.get_tts_audio(text, config, args)

    #response = ''
    #  pprint.pprint(config)

    #if config['preferred']['tts_service'] == 'voicerss':
        #from APIs.voicerss_tts import voicerss_tts
        #response = voicerss_tts(text, config, args)
    #elif config['preferred']['tts_service'] == 'google_translate_tts':
        #from APIs.google_translate_tts import google_translate_tts
        #response = google_translate_tts(text, config, args)
    ##  elif( config['preferred']['tts_service'] == 'offine_tts' ):
        ##  from  import
        ##  response = offine_tts(text, config, args)
    #elif config['preferred']['tts_service'] == 'ms_azure_tts':
        #from APIs.ms_azure_tts import ms_azure_tts
        #response = ms_azure_tts(text, config, args)
    ## elif( config['GENERAL']['tts_service'] == 'example_tts' ):
    ##   from example_tts import example_tts
    ##   response = example_tts(text, config, args)
    #else:
        #print("TTS service incorrectly set")
        #exit(1)

    return response
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
        audio_data= b'' # bytes
        for chunk in ebook_txt_chunks:
            #  print "************************************************"
            #  print chunk
            #  print "================================================"

            # if text empty or contains no alpha numeric char, skips
            if (not re.search('[a-zA-Z0-9]', chunk)): continue      

            cnt = cnt + 1
            print("         >Chunk:", cnt) # print a dot showing progress

            # to avoid clobbering servers
            #  time.sleep(3) 

            if DEBUG:
                fp = open(os.path.join(config['TMP']['tmp_dir'], str(cnt) + ".txt"), "w")
                fp.write(chunk)
                fp.close()
                #print("----------------File Chunk (begin)------------------")
                #print(chunk)
                #print("----------------File chunk (end)--------------------")

            # actually send the data
            if(not TEST):
                response = tts_api_selection(chunk)

                # join the mp3 fragments together
                # temp mp3 file has errors, needs re-encode
                audio_data = audio_data + response        
            else:
                # blank in test mode
                audio_data = b''
        
        # Write TMP mp3 file of joined chunks
        filename_tmp_audio = os.path.join(tmp_dir, 'joined-out.mp3')
        if(not TEST):
            f = open(filename_tmp_audio, 'wb')
            f.write(audio_data)
            f.close()
        
        # returns filename for re-encoding
        return filename_tmp_audio
# End: process_chunks






###############################################
# FFMPEG: re-encode audio
#   merged audio chunks have 
#   errors, need re-encode
def ffmpeg_reencode(filename_orig, filename_tmp_audio):
        """
        calls ffmpeg for reenconde
        """

        # output filename
        filename_output_audio = config['OUTPUT']['filename']

        # ffmpeg command for re-encoding
        ffmpeg_cmd = ['ffmpeg',
                '-hide_banner',
                '-loglevel', 'error',
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
# Process each file
#
def process_file(filename):
        """
        process file
        """

        # store the filename to variable
        config['INPUT']['filename'] = filename

        # output filename (without invalid chars)
        config['OUTPUT']['filename'] = re.sub(r"\.....?$", "." + args.format, 
                re.sub(r"[\?:\"\|\*\\><]", ".",
                filename
                ) )

        # Run the python TTS module instead of online services
        #  if config['GENERAL']['tts_service'] == 'offline_tts':
            
            #  text = open_text_file(filename)
            # Set Output file name
            #  offline_tts(text, config, args)
            #  return
            
        # open file and split into text chunks
        (ebook_txt_chunks, total_char_cnt, chunk_cnt) = split_file_into_text_chunks(filename)

        # Sends chunks of text to audio and merging
        print("  Coverting to audio:", str(total_char_cnt) , " charators, seperated in", str(chunk_cnt), "chunks.")
        filename_tmp_audio = process_chunks(ebook_txt_chunks)

        # re-encode broken audiofile
        ffmpeg_reencode(filename, filename_tmp_audio)
# End: process_file()








#######################################
# Main funcion
#
def main():
    """
    Main function for online-tts.py
    """
    print("main")
    # Get CLI args
    # make args global for easy
    global args
    args = parse_args()

    # setup temp dir
    global tmp_dir
    tmp_dir = tempfile.mkdtemp() #tmp dir to store mp3 chunks

    # generate config settings
    load_config()

    # get list of files inputed
    file_list = get_file_list(args.EBOOK)
    
    print("Using TTS service:", config['GENERAL']['tts_service'])

    # Get total char count for all files
    # in case your service has limits
    print("Total of", get_char_count_forall_files(file_list) , "charactors in ", len(file_list), "file(s)")

    if DEBUG: print("   Temp folder: ", tmp_dir)

    # Run for each file inputed
    for filename in file_list:
        process_file(filename)
        
    print("done.")
    exit()
    # End for each file
# End: main()


#################################
# Start it up
if __name__ == "__main__":
   main()
