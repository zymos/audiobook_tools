#!/usr/bin/python
# -*- coding: latin-1 -*-

#####################################################################
#	audiobook_reencode
#
#	Description: Re-encode all audiofile in a directory, with some 
#           bells and whistles
# 
#	Usage: id3_cover_art [DIRECTORY]
#
#	Author: ZyMOS, 03/2020
#
#       Requirements:
#           python, ffmpeg, ffprobe
#
#       Features: 
#           Encodes using ffmpeg
#           Accepts mp3, m4b, m4a (todo maybe flac)
#           Grabs audio files data using ffprobe, for re-encoding and embedding cover art
#           Split into chapters (not implemented)
#           Removes unneeded files (nfo/cue/m3u) (can be disabled)
#           Add genre="Audiobook" (can be disabled)
#           Normalize volume (can be disabled)
#			Won't re-encode if it is obvious it has been done before (can be forced)
#           Cover art:
#               Extracts cover art to cover.jpg (can be disabled)
#               Embeds cover art to each audiofile (can be disabled)
#               If directory contains multiple different audiobooks it won't
#                   try extract/embed cover art
#               Can delete original image file, after embedding (not default)
#
#
#       How the program works:
#           Walk through each subdirectory in the main directory
#               Check if audio exists in each directory
#                   Work on getting cover art
#                       Check if filenames in directory are similar
#                           Check if image file exist, otherwise try to extract it
#                   Generate data on each audio file
#           Process files though list
#               re-encode if bitrate is higher or changing format 
#               with settings from data compiled
#
#                           
#
#####################################################################



#####################################################################
# Global variables
#

# Defaults
bitrate_default = "32k"
samplerate_default = "22050"
version = "0.1"
program_name = "audiobook_reencoder(ffmpeg)-v" + version


# Filename's similarity ratio in a directory, 
#   must be >= for cover art to be added
#   this is to prevent adding cover art to a dir with diff audiobooks
filename_similarity_cover_art_percentage = 85








#####################################################################
# Includes
#
import argparse # CLI inputs
import os
import glob # searching file types
import re #regex
import subprocess # running programs
from difflib import SequenceMatcher # fuzzy matching of filenames
import pprint
import tempfile # for logging
import logging # for logging
import datetime # for logging




#####################################################################
# CLI Arguments
#
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
parser.add_argument('--bitrate', help="8k, 16k, 32k, 64k, 128k, etc (default 32k)")
parser.add_argument('--samplerate', help="16000, 22050, 44100, etc (default 22050)")
parser.add_argument('--threads', help="number of CPU threads to use (default 4)(Not Used Yet)")
parser.add_argument('--keep-original-files', help="do not delete original audio files", action="store_true")
parser.add_argument('--test', help="run without any action, extraction or reencoding", action="store_true")
parser.add_argument('--disable-normalize', help="do not normalize volume, faster encoding", action="store_true")
parser.add_argument('--disable-add-id3-encoded-by', help="Don't set ID3 encoded_by=\"" + program_name + "\"", action="store_true")
parser.add_argument('--ignore-errors', help="If there is an encoding failure, program will leave the file as is, and continue processing the rest of files", action="store_true")
parser.add_argument('--disable-id3-change', help="Don't change ID3 tags", action="store_true")
parser.add_argument('--force-normalization', help="Force re-encoder to normalize volume. By default, normalization is skipped if this encoder was likely run previously on file", action="store_true")
parser.add_argument('--delete-non-audio-files', help="Delete all non-audio files(not implemented yet)", action="store_true")
parser.add_argument('--delete-non-audio-image-files', help="Delete all non-audio, or non-image files(not implemented yet)", action="store_true")
# parser.add_argument('--', help="", action="store_true")
# parser.add_argument('--', help="", action="store_true")
# parser.add_argument('--', help="", action="store_true")
# parser.add_argument('--', help="", action="store_true")
parser.add_argument('--debug', help="prints debug info", action="store_true")




args = parser.parse_args()
path = args.directory
debug = args.debug





###############################################################################
# Function
#

