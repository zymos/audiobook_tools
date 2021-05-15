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

# DEBUG = 1
# TEST = 0








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
    parser = argparse.ArgumentParser(description='Converts a post to a txt/ssml file.', formatter_class=argparse.RawDescriptionHelpFormatter, epilog='\
Output filename can be dynamic, using variables extracted from webpage. \n\
    %a - author\n\
    %b - book title\n\
    %t - chapter title\n\
    %n - chapter number (extracted from chapter title, may not be reliable)\n\
    %N - chapter number (three digits w/ leading zeros, extracted from chapter title, may not be reliable)\n\
    %c - incremental count (starting with \"--start-number\", increments for each link in file)\n\
    %F - publication date YYYY-MM-DD\n\
    %T - publication time HH:MM:SS\n\
    Example: \"%b - Chapter %N\" -> \"Moby Dick - Chapter 003\"')

    parser.add_argument('INPUT', type=str, help='URL of post or file with list of URLs')

    #  parser.add_argument('-f', '--file', help='Use a file with list of URLs, instead of URL in CLI', action="store_true")
    #  parser.add_argument('-a', '--keep-asterisk', help='Speaks out asterisk[*] (off by default)', action="store_true")
    #  parser.add_argument('-q', '--keep-quotes', help='leave double quotes in place and may or may not be spoken (off by default)', action="store_true")
    #  parser.add_argument('--keep-problematic-chars', help=r'don\'t removes problematic charactors, that are often spoken [\"\\\/*]', action="store_true")
    parser.add_argument('--no-emphasis', help='don\'t emphasize some text in ssml', action="store_true")
    parser.add_argument('--debug', help='debug mode, more output', action="store_true")
    parser.add_argument('--test', help='test mode, no writing data', action="store_true")
    parser.add_argument('--format', type=str, help='Format to output (json stores metadata, txt and ssml)', choices=["txt", "ssml", "json"])
    parser.add_argument('--first-file-number', type=int, help='number for first output file\'s name, each additional file will increment this number, useful for keeping output files in order', default=1)
    parser.add_argument('--output-filename', type=str, help=r'filename to output, can be dynamic, see below')
    parser.add_argument('--remove_all_bad_chars', help=r'remove problematic charactors, that can change speech [, ], (, ), *, /, \, "', action="store_true")
    parser.add_argument('--remove-bad-char', type=str, help=r'remove problematic charactors, that can change speech, comman seperated. b=brackets, q=double_quotes, p=parentheses, a=asterisks, s=forward/back_slashs, u=underscore. example --remove-bad-char="b,a,q"')

    args = parser.parse_args()

    if args.debug: pprint.pprint(args)

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
#     config.update({'preferred':{'debug': False}})
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
    author = ''
    book_title = ''
    chap_title = ''
    cover = ''
    source = ''
    pub_date = ''
    pub_time = ''
    pub_year = ''
    chap_num = ''
    chap_num_3_dig = ''
    # chap_count = ''

    # site_code is entire website

    #h = HTMLParser()

    # gets page in tree of code tags
    tree = html.fromstring(site_code.text)

    # Extracts chapter title
    #  <meta property="og:title" content="*****title*****"/>
    title = tree.xpath('//meta[@property="og:title"]/@content')[0]
    chap_title = re.sub(r'(.*) - (.*) - (.*)', r'\1 - \2', title)

    # Chapter number
    (chap_num, chap_num_3_dig) = get_chap_number(chap_title)

    # File Count (from args)
    file_number = config['VARS']['file_number']

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
 
    # convert to string
    article_html = ''
    for line in content:
        article_html += str(tree.tostring(line).decode('utf-8'))

    # extracts publication date
    # <time datetime="2020-08-10T18:13:21.0000000Z" format="U" >
    # pub_date_time = str(tree.xpath('//meta[@property="article:published_time"]/@content')[0]
    pub_date_time = str(tree.xpath('//time/@datetime')[0])
    pub_date = re.sub('T.*', '', pub_date_time)

    # extracts publication year
    # <time datetime="2020-08-10T18:13:21.0000000Z" format="U" >
    pub_year = re.sub('-.*', '', pub_date)

    # Pub time
    pub_time = re.sub('.*T', '', pub_date_time)
    pub_time = re.sub(r'\+.*', '', pub_time)
    pub_time = re.sub(r'\..*', '', pub_time)

    meta = {'author': author,
            'book_title': book_title,
            'chap_title': chap_title,
            'chap_num': chap_num,
            'chap_num_3_dig': chap_num_3_dig,
            'file_number': file_number,
            'cover': cover,
            'source': source,
            'date': pub_date,
            'year': pub_year,
            'time': pub_time,
            'filename': ''}


    meta = create_filename(meta)

    #  pprint.pprint(meta)
    #  pprint.pprint(meta)

    # returns the string of articles txt, with tags and a decent filename to use
    return (article_html, meta)
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
    pub_time = ''
    pub_year = ''
    chap_num = ''
    chap_num_3_dig = ''
    # chap_count = ''
    # filename_out = ''



    #  h = HTMLParser()

    # gets page in tree of code tags
    tree = html.fromstring(site_code.text)

    # Author
    author = str(tree.xpath('//a[@rel="author"]/text()')[0])

    # Extracts chapter title
    #  <meta property="og:title" content="*****title*****"/>
    chap_title = str(tree.xpath('//meta[@property="og:title"]/@content')[0])
    #  print("chap:", chap_title , type(str(chap_title)))

    # Chapter number
    (chap_num, chap_num_3_dig) = get_chap_number(chap_title)

    # File Count (from args)
    file_number = config['VARS']['file_number']

    # Extracts book title TODO this probably doesnt work with all sites
    #  <meta property="og:site_name" content="*****title*****"/>
    book_title = str(tree.xpath('//meta[@property="og:site_name"]/@content')[0])


    # Extracts cover art
    # <meta property="og:image" content="********************">
    cover = str(tree.xpath('//meta[@property="og:image"]/@content')[0])


    # Extracts source
    # <meta property="og:url" content="*******************">
    source = str(tree.xpath('//meta[@property="og:url"]/@content')[0])


    # Pub date
    # <meta property="article:published_time
    pub_date_time = str(tree.xpath('//meta[@property="article:published_time"]/@content')[0])
    pub_date = re.sub('T[0-2].*', '', pub_date_time)
    pub_year = re.sub('-.*', '', pub_date)

    # Pub time
    pub_time = re.sub('.*T', '', pub_date_time)
    pub_time = re.sub(r'\+.*', '', pub_time)

    # extracts article contents
    # pages contents (found between <div class="entry-content">
    content = tree.xpath('//div[@class="entry-content"]')
    
    # convert to string
    article_html = ''
    for line in content:
        article_html += str(etree.tostring(line).decode('utf-8', errors='ignore'))

    meta = { 'author': author,
            'book_title': book_title,
            'chap_title': chap_title,
            'chap_num': chap_num,
            'chap_num_3_dig': chap_num_3_dig,
            'file_number': file_number,
            'cover': cover,
            'source': source,
            'date': pub_date,
            'year': pub_year,
            'time': pub_time,
            'filename': '' }

    # filename_out = re.sub(r'%a', meta['author'], filename_out)
    # print(filename_out)
    # filename_out = re.sub(r'%d', meta['book_title'], filename_out)
    # print(filename_out)
    # filename_out = re.sub(r'%t', meta['chap_title'], filename_out)
    # print(filename_out)
    # filename_out = re.sub(r'%n', meta['chap_num'], filename_out)
    # print(filename_out)
    # filename_out = re.sub(r'%N', meta['chap_num_3_digit'], filename_out)
    # print(filename_out)
    # filename_out = re.sub(r'%c', meta['chap_count'], filename_out)
    # print(filename_out)
    # filename_out = re.sub(r'%F', meta['date'], filename_out)
    # print(filename_out)
    # filename_out = re.sub(r'%T', meta['book_title'], filename_out)
    meta = create_filename(meta)

    if config['preferred']['debug']:
        print('--------------meta-----------------')
        pprint.pprint(meta)
        print('-----------meta (end)--------------')

    return (article_html, meta)
