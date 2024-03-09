#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
#####################################################################
#
#   ==[[Audiobook Reencoder]]==
#
#       Description: Re-encode all audiofile in a directory, with some 
#           bells and whistles
# 
#       Usage: audiobook-reencoder [DIRECTORY]
#
#       Author: ZyMOS, 03/2020 - 01-2022
#       License: GPL3
#
#       Requirements:
#           programs: python, ffmpeg, ffprobe
#           python modules: mutigen, imghdr
#           unicode support for pretty output
#       Features: 
#           Encodes using ffmpeg
#           Accepts input: mp3, m4b, m4a, flac, ogg, opus, aax, mp4
#           Grabs audio files data using ffprobe, for re-encoding and embedding cover art
#           Split into chapters
#           Removes unneeded files (nfo/cue/m3u) (can be disabled)
#           Add genre="Audiobook" (can be disabled)
#           Normalize volume using R128 specs @ -17dB (can be disabled)
#           Adds Cover art:
#               Extracts cover art to cover.jpg (can be disabled)
#               Embeds cover art to each audiofile (can be disabled)
#               Skips if directory contains multiple different audiobooks
#               Can delete original image file, after embedding (not default)
#
#
#       How the program works:
#           Walk through each subdirectory in the main directory
#               Check if audio exists in each directory, and create list
#                   Work on getting cover art
#                       Check if filenames in directory are similar
#                           Check if image file exist, otherwise try to extract it
#                   Generate data on each audio file
#           Process files though list
#               re-encode if 
#                   original bitrate is higher or 
#                   changing format or
#                   force reencode
#
#                           
 TODO
    add input flac


>FFREPORT=file="/tmp/audiobook_reencode/audiobook_reencode-log-22y01m17d-16-03/ffmpeg_output/03 What the Hell Did I Just Read.mp3.0.log:level=40" ffmpeg -loglevel error -y -i "/mnt/green1tb/000TO_REECODE/BBB/What the Hell Did I Just Read - David Wong 03 MP3/03 What the Hell Did I Just Read.mp3" -c:a libmp3lame -b:a 64k -ar 22050  -id3v2_version 3 -write_id3v1 1 -metadata compatible_brands= -metadata minor_version= -metadata major_brand=  -filter:a loudnorm "/tmp/audiobook_reencode/37921071/What the Hell Did I Just Read - David Wong 03 MP3/What the Hell Did I Just Read - David Wong 03 MP3/91723684783363403 What the Hell Did I Just Read.mp3"
03:31:34:DEBUG: ffmpeg error:
>b'Incorrect BOM value\nError reading comment frame, skipped\n'

why does this fail
    ↳ 022 Michael-Scott Earle - Star Justice Book 12_ Red Nova - End Credits.mp3
Errors detected:22) [|] 
05:36:55:ERROR:       Error: Cover art is set, but file doesn't exist
05:36:55:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:38:00:ERROR:       Error: Cover art is set, but file doesn't exist
05:38:00:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:39:45:ERROR:       Error: Cover art is set, but file doesn't exist
05:39:45:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:41:27:ERROR:       Error: Cover art is set, but file doesn't exist
05:41:27:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:43:10:ERROR:       Error: Cover art is set, but file doesn't exist
05:43:10:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:44:56:ERROR:       Error: Cover art is set, but file doesn't exist
05:44:56:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:46:23:ERROR:       Error: Cover art is set, but file doesn't exist
05:46:23:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:47:32:ERROR:       Error: Cover art is set, but file doesn't exist
05:47:32:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:48:36:ERROR:       Error: Cover art is set, but file doesn't exist
05:48:36:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:50:16:ERROR:       Error: Cover art is set, but file doesn't exist
05:50:16:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:51:54:ERROR:       Error: Cover art is set, but file doesn't exist
05:51:54:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:53:55:ERROR:       Error: Cover art is set, but file doesn't exist
05:53:55:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:55:24:ERROR:       Error: Cover art is set, but file doesn't exist
05:55:24:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:57:37:ERROR:       Error: Cover art is set, but file doesn't exist
05:57:37:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:58:46:ERROR:       Error: Cover art is set, but file doesn't exist
05:58:46:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
05:59:47:ERROR:       Error: Cover art is set, but file doesn't exist
05:59:47:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
06:01:32:ERROR:       Error: Cover art is set, but file doesn't exist
06:01:32:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
06:03:05:ERROR:       Error: Cover art is set, but file doesn't exist
06:03:05:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
06:05:04:ERROR:       Error: Cover art is set, but file doesn't exist
06:05:04:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
06:06:57:ERROR:       Error: Cover art is set, but file doesn't exist
06:06:57:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
06:08:11:ERROR:       Error: Cover art is set, but file doesn't exist
06:08:11:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg
06:08:12:ERROR:       Error: Cover art is set, but file doesn't exist
06:08:12:ERROR:         Filename: /tmp/audiobook_reencode/24974965/Star_Justice_Book_12%3A_Red_Nova__Michael-Scott_Earle/9855428880718556.jpg


### Minor bugs
 * spinner doesn't disapear sometimes if next string is shorter than spinner string
        ↳ Cipher Hill 12.mp3-] 
        ↳ Cipher Hill 13.mp3\] 
        ↳ Cipher Hill 14.mp3-] 
        ↳ Cipher Hill 15.mp3/]
  ↳ 024.mp3of 30) [\] 
    ↳ 025.mp3of 30) [|] 
    ↳ 026.mp3of 30) [\] 
    ↳ 027.mp3of 30) [|] 
    ↳ 028.mp3of 30) [/] 
    ↳ 029.mp3of 30) [-] 
    ↳ 030.mp3of 30) [\] 
done.ing (30 of 30) [-] 
        maybe spinner function isnt stoped (after error?)


* printed list of encoded files doesn't match true file list

* Very slow: Collecting audiobook files info...


 * printed encoding number flips after error detected 
    flips from current file number to error files number
        maybe spinner function isnt stoped






#####################################################################
"""




###################################################################################################
# Global variables
#

# Defaults
bitrate_default = "64k"
samplerate_default = "22050"
version = "0.1"

# volume normalization integrated volume(I) dB
loudnorm_int_vol = "-17"

# Filename's similarity ratio in a directory, 
#   must be >= for cover art to be added
#   this is to prevent adding cover art to a dir with diff audiobooks
filename_similarity_cover_art_percentage = 85

#  max_threads = 7

encode_speed_ratio = 15

program_name =  "audiobook_reencoder(ffmpeg)-v" + version # + "+loudnorm"



files_complete = []
total_duration = 0
total_file_count = 0
###################################################################################################
# Includes
#
import argparse # CLI inputs
import os
import glob # searching file types
import re #regex
from difflib import SequenceMatcher # fuzzy matching of filenames
import tempfile # for logging
import logging # for logging
import datetime # for logging
import random # for creating random filename
import shutil
# import json imghdr mutegen
from audiobook_tools.common.load_config import load_config
from audiobook_tools.common.spinner import Spinner

import sys

import subprocess # running programs
import queue # multithreading
import threading # multithreading



# setup a timer for debuging
import time
start_time = time.time()


# debug tools
import pprint
#  import pretty_errors

###################################################################################################
# Functions
#




#####################################################
# CLI Arguments
#
def parse_args():
    """
    CLI Arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=str, help='directory to process')
    parser.add_argument('--disable-extract-cover-art', help="Don't extract cover art from audio file to cover.jpg", action="store_true")
    parser.add_argument('--disable-embed-cover-art', help="Don't add cover art", action="store_true")
    parser.add_argument('--only-extract-cover-art', help="Only extract cover art to cover.jpg, no reencoding", action="store_true")
    parser.add_argument('--disable-reencode', help="No reencoding", action="store_true")
    parser.add_argument('--only-reencode', help="Only reencode", action="store_true")
    parser.add_argument('--disable-split-chapters', help="Don't split chapters", action="store_true")
    parser.add_argument('--disable-delete-unneeded-files', help="don't deletes nfo/cue/m3u files", action="store_true")
    parser.add_argument('--only-delete-unneeded-files', help="Only delete nfo/cue/m3u file, no reencode", action="store_true")
    parser.add_argument('--disable-add-id3-genre', help="Don't set ID3 tag genre=Audiobook", action="store_true")
    parser.add_argument('--only-add-id3-genre', help="Don't re-encode, just add ID3 tag genre=Audiobook", action="store_true")
    parser.add_argument('--force-add-cover-art', help="Ignores filename similarity ratio to decide weather to add cover art", action="store_true")
    parser.add_argument('--delete-image-file-after-adding', help="Delete image file from directory after adding it to id3 as cover art (unimplimented)", action="store_true")
    parser.add_argument('--audio-output-format', help="m4b or mp3 (default mp3)")
    parser.add_argument('--bitrate', help="8k, 16k, 32k, 48k, 56k, 64k, 128k, etc (default 32k)")
    parser.add_argument('--samplerate', help="16000, 22050, 44100, etc (default 22050)")
    parser.add_argument('--threads', help="number of CPU threads to use (default 4)")
    parser.add_argument('--keep-original-files', help="do not delete original audio files", action="store_true")
    parser.add_argument('--test', help="run without any action, extraction or reencoding", action="store_true")
    parser.add_argument('--disable-normalize', help="do not normalize volume, faster encoding", action="store_true")
    parser.add_argument('--disable-add-id3-encoded-by', help="Don't set ID3 encoded_by=\"" + program_name + "\"", action="store_true")
    parser.add_argument('--ignore-errors', help="If there is an encoding failure, program will leave the file as is, and continue processing the rest of files", action="store_true")
    parser.add_argument('--disable-id3-change', help="Don't change ID3 tags", action="store_true")
    parser.add_argument('--force-normalization', help="Force re-encoder to normalize volume. By default, normalization is skipped if this encoder was likely run previously on file", action="store_true")
    parser.add_argument('--force-reencode', help="Force re-encoder, even if it seems to already be re-encoded previously", action="store_true")
    parser.add_argument('--delete-non-audio-files', help="Delete all non-audio files(not implemented yet)", action="store_true")
    parser.add_argument('--delete-non-audio-image-files', help="Delete all non-audio, or non-image files(not implemented yet)", action="store_true")
    parser.add_argument('--save-files-with-error', help="Keep encoded files, even if errors are detected", action="store_true")
    # parser.add_argument('--', help="", action="store_true")
    parser.add_argument('--debug', help="prints debug info", action="store_true")

    args = parser.parse_args()

    
    return args
#END: parse_args())




##########################################################
# Setup logging
#
def setup_logging(): 
    """
    setup logging stuff
    """
    # make temp file for log
    temp_root_dir = os.path.join(tempfile.gettempdir(), 'audiobook_reencode')
    #  if not os.path.isdir(temp_root_dir):
        #  os.mkdir(temp_root_dir)

    
    logdir = os.path.join(temp_root_dir, "audiobook_reencode-log-" + datetime.datetime.now().strftime("%yy%mm%dd-%H-%M"))
    logfile = os.path.join(temp_root_dir, "audiobook_reencode-log-" + datetime.datetime.now().strftime("%yy%mm%dd-%H-%M") + ".log")

    # ffmpeg log output dir
    ffmpeg_log_dir = os.path.join(temp_root_dir, "audiobook_reencode-log-" + datetime.datetime.now().strftime("%yy%mm%dd-%H-%M"), "ffmpeg_output")
    ffmpeg_error_log_dir = os.path.join(temp_root_dir, "audiobook_reencode-log-" + datetime.datetime.now().strftime("%yy%mm%dd-%H-%M"), "ffmpeg_error_output")


    #this doesnt seem right FIXME
    #  logfile = mktmpdir(os.path.join(temp_root_dir, log_file))

    # create dirs
    #  print("log files: \n  " + temp_root_dir + "\n  " + ffmpeg_error_log_dir + "\n  " + ffmpeg_log_dir + "\n")
    if not os.path.exists(logdir):
        os.makedirs(logdir, exist_ok=True)
    if not os.path.exists(ffmpeg_error_log_dir):
        os.makedirs(ffmpeg_error_log_dir, exist_ok=True)
    if not os.path.exists(ffmpeg_log_dir):
        os.makedirs(ffmpeg_log_dir, exist_ok=True)


    # format logger
    logFormatterFile = logging.Formatter("%(asctime)s:%(levelname)s: %(message)s", datefmt='%I:%M:%S')
    logFormatterSteam = logging.Formatter("%(levelname)s: %(message)s")
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.DEBUG)
                
    # set logger to write to logfile
    fileHandler = logging.FileHandler(logfile)
    fileHandler.setFormatter(logFormatterFile)
    my_logger.addHandler(fileHandler)


    # set loger to write to stderr if debug
    if config['preferred']['debug']:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatterSteam)
        my_logger.addHandler(consoleHandler)
        
    return [my_logger, [logfile, ffmpeg_log_dir, ffmpeg_error_log_dir]] 