# main function
def main():
    
    audio_file_data = {}
    unneeded_files = []

    # Error checks
    error_checking()

    # Setup logging
    logger = setup_logging()

    # banner for test
    if args.test:
        print "******************************************************"
        print "* Running in test mode, no actions will be performed *"
        print "******************************************************"

    
    logger.debug("*********************************************************************")
    logger.debug("* Root directory: " + path)
    logger.debug("*********************************************************************")

    if os.path.isfile(path):
        # Process a single file
        if debug: 
            logger.debug("Generating audiobook data...")
        else:
            print "Generating audiobook files data..."
            # audio_file_data.update( process_directory(logger, dirpath, audio_files, audio_file_data) )      
        audio_file = [path]
        # audio_file_data[audio_file] = {}
        dirpath = os.path.dirname(path)
#! fix me
        audio_file_data = process_directory(logger, dirpath, audio_file, audio_file_data, True)
            # cover_art_file = extract_cover_art_ffmpeg(logger, audio_file, True)
            # audio_file_data[audio_file] = extract_audiofile_data(logger, audio_file)
            # if audio_file_data['cover_art_embeded']:
                # cover_art_file = extract_cover_art_ffmpeg(logger, audio_file, True)               

    else:
        # Walk though the directories to process audio folders
        if debug: 
            logger.debug("Extracting audiobook data from directory...")
        else:
            print "Generating audiobook files data..."
        for (dirpath, dir_list_in_dirpath, file_list) in os.walk(path):
            logger.debug(" ......................................................................")
            logger.debug(" : Processing directory: " + dirpath)
            # print " Entering directory: " + dirpath

            # Get lists of mp3, m4b/m4a, and jpg/png
            mp3_files = glob.glob(os.path.join(dirpath,'*.[mM][pP]3'))
            m4b_files = glob.glob(os.path.join(dirpath,'*.[mM]4[aAbB]'))
            audio_files = mp3_files + m4b_files
            # pprint.pprint(audio_files)

            # Create list of *.cue, *.m3u, *.nfo
            if not (args.only_reencode or args.only_add_id3_genre) and not args.disable_delete_unneeded_files:
                logger.debug("-  Checking dir for unneeded files")
                unneeded_files += glob.glob(os.path.join(dirpath,'*.[nN][fF][oO]'))
                unneeded_files += glob.glob(os.path.join(dirpath,'*.[cC][uU][eE]'))
                unneeded_files += glob.glob(os.path.join(dirpath,'*.[mM]3[uU]'))

            # Process directory if mp3/m4b/m4a is found
            if not args.only_delete_unneeded_files:
                if ( not audio_files):
                    logger.debug("   No audio files found in dir (mp3/m4b/m4a)")
                else:
                    logger.debug("-  Audio found in dir")
                    # Merger dictionaries
                    audio_file_data.update( process_directory(logger, dirpath, audio_files, audio_file_data) )
        # end of walk through directories
        

        # Delete un-needed files, removes *.cue, *.m3u, *.nfo
        if not (args.only_reencode or args.only_add_id3_genre) and not args.disable_delete_unneeded_files:
            print "Deleting unneeded (nfo/cue/m3u) files..."
            for file_name in unneeded_files:
                logger.debug("-  Deleting unneeded file: " + file_name)
                if not args.test:
                    os.remove(file_name)
        else:
            logger.debug("- Not deleting unneeded files")


 
    # print "HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
    # pprint.pprint(audio_file_data)
    # exit()


   # Encoding the files through the list
    # Re-encode the audio file
    total_count = len(audio_file_data)
    file_count = 1
    if debug:
        logger.debug("Encoding starting... ")
    else:
        print "Encoding starting... "
    if os.path.isfile(path):
        # encoding a single file
        reencode_audio_file(logger, audio_file_data[path], file_count, total_count)
    else:
        # encoding directory
        for (dirpath, dir_list_in_dirpath, file_list) in os.walk(path):
            # walking the dir again so encoding processes in expected order
            print "  " + os.path.basename(dirpath) + "/"
            # sort file list so its in alpha numberic order
            file_list.sort()
            for file_name in file_list:
                # print "    >" + file_name
                if os.path.join(dirpath, file_name) in audio_file_data:
                    # print "        yippy"
                    if not (args.only_extract_cover_art or args.only_delete_unneeded_files):
                        # preform action
                        reencode_audio_file(logger, audio_file_data[os.path.join(dirpath,file_name)], file_count, total_count)
                        file_count += 1
    # All done
    print "done."
    exit(0)
