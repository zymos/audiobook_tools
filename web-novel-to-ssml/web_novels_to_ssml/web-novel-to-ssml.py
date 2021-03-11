#/usr/bin/python
# coding: utf-8


########### -*- coding: latin-1 -*-



##########################################################################
# 
# Source: Web Novel Downloader and Converter to SSML/TXT 
#
#   Autor: Zef the Tinker
#
#   Date: 2020-2021
#
#   License: GPLv3
#
#   Description: Download and extracts webnovels from websites.
#       Then optimizes the text for Text-To-Speach, and saves as
#       text or ssml.
#
#   Sources currently working:
#        * royalroad.com 
#
#   Tested:
#       https://www.royalroad.com/fiction/31429/cinnamon-bun/
#
#
#
# 
# Output file name: [publish date] - [TITLE].[txt|ssml]
#
#
#
#   Configure:
#       $XDG_CONFIG_HOME
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

# regex
import re

# system stuff
import sys
#  import getopt
import os.path

#  import urllib3

# html stuff
from lxml import html
from lxml import etree
from html import unescape # html excape to utf
from html.parser import HTMLParser

# get contents of webpage
import requests

# command line args
import argparse

#  import validators

# for sleep func debug
import time

# debugging
import pprint
    




######################################
# Parse Args
#
def parse_args():
    # CLI Arguments
    parser = argparse.ArgumentParser(description='Converts a post to a txt or ssml file.')

    parser.add_argument('INPUT', type=str, help='URL of post or file with list of URLs')

    #  parser.add_argument('-f', '--file', help='Use a file with list of URLs, instead of URL in CLI', action="store_true")
    parser.add_argument('--format', type=str, help='Format to output (json stores metadata)', choices=["txt", "ssml", "json"], default="txt")
    parser.add_argument('-a', '--speak-asterisk', help='Speaks out asterisk[*] (off by default)', action="store_true")
    parser.add_argument('-q', '--dont-remove-quotes', help='Leave quotes in place and may or may not be spoken (off by default)', action="store_true")
    parser.add_argument('--out', type=str, help='filename to output')

    args = parser.parse_args()
    
    return args
# END:  parse_args()



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
    #  print(line)
    while line:
        #  print(line, "'")
        if re.search('[a-zA-Z0-9]', line): # ignore blank lines
            urls.append(line)
        line = f.readline()
    f.close()

    # returns a list of urls
    return urls
# END:  open_file_of_urls(filename)





################################
# RoyalRoad: Extract web novels
#
# Function returns: articles raw txt with tags (not any of the rest of webpage) 
#       and filename to save output as
#
# [title]: ID3: TAL Album/Movie/Show title; or TT2
#   <meta property="og:title" content="*****title*****"/>
# 
# [Article Text start]: 
#   <div class="chapter-inner chapter-content">
#
# [Article Text end]:
#   </div>
#
# [Author] ID3: TCM Composer
#   <meta property="books:author" content="********"/> (not always)
#   <meta name="twitter:creator" content="*********">
#
#
# [publish date] ID3: TYE Year
#   <time unixtime="1597083201" datetime="2020-08-10T18:13:21.0000000Z" ...
#
# [Thumbnail] ID3: 
#   <meta property="og:image" content="********************">
#   <meta name="twitter:image" content="*******************">
#
# [Source] ID3: WAS Official audio source webpage
#   <meta property="og:url" content="*******************">
#
# [Source site] TPB Publisher
#    <meta property="og:site_name" content="Royal Road">
#
# [output filename]: 
#   [extracted publication date] - [extracted title].[format]
# 
#
#
# TAL Album/Movie/Show title



##############################################
# Royal Road site: text extraction
#
def extract_txt_royalroad(site_code):
    # site_code is entire website

    h = HTMLParser()
    
    # gets page in tree of code tags
    tree = html.fromstring(site_code.text)

    # Extracts chapter title
    #  <meta property="og:title" content="*****title*****"/>
    title = tree.xpath('//meta[@property="og:title"]/@content')[0]
    chap_title = re.sub(r'(.*) - (.*) - (.*)', r'\1 - \2', title)

    # Extracts book title
    #  <meta property="og:title" content="*****title*****"/>
    book_title = re.sub(r'.* - ', '', title)

    # Extracts author
    #  <meta name="twitter:creator" content="*********">
    author = tree.xpath('//meta[@name="twitter:creator"]/@content')[0]

    # Extracts cover art
    # <meta property="og:image" content="********************">
    cover = tree.xpath('//meta[@property="og:image"]/@content')[0]

    # Extracts source
    # <meta property="og:url" content="*******************">
    source = tree.xpath('//meta[@property="og:url"]/@content')[0]

    # extracts article contents
    # pages contents (found between <div class="chapter-inner chapter-content">
    content = tree.xpath('//div[@class="chapter-inner chapter-content"]')

    # extracts publication date
    # <time datetime="2020-08-10T18:13:21.0000000Z" format="U" >
    pub_date = tree.xpath('//time/@datetime')[0]
    pub_date = re.sub('T.*', '', pub_date)

    # extracts publication year
    # <time datetime="2020-08-10T18:13:21.0000000Z" format="U" >
    pub_year = re.sub('-.*', '', pub_date)

    # set extention for output file
    #  if( args.format == "txt"):
        #  filename_out = pub_date + " - " + chap_title + ".txt"
    #  else:
    filename_out = pub_date + " - " + chap_title
    

    #  print("  * Title: ", title)
    #  print("  * Chap Title: ", chap_title)
    #  print("  * Title: ", title)
    #  print("  * Publication Date: ", pub_date)
    #  print("  * Saving to filename: " + filename_out)


    meta = { 'author': author,
            'book_title': book_title,
            'chap_title': chap_title,
            'cover': cover,
            'source': source,
            'date': pub_date,
            'year': pub_year,
            'filename': filename_out }

    #  pprint.pprint(meta)

    # returns the string of articles txt, with tags and a decent filename to use
    return (content, meta)
