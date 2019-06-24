#!/usr/bin/env python2
# -*- coding: utf-8 -*-

######################################################################################
######################################################################################
##                              m4b split
##  Author: valekhz
##  Contrib: Alex5719, ElieDeBrauwer, zymos
##  Date:   2010-2017
##  Description: converts m4b to mp3 and splits file into chapters
##  Requirements: ffmpeg, libmp4v2(optional)
##
##  Source: https://github.com/zymos/m4b-converter
##
##  References: https://github.com/valekhz/m4b-converter
##
#######################################################################################
#######################################################################################


##########################
# Import
#
import argparse
import ctypes
import datetime
import logging
import os
import re
import shutil
import subprocess
import sys
from textwrap import dedent



##########################
# Objects
#
class Chapter:
    # MP4 Chapter info.
    """
    Start, end, and duration times are stored in seconds.
    """
    def __init__(self, title=None, start=None, end=None, num=None):
        self.title = title
        self.start = round(int(start)/1000.0, 3)
        self.end = round(int(end)/1000.0, 3)
        self.num = num

    def duration(self):
        if self.start is None or self.end is None:
            return None
        else:
            return round(self.end - self.start, 3)

    def __str__(self):
        return '<Chapter Title="%s", Start=%s, End=%s, Duration=%s>' % (
            self.title,
            datetime.timedelta(seconds=self.start),
            datetime.timedelta(seconds=self.end),
            datetime.timedelta(seconds=self.duration()))





############################
# Functions
#


def run_command(log, cmdstr, values, action, ignore_errors=False, **kwargs):
    # Executes external command (FFMPEG) 
    # cmdstr = cmdstr + "xxx" # add and error to capture

    log.debug("Run_command: Command: %s" % cmdstr)
    log.debug("Run_command: Command with values: %s" % cmdstr%values)
    log.debug("Run_command: Action description: %s" % action)

    cmd = []

    # cmdstr=re.sub(' +', ' ', cmdstr)
    for opt in cmdstr.split(' '):
        cmd.append(opt % values)
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE )

    (stdout, output) = proc.communicate()
    if not ignore_errors and not proc.returncode == 0:
        msg = dedent('''
            An error occurred while %s.
              Command: %s
              Return code: %s
              Output: ---->
            %s''')
        log.error(msg % (action, cmdstr % values, proc.returncode, output))
        sys.exit(1)
    return output



def parse_args():
    # Parse command line arguments.

    parser = argparse.ArgumentParser(
        description='Split m4b audio book by chapters.')

    parser.add_argument('-o', '--output-dir', help='directory to store encoded files',
                        metavar='DIR')
    parser.add_argument('--custom-name', metavar='"STR"',
                        help='customize chapter filenames (see README)')
    parser.add_argument('--ffmpeg', default='ffmpeg', metavar='BIN',
                        help='path to ffmpeg binary (redundunt use encoder)')
    parser.add_argument('--encoder', metavar='BIN',
                        help='path to encoder binary (default: ffmpeg)')
    parser.add_argument('--encode-opts', default='-loglevel %(loglevel)s -y -i %(infile)s -ar %(sample_rate)d -ab %(bit_rate)dk -c:v copy %(outfile)s',
                        metavar='"STR"', help='custom encoding string (see README)')
    parser.add_argument('--ext', default='mp3', help='extension of encoded files (aac,flac,etc)')
    parser.add_argument('--pipe-wav', action='store_true', help='pipe wav to encoder')
    parser.add_argument('--skip-encoding', action='store_true',
                        help='do not encode audio (keep as .mp4)')
    parser.add_argument('--no-mp4v2', action='store_true',
                        help='use ffmpeg to retrieve chapters (not recommended)')
    parser.add_argument('--debug', action='store_true',
                        help='output debug messages and save to log file, also keeps tmp files')
    parser.add_argument('filename', help='m4b file(s) to be converted', nargs='+')

    parser.add_argument('--keep-tmp-files', action='store_true', 
            help='keep temporary files')
    parser.add_argument('--not-audiobook', action='store_true', 
            help='do not add genre=Audiobook')
    parser.add_argument('-b', '--bitrate', type=int, 
            help='bitrate for mp3 encoding, integer (example 64)')
    parser.add_argument('-s', '--samplerate', type=int,
            help='sample rate for mp3 encoding (example 22050')
    parser.add_argument('--extract-cover-art', action='store_true', 
            help='extracts cover art as cover.jpg')


    args = parser.parse_args()
    
    # if(args.custom_name):
        
    # else:
        # args.custom_name = '%(num)03d \- %(title)s'
        # args.custom_name_ = 1
    cwd = os.path.dirname(__file__)

    # Required when dropping m4b files onto m4b.py
    if not cwd == '':
        os.chdir(cwd)
        if args.output_dir is None:
            args.output_dir = cwd
    else:
        if args.output_dir is None:
            args.output_dir = os.getcwd()


    if args.encoder is None:
        args.encoder = args.ffmpeg

    return args