# end setup_logging








####################################################
# Print errors from file
#
def print_error_file(filename):
    """
    prints error from file
    """
    
    f = open(filename, "r")

    content = ''

    #  print(filename)
    for line in f:
        if re.search("ERROR", line):
            content += line

    # Print out errors at end of program
    if not content == '':
        print("Errors detected:")
        print(content)

    f.close()

    return
# End print_error_file()







####################################################
# Process the directory
#
def process_directory(logger, log_files, dirpath, audio_files, audio_file_data, single_file=False):
    """
    processes the directory
        delete unnedded files
        extract cover art

        dirpath = path to current dir
        audio_files = list of audio files in dir
        audio_file_data = dictionary holding audio file data
        
        returns updated audio_file_data
    """
    logger.debug("-  Processing directory: " + dirpath)
    
    global total_duration
    # ffmpeg log file
    #  ffmpeg_log_file = re.sub(log_file, "\.log")


    shared_cover_art_file = ''

    # Directories filename similarity
    similarity = filename_similarity(logger, audio_files)

    # Process each file to get data and find cover art
    for audio_file in audio_files:
        logger.debug("-  Grabing files data: " + os.path.basename(audio_file))
        #  if not debug: print(".", end="", flush=True)
        # Grab some embeded data and stats
        audio_file_data[audio_file] = extract_audiofile_data(logger, log_files, audio_file)
        #  pprint.pprint(audio_file_data[audio_file] )
        total_duration += audio_file_data[audio_file]['duration']
        
        # save if files name are similar
        audio_file_data[audio_file]['similarity'] = similarity

        # Extract the cover art from audio file to cover.jpg
        if not (config['preferred']['only_delete_unneeded_files'] or 
                config['preferred']['only_add_id3_genre'] or 
                config['preferred']['only_reencode']):
            if audio_file_data[audio_file]['cover_art_embeded']:
                audio_file_data = extract_cover_art(logger, audio_file, audio_file_data)

        # Set the cover art file is aproprite 
        #   (cover art not set) and (files in dir are similar) and (art exists)
        if shared_cover_art_file == '' and similarity and audio_file_data[audio_file]['cover_art_embeded']:
            shared_cover_art_file = audio_file_data[audio_file]['cover_art_file']
        

    # Cover art not found yet, look for image in dir
    if shared_cover_art_file == '':
        shared_cover_art_file = detect_cover_art_image_file(logger, dirpath)

    # ReProcess each file in the current directory if cover art extracted
    if not shared_cover_art_file == '':
        for audio_file in audio_files:
            #  if not debug: print(".", end="", flush=True)
            logger.debug("-  Processing file: " + audio_file)
            # Add cover art in each file
            audio_file_data[audio_file]['cover_art_file'] = shared_cover_art_file
            audio_file_data[audio_file]['cover_art_embeded'] = True

    # Print newline after dots
    #  if not debug: print("")

    return(audio_file_data)
# end process_directory()




#########################################################
# Check if required program exists in PATH 
#
def error_checking(logger, path):
    """
    Error checking function
    file exists
    valid bitrate
    etc

    """
    error_found = False


    # Check if input is a file or directory
    if not (os.path.isfile(path) or os.path.isdir(path)):
        logger.error("Error: \"" + path + "\" is not a directory or file")
        error_found = True
        
    # check if input is an audio file
    if os.path.isfile(path):
        (filename, ext) = os.path.splitext(path)
        if not ( re.search(r'\.mp3', path, re.IGNORECASE) or re.search(r'\.m4[ba]', path, re.IGNORECASE) ):
            logger.error("Error: \"" + path + "\" is not an audiofile (mp3/m4b/m4a)")
            logger.error("Input must be an audiofile (mp3/m4b/m4a) or directory with audio files in it.")
            error_found = True
        # check incompatible args
        if config['preferred']['only_extract_cover_art']:
            logger.error("Error: argument \"only-extract-cover-art\" is incompatible with single file as of now, this may be changed.")
            error_found = True       
        if config['preferred']['only_delete_unneeded_files']:
            logger.error("Error: argument \"only-delete-unneeded-files\" is incompatible with single file")
            error_found = True


    #   Required: ffmpeg, ffprobe    
    from distutils.spawn import find_executable
    
    if not find_executable('ffmpeg'):
        logger.error("Error: ffmpeg is required, not found")
        error_found = True
    if not find_executable('ffprobe'):
        logger.error("Error: ffprobe(from ffmpeg) is required, not found")
        error_found = True
    
    # Check the args for ffmpeg
    valid_bitrates = ['8k', '16k', '24k', '32k', '40k', '48k', '56k', '64k', '80k', '96k', '112k', '128k', '144k', '160k', '192k', '224k', '256k', '320k']

    valid_bandwidths = ['8000', '11025', '12000', '16000', '22050', '24000', '32000', '44100', '48000']

    bitrate_ok = 0
    if config['preferred']['bitrate']:
        for bit in valid_bitrates:
            if config['preferred']['bitrate'] == bit:
                bitrate_ok = 1
        if not bitrate_ok:
            logger.error("Error: Not a valid bitrate")
            logger.error("Valid options: '8k', '16k', '24k', '32k', '40k', '48k', '56k', '64k', '80k', '96k', '112k', '128k', '144k', '160k', '192k', '224k', '256k', '320k'")
            error_found = True
    
    bandwidth_ok = 0
    if config['preferred']['samplerate']:
        for band in valid_bandwidths:
            if config['preferred']['samplerate'] == band:
                bandwidth_ok = 1
        if not bandwidth_ok:
            logger.error("Error: Not a valid samplerate")
            logger.error("Valid options: '8000', '11025', '12000', '16000', '22050', '24000', '32000', '44100', '48000'")
            error_found = True

        if config['preferred']['disable_extract_cover_art'] and config['preferred']['only_extract_cover_art']:
            logger.error("Arguments: disable-extract-cover-art and only-extract-cover-art conflicts")
            error_found = True
        if config['preferred']['disable_reencode'] and config['preferred']['only_reencode']:
            logger.error("Arguments: disable_reencode and only_reencode conflicts")
            error_found = True
        if config['preferred']['disable_delete_unneeded_files'] and config['preferred']['only_delete_unneeded_files']:
            logger.error("Arguments: disable_delete_unneeded_files and only_delete_unneeded_files conflicts")
            error_found = True
        if config['preferred']['disable_add_id3_genre'] and config['preferred']['only_add_id3_genre']:
            logger.error("Arguments: disable_add_id3_genre and only_add_id3_genre conflicts")
            error_found = True
        if config['preferred']['disable_reencode'] and config['preferred']['force_normalization']:
            logger.error("Arguments: disable_reencode and force_normalization conflicts")
            error_found = True
        if config['preferred']['disable_id3_change'] and config['preferred']['only_add_id3_genre']:
            logger.error("Arguments: disable_id3_change and only_add_id3_genre conflicts")
            error_found = True
    
    err_param = 0
    if config['preferred']['only_extract_cover_art']:
        err_param +=1
    if config['preferred']['only_reencode']:
        err_param +=1
    if config['preferred']['only_delete_unneeded_files']:
        err_param +=1
    if config['preferred']['only_add_id3_genre']:
        err_param +=1
    if err_param > 1: # any two or more are true
        error_found = True
    
    # Exit if error
    if error_found:
        exit(1)
    return
# end error_checking()






###############################################################
# Compare Bitrate
#
def compare_bitrate(bitrate):
    """
    Check if stream bitrate is lower
 
    returns
    [Bolean, string]
   """
    #  print(bitrate)
    #  print(config['preferred']['bitrate'])

    if bitrate == '':
        # maybe VBR or something
        lower_bitrate = False
        lowest_bitrate = config['preferred']['bitrate']
        return [lower_bitrate, lowest_bitrate]

    stream_bitrate = float(round(float(re.sub(r'k', '', bitrate)))) # desired bitrate
    encode_bitrate = float(re.sub(r'k', '', config['preferred']['bitrate'])) # desired bitrate
    # 90% of bitrate so 63.9kpbs will become 64k, maybe put some inteligents later
    if stream_bitrate * 0.9 <= encode_bitrate:
        lower_bitrate = True
        lowest_bitrate = bitrate
    else:
        lower_bitrate = False
        lowest_bitrate = config['preferred']['bitrate']

    return [lower_bitrate, lowest_bitrate]
# End: compare_bitrate()



###############################################################
# Compare Samplerate
#
def compare_samplerate(samplerate):
    """
    Check if stream samplerate is lower

    returns
    [Bolean, string]
    """

    if samplerate == '':
        # not sure if this will ever happen
        lower_samplerate = False
        lowest_samplerate = config['preferred']['samplerate']
        return [lower_samplerate, lowest_samplerate]

    stream_samplerate = int(re.sub(r'k', '', samplerate)) # desired samplerate
    encode_samplerate = int(re.sub(r'k', '', config['preferred']['samplerate'])) # desired samplerate
    if stream_samplerate <= encode_samplerate:
        lower_samplerate = True
        lowest_samplerate = samplerate
    else:
        lower_samplerate = False
        lowest_samplerate = config['preferred']['samplerate']

    return [lower_samplerate, lowest_samplerate]
# End: compare_samplerate()