# end main




# Setup logging
def setup_logging(): 
    
    # make temp file for log
    temp_root_dir = os.path.join(tempfile.gettempdir(), 'audiobook_reencode')
    if not os.path.isdir(temp_root_dir):
        os.mkdir(temp_root_dir)
    log_file = "audiobook_reencode-log-" + datetime.datetime.now().strftime("%yy%mm%dd-%H-%M") + ".log"
    logfile = os.path.join(temp_root_dir, log_file)

    # format logger
    logFormatter = logging.Formatter("%(asctime)s: %(message)s", datefmt='%I:%M:%S')
    my_logger = logging.getLogger()
    my_logger.setLevel(logging.DEBUG)
		
    # set logger to write to logfile
    fileHandler = logging.FileHandler(logfile)
    fileHandler.setFormatter(logFormatter)
    my_logger.addHandler(fileHandler)

    # set loger to write to stderr if debug
    if args.debug:
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        my_logger.addHandler(consoleHandler)
	
    return my_logger 
# end setup_logging



# Process the directory
def process_directory(logger, dirpath, audio_files, audio_file_data, single_file=False):

    logger.debug("-  Processing directory: " + dirpath)

    
    # Process each file to get data and find cover art
    for audio_file in audio_files:
        logger.debug("-  Grabing files data: " + os.path.basename(audio_file))

        # Grab some embeded data and stats
        audio_file_data[audio_file] = extract_audiofile_data(logger, audio_file)


    # Extract the cover art from audio file to cover.jpg
    if not (args.only_delete_unneeded_files or args.only_add_id3_genre or args.only_reencode):
        cover_art_file = extract_cover_art(logger, dirpath, audio_files, audio_file_data, single_file)
    else:
        cover_art_file = ''
    # print "ooooooooooooooooooooooooooooooooooo" + cover_art_file

    # Process each file in the current directory
    for audio_file in audio_files:
        logger.debug("-  Processing file: " + audio_file)

        # Add cover art file to data var
        audio_file_data[audio_file]['cover_art_file'] = cover_art_file
        # print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" + audio_file_data[audio_file]['cover_art_file']

    return(audio_file_data)
# end process_directory




# Check if required program exists in PATH 
def error_checking():

    error_found = False


    # Check if input is a file or directory
    if not (os.path.isfile(path) or os.path.isdir(path)):
        print "Error: \"" + path + "\" is not a directory or file"
        error_found = True
        
    # check if input is an audio file
    if os.path.isfile(path):
        (filename, ext) = os.path.splitext(path)
        if not ( re.search('\.mp3', path, re.IGNORECASE) or re.search('\.m4[ba]', path, re.IGNORECASE) ):
            print "Error: \"" + path + "\" is not an audiofile (mp3/m4b/m4a)"
            print "Input must be an audiofile (mp3/m4b/m4a) or directory with audio files in it."
            error_found = True
        # check incompatible args
        if args.only_extract_cover_art:
            print "Error: argument \"only-extract-cover-art\" is incompatible with single file as of now, this may be changed."
            error_found = True       
        if args.only_delete_unneeded_files:
            print "Error: argument \"only-delete-unneeded-files\" is incompatible with single file"
            error_found = True


    #   Required: ffmpeg, ffprobe    
    from distutils.spawn import find_executable
    
    if not find_executable('ffmpeg'):
        print "Error: ffmpeg is required, not found"
        error_found = True
    if not find_executable('ffprobe'):
        print "Error: ffprobe(from ffmpeg) is required, not found"
        error_found = True
    
    # Check the args for ffmpeg
    valid_bitrates = ['8k', '16k', '24k', '32k', '40k', '48k', '56k', '64k', '80k', '96k', '112k', '128k', '144k', '160k', '192k', '224k', '256k', '320k']

    valid_bandwidths = ['8000', '11025', '12000', '16000', '22050', '24000', '32000', '44100', '48000']

    bitrate_ok = 0
    if args.bitrate:
        for bit in valid_bitrates:
            if args.bitrate == bit:
                bitrate_ok = 1
        if not bitrate_ok:
            print "Error: Not a valid bitrate"
            print "Valid options: '8k', '16k', '24k', '32k', '40k', '48k', '56k', '64k', '80k', '96k', '112k', '128k', '144k', '160k', '192k', '224k', '256k', '320k'"
            error_found = True
    bandwidth_ok = 0
    if args.samplerate:
        for band in valid_bandwidths:
            if args.samplerate == band:
                bandwidth_ok = 1
        if not bandwidth_ok:
            print "Error: Not a valid samplerate"
            print "Valid options: '8000', '11025', '12000', '16000', '22050', '24000', '32000', '44100', '48000'"
            error_found = True

    # Checking for confilicting args
