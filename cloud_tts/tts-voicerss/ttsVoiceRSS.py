#!/usr/bin/python2
# -*- coding: latin-1 -*-


########################################
# Configure
# 

DEBUG=1
VOICE='Linda'
LOCALE='en-us'
KEY='f46e67af78d74976833caaaed05b9719'
CHARACTOR_LIMIT=10000



#######################################
# Code
#

import pprint
import voicerss_tts
import os
#  import getopt
import argparse
import tempfile
import sys

######################################
# CLI Arguments
parser = argparse.ArgumentParser()
parser.add_argument('EBOOK', type=str, help='ebook txt file')
#  parser.add_argument('--format', help='Format of each file')
#  parser.add_argument('-a', '--speak-asterisk', help='Speaks out asterisk[*] (off by default)', action="store_true")
#  parser.add_argument('-q', '--dont-remove-quotes', help='Leave quotes in place and may or may not be spoken (off by default)', action="store_true")
args = parser.parse_args()

#  url = args.URL



#####################
# get the text


print("Opening: " + os.path.abspath(args.EBOOK))

# Initialize
text='eat me, please'
chunk_cnt=0
char_cnt=0
ebook_txt_chunks=[''] * 1000
tmp_dir = tempfile.mkdtemp() #tmp dir to store mp3 chunks

print("Temp folder ", tmp_dir)

# Open file
try:
    fin=open(os.path.abspath(args.EBOOK), 'r')
except:
    print("Error: Could not open file!")

# read first line
ebook_txt_line = fin.readline()
#while book has lines
while ebook_txt_line:
    # increment text chunk if > 90% of char limit, and reset cnt
    if char_cnt > CHARACTOR_LIMIT * 0.9:
        if DEBUG: print ("chunk count ", chunk_cnt, "; char_cnt: ", char_cnt)
        chunk_cnt = chunk_cnt + 1
        char_cnt = 0
    # increment current char cnt for chunk
    char_cnt = char_cnt + len(ebook_txt_line)
    # add text to chunk
    ebook_txt_chunks[chunk_cnt] = ebook_txt_chunks[chunk_cnt] + ebook_txt_line
    #read next line
    ebook_txt_line = fin.readline()

# close file
fin.close()
if DEBUG: print ("  > chunk count ", chunk_cnt, "; char_cnt: ", char_cnt)


print("Converting file in ", chunk_cnt, " peices.")



#####################
# request the speech
cnt=0
for chunk in ebook_txt_chunks:
    cnt = cnt + 1
    sys.stdout.write(".")
    if (chunk == ''): break # if text is empty break out of loop
    voice = voicerss_tts.speech({
            'key': KEY,
            'hl': LOCALE,
            'v': VOICE,
            'src': chunk,
            'r': '0',
            'c': 'mp3',
            'f': '16khz_16bit_stereo',
            'ssml': 'false',
            'b64': 'false'
        })
    if voice['error']:
        print("Error by VoiceRSS detected while converting chunk", cnt)
        print("Error: " + voice['error'])
        exit(1)

    if DEBUG: print("writing ,", str(cnt) + 'out.mp3')
    f = open(os.path.join(tmp_dir, str(cnt) + 'out.mp3'), 'w')
    #  try:
    f.write(voice['response'])
    #  except:
        #  print("Error: failure output file write, "  str(chunk) + 'out.mp3')
    f.close()

#  if(DEBUG):  
    #  pprint.pprint(voice['error'])
    #  print(type(voice['error']))

# check if failed
if(voice['error'] is None):
    print("success")
    #  print(voice['response'])
else:
    print("Error detected: " + voice['error'])
    exit(1)


####################
# Output the file