# END: extract_txt_royalroad(site_code):







######################################################
# Wordpress site: text extraction
#
def extract_txt_wordpress(site_code):

    #
    # Wordpress text extraction notes
    #
    #   Test if wordpress: <meta name="generator" content="WordPress.com" />
    #
    #   Book title: <meta property="og:site_name" content="The Wandering Inn" />
    #
    #   Cover art:  <meta property="og:image" content="https://wanderinginn.files.wordpress.com/2016/11/erin.png?w=200" />
    #
    #   Pub date:   <meta property="article:published_time" content="2016-08-31T02:16:55+00:00" />
    #
    #   Chapter title:  <meta property="og:title" content="1.10" />
    #
    #   Article contents:   <div class="entry-content">
    #                       </div><!-- .entry-content -->
    #

    author = ''
    book_title = ''
    chap_title = ''
    cover = ''
    source = ''
    pub_date = ''
    pub_year = ''
    filename_out = ''

    #  article_text = ""
    #  article_title = ''
    #  article_date = ''
    #  article_write = 0
    #  line_cnt=0
    # TAG_RE = re.compile(r'<[^>]+>')
    
    #  h = HTMLParser()
    h = HTMLParser()
    
    # gets page in tree of code tags
    tree = html.fromstring(site_code.text)

    # Extracts chapter title
    #  <meta property="og:title" content="*****title*****"/>
    chap_title = tree.xpath('//meta[@property="og:title"]/@content')[0]

    # Extracts book title
    #  <meta property="og:site_name" content="*****title*****"/>
    book_title = tree.xpath('//meta[@property="og:site_name"]/@content')[0]


    # Extracts cover art
    # <meta property="og:image" content="********************">
    cover = tree.xpath('//meta[@property="og:image"]/@content')[0]


    # Extracts source
    # <meta property="og:url" content="*******************">
    source = tree.xpath('//meta[@property="og:url"]/@content')[0]
    

    # Pub date
    # <meta property="article:published_time
    pub_date = tree.xpath('//meta[@property="article:published_time"]/@content')[0]
    pub_date = re.sub('T[0-2].*', '', pub_date)
    pub_year = re.sub('-.*', '', pub_date)



    # extracts article contents
    # pages contents (found between <div class="entry-content">
    content = tree.xpath('//div[@class="entry-content"]')

    # pages text
    #  html_content = site_code.text

    #  # split pages text into lines
    #  #   todo change to tree.xpath
    #  for line in html_content.split('\n'):
        #  line_cnt += 1
        #  # pages_line = line
        #  # print str(article_write) + "/" + str(line_cnt) + ": " + line

        #  # Get publish date
        #  if re.search('<meta property="article:published_time"', line):
            #  pub_date = re.sub('<meta property="article:published_time" content="', '', line)
            #  pub_date = re.sub('T[0-2].*', '', article_date)
            #  # extracts publication year
            #  pub_year = re.sub('-.*', '', pub_date)


        #  # Get posts title
        #  if re.search('<meta property="og:title"', line):
            #  chap_title = re.sub('<meta property="og:title" content="', '', line)
            #  chap_title = re.sub('".*', '', article_title)
            #  #  article_title = h.unescape(article_title.decode('utf-8',errors='ignore'))

        #  # article has ended
        #  if re.search('<!-- .entry-content -->', line):
            #  article_write = 0
            #  article_text += "</speak>"
        
        #  # Adding article text
        #  if article_write:
            #  article_text += line + "\n"

        #  # Article has started
        #  if re.search('<div class="entry-content">', line):
            #  article_write = 1
            #  article_text += article_title + "<break time=\"1s\" />\n\n"
       
    #  # print article_text.encode('utf-8')
    #  content = "<speak>\n<!--\nWordpress articles post: Metadata\n   <meta property=\"og:title\" content=\"\" />\n    <meta property=\"og:url\" content=\"\" />\n    <meta property=\"article:published_time\" content=\"\" />\n    <meta property=\"og:site_name\" content=\"\" />\n    <meta property=\"og:image\" content=\"\" />\n-->\n    <metadata>\n        <dc:date><dc:date>\n        <dc:publisher></dc:publisher>\n        <dc:source></dc:source>\n     <dc:title></dc:title>\n    </metadata>\n" + article_text



    # set extention for output file
    filename_out = pub_date + " - " + chap_title


    meta = { 'author': author,
            'book_title': book_title,
            'chap_title': chap_title,
            'cover': cover,
            'source': source,
            'date': pub_date,
            'year': pub_year,
            'filename': filename_out }


    return (content, meta)