# args.disable_extract_cover_art
# args.disable_embed_cover_art
# args.only_extract_cover_art
# args.disable_reencode
# args.only_reencode
# args.disable_split_chapters
# args.disable_delete_unneeded_files
# args.only_delete_unneeded_files
# args.disable_add_id3_genre
# args.only_add_id3_genre
# args.force_add_cover_art
# args.delete_image_file_after_adding
# args.audio_output_format
# args.bitrate
# args.samplerate
# args.threads
# args.keep_original_files
# args.test
# args.disable_normalize
# args.disable_add_id3_encoded_by
# args.ignore_errors
# args.disable_id3_change
# args.force_normalization


	if args.disable_extract_cover_art and args.only_extract_cover_art:
		print "Arguments: disable-extract-cover-art and only-extract-cover-art conflicts"
		error_found = True
	if args.disable_reencode and args.only_reencode:
		print "Arguments: disable_reencode and only_reencode conflicts"
		error_found = True
	if args.disable_delete_unneeded_files and args.only_delete_unneeded_files:
		print "Arguments: disable_delete_unneeded_files and only_delete_unneeded_files conflicts"
		error_found = True
	if args.disable_add_id3_genre and args.only_add_id3_genre:
		print "Arguments: disable_add_id3_genre and only_add_id3_genre conflicts"
		error_found = True
	if args.disable_reencode and args.force_normalization:
		print "Arguments: disable_reencode and force_normalization conflicts"
		error_found = True
	if args.disable_id3_change and args.only_add_id3_genre:
		print "Arguments: disable_id3_change and only_add_id3_genre conflicts"
		error_found = True
    if sum([args.only_extract_cover_art, args.only_reencode, args.only_delete_unneeded_files, args.only_add_id3_genre]) > 1: # any two or more are true
		error_found = True
    
    # Exit if error
    if error_found:
        exit(1)
    return
# end error_checking