# END: wordpress()



#########################################
# Generate a 3 digit string
#
def make_3_digit_number_string(number):
    """
    takes a number and returns a string with leading zeros (3 digits)
    """
    num = str(number)

    if len(num) == 1:
        num = '00' + num
    elif len(num) == 2:
        num = '0' + num
    return num
# End make_3_digit_number_string())



#########################################
# Get Chapter Number
#
def get_chap_number(chap_title):
    """
    Attempt to get Extract chapter number from chapter title
    and returns
    (string of chapter digits) and (str of chapter digits, 3 digits, leading zeros)
    """

    # Attempt to Extract chapter number from chapter title
    ct = text2digits.Text2Digits()
    chap_title = ct.convert(chap_title)
    chap_number = re.sub(r'^.*?([0-9])', r'\1', chap_title)
    chap_number = re.sub(r'([0-9])[^0-9\.:]{2,}[0-9]', r'\1', chap_number)
    chap_number = re.sub(r'[^0-9\.:][^0-9\.:][^0-9\.:].*', '', chap_title)
    chap_number = re.sub(r'[^0-9\.:]', '', chap_title)
    # create chapter number with leading zeros
    chap_num_3_dig = make_3_digit_number_string(chap_number)

    #  if len(chap_number) == 1:
        #  chap_num_3_dig = '00' + chap_number
    #  elif len(chap_number) == 2:
        #  chap_num_3_dig = '0' + chap_number
    #  else:
        #  chap_num_3_dig = chap_number

    # return both chapter number formats
    return (chap_number, chap_num_3_dig)
