#!/usr/bin/python
# -*- coding: utf-8 -*-

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
#   TODO
#       add force reencode
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



def parse_args():
    """
    CLI Arguments
    """

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

    
    return args
#END: parse_args())



###############################################################################
# Function
#

# main function
def main():
    
    audio_file_data = {}
    unneeded_files = []

    # CLI Arguments
    global args, path, debug
    args = parse_args()
    # generate config settings
    global config
    from audiobook_tools.common.load_config import load_config
    tmp_dir = ''
    config = load_config("audiobook-reencoder.conf", args, tmp_dir)
    path = args.directory
    debug = config['preferred']['debug']


    # Input/Arguments Error checks
    error_checking()

    # Setup logging
    logger = setup_logging()

    # banner for test
    if config['preferred']['test']:
        print("******************************************************")
        print("* Running in test mode, no actions will be performed *")
        print("******************************************************")

    
    logger.debug("*********************************************************************")
    logger.debug("* Root directory: " + path)
    logger.debug("*********************************************************************")

    # clean up tmp dir in case it ran before TODO remove and use tmp module
    clean_up_tmp_dir()
   
    # Processing
    if os.path.isfile(path):
        # Process a single file
        if debug: 
            logger.debug("Generating audiobook data...")
        else:
            print("Generating audiobook files data...")
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
        # Not a single file: Walk though the directories to process audio folders
        if debug: 
            logger.debug("Extracting audiobook data from directory...")
        else:
            print("Generating audiobook files data...")
        for (dirpath, dir_list_in_dirpath, file_list) in os.walk(path):
            logger.debug(" ......................................................................")
            logger.debug(" : Processing directory: " + dirpath)
            # print(" Entering directory: " + dirpath

            # Get lists of mp3, m4b/m4a, and jpg/png
            mp3_files = glob.glob(os.path.join(dirpath,'*.[mM][pP]3'))
            m4b_files = glob.glob(os.path.join(dirpath,'*.[mM]4[aAbB]'))
            audio_files = mp3_files + m4b_files
            # pprint.pprint(audio_files)

            # Create list of *.cue, *.m3u, *.nfo
            if not (config['preferred']['only_reencode'] or config['preferred']['only_add_id3_genre']) and not config['preferred']['disable_delete_unneeded_files']:
                logger.debug("-  Checking dir for unneeded files")
                unneeded_files += glob.glob(os.path.join(dirpath,'*.[nN][fF][oO]'))
                unneeded_files += glob.glob(os.path.join(dirpath,'*.[cC][uU][eE]'))
                unneeded_files += glob.glob(os.path.join(dirpath,'*.[mM]3[uU]'))

            # Process directory if mp3/m4b/m4a is found
            if not config['preferred']['only_delete_unneeded_files']:
                if ( not audio_files):
                    logger.debug("   No audio files found in dir (mp3/m4b/m4a)")
                else:
                    logger.debug("-  Audio found in dir")
                    # Merger dictionaries
                    audio_file_data.update( process_directory(logger, dirpath, audio_files, audio_file_data) )
        # end of walk through directories
        

        # Delete un-needed files, removes *.cue, *.m3u, *.nfo
        if not (config['preferred']['only_reencode'] or config['preferred']['only_add_id3_genre']) and not config['preferred']['disable_delete_unneeded_files']:
            print("Deleting unneeded (nfo/cue/m3u) files...")
            for file_name in unneeded_files:
                logger.debug("-  Deleting unneeded file: " + file_name)
                if not config['preferred']['test']:
                    os.remove(file_name)
        else:
            logger.debug("- Not deleting unneeded files")


 
    # print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH"
    # pprint.pprint(audio_file_data)
    # exit()


   # Encoding the files through the list
    # Re-encode the audio file
    total_count = len(audio_file_data)
    file_count = 1
    if debug:
        logger.debug("Encoding starting... ")
    else:
        print("Encoding starting... ")
    if os.path.isfile(path):
        # encoding a single file
        reencode_audio_file(logger, audio_file_data[path], file_count, total_count)
    else:
        # encoding directory
        for (dirpath, dir_list_in_dirpath, file_list) in os.walk(path):
            # walking the dir again so encoding processes in expected order
            print("  " + os.path.basename(dirpath) + "/")
            # sort file list so its in alpha numberic order
            file_list.sort()
            for file_name in file_list:
                # print("    >" + file_name
                if audio_file_data[os.path.join(dirpath, file_name)]['read_data_failed']:
                    # reading data filed earlier, so skiping encoding
                    print("Skip encoding \"" + file_name + "\", likly has an error in it")
                else:
                    if os.path.join(dirpath, file_name) in audio_file_data:
                        # print("        yippy"
                        if not (config['preferred']['only_extract_cover_art'] or config['preferred']['only_delete_unneeded_files']):
                            # preform action
                            reencode_audio_file(logger, audio_file_data[os.path.join(dirpath,file_name)], file_count, total_count)
                            file_count += 1
    # All done


    # clean up tmp dir at end
    clean_up_tmp_dir()

    print("done.")
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
    if config['preferred']['debug']:
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
    if not (config['preferred']['only_delete_unneeded_files'] or config['preferred']['only_add_id3_genre'] or config['preferred']['only_reencode']):
        audio_file_data = extract_cover_art(logger, dirpath, audio_files, audio_file_data, single_file)
    else:
        cover_art_file = ''
    # print("ooooooooooooooooooooooooooooooooooo" + cover_art_file

    # Process each file in the current directory
    # for audio_file in audio_files:
    #     logger.debug("-  Processing file: " + audio_file)

    #     # Add cover art file to data var
    #     audio_file_data[audio_file]['cover_art_file'] = cover_art_file
    #     # print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX" + audio_file_data[audio_file]['cover_art_file']

    return(audio_file_data)