###############################################################
# Generates data of audio file
#
def extract_audiofile_data(logger, log_files, audio_file):
    """
    Generates the files info
    bitrate
    cover art
    etc
    """

    # ffprobe
    # -show_format -show_chapters -show_streams
    #-loglevel -8 (removes unnessasary stuff)
    # -print_format flat 
    # https://trac.ffmpeg.org/wiki/FFprobeTips
    # ffprobe -loglevel -8 -show_format -show_chapters -show_streams


    import json

    # Create dictionary
    audio_file_data = {}
    audio_file_data['filename'] = audio_file
    audio_file_data['cover_art_embeded'] = False
    audio_file_data['codec_name'] = ''
    audio_file_data['lower_bitrate'] = False
    audio_file_data['encoded_by'] = ''
    audio_file_data['encoder_same'] = False
    audio_file_data['bitrate'] = ''
    audio_file_data['samplerate'] = ''
    audio_file_data['chapters_exist'] = False
    audio_file_data['cover_art_file'] = ''
    audio_file_data['title'] = ''
    audio_file_data['read_data_failed'] = False
    # add distinct metadata section
    audio_file_data['metadata'] = {}
    audio_file_data['remove_chapter_data'] = False
    audio_file_data['lower_samplerate'] = False
    audio_file_data['already_reencoded'] = False
    audio_file_data['dont_reencode'] = False
    audio_file_data['duration'] = 0 # in h

    # ffprobe command
    cmd = 'ffprobe ' +  ffmpeg_aax_activation_parameters(audio_file) + ' -loglevel 8 -show_format -show_chapters -show_streams -print_format json "' + audio_file + '"' 

    # Executing command
    logger.debug("------ffprobe-ing----")
    logger.debug(cmd)
    logger.debug("---------------------")
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, err) = p.communicate() # execute
    p_status = p.wait() # wait for command to finish


    # put ffprobe in to ffprobe_data dictionary
    ffprobe_data = json.loads(output)

    # Check if ffprobe failed
    if err or not ffprobe_data:
        audio_file_data['read_data_failed'] = True
        logger.error("reading \"" + audio_file + "\" with ffprobe, file probably broken") 
        if not config['preferred']['ignore_errors']:
            exit(1)       
        return(audio_file_data)

    # grab the audio-metadata
    
    # Prints ffprobe info in dictionary
    logger.debug(",,,,,,,,,,,,,,,,,,,,,,,, ffprobe data ,,,,,,,,,,,,,,,,,,,,,,,,")
    logger.debug(pprint.pformat(ffprobe_data))
    logger.debug(",,,,,,,,,,,,,,,,,,,,,,,, ffprobe data (end) ,,,,,,,,,,,,,,,,,,")



   

    # parse ffprobe output to extract data
    for stream in ffprobe_data['streams']:
        # Check for cover art
        if stream['codec_name'] == 'mjpeg' or stream['codec_name'] == 'png' or stream['codec_name'] == 'theora':
            audio_file_data['cover_art_embeded'] = True
            # logger.debug("-   Cover art exists")
        else:
            audio_file_data['cover_art_embeded'] = False
            # logger.debug("-   Cover art not embeded")

        # Check if mp3
        if stream['codec_name'] == 'mp3':
            audio_file_data['codec_name'] = 'mp3'
            if 'bit_rate' in stream.keys():
                audio_file_data['bitrate'] = str(int(stream['bit_rate'])/1000) + "k"
            if 'sample_rate' in stream.keys():
                audio_file_data['samplerate'] = stream['sample_rate']
            #copy metadata
            if 'format' in ffprobe_data.keys():
                if 'tags' in ffprobe_data['format'].keys():
                    audio_file_data['metadata'] = ffprobe_data['format']['tags']


        # Check if m4b/m4a
        if stream['codec_name'] == 'aac':
            audio_file_data['codec_name'] = 'm4b'
            if 'bit_rate' in stream.keys():
                audio_file_data['bitrate'] = str(int(stream['bit_rate'])/1000) + "k"
            if 'sample_rate' in stream.keys():
                audio_file_data['samplerate'] = stream['sample_rate']
            #copy metadata
            if 'format' in ffprobe_data.keys():
                if 'tags' in ffprobe_data['format'].keys():
                    audio_file_data['metadata'] = ffprobe_data['format']['tags']

        # ogg
        if  stream['codec_name'] == 'vorbis':
            audio_file_data['codec_name'] = 'ogg'
            if 'bit_rate' in stream.keys():
                audio_file_data['bitrate'] = str(int(stream['bit_rate'])/1000) + "k"
            if 'sample_rate' in stream.keys():
                audio_file_data['samplerate'] = stream['sample_rate']
            #copy metadata (from audio stream)
            if 'tags' in stream.keys():
                audio_file_data['metadata'] = stream['tags']

        # opus
        if stream['codec_name'] == 'opus':
            audio_file_data['codec_name'] = 'opus'
            if 'bit_rate' in stream.keys():
                audio_file_data['bitrate'] = str(int(stream['bit_rate'])/1000) + "k"
            if 'sample_rate' in stream.keys():
                audio_file_data['samplerate'] = stream['sample_rate']
            #copy metadata (from audio stream)
            if 'tags' in stream.keys():
                audio_file_data['metadata'] = stream['tags']

        # flac
        if  stream['codec_name'] == 'flac':
            audio_file_data['codec_name'] = 'flac'
            if 'bit_rate' in stream.keys():
                audio_file_data['bitrate'] = str(int(stream['bit_rate'])/1000) + "k"
            if 'sample_rate' in stream.keys():
                audio_file_data['samplerate'] = stream['sample_rate']
            #copy metadata
            if 'format' in ffprobe_data.keys():
                if 'tags' in ffprobe_data['format'].keys():
                    audio_file_data['metadata'] = ffprobe_data['format']['tags']

        # durration
        audio_file_data['duration'] = float(stream['duration'] ) # seconds


    # end of stream loop   

    # get the id3 encoder tag
    if 'encoded_by' in audio_file_data['metadata'].keys():
        audio_file_data['encoded_by'] = audio_file_data['metadata']['encoded_by']
    
    # get title
    if 'title' in audio_file_data['metadata'].keys():
            audio_file_data['title'] = audio_file_data['metadata']['title']
    if audio_file_data['title'] == '':
        audio_file_data['title'] = os.path.splitext(os.path.basename(audio_file))[0]
    

    # compare bitrate/samplerate  and check if re-encoded
    audio_file_data['lower_bitrate'] = compare_bitrate(audio_file_data['bitrate'])[0]
    audio_file_data['lower_samplerate'] = compare_samplerate(audio_file_data['samplerate'])[0]
    # FIXME-B
    if audio_file_data['encoded_by'] == program_name: 
        # already reencoded
        audio_file_data['already_reencoded'] = True



    # Get chapter data
    if not config['preferred']['disable_split_chapters']:
        if 'chapters' in ffprobe_data.keys():
            chapter_number = 1
            if len(ffprobe_data['chapters']) > 1:
                # Multiple chapters exist
                audio_file_data['chapters_exist'] = True
                audio_file_data['chapters_total'] = len(ffprobe_data['chapters'])
                audio_file_data['chapters'] = {} 
                
                # remove chap metadata
                audio_file_data['remove_chapter_data'] = True
                
                # for each chapter         
                for chap in ffprobe_data['chapters']:
                    # check if chap is less than  second ignore
                    if (float(chap['end_time']) - float(chap['start_time'])) < 1:
                        continue
                    else:
                        # Chapter index
                        index = chap['id']
                        audio_file_data['chapters'][index] = {}
                        audio_file_data['chapters'][index]['id'] = chapter_number # FIXME check if is needs index or chap_num
                        track_num = chapter_number
                        # chapter name
                        if '%03d' % track_num == chap['tags']['title']:
                            audio_file_data['chapters'][index]['name'] = chap['tags']['title']
                        elif '%02d' % track_num == chap['tags']['title']:
                            audio_file_data['chapters'][index]['name'] = chap['tags']['title'] 
                        else:                   
                            if track_num + 1 > 99:
                                audio_file_data['chapters'][index]['name'] = '%03d' % track_num + ' - ' + chap['tags']['title']
                            else:
                                audio_file_data['chapters'][index]['name'] = '%02d' % track_num + ' - ' + chap['tags']['title']
                        # chapter start time
                        audio_file_data['chapters'][index]['start_time'] = "%.2f" % float(chap['start_time'])
                        # chapter durration
                        audio_file_data['chapters'][index]['duration'] = "%.2f" % (float(chap['end_time']) - float(chap['start_time']))
                        # increment chapter_number
                        chapter_number += 1
            else: # probably doesn't have any chap meta, but remove it just incase
                audio_file_data['remove_chapter_data'] = True
            # there shouldn't be any chapters because only one chap > 1s
            if chapter_number == 2:
                audio_file_data['chapters_exist'] = False
                audio_file_data['remove_chapter_data'] = True
    # Chap meta (end)


    # Dont re-encode
    #   [lower bitrate/samplerate] and [not already_reencoded] and [no forced] and [no chap split] FIXME-A

    if audio_file_data['lower_bitrate']:
        if audio_file_data['lower_samplerate']:
            if audio_file_data['already_reencoded']:
                if not audio_file_data['chapters_exist']:
                    audio_file_data['dont_reencode'] = True

    #  audio_file_data['dont_reencode'] = True

    if audio_file_data['lower_bitrate'] and \
            audio_file_data['lower_samplerate'] and \
            audio_file_data['already_reencoded'] and \
            not audio_file_data['chapters_exist']:
        audio_file_data['dont_reencode'] = True

    if audio_file_data['lower_bitrate'] and \
            audio_file_data['lower_samplerate'] and \
            audio_file_data['already_reencoded'] and \
            (audio_file_data['chapters_exist'] and not config['preferred']['disable_split_chapters']):
        audio_file_data['dont_reencode'] = True


    # Force re-encode
    if config['preferred']['force_reencode'] or config['preferred']['force_normalization']:
        audio_file_data['dont_reencode'] = False


    logger.debug(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
    logger.debug(",,,,,,,,,,,,,,,,,,,,,,,, audio_file_data ,,,,,,,,,,,,,,,,,,,,,,,,,,,,")
    logger.debug(pprint.pformat(audio_file_data))
    logger.debug(",,,,,,,,,,,,,,,,,,,,,, audio_file_data (end) ,,,,,,,,,,,,,,,,,,,,,,,,")
    logger.debug(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,")

    return(audio_file_data)
# end extract_audiofile_data




########################################################
# AAX ffmpeg tags
#
def ffmpeg_aax_activation_parameters(filename):
    """
    creates the arguments to decode aax files
    input: file_extention str
    """
    #  print("Extension: " + os.path.splitext(filename)[1].lower())

    if os.path.splitext(filename)[1].lower() == '.aax':
        return "-activation_bytes " + config['GENERAL']['aax_authcode']
    else:
        return ""
# End: ffmpeg_aax_activation_parameters(filename):




########################################################
# Clean up dir
#
def clean_up_tmp_dir(logger):
    """
    Deletes the tmp dir
    """
    # dont delete log files
    
    temp_root_dir = config['TMP']['tmp_dir']

    logger.debug("Cleaning up tmp dir:" + temp_root_dir)
    # dirs = os.listdir( temp_root_dir )

    for root, dirs, files in os.walk(temp_root_dir, topdown=False):
        for name in files:
            (filen, ext) =  os.path.splitext(name)
            if not ext == ".log":           
                os.remove(os.path.join(root, name))
        for name in dirs:
            # if os.path.exists(os.path.join(root, name)):
            os.rmdir(os.path.join(root, name))

    return
# end clean_up_tmp_dir()




#################################################################
#   Add metadata
#
def add_metadata(logger, audio_filename, audio_file_data, chap_num):
    """
    Adds metadata
    logger: log stuff
    filename: to add cover art to
    audio_file_data: includes all info of file
    chap_num: files chapters number (int)
    """
    import imghdr

    # examples
    #  https://github.com/regosen/get_cover_art/tree/master/get_cover_art

    # For more information visit: http://mutagen.readthedocs.io/en/latest/user/id3.html
    #  TIT2: title
    #  TRCK (Track number/Position in set): 1
    #   TCON (Content type): Audio book (255)
    #   TCON=Audiobook
    #   # clear any leftovers from previous codecs (let ffmpeg take care of this)
    #   TXXX=compatible_brands=
    #   TXXX=major_brand=
    #   TXXX=minor_version=
    #      # add album cover
    #      id3.add(
    #          APIC(
    #              encoding=3,         # 3 is for UTF8, but here we use 0 (LATIN1) for 163, orz~~~
    #              mime='image/jpeg',  # image/jpeg or image/png
    #              type=3,             # 3 is for the cover(front) image
    #              data=open(cover_path, 'rb').read()
    #          )
    #      )
    #  COVER_FRONT = <PictureType.COVER_FRONT: 3>

    # import image lib (pillow?)
    from PIL import Image
    # Cover art file (APIC)
    cover_art_filename = audio_file_data['cover_art_file']
  
    # initialize
    mime_type=''

    # check if art file exists
    if not cover_art_filename == '' and os.path.isfile(cover_art_filename) and audio_file_data['cover_art_embeded']:
        add_cover_art = True
    elif (cover_art_filename == '' or not os.path.isfile(cover_art_filename)) and audio_file_data['cover_art_embeded']:
        logger.error("      Error: Cover art is set, but file doesn't exist")
        logger.error("        Filename: " + cover_art_filename)
        add_cover_art = False
    else:
        add_cover_art = False
    
    if add_cover_art:
        # Cover Art image info
        im = Image.open( cover_art_filename)
        width, height = im.size
        mode_to_bpp = {"1": 1, "L": 8, "P": 8, "RGB": 24, "RGBA": 32, "CMYK": 32, "YCbCr": 24, "LAB": 24, "HSV": 24, "I": 32, "F": 32}
        depth = mode_to_bpp[im.mode]
        img_format = im.format

        # Cover art Mime type
        if add_cover_art:
            if img_format.lower() == 'png':
                mime_type = 'image/png'
            elif img_format.lower() == 'jpeg':
                mime_type = 'image/jpeg'
            else:
                logger.error("     Warning: cover art file format unknown, not embedding cover art")
                mime_type = None
        else:
            mime_type = None
                #  return 1

    # Cover art Mime type
    #  if add_cover_art:
    #      if imghdr.what(cover_art_filename) == 'png':
    #          mime_type = 'image/png'
    #      elif imghdr.what(cover_art_filename) == 'jpeg':
    #          mime_type = 'image/jpeg'
    #      else:
    #          print("     Warning: cover art file format unknown, not embedding cover art")
    #          mime_type = None
    #  else:
    #      mime_type = None
    #          #  return 1

    # Audio codec
    output_format = config['preferred']['audio_output_format'] 
    
    # Track numbers (TRCK)
    if not chap_num == None:
        track_num = chap_num
        track_total = str(audio_file_data['chapters_total'])
        track_string = str(chap_num) + "/" + str(audio_file_data['chapters_total'])
    #  track_string = track_string.encode('utf-8') # ensure its unicode

    # Encoded_by: encode meta (ie this program) (TENC) maybe (TSSE), "audiobook_reencoder(ffmpeg)-v0.1
    encoded_by = program_name

    # Genre
    if not config['preferred']['disable_add_id3_genre'] :
        add_genre = True
    else:
        add_genre = False
    genre="Audiobook"

    if audio_file_data['title'] == '':
        add_title = True
    else:
        add_title = False
    new_title = os.path.splitext(os.path.basename(audio_file_data['filename']))[0]



    # Add MP3 (id3/APIC)
    if output_format == 'mp3' and not config['preferred']['test']:
        # import needed modules
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, APIC, error, TRCK, TENC, TCON, TIT2

        #open audio file
        aud = MP3(audio_filename, ID3=ID3)
        #  aud = ID3(audio_filename)
        
        # Title
        if add_title:
            aud.tags.add(TIT2(encoding=3, text=new_title))

        # Cover art
        if add_cover_art:
            if mime_type:
                if aud.tags.getall('APIC'):
                    aud.tags.delall("APIC") # Delete existing art
                aud.tags.add( APIC(
                        #  COVER_FRONT = <PictureType.COVER_FRONT: 3>
                        encoding=3,         # 3 is for UTF8
                        mime=mime_type,  # image/jpeg or image/png
                        type=3,             # 3 is for the cover(front) image
                        desc=u'Cover (front)',
                        data=open(cover_art_filename, 'rb').read()
                ) )

        # Genre
        aud.tags.add(TCON(encoding=3, text=u"Audiobook"))

        #Track
        #  aud.tags.add(TRCK(encoding=3, text=u"2/4")) #text=str(track_string))
        if not chap_num == None:
            aud.tags.add(TRCK(encoding=3, text=str(track_string)))

        # encoded_by "audiobook-reencoder(v...)"
        aud.tags.add(TENC(encoding=3, text=encoded_by))

        # print info
        if config["preferred"]["debug"]:
            logger.debug(aud.pprint())

        # save file
        aud.save()

        return 0
    # Add M4B cover art
    elif output_format == 'm4b' and not config['preferred']['test']:

        # import module
        from mutagen.mp4 import MP4
        from mutagen.m4a import M4ACover
        # open file
        aud = MP4(audio_filename)

        covr = []
        # open cover art
        #  if mime_type == 'image/jpeg':
            #  covr.appent( M4ACover(cover_art_filename, M4ACover.FORMAT_JPEG) )
        #  else:
            #  covr.appent( M4ACover(cover_art_filename, M4ACover.FORMAT_PNG) )

        # add cover art to file
        aud.tags['covr'] = covr
        # save file
        aud.save()
        return 0

    # OPUS Cover Art
    #   https://exiftool.org/TagNames/Vorbis.html#Comments
    #   http://pythonic.zoomquiet.top/data/20150618101351/index.html
    #   https://mutagen.readthedocs.io/en/latest/user/vcomment.html
    #   https://www.geeksforgeeks.org/extract-and-add-flac-audio-metadata-using-the-mutagen-module-in-python/
    #  'TITLE' 	Title
    #  'TRACKNUMBER' 	TrackNumber
    #  'ENCODED_BY' 	EncodedBy
    #  'GENRE' 	Genre
    #  'COVERART' 	CoverArt  (base64-encoded image)
    #  'COVERARTMIME' 	CoverArtMIMEType
    #  'METADATA_BLOCK_PICTURE' 	Picture
    elif output_format == 'opus' and not config['preferred']['test']:
        import base64
        from mutagen.oggopus import OggOpus
        from mutagen.flac import Picture # not sure why it needs to be flac

        # open audio
        aud = OggOpus(audio_filename)
        
        # open image
        with open("image.jpeg", "rb") as h:
            img_data = h.read()

        # Config
        picture = Picture()
        picture.data = img_data
        picture.type = 17
        picture.desc = u"Cover Art"
        picture.mime = mime_type
        picture.width = width
        picture.height = height
        picture.depth = depth
        picture_data = picture.write()
        encoded_data = base64.b64encode(picture_data)
        vcomment_value = encoded_data.decode("ascii")
        # write meta
        aud["metadata_block_picture"] = [vcomment_value]
        # Genre
        aud["GENRE"] = u"Audiobook"
        #Track
        if not chap_num == None:
            aud["TRACKNUMBER"] = str(track_string)
        # encoded_by "audiobook-reencoder(v...)"
        aud["ENCODED_BY"] = encoded_by
        # print info
        if config["preferred"]["debug"]:
            logger.debug(aud.pprint())
        # save
        aud.save()

    # FLAC
        #
        #  from mutagen import File
        #  from mutagen.flac import Picture, FLAC
        #
        #  def add_flac_cover(filename, albumart):
        #      audio = File(filename)
        #
        #      image = Picture()
        #      image.type = 3
        #      if albumart.endswith('png'):
        #          mime = 'image/png'
        #      else:
        #          mime = 'image/jpeg'
        #      image.desc = 'front cover'
        #      with open(albumart, 'rb') as f: # better than open(albumart, 'rb').read() ?
        #          image.data = f.read()
        #
        #      audio.add_picture(image)
        #      audio.save()
        #
 



    if add_cover_art:        
        logger.debug("  ~~~~~~~~~~~~~~~~~ cover art stuff~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        logger.debug("  ~   Audio filename: " + audio_filename)
        logger.debug("  ~   cover art filename: " + cover_art_filename)
        #  logger.debug("  ~   cover art file type: " + imghdr.what(cover_art_filename))
        logger.debug("  ~   mime type: " + mime_type)
        logger.debug("  ~   Height/Width/Depth: " + str(height) + "/" + str(width) + "/" + str(depth))
        logger.debug("  ~   Adding cover art: " + str(add_cover_art))
        #  logger.debug("  ~   output file format: " + output_format)
        #  logger.debug("  ~   Audio filename: " + audio_filename
        logger.debug("  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


# End: add_metadata()




######################################################
# Re-encode, file using ffmpeg
#
def reencode_audio_file(logger, log_files, audio_file_data, file_count, total_count):
    """
    Generate the ffmpeg command, and parameters
    returns False on error
    """
    
    #  ffmpeg encoding notes
    #  -map_chapters -1
    #      Remove chapters
    #   -metadata compatible_brands= -metadata minor_version= -metadata major_brand= -iTunSMPB=
    #      remove leftovers info from aax/m4b
    #  -filter:a loudnorm
    #      volume normalization
    #  -id3v2_version 3 -write_id3v1 1
    #      add/copy id3 v2.3 and 1.1
    #  -loglevel error
    #      ffmpeg output
    #  -y
    #      overwrite
    #  -i
    #      input file
    #  -c:a libmp3lame
    #      audio codec
    #  -b:a
    #      audio bitrate
    #  -ar
    #      audio sample rate
    #
    # -report
    #       log filename
    #
   
    # Metadata info
    # mp4/m4b
    #   media_type=2 is audiobook
    #   'compatible_brands': 'M4A mp42isom'
    #   'genre': 'Audiobook'
    # mp3
    #   stik=2 iTunes Media Type(2=audiobook)
    #       https://github.com/sergiomb2/libmp4v2/wiki/iTunesMetadata#user-content-media-type-stik
    # initialize spinner


    # Mediadata info
    #   https://github.com/sergiomb2/libmp4v2/wiki/iTunesMetadata
    #   http://mutagen.readthedocs.io/en/latest/user/id3.html


    #  spinner = Spinner()
    global files_complete



    # Skipping: no need to re-encode, skipping
    if audio_file_data['dont_reencode']:
        logger.debug("     File already re-encoded, skipping")

        files_complete.append({'file': (audio_file_data['filename']), 'status': 'skipped'})
        return True

    new_filename = ''

    # TMP folder
    temp_root_dir = mktmpdir(os.path.join(config['TMP']['tmp_dir'], os.path.basename(os.path.dirname(audio_file_data['filename']))))

    # Set the defaults
    # always add space in the begining of varable (except with filename
    ffmpeg_metadata = " "
    ffmpeg_cover_art = ' '
    ffmpeg_input_old = audio_file_data['filename']
    ffmpeg_input = audio_file_data['filename']
    ffmpeg_subdir = os.path.basename(os.path.dirname(audio_file_data['filename']))

    ffmpeg_cover_art = ' '
    ffmpeg_bitrate = ' '
    ffmpeg_samplerate = ' '
    ffmpeg_loudnorm = ' '
    ffmpeg_audio_codec = ' '
    ffmpeg_video_codec = ' '


    # Bitrate
    if not config['preferred']['audio_output_format']:
        config['preferred']['audio_output_format'] = "mp3"
    if config['preferred']['bitrate']:
        if audio_file_data['bitrate'] == '':
            # no bitrate found in file
            bitrate = config['preferred']['bitrate']
        else:
            # test for lowest bitrate
            bitrate = compare_bitrate(audio_file_data['bitrate'])[1] # lowest bitrate
    else:
        bitrate = bitrate_default

    # Samplerate
    if config['preferred']['samplerate']:
        if audio_file_data['samplerate'] == '':
            # samplerate not read from file
            samplerate = audio_file_data['samplerate']
        else:
            # test for lowest samplerate
            samplerate = compare_samplerate(audio_file_data['samplerate'])[1] # lowest samplerate
    else:
        samplerate = samplerate_default

    cover_art_same = False

    # Output filename
    #   final is orginal dir + filename + new ext   (original_dir/filename.mp3)
    #   ffmpeg_output = temp dir + random number + final file name (/tmp/audiobook_reencode/432432535235235-filename.mp3)
    final_output = os.path.splitext(ffmpeg_input)[0] + '.' +config['preferred']['audio_output_format']
    ffmpeg_output = mktmpdir(os.path.join(temp_root_dir, 
                                 os.path.basename(os.path.dirname(ffmpeg_input)),
                                 str(random.randrange(1, 999999999999999)) + os.path.basename(final_output)))

    # ffmpeg logging filename
    [log_file, ffmpeg_log_dir, ffmpeg_log_error_dir] = log_files
    ffmpeg_log_count = 0
    # remove any problematic chars
    ffmpeg_log_file = re.sub(r'[\:\?\'\"\*\+]', '-', os.path.join(ffmpeg_log_dir, os.path.basename(ffmpeg_input) + ".0.log"))
    while os.path.exists(ffmpeg_log_file):
        ffmpeg_log_count += 1
        ffmpeg_log_file = os.path.join(ffmpeg_log_dir, os.path.basename(ffmpeg_input) + "." + str(ffmpeg_log_count) + ".log")



    # Deciding to skip encoding
    chapter_it = False
    setting_same_as_file = False
    no_encode_args = False
    add_cover_art = False
    
    # Bitrates/Samplerate/Meta same, remove decimal for bitrate
    #  if ( re.sub(r'\.0', '', audio_file_data['bitrate']) == bitrate and audio_file_data['samplerate'] == samplerate and audio_file_data['encoded_by'] == program_name and not config['preferred']['force_normalization']):
    if audio_file_data['lower_bitrate'] and \
            audio_file_data['lower_samplerate']:
        setting_same_as_file = True

    # No need to Re-encode
    if config['preferred']['disable_reencode'] or config['preferred']['only_add_id3_genre'] or config['preferred']['only_extract_cover_art']:
        no_encode_args = True

    # Chapters
    if (audio_file_data['chapters_exist'] and (not config['preferred']['disable_split_chapters'])) and not no_encode_args:
        chapter_it = True

    # Cover Art
    if (audio_file_data['cover_art_embeded'] and audio_file_data['cover_art_file']) or \
            (not audio_file_data['cover_art_embeded'] and not audio_file_data['cover_art_file']) or \
            (config['preferred']['disable_embed_cover_art']):
        cover_art_same = True

    if config['preferred']['force_reencode']:
        no_need_to_reencode = False
    elif ( setting_same_as_file or no_encode_args ) and not chapter_it:
        # They are likely the same
        no_need_to_reencode = True # just copy
    else:
        # They are not the same
        no_need_to_reencode = False



    # No re-encode ffmpeg settings
    if no_need_to_reencode:
        ffmpeg_bitrate = ' '
        ffmpeg_samplerate = ' '
        ffmpeg_audio_codec = " -c:a copy"
        ffmpeg_cover_art = " -c:v copy"
        # ffmpeg_output = ffmpeg_input_old
    else:
        #Re-encode options

        # Set Codec and Output file's extention TODO Add opus, ogg HERE
        if config['preferred']['audio_output_format'] == 'm4b':
            ffmpeg_audio_codec = " -c:a libfdk_aac"
            # ffmpeg_output = re.sub('\.[a-zA-Z0-9]{3,4}$', '.m4b', audio_file_data['filename'])
        elif config['preferred']['audio_output_format'] == 'ogg':
            ffmpeg_audio_codec = " -c:a libvorbis"
        elif config['preferred']['audio_output_format'] == 'opus':
            ffmpeg_audio_codec = " -c:a libopus"
        else:
            # Should be mp3 (default)
            ffmpeg_audio_codec = " -c:a libmp3lame"
            # ffmpeg_output = re.sub('\.[a-zA-Z0-9]{3,4}$', '.mp3', audio_file_data['filename'])



        # Set Bitrate and Sample rate
        if not ( config['preferred']['only_add_id3_genre'] or config['preferred']['only_extract_cover_art']):
            # Bitrate
            if config['preferred']['bitrate']:
                ffmpeg_bitrate = " -b:a " + config['preferred']['bitrate']
            else:
                ffmpeg_bitrate = " -b:a " + bitrate_default
            # Samplerate
            if config['preferred']['samplerate']:
                ffmpeg_samplerate = " -ar " + config['preferred']['samplerate']
            else:
                ffmpeg_samplerate = " -ar " + samplerate_default
   
        # loadnorm flags (1-pass)
        if config['preferred']['force_normalization'] or \
                    not ( config['preferred']['disable_normalize'] or \
                    config['preferred']['disable_reencode'] or \
                    config['preferred']['only_extract_cover_art'] or \
                    config['preferred']['only_add_id3_genre']):
            ffmpeg_loudnorm = " -filter:a loudnorm=I=" + str(loudnorm_int_vol)
            # todo add check for ReplayGain metadata check 
            # ffprobe doesn't show APE tags, where mp3gain is usually placed

    # Adding metadata Genre and encoder
    if not config['preferred']['disable_id3_change']:
        if config['preferred']['audio_output_format'] == 'mp3':
            # makes sure id3 tags are writen and removes some leftovers from m4b files
            ffmpeg_metadata += " -id3v2_version 3 -write_id3v1 1 -metadata compatible_brands= -metadata minor_version= -metadata major_brand= -metadata iTunSMPB="
        if chapter_it: #FIXME maybe
            ffmpeg_metadata += " -map_chapters -1 " 

    logger.debug("  ~~~~~~~~~~~~~~~~~file info (audio_file_data)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    logger.debug("  ~   Encoding file: " + os.path.basename(audio_file_data['filename']))
    logger.debug("  ~      Dir: " + os.path.dirname(audio_file_data['filename']))
    logger.debug("  ~      Title: " + audio_file_data['title'])   
    logger.debug("  ~      Codec: " + audio_file_data['codec_name'] )
    logger.debug("  ~      bitrate: " + audio_file_data['bitrate'] )
    logger.debug("  ~      samplerate: " + audio_file_data['samplerate'] )
    logger.debug("  ~      encoded_by: " + audio_file_data['encoded_by'] )     
    logger.debug("  ~      Lower Bitrate: " + str( audio_file_data['lower_bitrate'] ))
    logger.debug("  ~      Lower samplerate: " + str( audio_file_data['lower_samplerate'] ))
    logger.debug("  ~      Embedded cover art: " + str( audio_file_data['cover_art_embeded'] ))
    logger.debug("  ~      Cover art file: " + os.path.basename(audio_file_data['cover_art_file']))
    logger.debug("  ~      Chapters: " +  str(audio_file_data['chapters_exist']))
    logger.debug("  ~      ffmpeg log output: " +  ffmpeg_log_file)
    logger.debug("------------------------------- audio_file_data (raw) ---------------------------")
    logger.debug(pprint.pformat(audio_file_data))
    logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~-------------------~~~~~~~~~~~~")

    if audio_file_data['chapters_exist']:
        for chap in audio_file_data['chapters']:
            logger.debug(" ~      \"" + audio_file_data['chapters'][chap]['name'] +"\" (" + str(audio_file_data['chapters'][chap]['id']) + " of " + str(audio_file_data['chapters_total']) + ")")
            logger.debug(" ~        Start:" + audio_file_data['chapters'][chap]['start_time'] + "s, Dur:" + audio_file_data['chapters'][chap]['duration'] + "s" )
    

    
    if no_need_to_reencode:
        files_complete.append({'file': ffmpeg_input, 'status': 'skipped'})
    else:
        ##################################
        # Chapters exist, so split
        if chapter_it:
            #############################
            # Encoding Chapters

            # Create dir to put chapter files (remove invalid chars)
            input_files_dir = os.path.dirname(ffmpeg_input)
            
            # subdirectory for chaptered
            if audio_file_data['title'] != '':
                ffmpeg_output_subdir = re.sub(r"[<>:;\"'|?*\\\/]", "", audio_file_data['title'])
            else:
                ffmpeg_output_subdir = os.path.splitext(os.path.basename(audio_file_data['filename']))[0]
            # Temp dir for chapters
            ffmpeg_output_chap_temp_dirname = mktmpdir(os.path.join(temp_root_dir, ffmpeg_output_subdir))
            logger.debug("making tmp dir: " + ffmpeg_output_chap_temp_dirname)
            
            
       
            # total tracks
            ffmpeg_track_total = str(audio_file_data['chapters_total'])

            ffmpeg_single_tmp = mktmpdir(os.path.join(temp_root_dir, "temp-single-" + str(random.randrange(1,99999999999999)) + "." + config['preferred']['audio_output_format']))
            

            # Encoding (1st stage) 
            #   copy id3, Remove chapter data, encode w/ codec/bitrate/samplerate, vol normalize
            ffmpeg_cmd = "FFREPORT=\"file=" + ffmpeg_log_file + ":level=40\" ffmpeg  " +  ffmpeg_aax_activation_parameters(ffmpeg_input) + \
                    " -loglevel error -y -i \"" + ffmpeg_input + "\"" + \
                    ffmpeg_audio_codec + ffmpeg_bitrate + ffmpeg_samplerate + ffmpeg_loudnorm + ffmpeg_metadata + \
                    " \"" + ffmpeg_single_tmp + "\"" 

            # start encoder message
            if debug:
                logger.debug("    Encoding (" + str(file_count) + " of " + str(total_count) + "): " + os.path.basename(ffmpeg_input_old) )
                logger.debug("Encoding: first stage")


            #  print("         Encoding: first stage"            )
            logger.debug(" ~~~~~~~~~~~~~~~~~~~~~ file encode info ~~~~~~~~~~~~~~~~~~~~~~~~")
            logger.debug(" ~   FFMPEG flags")
            logger.debug(" ~      bitrate: " +  ffmpeg_bitrate)
            logger.debug(" ~      samplerate: " +  ffmpeg_samplerate)
            logger.debug(" ~      metadata: " +  ffmpeg_metadata)
            logger.debug(" ~      loudnorm: " +  ffmpeg_loudnorm)
            logger.debug(" ~      audio codec: " +  ffmpeg_audio_codec)
            logger.debug(" ~      input: " +  os.path.basename(ffmpeg_input))          
            logger.debug(" ~      output: " +  os.path.basename(ffmpeg_output))
            logger.debug("  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            logger.debug("  ~~~~~~~~~~~~~~~~ ffmpeg (first stage)~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            logger.debug(" CMD: " + ffmpeg_cmd)
            logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 

            print_time(logger)
            # run encoding command (1st stage)
            encoder_error = reencode_audio_file_ffmpeg(logger, ffmpeg_cmd, ffmpeg_input, ffmpeg_single_tmp, log_file, ffmpeg_log_file)
            print_time(logger)

            # error found
            if encoder_error:
                logger.debug("Encoding failed on \"" + ffmpeg_input + "\", stopping encoding book")
                # skip file on error
                # stop spinner
                files_complete.append({'file': ffmpeg_input_old, 'status': 'failed'})
                #  if not debug:
                    #  spinner.stop()
                    #  print("!!!!!! Error encoding: skipping book... !!!!!!")

                return False 
                                
            # Chapters (2nd stage):Process each chap
            x=0
            for chap in audio_file_data['chapters']:    
                # dont print for each chapter only show the original file printed above
                # track num
                ffmpeg_track_num = str(audio_file_data['chapters'][chap]['id'])
                
                # Output file name
                ffmpeg_output = mktmpdir(os.path.join(ffmpeg_output_chap_temp_dirname, audio_file_data['chapters'][chap]['name'] + \
                                             "." + config['preferred']['audio_output_format']))

                # metadata track info
                #  ffmpeg_metadata_track = " -metadata track=\"" + ffmpeg_track_num + "/" + ffmpeg_track_total + "\""

                # Time (durration/start time)
                if float(audio_file_data['chapters'][chap]['start_time']) == 0:
                    ffmpeg_time = " -t " + str(audio_file_data['chapters'][chap]['duration'])
                else:
                    ffmpeg_time = " -ss " + str(audio_file_data['chapters'][chap]['start_time']) + " -t " + \
                        str(audio_file_data['chapters'][chap]['duration'])                

     
                # Encoding: ffmpeg command: spliting chapters (2nd stage)
                ffmpeg_cmd = "FFREPORT=file=\"" + ffmpeg_log_file + ":level=40\" ffmpeg -loglevel error -y -i \"" + ffmpeg_single_tmp + "\"" + ffmpeg_time + \
                    " -c:v copy -c:a copy \"" + ffmpeg_output + "\""

                logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
                logger.debug(" ~~~~~~~~~~~~~~ ( Chap " + ffmpeg_track_num + " ) ~~~~~~~~~~~~~~~~~~~~") 
                logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
 
                logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ encoding split chap (2nd stage)~~~~~~~~~~~~~~~~~~~~~")
                #  logger.debug(" ~    metadata tracks: " +  ffmpeg_metadata_track)
                logger.debug(" ~    metadata: " +  ffmpeg_metadata)
                logger.debug(" ~    record time: " +  ffmpeg_time)           
                #  logger.debug(" ~    tmp filename: " +  chap_filename_tmp)
                logger.debug(" ~    output dir: " +  ffmpeg_output_chap_temp_dirname)           
                logger.debug(" ~    output: " +  os.path.basename(ffmpeg_output))
                logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ encoding split chap (2nd stage) ~~~~~~~~~~~~~~~~~~")
                logger.debug(" ~ CMD: " + ffmpeg_cmd)
                logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                if debug:
                    logger.debug("      Spliting chapter: " + ffmpeg_track_num + "/" + ffmpeg_track_total)
                #  else:
                    #  print("         Splitting chapter: " + ffmpeg_track_num + "/" + ffmpeg_track_total)

                # Reencode command (Chap: 2nd stage)             
                print_time(logger)
                encoder_error = reencode_audio_file_ffmpeg(logger, ffmpeg_cmd, ffmpeg_input, ffmpeg_output, log_file, ffmpeg_log_file)
                print_time(logger)
                #  encoder_error = reencode_audio_file_ffmpeg(logger, ffmpeg_cmd, ffmpeg_input, ffmpeg_output_tmp, ffmpeg_cover_art)
                
                if encoder_error:
                    logger.error("Encoding failed, skipping chapter spliting and keeping original, " + ffmpeg_input)
                    logger.debug("Encoding failed on \"" + audio_file_data['chapters'][chap]['name'] + "\", stopping encoding of rest of book")
            
                    files_complete.append({'file': ffmpeg_input_old, 'status': 'failed'})
                    #  if not debug:
                        #  spinner.stop()
                        #  print("!!!!!!! Error: encoding failed of chapter.  Skipping files. !!!!!!")
                    #skipping
                    #  break
                    # I this this should be a return not a break for error
                    return False


                # run the encoding
                #  encoder_error = reencode_audio_file_ffmpeg(logger, ffmpeg_cmd_add_art, ffmpeg_output_tmp, ffmpeg_output, ffmpeg_cover_art)
                 
                # Add Metadata:
                #   to audio file (currently only add cover art because ffmpeg stuff works as is, 
                #   so why change it)
                #  if debug:  logger.debug("         Adding cover art and ID3 tags")
                #  else:       print("         Adding cover art and ID3 tags")
                #   add_metadata(logstuff, audiofilename, audiodatadic, chapnumber)
                if not config['preferred']['disable_id3_change']:
                    meta_status = add_metadata(logger, ffmpeg_output, audio_file_data, \
                                               audio_file_data['chapters'][chap]['id'])
                



            # temp dir temp to move
            temp_output = ffmpeg_output_chap_temp_dirname
            # dir to move to [input_file_loc]/[title_sub_dir]
            final_output = os.path.join(input_files_dir,ffmpeg_output_subdir)
        else:
            #---------------------------------------------------------------------------------------------------
            #- Encoding - Not-Chaptered
            #-
            #  ffmpeg_output = os.path.join(temp_root_dir,os.path.basename(ffmpeg_input))
            
            # Creating ffmpeg command
            ffmpeg_cmd = "FFREPORT=file=\"" + ffmpeg_log_file + ":level=40\" ffmpeg -loglevel error" + " -y -i \"" + ffmpeg_input + "\"" + ffmpeg_audio_codec + \
                ffmpeg_bitrate + ffmpeg_samplerate + ffmpeg_metadata + ffmpeg_loudnorm + " \"" + \
                ffmpeg_output + "\""

            logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            logger.debug(" ~~~~~~~~~~~~~~~~~~ffmpeg cmd (not chap)~~~~~~~~~~~~~~~~~")
            logger.debug(" ~   FFMPEG flags")
            logger.debug(" ~    bitrate: " +  ffmpeg_bitrate)
            logger.debug(" ~    samplerate: " +  ffmpeg_samplerate)
            #  logger.debug(" ~    cover art: " +  ffmpeg_cover_art)
            logger.debug(" ~    metadata: " +  ffmpeg_metadata)
            logger.debug(" ~    loudnorm: " +  ffmpeg_loudnorm)
            logger.debug(" ~    audio codec: " +  ffmpeg_audio_codec)
            logger.debug(" ~    input: " +  os.path.basename(ffmpeg_input))
            logger.debug(" ~    output: " +  os.path.basename(ffmpeg_output))
            logger.debug(" ~~~~~~~~~~~~~~~~~~ffmpeg cmd (not chap)~~~~~~~~~~~~~~~~~")
            logger.debug(" CMD: " + ffmpeg_cmd)
            logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

            if no_need_to_reencode:
                if debug:
                    logger.debug("      Skipping: This file has likely already been encoded by this program.")
                #  else:
                    #  print("      Skipping: This file has likely already been encoded by this program.")
                # stop spinner
                files_complete.append({'file': ffmpeg_input_old, 'status': 'skipped'})
                #  if not debug:
                    #  spinner.stop()
                # skipping, no error
                return True
        
 
            # Encoding file, without chapter start message
            if debug:
                logger.debug("    Encoding (" + str(file_count) + " of " + str(total_count) + "): " + os.path.basename(ffmpeg_input_old) )           
            if os.path.isfile(ffmpeg_input):
                # Send to Encoder
                print_time(logger)
                encoder_error = reencode_audio_file_ffmpeg(logger, ffmpeg_cmd, ffmpeg_input, ffmpeg_output, log_file, ffmpeg_log_file)
                print_time(logger)
            else:
                # this shouldn't happen
                logger.error("      Error: input file to ffmpeg doesn't exist.  This shouldn't happen!")
                logger.error("        Filename: " + ffmpeg_input)

                files_complete.append({'file': ffmpeg_input_old, 'status': 'failed'})
                # stop spinner
                #  if not debug:
                    #  spinner.stop()
                #skip
                #  encode failed
                return False
 
            # error detected
            if encoder_error and config['preferred']['save_files_with_error']:
                    return False
            elif encoder_error:
                logger.error("Encoding failed")
                # encoding failed
                 # stop spinner
                files_complete.append({'file': ffmpeg_input_old, 'status': 'failed'})
                #  if not debug:
                    #  spinner.stop()
                return False
            else:
                # no errors add meta     
                # Add Metadata to audio file (currently only add cover art because ffmpeg stuff works as is, so why change it)
                if debug:
                    logger.debug("         Adding cover art and ID3 tags")
                #  else:
                    #  print("         Adding cover art and ID3 tags")
                #   add_metadata(logstuff, audiofilename, audiodatadic, chapnumber)
                meta_status = add_metadata(logger, ffmpeg_output, audio_file_data, None)
 
            # single file to be moved
            temp_output = ffmpeg_output
            
            # file to move to
            final_output = os.path.splitext(ffmpeg_input)[0] + '.' + config['preferred']['audio_output_format']
        # End: single file encoding

        # Error delete tmp FIXME, i dont think this actually runs all errors return earlier
        if encoder_error:
            logger.debug("encoding failed, deleting temporary file:")
            if not config['preferred']['test'] and os.path.exists(temp_output):
                os.remove(temp_output)
            # stop spinner
            #  if not debug:
                #  spinner.stop()

            files_complete.append({'file': ffmpeg_input, 'status': 'failed'})
            return False
        else:
            # Success: All encoding 
            
            # Remove original file
            if os.path.exists(audio_file_data['filename']) and \
                    not config['preferred']['keep_original_files'] and \
                    not config['preferred']['test']:
                os.remove(audio_file_data['filename'])
    

            # Moving temp to new files
            if chapter_it: 
                # Chaptered
                logger.debug("Encoding success: moving old file to backup(in desired), moving new file to original")
                
                # Moving temp files to final location
                if not config['preferred']['test']:
                    if config['preferred']['keep_original_files']:
                        # Create backup
                        new_filename = mktmpdir(os.path.join(os.path.dirname(ffmpeg_input), \
                                                    "original-" + os.path.basename(ffmpeg_input)))
                        if os.path.exists(new_filename):
                            new_filename = mktmpdir(os.path.join(os.path.dirname(ffmpeg_input), \
                                                        "original2-" + os.path.basename(ffmpeg_input)))
                        shutil.move(ffmpeg_input,new_filename)
                    # Move temp to original location
                    if os.path.exists(final_output):
                        # if folder already exists , move to "folder-new"
                        if os.path.isfile(final_output): # it should be a dir but just in case
                            final_output = mktmpdir(os.path.splitext(final_output)[0] + '-new.' +  os.path.splitext(final_output)[1])
                        elif os.path.isdir(final_output):
                            final_output = mktmpdir(final_output + "-new")
                        logger.debug("Moving: " + temp_output + "\nTo: " + final_output)
                        shutil.move(temp_output,final_output)
                    else:
                        # original gone, move temp to original location
                        logger.debug("Moving: " + temp_output + "\nTo: " + final_output)
                        shutil.move(temp_output,final_output)

            else: 
                # Single file
                if not config['preferred']['test']:
                    if config['preferred']['keep_original_files']:
                        # backup files
                        new_filename = mktmpdir(os.path.join(os.path.dirname(ffmpeg_input), "original-" + os.path.basename(ffmpeg_input)))
                        if os.path.exists(new_filename):
                            new_filename = mktmpdir(os.path.join(os.path.dirname(ffmpeg_input), "original2-" + os.path.basename(ffmpeg_input)))
                        shutil.move(ffmpeg_input,new_filename)
                    if os.path.exists(final_output):
                        # if file already exists , delete, it shouldn't be there anyway
                        os.remove(final_output)
                    shutil.move(temp_output,final_output)
            # End: Moving

    files_complete.append({'file': final_output,'status': 'success'})
    # success
    return True
# End encode_audio_files()




##########################################################
# Run ffmpeg to actually re-encode
#
def reencode_audio_file_ffmpeg(logger, ffmpeg_cmd, ffmpeg_input, ffmpeg_output, log_file, ffmpeg_log_file):
    """
    actual encoding function
    """
    found_error = False

    if not config['preferred']['test']:
        pp = subprocess.Popen(ffmpeg_cmd , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (output, err) = pp.communicate() # execute
        pp_status = pp.wait() # wait for command to finish

        # check if encoding failed
        if err:
            found_error = True
            logger.debug("ffmpeg error: " + str(err))

            # Ignore the error, put file in original state, delete file with error
            if config['preferred']['ignore_errors']:
                # delete failed file
                if os.path.isfile(ffmpeg_output): 
                    os.remove(ffmpeg_output)
            else:
                # Encoding failed, Exiting
                if debug: 
                    logger.debug("Exiting after failure")
                else: 
                    print("\n<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>")
                    print("!!! Error: ffmpeg encoding failed!!!")
                    print(" See log for details.")
                    print(" audiobook_reencode log: " + log_file)
                    print(" ffmpeg log: " + ffmpeg_log_file)
                    print("<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>")
        else:
            found_error = False
            # encoding succeded

    return found_error
# end reencode_audio_file_ffmpeg()





#############################################################
# Extract embedded cover art
#
def extract_cover_art_ffmpeg(logger, audio_file):
    """
    Extract the cover art
    """



    # Temp Dir
    img_tmp_dir = mktmpdir(os.path.join(config['TMP']['tmp_dir'], os.path.basename(os.path.dirname(audio_file))))

    # Create random filename
    random_cover_art_name = mktmpdir(os.path.join(img_tmp_dir, str(int(random.random()*10000000000000000)) + ".jpg"))

    cmd = 'ffmpeg -y -i "' + audio_file + '" "' + random_cover_art_name + '"'
    logger.debug("^ > ffmpeg extracting: " + os.path.basename(random_cover_art_name)) # + output_file)
    logger.debug("^     " + cmd)
    if not config['preferred']['test']:
        pp = subprocess.Popen(cmd , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (output, err) = pp.communicate() # execute
        pp_status = pp.wait() # wait for command to finish
        # logger.debug(err)
    return random_cover_art_name
# end extract_cover_art_ffmpeg





########################################################
# Detect cover art image file
#
def detect_cover_art_image_file(logger, dirpath):
    """
    scan folder for image files, check if audio filenames are similar so we know if cover art applies to all

    """
    cover_art = ''
    dir_cover_art = ''

    # See if we can fing cover art in dir
    if True:
        # jpg/png (full dir)
        cover_art_list = glob.glob(os.path.join(dirpath,'*.[pP[nN][gG]')) + glob.glob(os.path.join(dirpath,'*.[jJ][pP][gG]')) 
        # mp3_files = glob.glob(os.path.join(dirpath,'*.[mM][pP]3'))
        # m4b_files = glob.glob(os.path.join(dirpath,'*.[mM]4[aAbB]'))
        # audio_files = mp3_files + m4b_files

        # Set the cover art to image in dir
        if cover_art_list:
            # Check if a likly image is cover art
            # logger.debug("-   > Images exists: " # + str(cover_art_list))
            for image in cover_art_list:
                # cover.jpg or cover.png is the most likly
                if( re.search(r'cover\.jpg$', image, re.IGNORECASE) or re.search(r'cover\.png$', image, re.IGNORECASE) ):
                    return image

                elif( re.search('cover', image, re.IGNORECASE) ): 
                    # prefer in cover is used anywhere in name
                    return image

                elif(image): # not empty
                    # otherwise use the first image
                    return image

                else:
                    logger.error("Error/Bug in program: cover art image was found, yet not.")
                    return ''
        else:
            # Extract cover art from audio file
            logger.debug("-    > No image files, cover art in dir")
            return ''

# End: detect_cover_art_image_file()






########################################################
# Extracting cover art from directory or mp3 file
#
def extract_cover_art(logger, audio_file, audio_file_data):
    """
    # extracts and/or sets cover art
    # preference, embedded
    # if embedded
    #   extract to temp folder
    # if no embedded, 
    #   check for filename similarity in dir
    #       check for image in dir
    #           set cover art
    # else 
    #   cover art False
    #
    # Notes: need to keep audio_files var because only doing one dir at a time
    """


    cover_art = ''
    dir_cover_art = ''




    # See if embedded art exists


    # Extracting when the file chapters
    # if not config['preferred']['disable_split_chapters'] and audio_file_data
    # TODO FIX


    if True:
            # Check if a file in dir has embedded art
            file_with_embedded_cover_art = ''
            logger.debug(" ^^^^^^^^^^^^^^^^^ Extract Cover Art (dirpath) ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            # add similarity to data file, just in case needed
            #  audio_file_data[audio_file]['dir_filename_similarity'] = dir_filename_similarity
            # extract art
            if audio_file_data[audio_file]['cover_art_embeded']:
                file_with_embedded_cover_art = audio_file
                
                #extract cover art
                cover_art_file = extract_cover_art_ffmpeg(logger, audio_file)
                #  extract_cover_art_ffmpeg(logger, file_with_embedded_cover_art, random_cover_art_name, single_file)
                
                # Save cover art location in dict
                audio_file_data[audio_file]['cover_art_file'] = cover_art_file
                logger.debug("^    > Audio File: " + os.path.basename(audio_file))
                logger.debug("^         > Using cover art embedded in : " + os.path.basename(cover_art_file))
                audio_file_data[audio_file]['cover_art_file'] = cover_art_file
                audio_file_data[audio_file]['cover_art_embeded'] = True

            else:
                logger.debug("^    > Audio File: No cover art: " + os.path.basename(audio_file))
            logger.debug(" ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")


    return audio_file_data
# end def extract_cover_art







#############################################################
# Print a string of 80 chars, fill in with spaces
#
def print_80_char(text):
    """
    prints a string of 80 chars or more"""


    while len(text) < 80:
        text += " "

    print(text)

# End: print_80_char()


##############################################################
# Check similarity of list of filenames
#
def filename_similarity(logger, filename_list):
    """
    Check the similarty of filenames in a dir
    if they are similar, they can use common cover art
    """

    # if there is only one file no calculation needed
    if (len(filename_list) <= 1):
        logger.debug("-    > Filename similarity, single file, 100%")
        return True

    # Calculate a percentage of files similarity
    ratios = []
    s = SequenceMatcher()
    # Pass though list and compare with each other item in list
    # then average the ratio
    #   removeing file numbers count improves accuracy, ie 001 002 003
    for a in filename_list:
        abase = re.sub('[0-9]?[0-9][0-9]', '', os.path.basename(a))
        s.set_seq2(abase)
        for b in filename_list:
            bbase = re.sub('[0-9]?[0-9][0-9]', '', os.path.basename(b))

            if not abase == bbase:
                s.set_seq1(bbase)
                ratios.append(int(100 * s.ratio()))
    
    # Calculate average of ratios
    if not len(ratios): 
        avg_ratio = 100 # may happen if all modified filenames are the same ie files named 001-32k.mp3
    else:
        avg_ratio = sum(ratios)/len(ratios)
        
    logger.debug("-    > Filename similarity ratio: " + str(avg_ratio) + "% (Cut off set to " + str(filename_similarity_cover_art_percentage) + "%)")
    
    # If percentage is large enough, then they are similar
    if avg_ratio >= filename_similarity_cover_art_percentage:
        return True
    else:
        return False
# end filename_similarity



#################################################
# Print intro banner
#
def print_banner(log_filename, config):
    # print info
    print("╭─────────────────────────────────────────────────────────────────────╼")
    print("│ Audiobook Tools: " + program_name)
    print("│  Encoder settings: " + config['preferred']['audio_output_format'] + " @ " + config['preferred']['bitrate'] + "bps/" + config['preferred']['samplerate'] + "Hz")
    options = []
    #  if not config['preferred']['disable_add_id3_genre']:
        #  options.append('genre')
    if not config['preferred']['disable_embed_cover_art']:
        options.append( 'cover art')
    if not config['preferred']['disable_normalize']:
        options.append ( 'normalize')
    if not config['preferred']['disable_delete_unneeded_files']:
        options.append ( 'remove cue/nfo/m3u')
    if config['preferred']['keep_original_files']:
        options.append ( 'keep originals')
    if not config['preferred']['disable_split_chapters']:
        options.append ( 'split chapters')
    if config['preferred']['force_reencode']:
        options.append('force reencode')
    #  else:
        #  options.append('skip lower ')

    option_str = ", ".join(options)
    from textwrap import wrap
    option_str_array = wrap(option_str, 70)
    print("│  Options: ")#, end="")
    for text in option_str_array:
        print("│    " + text)
    print("│  Log file: ")
    print("│    " + log_filename)
    print("╰──────────────────────────────────────────────────────────────────────╼")
# End: print_banner()






#####################################################
# Summary of all files
#
def print_summary(config): #common_vars):
    """ 
    print info
    """
    threads =  int(config['preferred']['threads'])
    global total_duration
    global total_file_count

    print("╭─────────────────────────────────────────────────────────────────────╼")
    print_80_char("│ Summary of files:  ") 
    print_80_char("│  File count: " + str(total_file_count) )
    print_80_char("│  Total audiobooks duration: " + str(round(total_duration/60/60,1)) + "h")
    print_80_char("│  Estimated encoding time: " + str(round(total_duration / threads / encode_speed_ratio /60/60,2)) + "h (very rough estimate)")
    print("╰──────────────────────────────────────────────────────────────────────╼")

# End: print_summary()






##################################################
# Make TMP folder
#
def mktmpdir(tmp_file):
    """
    checks and creates tmp folder if nessesary
    """
    tmp_dir = os.path.dirname(tmp_file)

    # check and create dir
    os.makedirs(tmp_dir, exist_ok=True)


    return tmp_file
# End: mktmpdir()






##################################################
# Print time for debuging
#
def print_time(logger):
    """
    prints time foe debuging
    """
    #  logger.debug()
    logger.debug("{{{{{{{{{{{{{{{{{{{{ Time: " + str(round(time.time() - start_time,3)) + "s }}}}}}}}}}}}}}}}}}}}}}")
    #  logger.debug()
# End print_time(logger)





##################################################
# Collecting info on files
#
def collect_file_info(logger, config, path, log_filenames):
    """
    collecting audio file info
    """

    # initialize
    audio_file_data = {}
    unneeded_files = []
    global total_file_count
    global total_duration
    #  debug = config['preferred']['debug']
    
    # initialize spinner
    spinner = Spinner()
 
    if debug: 
        logger.debug("Collecting audiobook files info...")
    else:
        #  print("Generating audiobook files data...", end="", flush=True)
        # start spinner for collecting data
        print("◎ Collecting audiobook files info...")
        spinner.start("")
   
    # Processing
    if os.path.isfile(path):
        # Process a single file
           # audio_file_data.update( process_directory(logger, dirpath, audio_files, audio_file_data) )      
        audio_file = [path]
        # audio_file_data[audio_file] = {}
        dirpath = os.path.dirname(path)
#! fix me
        audio_file_data = process_directory(logger, log_filenames, dirpath, audio_file, audio_file_data, True)

    else:
        # Not a single file: Walk though the directories to process audio folders
        for (dirpath, dir_list_in_dirpath, file_list) in os.walk(path):
            logger.debug(" ......................................................................")
            logger.debug(" : Processing directory: " + dirpath)
            # print(" Entering directory: " + dirpath

            # Get lists of mp3, m4b/m4a, and jpg/png
            #  mp3_files = glob.glob(os.path.join(dirpath,'*.[mM][pP]3'))
            #  m4b_files = glob.glob(os.path.join(dirpath,'*.[mM]B]'))
            #  audio_files = mp3_files + m4b_filesbb

            # Adds mp3/m4b/m4a/aax/ogg/flac/opus
            audio_files_tmp =  glob.glob(os.path.join(dirpath,'*.[mM][pP]3')) +\
                glob.glob(os.path.join(dirpath,'*.[mM]4[aAbB]')) +\
                glob.glob(os.path.join(dirpath,'*.[oO][gG][gG]')) +\
                glob.glob(os.path.join(dirpath,'*.[aA][aA][xX]')) +\
                glob.glob(os.path.join(dirpath,'*.[fF][lL][aA][cC]')) +\
                glob.glob(os.path.join(dirpath,'*.[oO][pP][uU][sS]')) +\
                glob.glob(os.path.join(dirpath,'*.[mM][pP]4'))

            # Ignore dirs with audio extentions
            audio_files = []
            for file in audio_files_tmp:
                if os.path.isfile(file):
                    audio_files.append(file)
                    total_file_count += 1

            # Create list of *.cue, *.m3u, *.nfo
            if not (config['preferred']['only_reencode'] or config['preferred']['only_add_id3_genre']) and not config['preferred']['disable_delete_unneeded_files']:
                logger.debug("-  Checking dir for unneeded files")
                unneeded_files += glob.glob(os.path.join(dirpath,'*.[nN][fF][oO]'))
                unneeded_files += glob.glob(os.path.join(dirpath,'*.[cC][uU][eE]'))
                unneeded_files += glob.glob(os.path.join(dirpath,'*.[mM]3[uU]'))

            # Process directory if mp3/m4b/m4a is found
            if not config['preferred']['only_delete_unneeded_files']:
                if ( not audio_files):
                    logger.debug("   No audio files found in dir (mp3/m4b/m4a/aax/ogg/flac/opus)")
                else:
                    logger.debug("-  Audio found in dir")
                    logger.debug("`````````````````````` audio files in (" + dirpath + ") ```````````") 
                    logger.debug(pprint.pformat(audio_files))
                    logger.debug("`````````````````````````````````````````````````````````````````")
                    # Add audio files to audio_file_data - Merger dictionaries
                    audio_file_data.update( process_directory(logger, log_filenames, dirpath, audio_files, audio_file_data) )
        # end of walk through directories
        

        # Delete un-needed files, removes *.cue, *.m3u, *.nfo
        if not (config['preferred']['only_reencode'] or config['preferred']['only_add_id3_genre']) and not config['preferred']['disable_delete_unneeded_files']:
            if debug: print("Deleting unneeded (nfo/cue/m3u) files...")
            for file_name in unneeded_files:
                logger.debug("-  Deleting unneeded file: " + file_name)
                if not config['preferred']['test']:
                    os.remove(file_name)
 

    # Stop spinner
    if not debug:
        spinner.stop()

    print_time(logger)

    # data of all files
    #  total_data = [total_file_count, total_duration]
    return audio_file_data
# End: collect_file_info





#########################################################
# add file to encode to Queue
#
def add_to_queue(q):
    """
    add to queue
    """
    while True:
        try:
            #  [name, path] = q.get()
            [logger, log_filenames, audio_file_data, file_count, total_count, dirpath,file_name] = q.get()

            success = reencode_audio_file(logger, log_filenames, audio_file_data[os.path.join(dirpath,file_name)], file_count, total_count)
            q.task_done()
            #  return
        except queue.Empty:
            return
# End: add_to_queue()







#########################################################
# Encode files
#
def encode_files(logger, config, log_filenames, path, audio_file_data):
    """
    encode all files
    """
    

    # initialize spinner
    spinner = Spinner()
 
    # initialize 
    error_list = []
    total_count_to_encode = 0

    from queue import Queue
    from threading import Thread

    max_threads = int(config['preferred']['threads'])

    q = Queue(maxsize=0)

    # Create some threads posibilities
    for i in range(max_threads):
        worker = Thread(target=add_to_queue, args=(q,))
        worker.setDaemon(True)
        worker.start()


    # Encoding the files through the list
    # Re-encode the audio file
    total_count = len(audio_file_data)
    file_count = 1
    if debug:
        logger.debug("Encoding starting... ")
    else:
        print("◎ Encoding starting... ")
    if os.path.isfile(path):
        # encoding a single file (no extra thread)
        total_count_to_encode = 1
        success = reencode_audio_file(logger, log_filenames, audio_file_data[path], file_count, total_count)
        if not success:
            error_list.append(audio_file_data[path])
            print("Error: Encoding failure detected.")
            # exit all
            worker.terminate()
            worker.join()
            sys.exit(1)
    else:
        # encoding directory
        for (dirpath, dir_list_in_dirpath, file_list) in os.walk(path):
            # walking the dir again so encoding processes in logical order (maybe change to add numbering to audio_file_data var)

            # add indented dir tree 
            # https://stackoverflow.com/questions/41632989/combine-output-of-multiple-os-walk-runs
            level = dirpath.replace(path, '').count(os.sep)
            subindent = ''
            #  if level > 0:
                #  indent = ' ' * (level-1) + '>'
            subindent = '   ' * (level) + '↳ '
            print("  " + subindent + os.path.basename(dirpath) + "/")

            # sort file list so its in alpha numberic order
            #  print_time()
            #  logger.debug(">>>>>>> sort file list so its in alpha numberic order <<<<<<<<<")
            file_list.sort()
            #  print_time()


            for file_name in file_list:

                """
                https://www.tutorialspoint.com/python/python_multithreading.htm
                https://www.troyfawkes.com/learn-python-multithreading-queues-basics/
                # within loop
                thread_cnt=0
                threading.activeCount()
                isAlive()
                if thread_cnt <= thread_max:
                    thread_1 = open thread()
                    thread_cnt += 1
                """


                if 'read_data_failed' in audio_file_data:
                    # reading data filed earlier, so skiping encoding
                    print("Skip encoding \"" + file_name + "\", likly has an error in it")
                    logger.error("Skip encoding \"" + file_name + "\", likly has an error in it")
                else:
                    if os.path.join(dirpath, file_name) in audio_file_data:
                        if not (config['preferred']['only_extract_cover_art'] or config['preferred']['only_delete_unneeded_files']):
                            # preform action
                            
                            success = True
                            #  q.put([file_name, dirpath])
                            # create a count for ques
                            total_count_to_encode += 1
                            
                            # Add to queue: add a file to the encoding queue
                            q.put([logger, log_filenames, audio_file_data, file_count, total_count, dirpath, file_name])

                            file_count += 1


    time.sleep(1)

    # counts
    files_count_current = total_count_to_encode - q.qsize()
    files_count_past = 1
    # arrays
    files_list_past = files_complete
    #  last_files = True
    # print
    last_file = ''

    print(" ◎ Encoding progress...                                             ")

    # print any files done or skipped in the first second
    x = 0
    skipped = False
    while x < files_count_current -1:
        try:
            files_complete[x]['status']
        except IndexError:
            break
        if(files_complete[x]['status'] == 'skipped'): # dont print each file if skipped
            skipped = True
        else:
            print( "   ⊛ " + files_complete[x]['status'] + ": " + files_complete[x]['file'] )
        x += 1
    if(skipped):
        print( "   ⊛ some files skipped")

    # print files as they complete and display spinner
    spinner.start("➤ Encoding: (" + str(files_count_current) + " of " + str(total_count_to_encode) + ")" )
    # loop until done encoding all files
    while not q.empty():
        #  print(q.qsize())
        # wait until recompair
        time.sleep(0.01)
        # is there a change?
        #  print(" q=" + str(q.qsize()) + "; current=" + str(files_count_current) + "; past=" + str(files_count_past))
        files_count_current =  total_count_to_encode - q.qsize()
        if not files_count_past == files_count_current and len(files_complete) > 0:
            # stop spinner
            spinner.stop()
            del spinner # removes flicker bug


            print("   ⊛ " + files_complete[-1]['status'] + ": " + files_complete[-1]['file'] )
            files_count_past = files_count_current
            last_file = files_complete[-1]['file']


            spinner = Spinner()
        #      pprint.pprint(change_list)
            spinner.start("➤ Encoding: (" + str(files_count_current) + " of " + str(total_count_to_encode) + ")" )

    q.join()
    spinner.stop()
    del spinner

    #  pprint.pprint( last_file  )
    # sometimes the last few dont get caught
    if len(files_complete) >0:
        if not files_complete[-1]['file'] == last_file:
            #  if len(files_complete) > 1:
                #  if not files_complete[-2]['file'] == last_file:
                    #  print("   ⊛ " + files_complete[-2]['status'] + ": " + files_complete[-2]['file'] ) # print next to last
            print("   ⊛ " + files_complete[-1]['status'] + ": " + files_complete[-1]['file'] ) # print last
    #  print("╰─────────────────────────────────────────────────────────────────────────╼   ")

    #
    return error_list
# End: encode_files()






##################################################
# main function
#
def main():
    """
    Main fuction
    """
    

    # initialize
    audio_file_data = {}
    unneeded_files = []
    error_list = []
    #  files_complete = []
  
    start_time = time.time()

    # CLI Arguments
    global args, path, debug
    args = parse_args()
    # generate config settings
    global config

    #  global files_complete
    # Create Temp Dir
    tmp_dir = mktmpdir(os.path.join(tempfile.gettempdir(), 'audiobook_reencode', str(random.randrange(1,99999999))))

    # Load config file
    config = load_config("audiobook-reencoder.conf", args, tmp_dir)
    path = args.directory
    debug = config['preferred']['debug']
       # Setup logging
    [logger, log_filenames] = setup_logging()
    [log_filename, log_ffmpeg, log_ffmpeg_error] = log_filenames

    # Input/Arguments Error checks
    error_checking(logger, path)

   #  spinner = spin()


    # banner for test
    if config['preferred']['test']:
        print("******************************************************")
        print("* Running in test mode, no actions will be performed *")
        print("******************************************************")

    
    logger.debug("************************ directories ************************************")
    logger.debug("* Root directory: " + path)
    logger.debug("* Temp dir: " + tmp_dir)
    logger.debug("************************* directories (end) *******************************")
    logger.debug('~~~~~~~~~~~~~~~~~~~~ Config ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    logger.debug(pprint.pformat(config))
    logger.debug('~~~~~~~~~~~~~~~~~~~~ Config (end) ~~~~~~~~~~~~~~~~~~~~~~~')


    # Print Banner
    print_banner(log_filename, config)


    print_time(logger)


    #  common_vars = {'logger': logger,
                   #  'config': config,
                   #  'spinner': spinner,
                   #  'path': path,
                   #  'log_filenames': log_filenames,
                   #  'debug': debug}


    # Collect the audio file info and store in var
    audio_file_data = collect_file_info(logger, config, path, log_filenames)

    #print a summary of files
    print_summary(config) #common_vars)

    # encode all files
    error_list = encode_files(logger, config, log_filenames, path, audio_file_data)


    # All done
    # clean up tmp dir at end
    #  clean_up_tmp_dir(logger)
   
    #  pprint.pprint(files_complete)
    # Print out all errors before exit
    if not len(error_list) == 0:
        print("done.")
        print("!!!!!! Error: some files had encoding errors, failed files !!!!!!")
        #  for file in error_list:
            #  print("• " + str(file[file_name]) + "\n")
        print("!!!!!! Read log for details: " + log_filename + " !!!!!!")
        exit(1)

    stop_time = time.time()

    # not sure this does anything
    #  print_error_file(log_filename)

    #  print_time(logger)

    error_cnt = 0
    success_cnt = 0
    skip_cnt = 0

    # TODO add sort
    error_text = "╭─────────────────────────────────────────────────────────────────────────╼\n"
    error_text += "│ Encoding FAILED with following files:                    \n"
    for i in range(len(files_complete)):
        if files_complete[i]['status'] == 'failed':
            error_text += "│   ⊛ " + files_complete[i]["file"] + "      \n"
            error_cnt += 1
        if files_complete[i]['status'] == 'skipped':
            skip_cnt += 1
        if files_complete[i]['status'] == 'success':
            success_cnt += 1
    error_text += "│ See logfile for details: \n"
    error_text += "│   " + log_filename + "\n" 
    error_text += "╰────────────────────────────────────────────────────────────────────────╼"

    if error_cnt > 0:
        print(error_text)
    #  pprint.pprint(files_complete)

    print("╭────────────────────────────────────────────────────────────────────────╼")
    print("│ Encoding summary:                                     ")
    #  print("│   Total file duration time: " + str(round((total_duration),1)) + "s")
    print("│   Successful: " + str(success_cnt))
    print("│   Failures: " + str(error_cnt))
    print("│   Skipped: " + str(skip_cnt))
    print("│   Encoding time: " + str(round((stop_time-start_time)/60/60,1)) + "h")
    print("│   Encoding rate: " + str(int(total_duration/(stop_time-start_time))) + " x")
    print("╰─────────────────────────────────────────────────────────────────────────╼")


   # spaces are a workaround for spinner output problem when len(text) < len(spinner)
    print("done.                                    ")
    exit(0)
# end main




###########################################
# Start it up
#
if __name__ == "__main__":
   main()