# Generates data of audio file
def extract_audiofile_data(logger, audio_file):
    # ffprobe
    # -show_format -show_chapters -show_streams
    #-loglevel -8 (removes unnessasary stuff)
    # -print_format flat 
    # https://trac.ffmpeg.org/wiki/FFprobeTips
    # ffprobe -loglevel -8 -show_format -show_chapters -show_streams


    # ffmpeg -i in.mp3 -f ffmetadata metadata.txt
    # ffmpeg32 -i in.mp3 -i metadata.txt -map_metadata 1 -c:a copy -id3v2_version 3 -write_id3v1 1 out.mp3
    # Example of output

    import json

    # Create dictionary
    audio_file_data = {}
    audio_file_data['filename'] = audio_file
    audio_file_data['cover_art_embeded'] = False
    audio_file_data['codec_name'] = ''
    audio_file_data['low_bitrate'] = False
    audio_file_data['encoded_by'] = ''
    audio_file_data['encoder_same'] = False
    audio_file_data['bitrate'] = ''
    audio_file_data['samplerate'] = ''
    audio_file_data['chapters_exist'] = False


    # ffprobe command
    cmd = 'ffprobe -loglevel -8 -show_format -show_chapters -show_streams -print_format json "' + audio_file + '"' 
    # Executing command
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, err) = p.communicate() # execute
    p_status = p.wait() # wait for command to finish

    # put ffprobe in to ffprobe_data dictionary
    ffprobe_data = json.loads(output)

    # pprint.pprint(ffprobe_data)

    # parse ffprobe output to extract data
    for stream in ffprobe_data['streams']:
        # Check for cover art
        if stream['codec_name'] == 'mjpeg' or stream['codec_name'] == 'png':
            audio_file_data['cover_art_embeded'] = True
            # logger.debug("-   Cover art exists")
        else:
            audio_file_data['cover_art_embeded'] = False
            # logger.debug("-   Cover art not embeded")

        # Check if mp3
        if stream['codec_name'] == 'mp3':
            audio_file_data['codec_name'] = 'mp3'
            audio_file_data['bitrate'] = str(int(stream['bit_rate'])/1000) + "k"
            audio_file_data['samplerate'] = stream['sample_rate']
            # logger.debug("-   Codec: mp3")
            if stream['bit_rate'] == "32000" or stream['bit_rate'] == "16000" or stream['bit_rate'] == "8000":
                # logger.debug("-   Bitrate: 32k or less, no need to reencode")
                audio_file_data['low_bitrate'] = True
            else:
                # logger.debug("-   Bitrate: " + stream['bit_rate'] + ", will reencode")
                audio_file_data['low_bitrate'] = False


        # Check if m4b/m4a
        if stream['codec_name'] == 'aac':
            audio_file_data['codec_name'] = 'm4b'
            audio_file_data['bitrate'] = stream['bit_rate']
            audio_file_data['samplerate'] = str(int(stream['sample_rate'])/1000) + "k"
    # end of stream loop   

    # get the id3 encoder tag
    if 'encoded_by' in ffprobe_data['format']['tags'].keys():
        audio_file_data['encoded_by'] = ffprobe_data['format']['tags']['encoded_by']

    # Get chapter data
    if not args.disable_split_chapters:
        if 'chapters' in ffprobe_data.keys():
            if len(ffprobe_data['chapters']) > 1:
                # Multiple chapters exit
                audio_file_data['chapters_exist'] = True
                audio_file_data['chapters_total'] = len(ffprobe_data['chapters'])
                audio_file_data['chapters'] = {} 
                # for each chapter          
                for chap in ffprobe_data['chapters']:
                    # Chapter index
                    index = 'chapter' + str(chap['id']+1)
                    audio_file_data['chapters'][index] = {}
                    audio_file_data['chapters'][index]['id'] = chap['id'] + 1
                    track_num = chap['id'] + 1
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



    return(audio_file_data)
# end extract_audiofile_data




