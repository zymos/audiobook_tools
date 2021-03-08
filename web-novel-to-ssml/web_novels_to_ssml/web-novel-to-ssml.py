#/usr/bin/python
# -*- coding: latin-1 -*-



##########################################################################
# 
# Source: royalroad.com 
#
#
# [title]: 
#   <meta property="og:title" content="*****title*****"/>
# 
# [Text start]: 
#   <div class="chapter-inner chapter-content">
# [Text end]:
#   </div>
#
# Output file name: [TITLE].ssml
#
# 
# [publish date] 
#   <time unixtime="1597083201" datetime="2020-08-10T18:13:21.0000000Z" 
#
# [Thumbnail]
#   <meta name="twitter:image" content="
#
# 
# Output file name: [publish date] - [TITLE].[txt|ssml]
#
#
#
#
# bugs
#   Chapter Sixty-Eight
#   "You're Awawen? Hi Awawen! Let's be friends!"
#   Youâre Awawen? Hi Awawen! Letâs be friends!
#
#########################################################################




#########################################################################
# Configure
#

DEBUG = 0









##########################################################################
# Code
#


##########################
# imports
#
import re
import sys
import getopt

import urllib3
from lxml import html

from lxml import etree
from html import unescape # html excape to utf

import requests
from html.parser import HTMLParser
import argparse
#  import validators
# for sleep func debug
import time
import os.path







############################
# Parse Args
#
def parse_args():
    # CLI Arguments
    parser = argparse.ArgumentParser(description='Converts a post to a txt or ssml file.')

    parser.add_argument('INPUT', type=str, help='URL of post or file with list of URLs')

    #  parser.add_argument('-f', '--file', help='Use a file with list of URLs, instead of URL in CLI', action="store_true")
    parser.add_argument('--format', type=str, help='Format to output', choices=["txt", "ssml"], default="txt")
    parser.add_argument('-a', '--speak-asterisk', help='Speaks out asterisk[*] (off by default)', action="store_true")
    parser.add_argument('-q', '--dont-remove-quotes', help='Leave quotes in place and may or may not be spoken (off by default)', action="store_true")
    parser.add_argument('--out', type=str, help='filename to output')

    args = parser.parse_args()
    
    return args





############################
# Process file
#
def open_file_of_urls(filename):
    # open file
    urls = []

    # open file
    f = open(filename, "rt")

    # read each line into array
    line = f.readline()
    while line:
        if not re.match('[a-zA-Z0-9]', line): # ignore blank lines
            urls.append(line)
        line = f.readline()
    f.close()

    # returns a list of urls
    return urls

############################
# Extract web novels txt from royalroad site

def extract_txt_royalroad(url):

    try:
        #  response = urllib3.urlopen(url)
        response = requests.get(url)
    except:
        print("Error: not a valid URL: " + url)
        return
    
    h = HTMLParser()

    tree = html.fromstring(response.text)

    #  <meta property="og:title" content="*****title*****"/>
    article_title = tree.xpath('//meta[@property="og:title"]/@content')[0]

    # pages contents (found between <div class="chapter-inner chapter-content">
    content = tree.xpath('//div[@class="chapter-inner chapter-content"]')

    pub_date = tree.xpath('//time/@datetime')[0]
    #  print(pub_date)
    pub_date = re.sub('T.*', '', pub_date)
    #  ="2020-08-10T18:13:21.0000000Z" format="U" >

    # returns the string of articles txt, publication date and title

    # set extention for output file
    if( args.format == "txt"):
        filename = pub_date + " - " + article_title + ".txt"
    else:
        filename = pub_date + " - " + article_title + ".ssml"
    
    print("  * Title: ", article_title)
    print("  * Publication Date: ", pub_date)
    print("  * Saving to filename: " + filename_out)


    return (content, filename_out)