# end process_directory




# Check if required program exists in PATH 
def error_checking():

    error_found = False


    # Check if input is a file or directory
    if not (os.path.isfile(path) or os.path.isdir(path)):
        print("Error: \"" + path + "\" is not a directory or file")
        error_found = True
        
    # check if input is an audio file
    if os.path.isfile(path):
        (filename, ext) = os.path.splitext(path)
        if not ( re.search('\.mp3', path, re.IGNORECASE) or re.search('\.m4[ba]', path, re.IGNORECASE) ):
            print("Error: \"" + path + "\" is not an audiofile (mp3/m4b/m4a)")
            print("Input must be an audiofile (mp3/m4b/m4a) or directory with audio files in it.")
            error_found = True
        # check incompatible args
        if config['preferred']['only_extract_cover_art']:
            print("Error: argument \"only-extract-cover-art\" is incompatible with single file as of now, this may be changed.")
            error_found = True       
        if config['preferred']['only_delete_unneeded_files']:
            print("Error: argument \"only-delete-unneeded-files\" is incompatible with single file")
            error_found = True


    #   Required: ffmpeg, ffprobe    
    from distutils.spawn import find_executable
    
    if not find_executable('ffmpeg'):
        print("Error: ffmpeg is required, not found")
        error_found = True
    if not find_executable('ffprobe'):
        print("Error: ffprobe(from ffmpeg) is required, not found")
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
            print("Error: Not a valid bitrate")
            print("Valid options: '8k', '16k', '24k', '32k', '40k', '48k', '56k', '64k', '80k', '96k', '112k', '128k', '144k', '160k', '192k', '224k', '256k', '320k'")
            error_found = True
    
    bandwidth_ok = 0
    if config['preferred']['samplerate']:
        for band in valid_bandwidths:
            if config['preferred']['samplerate'] == band:
                bandwidth_ok = 1
        if not bandwidth_ok:
            print("Error: Not a valid samplerate")
            print("Valid options: '8000', '11025', '12000', '16000', '22050', '24000', '32000', '44100', '48000'")
            error_found = True

        if config['preferred']['disable_extract_cover_art'] and config['preferred']['only_extract_cover_art']:
            print("Arguments: disable-extract-cover-art and only-extract-cover-art conflicts")
            error_found = True
        if config['preferred']['disable_reencode'] and config['preferred']['only_reencode']:
            print("Arguments: disable_reencode and only_reencode conflicts")
            error_found = True
        if config['preferred']['disable_delete_unneeded_files'] and config['preferred']['only_delete_unneeded_files']:
            print("Arguments: disable_delete_unneeded_files and only_delete_unneeded_files conflicts")
            error_found = True
        if config['preferred']['disable_add_id3_genre'] and config['preferred']['only_add_id3_genre']:
            print("Arguments: disable_add_id3_genre and only_add_id3_genre conflicts")
            error_found = True
        if config['preferred']['disable_reencode'] and config['preferred']['force_normalization']:
            print("Arguments: disable_reencode and force_normalization conflicts")
            error_found = True
        if config['preferred']['disable_id3_change'] and config['preferred']['only_add_id3_genre']:
            print("Arguments: disable_id3_change and only_add_id3_genre conflicts")
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
    audio_file_data['cover_art_file'] = ''
    audio_file_data['title'] = ''
    audio_file_data['read_data_failed'] = False

    # ffprobe command
    cmd = 'ffprobe -loglevel 8 -show_format -show_chapters -show_streams -print_format json "' + audio_file + '"' 
    # Executing command
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, err) = p.communicate() # execute
    p_status = p.wait() # wait for command to finish


    # put ffprobe in to ffprobe_data dictionary
    ffprobe_data = json.loads(output)


    if err or not ffprobe_data:
        audio_file_data['read_data_failed'] = True
        logger.debug("Error reading \"" + audio_file + "\" with ffprobe, file probably broken") 
        if not config['preferred']['ignore_errors']:
            exit(1)       
        return(audio_file_data)

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
    
    # get title
    if 'title' in ffprobe_data['format']['tags'].keys():
        audio_file_data['title'] = ffprobe_data['format']['tags']['title']


    # Get chapter data
    if not config['preferred']['disable_split_chapters']:
        if 'chapters' in ffprobe_data.keys():
            if len(ffprobe_data['chapters']) > 1:
                # Multiple chapters exit
                audio_file_data['chapters_exist'] = True
                audio_file_data['chapters_total'] = len(ffprobe_data['chapters'])
                audio_file_data['chapters'] = {} 
                # for each chapter          
                for chap in ffprobe_data['chapters']:
                    # Chapter index
                    index = chap['id']
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



