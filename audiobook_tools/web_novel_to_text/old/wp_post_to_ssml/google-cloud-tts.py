#!/usr/bin/python


################################################################
# google-cloud-tts.sh
#
#   Author: ZyMOS
#   Date: 07/2019
#   License: GPLv3
#
#   Usage: google-cloud-tts.sh [TEXT_FILE]
#
#   Requirements:
#       ffmpeg
#       base64
#       Google Cloud SDK
#       Google Cloud account
#           Create Google Cloud Platform project
#           Enable the Cloud Text-to-Speech API
#           Set up authentication key, and download json file
#           Google Cloud Text-to-Speech: enabled
#           Google application credential json file
#
#   Useful links:
#       https://cloud.google.com/text-to-speech/
#       https://cloud.google.com/text-to-speech/docs/
#       https://cloud.google.com/text-to-speech/docs/quickstart-protocol
#       https://cloud.google.com/text-to-speech/quotas
#       https://cloud.google.com/text-to-speech/pricing
#
#   Notes:
#       Standard (non-WaveNet) voices < 4 million characters free
#       WaveNet voices < 1 million characters free
#       Max characters per request < 5,000; shorter requests give less errors
#       Characters per minute   150,000
#
#   Useful tools:
#       Calibre
#           ebook-convert zzzzzzz.epub zzzzzzz.txt
#
#
#   Bugs:
#       pronunciation check for isnt -> isn't 
#           Im



############################################################################

import os
import argparse
import re

############
# Configure
#

###############################
# Google credential json file
GOOGLE_APPLICATION_CREDENTIALS_DEFAULT="~/.auth/google.json"



###############################
# Voices
#   run the following command to find available voices
#       curl -H "Authorization: Bearer "$(gcloud auth application-default print-access-token) \
#       -H "Content-Type: application/json; charset=utf-8" \
#       "https://texttospeech.googleapis.com/v1/voices" > voices.txt
#
# All 3 variables required to match google's specific voice, comment out all voices not used
#
#   List of voices:
#       https://cloud.google.com/text-to-speech/docs/voices
#
#
# Wavenet voice (better, but more expensive, <1M free)


# Basic male voice
SPEACHVOICE_DEFAULT_MALE='en-US-Standard-B'


# Basic female voice
LANGUAGECODE_DEFAULT='en-US'
SPEACHVOICE_DEFAULT='en-US-Standard-C'
GENDER_DEFAULT='FEMALE'

# Best female voice
# LANGUAGECODE='en-US'
# SPEACHVOICE='en-US-Wavenet-F'
# GENDER='FEMALE'

SPEAKINGRATE='0.95' # 1 is default


####################
# MP3 info
BITRATE="32k"

###################
# Debuging
DELETETMPFILES=0

ME = os.environ['HOME']

GOOGLE_APPLICATION_CREDENTIALS=""




##########################################################################################
##########################################################################################
## Code
##

def get_args():
       parser = argparse.ArgumentParser()
       parser.add_argument('BOOKS', type=str, help='')
       parser.add_argument('--ssml', '-s', help='', action="store_true")
       parser.add_argument('--output', '-o', type=str, help='')

       parser.add_argument('--gender', type=str, help='')
       parser.add_argument('--voicename', type=str, help='')
       parser.add_argument('--google-auth-file', type=str, help='')
       args = parser.parse_args()
       return args




def usage_function():
    print("pooooooooooooo")




def error_check():


    global GOOGLE_APPLICATION_CREDENTIALS
    #  x = GOOGLE_APPLICATION_CREDENTIALS

    # google cred file not found
    if not os.path.isfile(GOOGLE_APPLICATION_CREDENTIALS):
        print("Error: Google Cloud credential file does not exist or is not set")
        print("Set json credential file's location to environment variable")
        print("export GOOGLE_APPLICATION_CREDENTIALS=[files_location]")
        print("or is located in " + GOOGLE_APPLICATION_CREDENTIALS_DEFAULT)
        print("See for details: https://console.cloud.google.com/apis/credentials")
        print()
        usage_function()
        exit(1)

    # ffmpeg not found
    if not which("ffmpeg"):
        print("ERROR ffmpeg is not installed")
        print("Without it, this script will break.")
        usage_function
        exit(1)

    #gcloud is not installed
    if not which("gcloud"):
        print("ERROR: gcloud was not installed")
        print("Without it, this script will break.")
        usage_function
        exit(1)
        

                # other requirements not found
                    # if ! [[ `which bash` || `which pwd` || `which readline` || `which dirname` || `which mktemp` || `which split` || `which type` || `which cut` || `which file` || `which grep` || `which base64` ]]; then
                      # print("ERROR: the following programs are required, they are usually preinstalled on")
                        # print("most systems.")
                          # print("Requirements: bash, pwd, readline, dirname, mktemp, split, type, cut, file, grep, base64, echo, sed")
                            # echo
                              # usage_function
                                # exit 1
                                # fi


    # Gender check
    # if SPEACHVOICE :
        # print("Error: voicename not set")
        # usage_function
        # exit(1)
    # else
        # if GENDER:
            # if ( GENDER == "male" or GENDER == "MALE" ):
 # GENDER="MALE"
     # elif [ $GENDER == "female" || $GENDER == "FEMALE" ];then
     # GENDER="FEMALE"
  # else
 # echo "Error: $GENDER is not a valid gender"
    # echo
     # usage_function
          # exit 1







def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None




def main():
    # Variables
    SYNTHTXT="synthesize-text.txt"
    SYNTHAUD="synthesize-aud.mp3"
    SPLITSIZE=1000
    global GOOGLE_APPLICATION_CREDENTIALS
        # create absolute path
    # if ! [[ "$BOOKNAME" = /* ]]; then
        # BOOKNAME="$(pwd)/$BOOKNAME"
        # fi

    # Current working directory
    CURRENT_WORKING_DIR=os.getcwd()

    # CLI args
    ARGS=get_args()

    # setting cred file
    if ARGS.google_auth_file:
        GOOGLE_APPLICATION_CREDENTIALS= os.path.abspath(ARGS.google_auth_file)
    else:
        HOME = os.environ['HOME']
        if re.match("~", GOOGLE_APPLICATION_CREDENTIALS_DEFAULT):
            GOOGLE_APPLICATION_CREDENTIALS= os.path.abspath(re.sub('~', HOME, GOOGLE_APPLICATION_CREDENTIALS_DEFAULT))
        else:
            print("Google Application credentials file not found.")
            exit(1)

    print(GOOGLE_APPLICATION_CREDENTIALS)

    # check for basic errors
    error_check();

#############################
#Start it up
if __name__ == "__main__":
       main()