############################
# Process each URLs
#
def process_url(url):
    global args

    if( re.match('royalroad\.com', url )):
        (content, filename) = extract_txt_royalroad(url)
    else:
        return

    article_text = ""
    article_title = ''
    article_date = ''
    article_write = 0
    line_cnt=0
    
    for line in content:
    #  for line in html_content.split('\n'):


        # line_mod is the output
        line_mod = etree.tostring(line).decode('utf-8')

        # text line adds break
        line_mod = re.sub('<p>', '', line_mod)

        line_mod = re.sub('</p>', '@!@!@!@!break time="200ms"/!@!@!@!@\n', line_mod)

        # nbsp space
        line_mod = re.sub('&nbsp;', '@!@!@!@!break time="200ms"/!@!@!@!@  ', line_mod)
        
        # line breaks
        line_mod = re.sub('<br ?[\/]?>', "\n", line_mod)
        #  line_mod = re.sub('<br \\>', "\n", line_mod)


        # convert html escape code
        line_mod = unescape(line_mod)

        # remove spoken asterisk
        if not args.speak_asterisk:
            line_mod = re.sub('\*', '', line_mod)

        # remove spoken quotes
        if not args.dont_remove_quotes:
            line_mod = re.sub('[“”„“‟”"❝❞⹂〝〞〟＂]', '', line_mod)
            # line_mod = re.sub("['\''’‚‘´\`]", "’", line_mod)
            
            # sed 's/['\''’‚‘´\`]/’/g' |\
            # sed 's/[“”„“‟”"❝❞⹂〝〞〟＂]/"/g' |\
            # sed 's/…/\.\.\. /g' |\
            # sed 's/[–]/-/g'  `</speak>"
        # —

        # fix single quotes
        line_mod = re.sub("['\''’‚‘´\`']", "’", line_mod)
        #  â

        # emphasised text
        line_mod = re.sub('<strong>', '@!@!@!@!emphasis level="moderate"!@!@!@!@', line_mod)
        line_mod = re.sub('</strong>', '@!@!@!@!/emphasis!@!@!@!@\n', line_mod)

        line_mod = re.sub('<em>', '@!@!@!@!emphasis level="moderate"!@!@!@!@', line_mod)
        line_mod = re.sub('</em>', '@!@!@!@!/emphasis!@!@!@!@\n', line_mod)

        line_mod = re.sub('<[^>]+>', '', line_mod) # remove any html tags codes not em, strong
        
        
        # Extra breaks
        # ': ', '…', '—' '—-' '—'
        line_mod = re.sub('—-', '@!@!@!@!break time="200ms"/!@!@!@!@ ', line_mod)
        line_mod = re.sub('—', '@!@!@!@!break time="200ms"/!@!@!@!@ ', line_mod)
        line_mod = re.sub('…', '@!@!@!@!break time="200ms"/!@!@!@!@ ', line_mod)
        # add pause for colon "Speaking: Words"
        if re.search('[a-zA-Z]: [a-zA-Z]', line_mod): 
            line_mod = re.sub(': ', '@!@!@!@!break time="200ms"/!@!@!@!@ ', line_mod)

        
        # Avoid removing ssml tags
        line_mod = re.sub('@!@!@!@!', '<', line_mod)
        line_mod = re.sub('!@!@!@!@', '>', line_mod)
        
        # if txt file remove all html tags
        if ( args.format == "txt"):
            line_mod = re.sub('<[^>]+>', '', line_mod) # remove any tags


        # Add line to text
        article_text += line_mod + "\n"

    # end loop for each line
    
    # print article 
    if DEBUG: print(article_text)

    file = open(filename, "w")
    
    # add ssml tags and write to file
    if( args.format == "ssml"):
        file.write("<speak>\n" + article_text + "</speak>\n")
    else:
        file.write(article_text)

    file.close()





############################
# Main
#
def main():
    # argv = sys.argv[1:]
    
    # Process command line args
    global args 
    args = parse_args()
    
    #  url = args.URL
    
    # url = 'https://www.royalroad.com/fiction/31429/cinnamon-bun/chapter/533652/chapter-sixty-seven-fairness'

    # print('ARGV      :', url)
    urls = []
    if os.path.isfile(args.INPUT):
        print("Opening file of URLs")
        urls = open_file_of_urls(args.INPUT)
    else:
        urls.append(args.INPUT)

    for url in urls:
        print(" >Processing URL:", url)
        process_url(url)

# def main() ...end...
      



#################################
# Start it up
if __name__ == "__main__":
   main()