# End: get_chap_number()





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
        'file_number': file_number,
        'filename': '' }

    Output Filename Format
    %a - author
    %b - book title
    %t - chapter title
    %n - chapter number
    %N - chapter number, three digits, with leading zeros
    %c - file number
    %F - publication date YYYY-MM-DD
    %T - publication time HH:MM:SS
    """

    # text2digits
    filename_out = config['preferred']['output_filename']

    # print(filename_out)
    filename_out = re.sub(r'%a', meta['author'], filename_out)
    # print(filename_out)
    filename_out = re.sub(r'%b', meta['book_title'], filename_out)
    # print(filename_out)
    filename_out = re.sub(r'%t', meta['chap_title'], filename_out)
    # print(filename_out)
    filename_out = re.sub(r'%n', meta['chap_num'], filename_out)
    # print(filename_out)
    filename_out = re.sub(r'%N', meta['chap_num_3_dig'], filename_out)
    # print(filename_out)
    filename_out = re.sub(r'%c', make_3_digit_number_string(meta['file_number']), filename_out)
    # print(filename_out)
    filename_out = re.sub(r'%F', meta['date'], filename_out)
    # print(filename_out)
    filename_out = re.sub(r'%T', meta['time'], filename_out)
    # print(filename_out)


    # filename_out = meta['date'] + " - " + meta['chap_title']

    # Ensure no forbiden chars in filename
    filename_out = re.sub(r"[\?:\"\|\*\\><]", ".", filename_out)

    # Set file extension
    if(config['preferred']['format'] == "json"):
        filename_out = filename_out + '.json'
    elif(config['preferred']['format']== "ssml"):
        filename_out = filename_out + ".ssml"
    else: # text
        filename_out = filename_out + ".txt"

    # Store filename in meta var
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
        if config['preferred']['debug']: print("  > Royal Road article found")
        (content, meta) = extract_txt_royalroad(site_code)
    elif( re.search(r'meta name="generator" content="WordPress.com"', html_content, re.IGNORECASE)):
        if config['preferred']['debug']: print("  > WordPress article found")
        (content, meta) = extract_txt_wordpress(site_code)
    else:
        print("  > Unknown web-novel type for\'", url, "'")
        print("Skipping...")
        return

    # Convert to single string from etree
    article_html = content

    # print("@@@@@@@@@@@@@@@@@@@@ article_html @@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print(article_html)
    # print("@@@@@@@@@@@@@@@@@ article_html (end) @@@@@@@@@@@@@@@@@@@@@@@")


    # process each line for basic correction to make tts better with less
    # incorrect speach
    import sys
    #  print(sys.path)

    from audiobook_tools.common.text_conversion import html_article2ssml,ssml2text
    #  try:
        #  from audiobook_tools.common.text_conversion import html_article2ssml
    #      from common.text_conversion import html_article2ssml
    #  except:
    #      print("error loading audiobook_tools(html_article2ssml) python files")
    #      exit(1)
    article_ssml = html_article2ssml(article_html, config, args)

    # Convert ssml to text
    #  try:
    #      from audiobook_tools.common.text_conversion import ssml2text
    #  except:
    #      print("error loading audiobook_tools(ssml2text) python files")
    #      exit(1)
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
    config = load_config("web-novel-to-text.conf", args, "")

    # enable DEBUG TODO (to be reimplemented)
    global DEBUG
    global TEST
    if config['preferred']['debug']: DEBUG = 1
    else: DEBUG = 0
    if config['preferred']['test']: TEST = 1
    else: TEST = 0

    # Get url(s) from input or file
    urls = []
    # if its a file, open it and treat as a list of urls
    if os.path.isfile(args.INPUT):
        print("Opening file of URLs")
        urls = open_file_of_urls(args.INPUT)
        #  pprint.pprint(urls)
    else:
        # if not a file, input is treated as url
        urls.append(args.INPUT)


    # process url(s)
    for url in urls:
        # Process URLs from input or file
        print("Processing URL:", url.rstrip())
        file = process_url(url.rstrip())
        print("  File:", file)
        # increments the file number for output filenames
        config['VARS']['file_number'] += 1
    
    print("done.")
# END: def main()




######################################################
# Start it up
if __name__ == "__main__":
   main()