# Re-encode, file using ffmpeg
def reencode_audio_file(logger, audio_file_data, file_count, total_count):
    # -i INPUT
    # -c:a libfdk_aac
    # -c:a libmp3lame
    # -b:a BITRATE
    # -y (overwrite)
    # -ar SAMPLERATE
    # -metadata genre="Audiobook"



    # Set the defaults
    # always add space in the begining of varable (except with filename
    ffmpeg_metadata = " "
    ffmpeg_cover_art = ' '
    ffmpeg_input_old = audio_file_data['filename']
    ffmpeg_subdir = os.path.basename(os.path.dirname(audio_file_data['filename']))
    ffmpeg_output = ffmpeg_input_old
    ffmpeg_cover_art = ' '
    ffmpeg_bitrate = ' '
    ffmpeg_samplerate = ' '
    ffmpeg_loudnorm = ' '
    ffmpeg_audio_codec = ' '
    ffmpeg_video_codec = ' '
    if not args.audio_output_format:
        args.audio_output_format = "mp3"
    if args.bitrate:
        bitrate = args.bitrate
    else:
        bitrate = bitrate_default
    if args.samplerate:
        samplerate = args.samplerate
    else:
        samplerate = samplerate_default
    cover_art_same = False


    # print "sadddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"
    # print audio_file_data['encoded_by']
    # print program_name
    # print "sadddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd"


    # Skip reencoding: bitrates, samplerate, encoded_by
    if (audio_file_data['cover_art_embeded'] and audio_file_data['cover_art_file']) or (not audio_file_data['cover_art_embeded'] and not audio_file_data['cover_art_file']) or (args.disable_embed_cover_art):
        cover_art_same = True
    if ( audio_file_data['bitrate'] == bitrate and audio_file_data['samplerate'] == samplerate and audio_file_data['encoded_by'] == program_name and not args.force_normalization) or args.disable_reencode or args.only_add_id3_genre or args.only_extract_cover_art:
        # They are likely the same
        no_need_to_reencode = True # just copy
    else:
        # They are not the same
        no_need_to_reencode = False


    # Input file name (renaming file)
    ffmpeg_input = os.path.dirname(ffmpeg_input_old) + "/original-" + os.path.basename(ffmpeg_input_old)
    logger.debug("- Moving '" + os.path.basename(ffmpeg_input_old) + "' to '" + os.path.basename(ffmpeg_input) + "'")
    if not args.test:
        os.rename(ffmpeg_input_old, ffmpeg_input)


    # No re-encode ffmpeg settings
    if no_need_to_reencode:
        ffmpeg_bitrate = ' '
        ffmpeg_samplerate = ' '
        ffmpeg_audio_codec = " -c:a copy"
        ffmpeg_cover_art = " -c:v copy"
        # ffmpeg_output = ffmpeg_input_old
    else:
        #Re-encode options

        # Set Codec and Output file's extention
        if args.audio_output_format == 'm4b':
            ffmpeg_audio_codec = " -c:a libfdk_aac"
            ffmpeg_output = re.sub('\.[a-zA-Z0-9]{3,4}$', '.m4b', audio_file_data['filename'])
        else:
            # Should be mp3
            ffmpeg_audio_codec = " -c:a libmp3lame"
            ffmpeg_output = re.sub('\.[a-zA-Z0-9]{3,4}$', '.mp3', audio_file_data['filename'])

        # Set Bitrate and Sample rate
        if not ( args.only_add_id3_genre or args.only_extract_cover_art):
            # Bitrate
            if args.bitrate:
                ffmpeg_bitrate = " -b:a " + args.bitrate
            else:
                ffmpeg_bitrate = " -b:a " + bitrate_default
            # Samplerate
            if args.samplerate:
                ffmpeg_samplerate = " -ar " + args.samplerate
            else:
                ffmpeg_samplerate = " -ar " + samplerate_default
   
        # loadnorm flags (1-pass)
        if args.force_normalization or not ( args.disable_normalize or args.disable_reencode or args.only_extract_cover_art or args.only_add_id3_genre):
            ffmpeg_loudnorm = " -filter:a loudnorm"
            # todo add check for ReplayGain metadata check 

    # Adding metadata Genre and encoder
    if not args.disable_id3_change:
        if not (args.disable_add_id3_encoded_by or args.only_add_id3_genre ):
            ffmpeg_metadata= " -metadata encoded_by=\"" + program_name + "\""
        if not args.disable_add_id3_genre :
            ffmpeg_metadata += " -metadata genre=\"Audiobook\""
        if args.audio_output_format == 'mp3':
            # makes sure id3 tags are writen and removes some leftovers from m4b files
            ffmpeg_metadata += " -metadata compatible_brands= -metadata minor_version= -metadata major_brand= -id3v2_version 3 -write_id3v1 1"

    # Cover art
    if not cover_art_same:
        if args.audio_output_format == 'm4b':
            if debug:
                logger.debug("Warning: embedded cover art in m4b files is currently unimplemented")
            else:
                print "Warning: embedded cover art in m4b files is currently unimplemented"
        if audio_file_data['cover_art_file'] and not audio_file_data['cover_art_embeded']: 
            # should be mp3 and can add cover art
            ffmpeg_cover_art =" -i \"" + audio_file_data['cover_art_file'] + "\" -map 0:0 -map 1:0 -c:v copy -metadata:s:v title=\"Album cover\" -metadata:s:v comment=\"Cover (front)\""
            # put after audio input

    # Encode in seperate chapter file       
    # if not args.disable_split_chapters and audio_file_data['chapters_exist']: 

    # Creating ffmpeg command
    ffmpeg_cmd = "ffmpeg -loglevel error" + " -i \"" + ffmpeg_input + "\"" + ffmpeg_cover_art + ffmpeg_audio_codec + ffmpeg_bitrate + ffmpeg_samplerate + ffmpeg_metadata + ffmpeg_loudnorm + " \"" + ffmpeg_output + "\""
    
    logger.debug("  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    logger.debug("  ~   Encoding file: " + os.path.basename(audio_file_data['filename']))
    logger.debug("  ~       Dir: " + os.path.dirname(audio_file_data['filename']))
    logger.debug("  ~      Codec: " + audio_file_data['codec_name'] )
    logger.debug("  ~      bitrate: " + audio_file_data['bitrate'] )
    logger.debug("  ~      samplerate: " + audio_file_data['samplerate'] )
    logger.debug("  ~      encoded_by: " + audio_file_data['encoded_by'] )     
    logger.debug("  ~      Greater than 32k bitrate: " + str( not audio_file_data['low_bitrate'] ))
    logger.debug("  ~      Embedded cover art: " + str( audio_file_data['cover_art_embeded'] ))
    logger.debug("  ~      Cover art file: " + os.path.basename(audio_file_data['cover_art_file']))
    logger.debug(" ~   FFMPEG flags")
    logger.debug(" ~    bitrate: " +  ffmpeg_bitrate)
    logger.debug(" ~    samplerate: " +  ffmpeg_samplerate)
    logger.debug(" ~    cover art: " +  ffmpeg_cover_art)
    logger.debug(" ~    metadata: " +  ffmpeg_metadata)
    logger.debug(" ~    loudnorm: " +  ffmpeg_loudnorm)
    logger.debug(" ~    audio codec: " +  ffmpeg_audio_codec)
    logger.debug(" ~    input: " +  os.path.basename(ffmpeg_input))
    logger.debug(" ~    output: " +  os.path.basename(ffmpeg_output))
    logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    logger.debug(" CMD: " + ffmpeg_cmd)
    logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")


    # Encoding file
    print "    Encoding (" + str(file_count) + " of " + str(total_count) + "): " + os.path.basename(ffmpeg_input_old) 
    if no_need_to_reencode:
        if debug:
            logger.debug("      Skipping: This file has likely already been encoded by this program.")
        else:
            print "      Skipping: This file has likely already been encoded by this program."
    if not args.test:
        pp = subprocess.Popen(ffmpeg_cmd , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (output, err) = pp.communicate() # execute
        pp_status = pp.wait() # wait for command to finish
        # logger.debug("ffmpeg err output:" + err)

        # check if encoding failed
        if err:
            # print error
            if debug:
                logger.debug("Error: encoding failed!\nffmpeg command:\n>" + ffmpeg_cmd)
                logger.debug("ffmpeg error: " + err)
            else:
                logger.debug("Error: encoding failed!\nffmpeg command:\n>" + ffmpeg_cmd)
                logger.debug("ffmpeg error:\n>" + err)

            # Ignore the error, put file in original state, delete file with error
            if args.ignore_errors:
                if debug:
                    logger.debug("Moving files back to original state")
                else:
                    print "   Moving files back to original state, and continuing to next file"
                if os.path.isfile(ffmpeg_output): 
                    os.remove(ffmpeg_output)
                os.rename(ffmpeg_input,ffmpeg_output)
            else:
                # Encoding failed, Exiting
                if debug: logger.debug("Exiting after failure")
                else: print "Exiting after failure"             
                exit(1)
        else:
            # encoding succeded

            if not args.keep_original_files and not args.test:
                # delete original files  
                logger.debug("Deleting original file:" + os.path.basename(ffmpeg_input))
                os.remove(ffmpeg_input)

            # Delete cover art image file
            if args.delete_image_file_after_adding and not args.test:
                logger.debug("Deleting image file:" + os.path.basename(ffmpeg_cover_art))
                os.remove(ffmpeg_cover_art)

    return
# end encode_audio_files





# Extract embedded cover art
def extract_cover_art_ffmpeg(logger, audio_file, single_file=False):
    if single_file:
        output_file = 'temp'
        # make temp file for log
        temp_root_dir = os.path.join(tempfile.gettempdir(), 'audiobook_reencode')
        if not os.path.isdir(temp_root_dir):
            os.mkdir(temp_root_dir)
        output_file = os.path.join(temp_root_dir, "cover.jpg")

    logger.debug("-   > ffmpeg extracting: cover.jpg") # + output_file)
    if not args.test:
        cmd = 'ffmpeg -y -i "' + audio_file + '" "' + output_file + '"'
        pp = subprocess.Popen(cmd , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (output, err) = pp.communicate() # execute
        pp_status = pp.wait() # wait for command to finish
        # logger.debug(err)
    return(output_file)
# end extract_cover_art_ffmpeg








# Extracting cover art from directory or mp3 file
def extract_cover_art(logger, dirpath, audio_files, audio_file_data, single_file=False):
    #   dirpath is the directory with audio files

    cover_art = '';
    extract_embedded_true = False
    
    if single_file:
        extract_embedded_true = True
    else:
        # Get lists of mp3, m4b/m4a, and jpg/png (full dir)
        cover_art_list = glob.glob(os.path.join(dirpath,'*.png')) + glob.glob(os.path.join(dirpath,'*.jpg')) 
        # mp3_files = glob.glob(os.path.join(dirpath,'*.[mM][pP]3'))
        # m4b_files = glob.glob(os.path.join(dirpath,'*.[mM]4[aAbB]'))
        # audio_files = mp3_files + m4b_files

        # Check to see if cover art should not be added to files in dir
        if not filename_similarity(logger, audio_files):
            logger.debug("-    > Cover art will not be added")
            return ''


        # Set the cover art to image in dir
        if cover_art_list:
            # Check if a likly image is cover art
            # logger.debug("-   > Images exists: " # + str(cover_art_list))
            for image in cover_art_list:
                # cover.jpg or cover.png is the most likly
                if( re.search('cover\.jpg$', image, re.IGNORECASE) or re.search('cover\.png$', image, re.IGNORECASE) ):
                    cover_art = image
                    break
                elif( re.search('cover', image, re.IGNORECASE) ): 
                    # prefer in cover is used anywhere in name
                    cover_art = image
                    break
                elif(image): # not empty
                    # otherwise use the first image
                    cover_art = image
                    break
                else:
                    print "Error in program: cover art image was found yet not."
                    exit(1)
        else:
            # Extract cover art from audio file
            logger.debug("-    > No image files, cover art in dir")
            extract_embedded_true = True

    
    if extract_embedded_true:
            # Check if a file in dir has embedded art
            file_with_embedded_cover_art = ''
            for audio_file in audio_files:
                if audio_file_data.get(audio_file)['cover_art_embeded']:
                    file_with_embedded_cover_art = audio_file


            # Some debug info
            if file_with_embedded_cover_art == '':
                logger.debug("-     > No embedded art found ")
            else:
                logger.debug("-    > Using cover art embedded in : " + os.path.basename(file_with_embedded_cover_art))
                cover_art = extract_cover_art_ffmpeg(logger, file_with_embedded_cover_art, single_file)


    logger.debug("-    > Cover art is: " + os.path.basename(cover_art))
    return cover_art
# end def extract_cover_art




# Check similarity of list of filenames
def filename_similarity(logger, filename_list):

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





###########################################
# Start it up
#
if __name__ == "__main__":
   main()
