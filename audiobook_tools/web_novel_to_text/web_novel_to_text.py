#/usr/bin/python
# coding: utf-8

"""
##############################################################################
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
#       * royalroad.com 
#       * wordpress articles
#       * to add: Webnovel, Wattpad, scribblehub.com
#   Tested:
#       https://www.royalroad.com/fiction/31429/cinnamon-bun/
#       https://wanderinginn.com/table-of-contents/
#
#
#
# 
# Output file name: [publish date] - [TITLE].[txt|ssml]
#
#
#
# bugs
#   check it if date all ready exists
#
# TODO
#   use config file
#   embed meta in ssml comments
#   configurable output filename
#   option: no empisis
#
###############################################################################
"""



##############################################################################
# Configure
#

DEBUG = 1
TEST = 0








###############################################################################
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
    
# for filenames with spelled out numbers TODO
use_text2digits = 1
try:
    from text2digits import text2digits
except:
    print("Warning: module 'text2digits' not installed")
    print("   Used for converting spelled out numbers to numeric charactors")
    print("   Useful for keeping file names in order when spelled out chapters")
    print("   Install: pip3 install text2digits")
    use_text2digits = 0




######################################
# Parse Args
#
def parse_args():
    """
    get args
    """

    # CLI Arguments
    parser = argparse.ArgumentParser(description='Converts a post to a txt or ssml file.')

    parser.add_argument('INPUT', type=str, help='URL of post or file with list of URLs')

    #  parser.add_argument('-f', '--file', help='Use a file with list of URLs, instead of URL in CLI', action="store_true")
    parser.add_argument('--format', type=str, help='Format to output (json stores metadata)', choices=["txt", "ssml", "json"])
    parser.add_argument('-a', '--speak-asterisk', help='Speaks out asterisk[*] (off by default)', action="store_true")
    parser.add_argument('-q', '--dont-remove-quotes', help='Leave quotes in place and may or may not be spoken (off by default)', action="store_true")
    parser.add_argument('--dont-emphasize', help='Don\'t use emphasize tag in ssml', action="store_true")
    parser.add_argument('--output-format', type=str, help='filename to output')

    args = parser.parse_args()
    
    if DEBUG: pprint.pprint(args)

    return args
# END:  parse_args()




##########################################
# Config file
#
# def load_config():
#     """
#     Config file
#     """

#     # Get config file location
#     global config
#     config = {}

#     # set app name and gets config location
#     appname = "audiobook-tools"
#     appauthor = "audiobook-tools"
#     config_filename = "web-novel-to-text.conf"
#     config_file = os.path.join(user_config_dir(appname, appauthor), config_filename) 
#     default_config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), config_filename)
    
#     #  print(default_config_file)

#     # read config file
#     if os.path.isfile(config_file):  
#         cfg = configparser.ConfigParser()
#         cfg.read(config_file)
#     elif os.path.isfile(default_config_file):
#         print("Config file:", default_config_file)
#         cfg = configparser.ConfigParser()
#         cfg.read(default_config_file)
#     else:
#         print("Config file not found.")
#         print(" Not:", config_file)
#         print(" Not:", default_config_file)
#         exit(1)

#     # create dictionary
#     config = {s:dict(cfg.items(s)) for s in cfg.sections()}

#     # Variables
#     # config['GENERAL']['delay_between_requests']



#     # Set Prefered settings

#     #  Overrides via commandline
#     #  voice
#     #  config.update({'preferred':{'voice': ''}})
#     #  if( args.voice ):
#         #  config['preferred']['voice'] = args.voice
#     #  elif config[config['GENERAL']['tts_service']].get('voice') is not None:
#         #  config['preferred']['voice'] = config[config['GENERAL']['tts_service']]['voice'] 



#     ####################
#     # Preferred Settings
    
#     # create the 'preferred' key
#     config.update({'preferred':{'preferrences': 1}})

#     # TTS Service
#     #  if args.profile :
#         #  if config[args.profile].get('tts_service') is not None:
#             #  config['preferred']['tts_service'] = config[args.profile]['tts_service']
#         #  else:
#             #  config['preferred']['tts_service'] =  config['GENERAL']['tts_service']
#     #  else:
#         #  config['preferred']['tts_service'] =  config['GENERAL']['tts_service']
#     #  print("------------------------------------------------")
#     #  print("            a",vars(args)['format'])
#     #  print("            a",type(vars(args)))