# END: wordpress








#########################################################
# Correct articles text for better speach
#
def generate_ssml(content):

    article_write = 0
    line_cnt=0

    # add tag if ssml
    #  if( args.format == "ssml"):
        #  article_text = "<speak>\n"
    #  else:
        #  article_text = ""
    
    #  print("type", type(content))
    article_text = "<speak>\n"

    for line in content:
        #  print("line type", type(line))
        #  print("line etree", type(etree.tostring(line)))
        # line_mod is the output

        line_mod = etree.tostring(line).decode('utf-8')

        #  line_mod = line.decode('utf-8')
        

        # text line adds break
        line_mod = re.sub('<p>', '', line_mod)

        line_mod = re.sub('</p>', '@!@!@!@!break time="200ms"/!@!@!@!@\n', line_mod)

        # nbsp space
        line_mod = re.sub('&nbsp;', '@!@!@!@!break time="200ms"/!@!@!@!@  ', line_mod)
        
        # line breaks
        line_mod = re.sub('<br ?[\/]?>', "@!@!@!@!break time=\"400ms\"/!@!@!@!@\n", line_mod)
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

        #  â<80><99> problem   0xE2, 0x80 and 0x99
        #  line_mod = re.sub(u"\xE2\x80\x99",  "", line_mod) #byte substitute

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
        

        # Removes Previous Chapter Next Chapter
        line_mod = re.sub('Previous Chapter\s*Next Chapter', '', line_mod)

        
        # Avoid removing ssml tags
        line_mod = re.sub('@!@!@!@!', '<', line_mod)
        line_mod = re.sub('!@!@!@!@', '>', line_mod)
        
        # if txt file remove all html tags
        #  if ( args.format == "txt"):
            #  line_mod = re.sub('<[^>]+>', '', line_mod) # remove any tags


        # Add line to text
        article_text += line_mod + "\n"

    # add tag if ssml
    #  if( args.format == "ssml"):
        #  article_text = "</speak>\n"
    article_text += "</speak>\n"

    # return modified text
    return article_text
# END: generate_ssml()





##########################################################
# Process each URLs
#
def process_url(url):
    global args

    # grab the url text
    try:
        #  response = urllib3.urlopen(url)
        site_code = requests.get(url)
    except:
        print("Error: not a valid URL: " + url)
        return


    html_content = site_code.text

    #  print(html_content)
    # decide which web novel source and how to extract text 
    # and a useful output filename to use
    #  usually [publication date] - [article title].[output format]
    if re.search(r"royalroad\.com", url, re.IGNORECASE):
        if DEBUG: print("  > Royal Road article found")
        (content, meta) = extract_txt_royalroad(site_code)
    elif( re.search(r'meta name="generator" content="WordPress.com"', html_content, re.IGNORECASE)):
        if DEBUG: print("  > WordPress article found")
        (content, meta) = extract_txt_wordpress(site_code)
    else:
        print("  >Unknown web-novel type for\'", url, "'")
        print("Skipping...")
        return


    # process each line for basic correction to make tts better with less 
    # incorrect speach
    article_ssml = generate_ssml(content)
    article_text  = re.sub('<[^>]+>', '', article_ssml) # remove any tags

    #  print(article_ssml)
    # print article 
    if DEBUG: print(article_text)

    # Write to output file
    if(args.format == "json"):
        # json stores metadata, article txt and ssml
        import json
        # Write meta info to file
        meta['txt'] = str(article_text)
        meta['ssml'] = str(article_ssml)
        meta_json = json.dumps(meta)
        file = open(meta['filename'] + '.json', "w")
        file.write(meta_json)
        file.close()
    elif(args.format == "ssml"):
        file = open(meta['filename'] + ".ssml", "w")   
        file.write(article_ssml)
        file.close()
    else: # text
        file = open(meta['filename'] + ".txt", "w")   
        file.write(article_text)
        file.close()


# END: process_url()




####################################################
# Main
#
def main():
    
    # Process command line args
    global args 
    args = parse_args()

    load_config_file()

    # Get urls
    urls = []
    # if its a file, open it and treat as a list of urls
    if os.path.isfile(args.INPUT):
        print("Opening file of URLs")
        urls = open_file_of_urls(args.INPUT)
        #  pprint.pprint(urls)
    else:
        # if not a file, input is treated as url
        urls.append(args.INPUT)


    # process urls
    for url in urls:
        print(" >Processing URL:", url.rstrip())
        process_url(url.rstrip())
# END: def main()
      



######################################################
# Start it up
if __name__ == "__main__":
   main()