def setup_logging(args, basename):
    # Setup logger. 
    """In debug mode debug messages will be saved to a log file."""

    log = logging.getLogger(basename)

    sh = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)s: %(message)s")

    sh.setFormatter(formatter)

    if args.debug:
        level = logging.DEBUG
        filename = '%s.log' % basename
        fh = logging.FileHandler(os.path.join(os.path.dirname(__file__), filename), 'w')
        fh.setLevel(level)
        log.addHandler(fh)
    else:
        level = logging.INFO

    log.setLevel(level)
    sh.setLevel(level)
    log.addHandler(sh)

    log.debug('Logging started.')
    if args.debug:
        s = ['Options:']
        for k, v in args.__dict__.items():
            s.append('    %s: %s' % (k, v))
        log.debug('\n'.join(s))
    return log




def ffmpeg_metadata(args, log, filename):
    # Load metadata using the command output from ffmpeg.
    """
    Note: Not all chapter types are supported by ffmpeg and there's no Unicode support.
    ffprobe might work better
    """

    chapters = []
    
    # Grabbing metadata from ffmpeg, 
    # using 'ffprobe -show_chapters -print_format csv'  would work too
    values = dict(ffmpeg=args.ffmpeg, infile=filename)
    cmd = '%(ffmpeg)s -i %(infile)s'
    log.debug('Retrieving metadata from output of command: %s' % (cmd % values))

    output = run_command(log, cmd, values, 'retrieving metadata from ffmpeg output',
        ignore_errors=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    raw_metadata = (output.split("    Chapter ")[0]).split('Input #')[1]
    raw_chapters = output.split("    Chapter ")[1:]

    # Parse stream and metadata
    re_stream = re.compile(r'[\s]+Stream .*: Audio: .*, ([\d]+) Hz, .*, .*, ([\d]+) kb\/s')
    re_duration = re.compile(r'[\s]+Duration: (.*), start: (.*), bitrate: ([\d]+) kb\/s')

    try:
        stream = re_stream.search(output)
        sample_rate, bit_rate = int(stream.group(1)), int(stream.group(2))
    except Exception:
        sample_rate, bit_rate = 44100, 64

    metadata = {}
    for meta in raw_metadata.split('\n')[2:]:
        if meta.startswith('  Duration: '):
            m = re_duration.match(meta)
            if m:
                metadata['duration'] = m.group(1).strip()
                metadata['start'] = m.group(2).strip()
        else:
            key = (meta.split(':')[0]).strip()
            value = (':'.join(meta.split(':')[1:])).strip()
            metadata[key] = value

    # Parse chapters
    re_chapter = re.compile('^#[\d\.]+: start ([\d|\.]+), end ([\d|\.]+)[\s]+Metadata:[\s]+title[\s]+: (.*)')
    n = 1
    for raw_chapter in raw_chapters:
        m = re.match(re_chapter, raw_chapter.strip())
        start = float(m.group(1)) * 1000
        e = float(m.group(2)) * 1000
        duration = e - start
        title = unicode(m.group(3), errors='ignore').strip()
        chapter = Chapter(num=n, title=title, start=start, end=e)
        chapters.append(chapter)
        n += 1

    return chapters, sample_rate, bit_rate, metadata



def mp4v2_metadata(filename):
    # Load metadata with libmp4v2. 
    """Supports both chapter types and Unicode."""

    from libmp4v2 import MP4File

    mp4 = MP4File(filename)
    mp4.load_meta()

    chapters = mp4.chapters
    sample_rate = mp4.sample_rate
    bit_rate = mp4.bit_rate
    metadata = {}

    mp4.close()

    return chapters, sample_rate, bit_rate, metadata



def load_metadata(args, log, filename):
    # Load metadata from ffmpeg or libmp4v2
    if args.no_mp4v2:
        log.debug('Loading metadata using ffmpeg...')
        return ffmpeg_metadata(args, log, filename)
    else:
        log.debug('Loading metadata using libmp4v2...')
        return mp4v2_metadata(filename)



def show_metadata_info(args, log, chapters, sample_rate, bit_rate, metadata):
    # Show a summary of the parsed metadata.

    log.info(dedent('''
        \tDetected M4B Metadata:
          \t  Chapters: %d
          \t  Bit rate: %d kbit/s
          \t  Sampling freq: %d Hz''' % (len(chapters), bit_rate, sample_rate)))

    if args.debug and chapters:
        log.debug(dedent('''
            \tChapter data:
              \t  %s''' % '\n'.join(['  %s' % c for c in chapters])))

    if args.no_mp4v2 and not chapters:
        log.warning("No chapters were found. There may be chapters present but ffmpeg can't read them. Try to enable mp4v2.")
        log.info('Do you want to continue? (y/N)')
        cont = raw_input('> ')
        if not cont.lower().startswith('y'):
            sys.exit(1)



def extract_cover_art(args, log, output_dir, filename):
    # Extract the cover art to 'cover.jpg'.
    
    cover_file= os.path.join(output_dir, "cover.jpg")

    extract_values = dict(ffmpeg=args.ffmpeg, orig_file=filename, cover_file=cover_file)

    if(os.path.exists(cover_file)):
        log.debug('cover.jpg file already exists')
    else:
        extract_cmd = '%(ffmpeg)s -i %(orig_file)s -an -f image2 %(cover_file)s'
        # maybe add this -vframes 1
        log.info('Extracting cover art...')
        log.debug('Extract cover art command: %s' % (extract_cmd % extract_values))
        run_command(log, extract_cmd, extract_values, 'extracting cover art', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if(not(os.path.exists(cover_file))):
            log.info('Warning: cover art could not be extracted, this is a bug, sorry.')




def encode(args, log, output_dir, temp_dir, filename, basename, sample_rate, bit_rate, metadata):
    # Encode audio.

    # Create output and temp directory
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    if not os.path.isdir(temp_dir):
        os.makedirs(temp_dir)

    if args.skip_encoding:
        encoded_file = filename
        args.ext = 'mp4'
        return encoded_file
    else:
        fname = '%s.%s' % (basename, args.ext)
        encoded_file = os.path.join(temp_dir, fname)

    if(not(args.bitrate is None)): #bitrate from args
        log.debug('Setting bitrate to %d kbps' % (args.bitrate))
        bit_rate=args.bitrate
    elif(bit_rate <= 32 ): # 
        log.debug('Changing bitrate from %dk to 32k, to increase compatability' % bit_rate)
        bit_rate=32   
    elif(bit_rate >= 33 and bit_rate <= 48 ):  
        log.debug('Changing bitrate from %dk to 48k, to increase compatability' % bit_rate)
        bit_rate=48
    elif(bit_rate >= 49 and bit_rate <= 64 ): # bitrate of 63k is common for m4b, but not mp3
        log.debug('Changing bitrate from %dk to 64k, to increase compatability' % bit_rate)
        bit_rate=64        
    elif(bit_rate >= 65 and bit_rate <= 96 ):
        log.debug('Changing bitrate from %dk to 96k, to increase compatability' % bit_rate)
        bit_rate=96
    elif(bit_rate >= 97 and bit_rate <= 159 ): 
        log.debug('Changing bitrate from %dk to 128k, to increase compatability' % bitrate)
        bit_rate=128
    elif(bit_rate >= 160 ): 
        log.debug('Changing bitrate from %dk to 160k, to increase compatability' % bitrate)
        bit_rate=160        
    if(not(args.samplerate is None)): # sample rate from args
        log.debug('Setting sample rate to %d Hz' % (args.samplerate))
        sample_rate=args.samplerate

    if(args.debug): # improved ffmpeg debug output
        ffmpeg_loglevel='debug'
    else:
        ffmpeg_loglevel='panic'


    cmd_values = dict(ffmpeg=args.ffmpeg, encoder=args.encoder, infile=filename,
        sample_rate=sample_rate, bit_rate=bit_rate, outfile=encoded_file, loglevel=ffmpeg_loglevel)

    if os.path.isfile(encoded_file):
        log.info("Found a previously encoded file '%s'. Do you want to re-encode it? (y/N/q)" % encoded_file)
        i = raw_input('> ')
        if i.lower().startswith('q'):
            sys.exit(0)
        elif not i.lower() == 'y':
            return encoded_file

    # Build encoding options
    if not '%(outfile)s' in args.encode_opts:
        log.error('%(outfile)s needs to be present in the encoding options. See the README.')
        sys.exit(1)
    

    encode_cmd = '%%(encoder)s %s' % args.encode_opts
    if args.pipe_wav:
        encode_cmd = '%(ffmpeg)s -i %(infile)s -f wav pipe:1 | ' + encode_cmd
    
    log.info(dedent('''
        \tEncoding %s:
          \t  Bit rate: %d kbit/s
          \t  Sampling freq: %d Hz''' % (args.ext, bit_rate, sample_rate)))
    log.info('Encoding audio (may take some time)...')
    log.debug('Encoding with command: %s' % (encode_cmd % cmd_values))

    encode_cmd = re.sub(' +', ' ', encode_cmd) # double spaces change output to ' '
    run_command(log, encode_cmd, cmd_values, 'encoding audio', shell=args.pipe_wav, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    return encoded_file



def split(args, log, output_dir, encoded_file, chapters, temp_dir):
    # Split encoded audio file into chapters.
    """
    Note: ffmpeg on Windows can't take filenames with Unicode characters so we
    write the split file to a non-unicode temp file then rename it. This is not
    necessary on other platforms.
    """
    re_format = re.compile(r'%\(([A-Za-z0-9]+)\)')
    re_sub = re.compile(r'[\\\*\?\"\<\>\|]+')

    if(len(chapters) == 0): # no chapters, single file
        log.info("No chapters: using single encoded file")
        log.debug('Moving \n%s to \n%s' % (encoded_file,output_dir))
        try:
            shutil.move(encoded_file,output_dir)
        except:
            log.debug("File already exists,")
            log.debug('Removing %s' % (os.path.join(output_dir, os.path.basename(encoded_file))))
            os.remove(os.path.join(output_dir, os.path.basename(encoded_file)))
            try:
                log.debug('Moving \n%s to \n%s' % (os.path.basename(encoded_file),output_dir))
                shutil.move(encoded_file,output_dir)
            except:
                log.info("Error there is a problem")
    else:
        # for each chapter
        for chapter in chapters:
            values = dict(num=chapter.num, title=chapter.title, start=chapter.start, end=chapter.end, duration=chapter.duration(), chapters_total=len(chapters))
            
            # Create output filename
            # remove special chars, control chars and all around anoying chars
            if(not(args.custom_name)):
                 custom_name = '%(num)03d - %(title)s'
            else:
                 custom_name = args.custom_name
            chapter_name = re_sub.sub('', (custom_name % values).replace('/', '-').replace(':', '-'))
            if not isinstance(chapter_name, unicode):
                chapter_name = unicode(chapter_name, 'utf-8')
            chapter_name = re.sub('[^a-zA-Z0-9!\(\)\.,_\-µÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖ×ØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõö÷øùúûüýþÿ ]', '', chapter_name) # remove annoying chars
            # if chap name is blank or title=chap_num, correct
            if(chapter_name == ''): 
                log.debug("Invalid chapter name: %s, using '%(num)03d", chapter_name)              
                chapter_name = "%03d" % chapter.num
            if(chapter.title == "%03d" % chapter.num): 
                log.debug("Chapter number is the same as title, removing redundancy")              
                chapter_name = "%03d" % chapter.num
                # print(chapter_name)
                # sys.exit(0)


            chapter_name = re.sub(' +', ' ', chapter_name) # remove multiple space

            # temporarly rename file in windows
            if sys.platform.startswith('win'):
                fname = os.path.join(output_dir, '_tmp_%d.%s' % (chapter.num, args.ext))
            else:
                fname = os.path.join(output_dir, '%s.%s' % (chapter_name, args.ext))
            
            # cover art
            # cover_file=os.path.join(temp_dir, "cover.jpg")
            # if(chapter.num == 1):
                # cover_param='-c:v copy'
            # elif(os.path.exists(cover_file)):
                # log.debug("Adding cover metadata")
                # cover_param = '-i %(cover_file)s -map 0 -map 1 -c:v copy -metadata:s:v title=%(cover_title)s -metadata:s:v comment=%(cover_comment)s'
                # ffmpeg -i original.mp3 -i cover.png -map 0:0 -map 1:0 -metadata:s:v title="Album cover" -metadata:s:v comment="Cover (Front)" -id3v2_version 3 -write_id3v1 1 result.mp3
            # else: # no cover exist
                # cover_param=''
                # log.debug("No cover.jpg, not adding the metadata")
            metadata_param=''
            if(not(args.not_audiobook)): # add genre=Audiobook, should work with mp3 and m4b
                # log.debug("Adding genre=Audiobook")
                metadata_genre='-metadata genre=Audiobook' # -metadata:s:a genre=Audiobook maybe
                metadata_param=metadata_genre
            if(args.ext == 'mp3'): # add ID3 tag
                # log.debug("Adding mp3 id3")
                metadata_id3='-id3v2_version 3 -write_id3v1 1'
                metadata_param=" ".join([metadata_param, metadata_id3])
            # log.debug("Adding track metadata")
            metadata_track='-metadata track=' + str(chapter.num) + '/' + str(len(chapters))
            metadata_param=" ".join([metadata_param, metadata_track])
            log.debug("metadata params: %s", metadata_param)
            # metadata_param='-metadata genre=Audiobook -metadata track=1/1' 
            # cover_param='-c:v copy'

            if(args.debug):
                ffmpeg_loglevel='debug'
            else:
                ffmpeg_loglevel='panic'

            # Get ready to reencode
            values = dict(ffmpeg=args.ffmpeg, duration=str(chapter.duration()),
                start=str(chapter.start), metadata=metadata_param,
                tmp_enc_file=encoded_file, chap_file=fname.encode('utf-8'),
                loglevel=ffmpeg_loglevel)
            if(chapter.num == len(chapters)): # last chapter
                split_cmd = '%(ffmpeg)s -loglevel %(loglevel)s -y -i %(tmp_enc_file)s -c:a copy ' + metadata_param + ' -c:v copy -ss %(start)s %(chap_file)s'
                log.debug("Last chapter encode")
            else:
                split_cmd = '%(ffmpeg)s -loglevel %(loglevel)s -y -i %(tmp_enc_file)s -c:a copy ' + metadata_param + ' -c:v copy -t %(duration)s -ss %(start)s %(chap_file)s'

            # split_cmd = '%(ffmpeg)s -loglevel %(loglevel)s -y -i %(tmp_enc_file)s ' + cover_param + ' -c:a copy ' + metadata_param + ' -t %(duration)s -ss %(start)s %(chap_file)s'
            split_cmd = re.sub(' +', ' ', split_cmd) # double spaces change output to ' '
            #split_cmd = '%(ffmpeg)s -y -i %(outfile)s -c:a copy -c:v copy -t %(duration)s -ss %(start)s -metadata track="%(num)s/%(chapters_total)s" -id3v2_version 3 %(infile)s'
            # -metadata track="X/Y" -id3v2_version 3 -write_id3v1 1
            log.info("Splitting chapter %2d/%2d '%s.%s'..." % (chapter.num, len(chapters), chapter_name, args.ext))
            log.debug('Splitting with command: %s' % (split_cmd % values))

            run_command(log, split_cmd, values, 'splitting audio file', stdout=subprocess.PIPE, stderr=subprocess.PIPE)

            # Rename file in windows
            if sys.platform.startswith('win'):
                new_filename = os.path.join(output_dir, '%s.%s' % (chapter_name, args.ext))
                log.debug('Renaming "%s" to "%s".\n' % (fname, new_filename))
                shutil.move(fname, new_filename)



############################
# Main
#
def main():
    if sys.version_info[0] >= 3:
        raise Exception("This script sadly does not work with python3")

    # Current working directory
    cwd = os.getcwd()

    # parse arguments
    args = parse_args()

    # for each m4b file
    for filename in args.filename:
        
        # fixes relative path
        if(not(os.path.isabs(filename))):
            filename = os.path.join(cwd, filename)

        # create output directory
        # full_filename = os.path.join(cwd, filename)
        basename = os.path.splitext(os.path.basename(filename))[0]
        output_dir = os.path.join(args.output_dir, basename)
        # skip encoding xor create tmp dir
        if args.skip_encoding:
            temp_dir = output_dir
        else:
            temp_dir = os.path.join(output_dir, 'temp')

        # setup logging
        log = setup_logging(args, basename)

        # File does not exist
        if(not(os.path.isfile(filename))):
            log.info("File does not exist: '%s'." % filename)
            exit(1)

        output_dir = output_dir.decode('utf-8')

        # Print some basic info
        log.info("M4B Split: '%s'." % os.path.basename(filename))
        log.debug("Full filename: '%s'" % filename)
        log.debug("New directory for chapters: '%s' " % basename)
        log.debug("Output dir: '%s' " % output_dir)


        # grab metadata
        chapters, sample_rate, bit_rate, metadata = load_metadata(args, log, filename)
        show_metadata_info(args, log, chapters, sample_rate, bit_rate, metadata)

        # encode to mp3
        encoded_file = encode(args, log, output_dir, temp_dir, filename,
            basename, sample_rate, bit_rate, metadata)

        # extract the cover art
        if(args.extract_cover_art and not(args.pipe_wav)): # not sure if it can be piped
            extract_cover_art(args, log, output_dir, filename)
        
        # split into chapter files
        split(args, log, output_dir, encoded_file, chapters, temp_dir)

        # deletes temporary files
        if(not(args.keep_tmp_files) and not(args.skip_encoding)):
            log.debug("Cleaning up temporary files")
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    main()