#     #  pprint.pprint(vars(args))
#     #  pprint.pprint(vars(args).keys())

#     #  print("================================================")
#     # Preferred vars 
#     preferred_vars = ('format','delay_between_requests')
#     # go through each setting
#     for setting in preferred_vars:
#         config['preferred'].update({setting: ''}) 
#         if setting in vars(args).keys(): # var exists
#             if vars(args)[setting]: # var is set
#                 config['preferred'][setting] = vars(args)[setting]
#         elif config['GENERAL'].get(setting) is not None:
#             config['preferred'][setting] = config['GENERAL'][setting] 
    

#     # Debugging and testing
#     config.update({'DEBUG':{'debug': False}})
#     config['DEBUG'].update({'test': False})
#     if DEBUG:
#         config['DEBUG']['debug'] = True
#     if TEST:
#         config['DEBUG']['test'] = True


#     # Places to store variables
#     #  config.update({'INPUT':{'filename': ''}}) 
#     #  config.update({'INPUT':{'text': ''}}) 
#     #  config.update({'INPUT':{'text_ssml': ''}}) 
#     #  config.update({'INPUT':{'text_chunk': ''}}) 
#     #  config.update({'OUTPUT':{'filename': ''}}) 
#     #  config.update({'TMP':{'tmp_dir': tmp_dir}})

#     if DEBUG: 
#         print("Config file:", config_file)
#         print("------------------------config------------------------")
#         pprint.pprint(config)
#         print("------------------------------------------------------")
#     #  return config
# # End load_config










###########################################
# Process file
#
def open_file_of_urls(filename):
    """
    open file create list of urls
    """

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





#########################################
# RoyalRoad: Extract web novels
#

def extract_txt_royalroad(site_code):
    """
    Function returns: articles raw txt with tags (not any of the rest of webpage) 
         and filename to save output as

    [title]: ID3: TAL Album/Movie/Show title; or TT2
     <meta property="og:title" content="*****title*****"/>

    [Article Text start]: 
     <div class="chapter-inner chapter-content">

    [Article Text end]:
     </div>

    [Author] ID3: TCM Composer
     <meta property="books:author" content="********"/> (not always)
     <meta name="twitter:creator" content="*********">


    [publish date] ID3: TYE Year
     <time unixtime="1597083201" datetime="2020-08-10T18:13:21.0000000Z" ...

    [Thumbnail] ID3: 
     <meta property="og:image" content="********************">
     <meta name="twitter:image" content="*******************">

    [Source] ID3: WAS Official audio source webpage
     <meta property="og:url" content="*******************">

    [Source site] TPB Publisher
      <meta property="og:site_name" content="Royal Road">

    [output filename]: 
     [extracted publication date] - [extracted title].[format]

    TAL Album/Movie/Show title

    """

    # site_code is entire website

    #h = HTMLParser()
    
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




    meta = { 'author': author,
            'book_title': book_title,
            'chap_title': chap_title,
            'cover': cover,
            'source': source,
            'date': pub_date,
            'year': pub_year,
            'filename': '' }


    meta = create_filename(meta)

    #  pprint.pprint(meta)
    #  pprint.pprint(meta)

    # returns the string of articles txt, with tags and a decent filename to use
    return (content, meta)
# END: extract_txt_royalroad(site_code):







################################################
# Wordpress site: text extraction
#
def extract_txt_wordpress(site_code):

    """
     Wordpress text extraction notes
    
     Test if wordpress: <meta name="generator" content="WordPress.com" />
    
     Book title: <meta property="og:site_name" content="The Wandering Inn" />
    
     Cover art:  <meta property="og:image" content="https://wanderinginn.files.wordpress.com/2016/11/erin.png?w=200" />
    
     Pub date:   <meta property="article:published_time" content="2016-08-31T02:16:55+00:00" />
    
     Chapter title:  <meta property="og:title" content="1.10" />
    
     Article contents:   <div class="entry-content">
                         </div><!-- .entry-content -->
    """

    author = ''
    book_title = ''
    chap_title = ''
    cover = ''
    source = ''
    pub_date = ''
    pub_year = ''
    # filename_out = ''


    
    #  h = HTMLParser()
    
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
    


    meta = { 'author': author,
            'book_title': book_title,
            'chap_title': chap_title,
            'cover': cover,
            'source': source,
            'date': pub_date,
            'year': pub_year,
            'filename': '' }


    meta = create_filename(meta)

    return (content, meta)