# Clean up dir
def clean_up_tmp_dir():

    temp_root_dir = os.path.join(tempfile.gettempdir(), 'audiobook_reencode')
    # dont delete log files

    logging.debug("Cleaning up tmp dir:" + temp_root_dir)
    # dirs = os.listdir( temp_root_dir )

    for root, dirs, files in os.walk(temp_root_dir, topdown=False):
        for name in files:
            (filen, ext) =  os.path.splitext(name)
            if not ext == ".log":           
                os.remove(os.path.join(root, name))
        for name in dirs:
            # if os.path.exists(os.path.join(root, name)):
            os.rmdir(os.path.join(root, name))

    # for filename in dirs:
    #     (filen, ext) =  os.path.splitext(filename)
    #     if not ext == ".log":
    #         os.remove(os.path.join(temp_root_dir, filename))
    return
# end clean_up_tmp_dir


# Re-encode, file using ffmpeg
def reencode_audio_file(logger, audio_file_data, file_count, total_count):

    new_filename = ''

    temp_root_dir = os.path.join(tempfile.gettempdir(), 'audiobook_reencode')

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
    if not config['preferred']['audio_output_format']:
        config['preferred']['audio_output_format'] = "mp3"
    if config['preferred']['bitrate']:
        bitrate = config['preferred']['bitrate']
    else:
        bitrate = bitrate_default
    if config['preferred']['samplerate']:
        samplerate = config['preferred']['samplerate']
    else:
        samplerate = samplerate_default
    cover_art_same = False
    ffmpeg_output = os.path.join(temp_root_dir, re.sub('\.[a-zA-Z0-9]{3,4}$', '.' + config['preferred']['audio_output_format'], ffmpeg_input))

    # Deciding to skip encoding
    chapter_it = False
    setting_same_as_file = False
    no_encode_args = False
    add_cover_art = False

    # Bitrates/Samplerate/Meta same, remove decimal for bitrate
    if ( re.sub(r'\.0', '', audio_file_data['bitrate']) == bitrate and audio_file_data['samplerate'] == samplerate and audio_file_data['encoded_by'] == program_name and not config['preferred']['force_normalization']):
        setting_same_as_file = True

    # No need to Re-encode
    if config['preferred']['disable_reencode'] or config['preferred']['only_add_id3_genre'] or config['preferred']['only_extract_cover_art']:
        no_encode_args = True

    # Chapters
    if (audio_file_data['chapters_exist'] and (not config['preferred']['disable_split_chapters'])) and not no_encode_args:
        chapter_it = True

    # Re-encode
    if (audio_file_data['cover_art_embeded'] and audio_file_data['cover_art_file']) or (not audio_file_data['cover_art_embeded'] and not audio_file_data['cover_art_file']) or (config['preferred']['disable_embed_cover_art']):
        cover_art_same = True
    if ( setting_same_as_file or no_encode_args ) and not chapter_it:
        # They are likely the same
        no_need_to_reencode = True # just copy
    else:
        # They are not the same
        no_need_to_reencode = False

    # Cover Art
    if not ( config['preferred']['disable_embed_cover_art'] or config['preferred']['disable_reencode'] or config['preferred']['only_add_id3_genre'] ):
        if ( not config['preferred']['disable_split_chapters'] and audio_file_data['chapters_exist'] and audio_file_data['cover_art_file'] ) or ( audio_file_data['cover_art_file'] and not audio_file_data['cover_art_embeded'] ):
            add_cover_art = True


    # Input file name (renaming file)
    # ffmpeg_input = os.path.dirname(ffmpeg_input_old) + "/original-" + os.path.basename(ffmpeg_input_old)
    # logger.debug("- Moving '" + os.path.basename(ffmpeg_input_old) + "' to '" + os.path.basename(ffmpeg_input) + "'")
    # if not config['preferred']['test']:
    #     os.rename(ffmpeg_input_old, ffmpeg_input)


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
        if config['preferred']['audio_output_format'] == 'm4b':
            ffmpeg_audio_codec = " -c:a libfdk_aac"
            # ffmpeg_output = re.sub('\.[a-zA-Z0-9]{3,4}$', '.m4b', audio_file_data['filename'])
        else:
            # Should be mp3
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
        if config['preferred']['force_normalization'] or not ( config['preferred']['disable_normalize'] or config['preferred']['disable_reencode'] or config['preferred']['only_extract_cover_art'] or config['preferred']['only_add_id3_genre']):
            ffmpeg_loudnorm = " -filter:a loudnorm"
            # todo add check for ReplayGain metadata check 
            # ffprobe doesn't show APE tags, where mp3gain is usually placed

    # Adding metadata Genre and encoder
    if not config['preferred']['disable_id3_change']:
        if not (config['preferred']['disable_add_id3_encoded_by'] or config['preferred']['only_add_id3_genre'] ):
            ffmpeg_metadata= " -metadata encoded_by=\"" + program_name + "\""
        if not config['preferred']['disable_add_id3_genre'] :
            ffmpeg_metadata += " -metadata genre=\"Audiobook\""
        if config['preferred']['audio_output_format'] == 'mp3':
            # makes sure id3 tags are writen and removes some leftovers from m4b files
            ffmpeg_metadata += " -metadata compatible_brands= -metadata minor_version= -metadata major_brand= "

    # Cover art
    if not no_need_to_reencode: #cover_art_same:
        if config['preferred']['audio_output_format'] == 'm4b':
            if debug:
                logger.debug("Warning: embedded cover art in m4b files is currently unimplemented")
            else:
                print("Warning: embedded cover art in m4b files is currently unimplemented")
        if add_cover_art:
            # should be mp3 and can add cover art
            ffmpeg_cover_art =" -i \"" + audio_file_data['cover_art_file'] + "\" -map 0:0 -map 1:0 -c:v copy -metadata:s:v title=\"Album cover\" -metadata:s:v comment=\"Cover (front)\""
            # put after audio input
        else:
            logger.debug("Not adding cover art")
    
    logger.debug("  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    logger.debug("  ~   Encoding file: " + os.path.basename(audio_file_data['filename']))
    logger.debug("  ~       Dir: " + os.path.dirname(audio_file_data['filename']))
    logger.debug("  ~      Title: " + audio_file_data['title'])   
    logger.debug("  ~      Codec: " + audio_file_data['codec_name'] )
    logger.debug("  ~      bitrate: " + audio_file_data['bitrate'] )
    logger.debug("  ~      samplerate: " + audio_file_data['samplerate'] )
    logger.debug("  ~      encoded_by: " + audio_file_data['encoded_by'] )     
    logger.debug("  ~      Greater than 32k bitrate: " + str( not audio_file_data['low_bitrate'] ))
    logger.debug("  ~      Embedded cover art: " + str( audio_file_data['cover_art_embeded'] ))
    logger.debug("  ~      Cover art file: " + os.path.basename(audio_file_data['cover_art_file']))
    logger.debug(" ~    Chapters: " +  str(audio_file_data['chapters_exist']))

    if audio_file_data['chapters_exist']:
        for chap in audio_file_data['chapters']:
            logger.debug(" ~      \"" + audio_file_data['chapters'][chap]['name'] +"\" (" + str(audio_file_data['chapters'][chap]['id']) + " of " + str(audio_file_data['chapters_total']) + ")")
            logger.debug(" ~        Start:" + audio_file_data['chapters'][chap]['start_time'] + "s, Dur:" + audio_file_data['chapters'][chap]['duration'] + "s" )

    logger.debug(" ~   FFMPEG flags")
    logger.debug(" ~    bitrate: " +  ffmpeg_bitrate)
    logger.debug(" ~    samplerate: " +  ffmpeg_samplerate)
    logger.debug(" ~    cover art: " +  ffmpeg_cover_art)
    logger.debug(" ~    metadata: " +  ffmpeg_metadata)
    logger.debug(" ~    loudnorm: " +  ffmpeg_loudnorm)
    logger.debug(" ~    audio codec: " +  ffmpeg_audio_codec)
    logger.debug(" ~    input: " +  os.path.basename(ffmpeg_input))          
    logger.debug(" ~    output: " +  os.path.basename(ffmpeg_output))
    logger.debug("  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    
    if no_need_to_reencode:
        print("Skipping: (" + str(file_count) + " of " + str(total_count) + "): " + os.path.basename(ffmpeg_input))
    else:
        ##################################
        # Chapters exist, so split
        if chapter_it:
            #############################
            # Encoding Chapters

            # Create dir to put chapter files (remove invalid chars)
            input_files_dir = os.path.dirname(ffmpeg_input)
            ffmpeg_output_subdir = re.sub("[<>:;\"'|?*\\\/]", "", audio_file_data['title'])
            ffmpeg_output_chap_temp_dirname = os.path.join(temp_root_dir, ffmpeg_output_subdir)

            # Remove chapter data from single file
            ffmpeg_metadata += " -map_chapters -1"

            logger.debug("making tmp dir: " + ffmpeg_output_chap_temp_dirname)
            if not os.path.isdir(ffmpeg_output_chap_temp_dirname):
                os.mkdir(ffmpeg_output_chap_temp_dirname)

            # total tracks
            ffmpeg_track_total = str(audio_file_data['chapters_total'])

            ffmpeg_single_tmp = os.path.join(temp_root_dir, "temp-single." + config['preferred']['audio_output_format'])
            
            # Encoding (1st stage) 
            #   copy id3, Remove chapter data, encode w/ codec/bitrate/samplerate, vol normalize
            ffmpeg_cmd = "ffmpeg -loglevel error -y -i \"" + ffmpeg_input + "\"" + ffmpeg_audio_codec + ffmpeg_bitrate + ffmpeg_samplerate + ffmpeg_loudnorm + " -id3v2_version 3 -write_id3v1 1 -map_chapters -1 \"" + ffmpeg_single_tmp + "\"" 

            if debug:
                logging.debug("    Encoding (" + str(file_count) + " of " + str(total_count) + "): " + os.path.basename(ffmpeg_input_old) )
                logging.debug("Encoding: first stage")
            else:
                print("    Encoding (" + str(file_count) + " of " + str(total_count) + "): " + os.path.basename(ffmpeg_input_old))
                print("         Encoding: first stage"            )
            logger.debug("  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            logger.debug(" CMD: " + ffmpeg_cmd)
            logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~") 
            # encoding (1st stage)
            encoder_error = reencode_audio_file_ffmpeg(logger, ffmpeg_cmd, ffmpeg_input, ffmpeg_single_tmp, ffmpeg_cover_art)
            if encoder_error:
                logger.debug("Encoding failed on \"" + ffmpeg_input + "\", stopping encoding book")
                return   
                                
            # Process each chap
            x=0
            for chap in audio_file_data['chapters']:    

    # DELETE ME
                x += 1
                if x == 5:
                    break

                # track num
                ffmpeg_track_num = str(audio_file_data['chapters'][chap]['id'])
                # output file name
                ffmpeg_output = os.path.join(ffmpeg_output_chap_temp_dirname, audio_file_data['chapters'][chap]['name'] + "." + config['preferred']['audio_output_format'])
                ffmpeg_output_tmp = os.path.join(temp_root_dir, "temp." + config['preferred']['audio_output_format'])

                # metadata track info
                ffmpeg_metadata_track = " -metadata track=\"" + ffmpeg_track_num + "/" + ffmpeg_track_total + "\""
                # time
                if float(audio_file_data['chapters'][chap]['start_time']) == 0:
                    ffmpeg_time = " -t " + str(audio_file_data['chapters'][chap]['duration'])
                else:
                    ffmpeg_time = " -ss " + str(audio_file_data['chapters'][chap]['start_time']) + " -t " + str(audio_file_data['chapters'][chap]['duration'])                

     

                logger.debug(" ~    metadata tracks: " +  ffmpeg_metadata_track)            
                logger.debug(" ~    metadata: " +  ffmpeg_metadata)
                logger.debug(" ~    record time: " +  ffmpeg_time)           
                logger.debug(" ~    output dir: " +  ffmpeg_output_chap_temp_dirname)           
                logger.debug(" ~    output: " +  os.path.basename(ffmpeg_output))


                # Encodding: spliting chapters (2nd stage)
                ffmpeg_cmd = "ffmpeg -loglevel error -y -i \"" + ffmpeg_single_tmp + "\"" + ffmpeg_time + " -c:v copy -c:a copy -id3v2_version 3 -write_id3v1 1 \"" + ffmpeg_output_tmp + "\""
                logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                logger.debug(" CMD: " + ffmpeg_cmd)
                logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                if debug:
                    logging.debug("         Spliting chapter: " + ffmpeg_track_num + "/" + ffmpeg_track_total)
                else:
                    print("         Splitting chapter: " + ffmpeg_track_num + "/" + ffmpeg_track_total)
                # Send to encoder             
                encoder_error = reencode_audio_file_ffmpeg(logger, ffmpeg_cmd, ffmpeg_input, ffmpeg_output_tmp, ffmpeg_cover_art)
                if encoder_error:
                    logger.debug("Encoding failed on \"" + audio_file_data['chapters'][chap]['name'] + "\", stopping encoding of rest of book")
                    break

                # Encoding: adding cover are and metadata (3rd stage)
                ffmpeg_cmd_add_art = "ffmpeg -loglevel error" + " -y -i \"" + ffmpeg_output_tmp + "\"" + ffmpeg_cover_art + " -c:a copy" + ffmpeg_metadata + ffmpeg_metadata_track + "  -id3v2_version 3 -write_id3v1 1 \"" + ffmpeg_output + "\""   
                if debug:
                    logger.debug("         Adding cover art and ID3 tags")
                else:
                    print("         Adding cover art and ID3 tags")
                logger.debug("  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                logger.debug(" CMD: " + ffmpeg_cmd_add_art)
                logger.debug(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")                 
                encoder_error = reencode_audio_file_ffmpeg(logger, ffmpeg_cmd_add_art, ffmpeg_output_tmp, ffmpeg_output, ffmpeg_cover_art)
                if encoder_error:
                    logger.debug("Encoding failed on \"" + audio_file_data['chapters'][chap]['name'] + "\", stopping encoding of rest of book")
                    break
                else:
                    logger.debug("Moving tmp chapter file, to  ")
                    os.rename(ffmpeg_output_tmp, ffmpeg_output)
            # end chapter loop, encoding done

            # dir temp to move
            temp_output = ffmpeg_output_chap_temp_dirname
            # dir to move to
            final_output = os.path.join(input_files_dir,ffmpeg_output_subdir)
        else:
            ####################################
            # Encoding - Not-Chaptered

            ffmpeg_output = os.path.join(temp_root_dir,os.path.basename(ffmpeg_input))
            
            # Creating ffmpeg command
            ffmpeg_cmd = "ffmpeg -loglevel error" + " -y -i \"" + ffmpeg_input + "\"" + ffmpeg_cover_art + ffmpeg_audio_codec + ffmpeg_bitrate + ffmpeg_samplerate + ffmpeg_metadata + ffmpeg_loudnorm + " \"" + ffmpeg_output + "\""

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
            # Encoding file, without chapter
            print("    Encoding (" + str(file_count) + " of " + str(total_count) + "): " + os.path.basename(ffmpeg_input_old) )
            if no_need_to_reencode:
                if debug:
                    logger.debug("      Skipping: This file has likely already been encoded by this program.")
                else:
                    print("      Skipping: This file has likely already been encoded by this program.")
        
            
            # Send to Encoder
            encoder_error = reencode_audio_file_ffmpeg(logger, ffmpeg_cmd, ffmpeg_input, ffmpeg_output, ffmpeg_cover_art)
            if encoder_error:
                logger.debug("Encoding failed")
            temp_output = ffmpeg_output
            final_output = ffmpeg_input
        # end single file encoding

        # Error delete tmp
        if encoder_error:
            logger.debug("encoding failed, deleting temporary file:")
            if not config['preferred']['test'] and os.path.exists(temp_output):
                os.remove(temp_output)
        else: 
            # encoding sucess
            if chapter_it:
                logger.debug("Encoding success: moving old file to backup(in desired), moving new file to original")
                # create backup of original
                if config['preferred']['keep_original_files'] and not config['preferred']['test']:
                    new_filename = os.path.join(os.path.dirname(ffmpeg_input), "original-" + os.path.basename(ffmpeg_input))
                    if os.path.exists(new_filename):
                        new_filename = os.path.join(os.path.dirname(ffmpeg_input), "original2-" + os.path.basename(ffmpeg_input))
                    os.rename(ffmpeg_input,new_filename)
                # move temp to original location
                if os.path.exists(final_output):
                    # if folder already exists , move to "folder-new"
                    final_output = final_output + "-new"
                os.rename(temp_output,final_output)
            else: # single file
                if config['preferred']['keep_original_files'] and not config['preferred']['test']:
                    new_filename = os.path.join(os.path.dirname(ffmpeg_input), "original-" + os.path.basename(ffmpeg_input))
                    if os.path.exists(new_filename):
                        new_filename = os.path.join(os.path.dirname(ffmpeg_input), "original2-" + os.path.basename(ffmpeg_input))
                    os.rename(ffmpeg_input,new_filename)
                if os.path.exists(final_output):
                    # if folder already exists , delete
                    os.remove(final_output)
                os.rename(temp_output,final_output)
    return
# end encode_audio_files



# Run ffmpeg to actually re-encode
def reencode_audio_file_ffmpeg(logger, ffmpeg_cmd, ffmpeg_input, ffmpeg_output, ffmpeg_cover_art):

    found_error = False

    if not config['preferred']['test']:
        pp = subprocess.Popen(ffmpeg_cmd , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (output, err) = pp.communicate() # execute
        pp_status = pp.wait() # wait for command to finish

        # check if encoding failed
        if err:
            found_error = True
            # print error
            if debug:
                logger.debug("Error: encoding failed!\nffmpeg command:\n>" + ffmpeg_cmd)
                logger.debug("ffmpeg error: " + err)
            else:
                logger.debug("Error: encoding failed!\nffmpeg command:\n>" + ffmpeg_cmd)
                logger.debug("ffmpeg error:\n>" + err)

            # Ignore the error, put file in original state, delete file with error
            if config['preferred']['ignore_errors']:
                if debug:
                    logger.debug("Moving files back to original state")
                else:
                    print("   Moving files back to original state, and continuing to next file")
                if os.path.isfile(ffmpeg_output): 
                    os.remove(ffmpeg_output)
                os.rename(ffmpeg_input,ffmpeg_output)
            else:
                # Encoding failed, Exiting
                if debug: logger.debug("Exiting after failure")
                else: print("Exiting after failure")
                exit(1)
        else:
            found_error = False
            # encoding succeded

    return found_error


# end reencode_audio_file_ffmpeg



# Extract embedded cover art
def extract_cover_art_ffmpeg(logger, audio_file, cover_art_output_name, single_file=False):

    # if single_file:
    #     output_file = '
    #
    #     # make temp file for log
    #     temp_root_dir = os.path.join(tempfile.gettempdir(), 'audiobook_reencode')
    #     if not os.path.isdir(temp_root_dir):
    #         os.mkdir(temp_root_dir)
    #     output_file = os.path.join(temp_root_dir, "cover.jpg")
    output_file=cover_art_output_name

    logger.debug("-   > ffmpeg extracting: cover.jpg") # + output_file)
    if not config['preferred']['test']:
        cmd = 'ffmpeg -y -i "' + audio_file + '" "' + output_file + '"'
        pp = subprocess.Popen(cmd , stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        (output, err) = pp.communicate() # execute
        pp_status = pp.wait() # wait for command to finish
        # logger.debug(err)
    return
# end extract_cover_art_ffmpeg








# Extracting cover art from directory or mp3 file
def extract_cover_art(logger, dirpath, audio_files, audio_file_data, single_file=False):
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

    #   dirpath is the directory with audio files
    import random

    # create random cover art filename in temp folder
    temp_root_dir = os.path.join(tempfile.gettempdir(), 'audiobook_reencode')
    if not os.path.isdir(temp_root_dir):
        os.mkdir(temp_root_dir)


    cover_art = ''


    # See if we can fing cover art in dir
    if True:
        # Get lists of mp3, m4b/m4a, and jpg/png (full dir)
        cover_art_list = glob.glob(os.path.join(dirpath,'*.png')) + glob.glob(os.path.join(dirpath,'*.jpg')) 
        # mp3_files = glob.glob(os.path.join(dirpath,'*.[mM][pP]3'))
        # m4b_files = glob.glob(os.path.join(dirpath,'*.[mM]4[aAbB]'))
        # audio_files = mp3_files + m4b_files

        # Check to see if cover art should not be added to files in dir
        if not filename_similarity(logger, audio_files):
            logger.debug("-    > Cover art will not be added")
            dir_filename_similarity = False
            dir_cover_art = ''
        else:
            dir_filename_similarity = True

        # Set the cover art to image in dir
        if cover_art_list:
            # Check if a likly image is cover art
            # logger.debug("-   > Images exists: " # + str(cover_art_list))
            for image in cover_art_list:
                # cover.jpg or cover.png is the most likly
                if( re.search('cover\.jpg$', image, re.IGNORECASE) or re.search('cover\.png$', image, re.IGNORECASE) ):
                    dir_cover_art = image
                    break
                elif( re.search('cover', image, re.IGNORECASE) ): 
                    # prefer in cover is used anywhere in name
                    dir_cover_art = image
                    break
                elif(image): # not empty
                    # otherwise use the first image
                    dir_cover_art = image
                    break
                else:
                    print("Error in program: cover art image was found yet not.")
                    exit(1)
        else:
            # Extract cover art from audio file
            logger.debug("-    > No image files, cover art in dir")
            dir_cover_art = ''
  


    # See if embedded art exists


    # Extracting when the file chapters
    # if not config['preferred']['disable_split_chapters'] and audio_file_data
# TODO FIX


    if True:
            # Check if a file in dir has embedded art
            file_with_embedded_cover_art = ''
            for audio_file in audio_files:
                # add similarity to data file, just in case needed
                audio_file_data[audio_file]['dir_filename_similarity'] = dir_filename_similarity
                # extract art
                if audio_file_data.get(audio_file)['cover_art_embeded']:
                    file_with_embedded_cover_art = audio_file
                    
                    # Create random filename
                    random_cover_art_name = os.path.join(temp_root_dir, str(int(random.random()*100000000000)) + ".jpg")
                    #extract cover art
                    extract_cover_art_ffmpeg(logger, file_with_embedded_cover_art, random_cover_art_name, single_file)
                    audio_file_data[audio_file]['cover_art_file'] = random_cover_art_name
                    logger.debug("-    > Using cover art embedded in : " + os.path.basename(file_with_embedded_cover_art))
                else:
                    # no embedded art
                    if dir_cover_art:
                        # cover art is in dir, set it to data file
                        audio_file_data[audio_file]['cover_art_file'] = dir_cover_art


    logger.debug("-    > Cover art is: " + os.path.basename(cover_art))
    return audio_file_data
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