# END: wordpress





#########################################
# Create filename
#
def create_filename(meta):
    """
        meta = { 'author': author,
            'book_title': book_title,
            'chap_title': chap_title,
            'cover': cover,
            'source': source,
            'date': pub_date,
            'year': pub_year,
            'filename': '' }
    """

    filename_out = meta['date'] + " - " + meta['chap_title']


    filename_out = re.sub(r"[\?:\"\|\*\\><]", ".", filename_out) 

    if(config['preferred']['format'] == "json"):
        filename_out = filename_out + '.json'
    elif(config['preferred']['format']== "ssml"):
        filename_out = filename_out + ".ssml"
    else: # text
        filename_out = filename_out + ".txt"   


    meta['filename'] = filename_out

    return meta
# End create_filename()





##########################################################
# Process each URLs
#
def process_url(url):
    """
    Process each URL
    """
    #  global args

    # grab the url text
    try:
        #  response = urllib3.urlopen(url)
        site_code = requests.get(url)
    except:
        print("Error: not a valid URL: " + url)
        return

    # get html text
    html_content = site_code.text

    # print("######################html###############################")
    # print(html_content)
    # print("################### html (end) ##########################")

    # decide which web novel source and how to extract text 
    #   and a useful output filename to use
    if re.search(r"royalroad\.com", url, re.IGNORECASE):
        if config['DEBUG']['debug']: print("  > Royal Road article found")
        (content, meta) = extract_txt_royalroad(site_code)
    elif( re.search(r'meta name="generator" content="WordPress.com"', html_content, re.IGNORECASE)):
        if config['DEBUG']['debug']: print("  > WordPress article found")
        (content, meta) = extract_txt_wordpress(site_code)
    else:
        print("  > Unknown web-novel type for\'", url, "'")
        print("Skipping...")
        return

    # Convert to single string from etree
    article_html = ''
    for line in content:
        article_html += str(etree.tostring(line)).strip()    

    # print("@@@@@@@@@@@@@@@@@@@@ article_html @@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print(article_html)    
    # print("@@@@@@@@@@@@@@@@@ article_html (end) @@@@@@@@@@@@@@@@@@@@@@@")


    # process each line for basic correction to make tts better with less 
    # incorrect speach
    try:
        from audiobook_tools.common.text_conversion import html_article2ssml
    except:
        print("error loading audiobook_tools python files")
        exit(1) 
    article_ssml = html_article2ssml(article_html, config, args)

    # Convert ssml to text
    try:
        from audiobook_tools.common.text_conversion import ssml2text
    except:
        print("error loading audiobook_tools python files")
        exit(1)
    #article_text  = re.sub('<[^>]+>', '', article_ssml) # remove any tags
    article_text = ssml2text(article_ssml)

    #  if DEBUG: 
        #  print("----------------------TEXT-------------------------------")
        #  print(article_text)
        #  print("---------------------------------------------------------")
        # print(article_ssml)

    # Write to output file (without invalid chars)
    #  meta['filename'] = re.sub(r"[\?:\"\|\*\\><]", ".", meta['filename'] ) 
    if(config['preferred']['format'] == "json"):
        # json stores metadata, article txt and ssml
        import json
        # Write meta info to file
        meta['txt'] = str(article_text)
        meta['ssml'] = str(article_ssml)
        text_w = json.dumps(meta)
        #  filename = meta['filename'] + '.json'
    elif(config['preferred']['format']  == "ssml"):
        #  filename = meta['filename'] + ".ssml"
        text_w = article_ssml
    else: # text
        #  filename = meta['filename'] + ".txt"   
        text_w = article_text
    
    # Writing file
    file = open(meta['filename'], "w")   
    file.write(text_w)
    file.close()

    # Sleep between Requests
    time.sleep(float(config['GENERAL']['delay_between_requests']))

    return meta['filename']
# END: process_url()




####################################################
# Main
#
def main():
    """
    Main function
    """
    # Process command line args

    global args 
    args = parse_args()

    # generate config settings
    global config
    from audiobook_tools.common.load_config import load_config
    config = load_config("web-novel-to-text.conf", args, "", DEBUG, TEST)

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
        print("Processing URL:", url.rstrip())
        file = process_url(url.rstrip())
        print("  File:", file)

    print("done.")
# END: def main()
      



######################################################
# Start it up
if __name__ == "__main__":
   main()