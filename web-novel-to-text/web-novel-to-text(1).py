#/usr/bin/python
# coding: utf-8


##############################################################################################
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
#############################################################################################




#############################################################################################
# Configure
#

DEBUG = 0
TEST = 0








#############################################################################################
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
    
# for filenames with spelled out numbers
use_text2digits = 1
try:
    from text2digits import text2digits
except:
    print("Warning: module 'text2digits' not installed")
    print("   Used for converting spelled out numbers to numeric charactors")
    print("   Useful for keeping file names in order when spelled out chapters")
    print("   Install: pip3 install text2digits")
    use_text2digits = 0


# for loading config files
try:
    from appdirs import *
except:
    print("Error: module 'appdirs' not installed")
    print("Install: pip install appdirs")
    exit(1)
try:
    import configparser
    config_file = configparser.ConfigParser()
except:
    print("Error: module 'configparser' not installed")
    print("Install: pip install configparser")
    exit(1)






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
    
    if DEBUG: pprint.pprint(args)

    return args
# END:  parse_args()




##########################################
# Config file
#
def load_config():
    
    # Get config file location
    global config
    config = {}

    # set app name and gets config location
    appname = "audiobook-tools"
    appauthor = "audiobook-tools"
    config_filename = "web-novel-to-text.conf"
    config_file = os.path.join(user_config_dir(appname, appauthor), config_filename) 
    default_config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), config_filename)
    
    #  print(default_config_file)

    # read config file
    if os.path.isfile(config_file):  
        cfg = configparser.ConfigParser()
        cfg.read(config_file)
    elif os.path.isfile(default_config_file):
        print("Config file:", default_config_file)
        cfg = configparser.ConfigParser()
        cfg.read(default_config_file)
    else:
        print("Config file not found.")
        print(" Not:", config_file)
        print(" Not:", default_config_file)
        exit(1)

    # create dictionary
    config = {s:dict(cfg.items(s)) for s in cfg.sections()}

    # Variables
    # config['GENERAL']['delay_between_requests']



    # Set Prefered settings

    #  Overrides via commandline
    #  voice
    #  config.update({'preferred':{'voice': ''}})
    #  if( args.voice ):
        #  config['preferred']['voice'] = args.voice
    #  elif config[config['GENERAL']['tts_service']].get('voice') is not None:
        #  config['preferred']['voice'] = config[config['GENERAL']['tts_service']]['voice'] 



    ####################
    # Preferred Settings
    
    # create the 'preferred' key
    config.update({'preferred':{'preferrences': 1}})

    # TTS Service
    #  if args.profile :
        #  if config[args.profile].get('tts_service') is not None:
            #  config['preferred']['tts_service'] = config[args.profile]['tts_service']
        #  else:
            #  config['preferred']['tts_service'] =  config['GENERAL']['tts_service']
    #  else:
        #  config['preferred']['tts_service'] =  config['GENERAL']['tts_service']
    #  print("------------------------------------------------")
    #  print("            a",vars(args)['format'])
    #  print("            a",type(vars(args)))

    #  pprint.pprint(vars(args))
    #  pprint.pprint(vars(args).keys())

    #  print("================================================")
    # Preferred vars 
    preferred_vars = ('format','delay_between_requests')
    # go through each setting
    for setting in preferred_vars:
        config['preferred'].update({setting: ''}) 
        if setting in vars(args).keys(): # var exists
            if vars(args)[setting]: # var is set
                config['preferred'][setting] = vars(args)[setting]
        elif config['GENERAL'].get(setting) is not None:
            config['preferred'][setting] = config['GENERAL'][setting] 
    

    # Debugging and testing
    config.update({'DEBUG':{'debug': False}})
    config['DEBUG'].update({'test': False})
    if DEBUG:
        config['DEBUG']['debug'] = True
    if TEST:
        config['DEBUG']['test'] = True


    # Places to store variables
    #  config.update({'INPUT':{'filename': ''}}) 
    #  config.update({'INPUT':{'text': ''}}) 
    #  config.update({'INPUT':{'text_ssml': ''}}) 
    #  config.update({'INPUT':{'text_chunk': ''}}) 
    #  config.update({'OUTPUT':{'filename': ''}}) 
    #  config.update({'TMP':{'tmp_dir': tmp_dir}})

    if DEBUG: 
        print("Config file:", config_file)
        print("------------------------config------------------------")
        pprint.pprint(config)
        print("------------------------------------------------------")
    #  return config
# End load_config










###########################################
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
    
    #  print(type(chap_title),type(content))

    #  chap_title = etree.tostring("".join(chap_title)).decode('utf-8')

    #  print("".join(chap_title))bytes(line_mod, 'utf-8').decode('utf-8', 'ignore')

    #  content = [bytes(etree.tostring(s), 'utf-8').decode('utf-8', 'ignore') for s in content] 

    #  content.insert(0, "".join(chap_title))
    #  print(type(chap_title),type(content[0]))
    #  pprint.pprint(content)
    #  exit()
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



    #  # set extention for output file
    #  filename_out = pub_date + " - " + chap_title


    #  meta = { 'author': author,
            #  'book_title': book_title,
            #  'chap_title': chap_title,
            #  'cover': cover,
            #  'source': source,
            #  'date': pub_date,
            #  'year': pub_year,
            #  'filename': filename_out }


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






#########################################################
# Correct articles text for better speach
#
def generate_ssml(content):

    article_write = 0
    line_cnt=0

    article_text = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="string">\n'

    for line in content:
        #  print("line type", type(line))
        #  print("line etree", type(etree.tostring(line)))
        # line_mod is the output
        
        # strip leading/trailing whitespace
        
        # remove non-unicode chars
        #  print(line)
        #  exit()
        #  newlist = [str(s) for s in line]
        #  pprint.pprint(newlist)
        #  exit()
        #  if re.search('etree', str(type(line))):
            #  print(str(type(line)))
            #  exit()
        line_mod = etree.tostring(line).decode('utf-8')
            #  print('etree')
        #  else:
            #  line_mod = str(line)
            #  print("str")

        line_mod = bytes(line_mod, 'utf-8').decode('utf-8', 'ignore')

        # remove leading/tailing with space
        line_mod = line_mod.strip()

        #  line_mod = re.sub('<br \\>', "\n", line_mod)


        # convert html escape code
        line_mod = unescape(line_mod)

        # remove spoken asterisk
        if not args.speak_asterisk:
            line_mod = re.sub('\*', '', line_mod)

        # remove spoken quotes
        if not args.dont_remove_quotes:
            line_mod = re.sub('[“”„“‟”"❝❞⹂〝〞〟＂]', '', line_mod)
        else:
            line_mod = re.sub('[“”„“‟”"❝❞⹂〝〞〟＂]', '"', line_mod)
            # line_mod = re.sub("['\''’‚‘´\`]", "’", line_mod)
            
            # sed 's/['\''’‚‘´\`]/’/g' |\
            # sed 's/[“”„“‟”"❝❞⹂〝〞〟＂]/"/g' |\
            # sed 's/…/\.\.\. /g' |\
            # sed 's/[–]/-/g'  `</speak>"
        # —

        # fix single quotes
        line_mod = re.sub("['\''’‚‘´\`']", "’", line_mod)

        # 2+ white space
        line_mod = re.sub("[ \t][ \t]*", " ", line_mod)
    
        # fix single quotes
        line_mod = re.sub("['\''’‚‘´\`']", "’", line_mod)


        # 2+ single quote
        line_mod = re.sub("[’][’]*", "’", line_mod)
        line_mod = line_mod.replace('’’', '')
        

        # text line adds break
        line_mod = re.sub('<p>', '', line_mod)
        line_mod = re.sub('</p>', '@!@!@!@!break time="200ms"/!@!@!@!@\n', line_mod)

        # nbsp space
        line_mod = re.sub('&nbsp;', '@!@!@!@!break time="200ms"/!@!@!@!@  ', line_mod)
        
        # line breaks
        line_mod = re.sub('<br ?[\/]?>', '@!@!@!@!break time=\"400ms\"/!@!@!@!@\n', line_mod)


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
        
        # Add line to text
        article_text += line_mod + "\n"

    article_text += "</speak>\n"

    # final fixes
    # white space + newline
    article_text = re.sub("[ \t]*\n", "\n", article_text)

    # 2+ new line
    article_text = re.sub("[\n][\n]*", "\n", article_text)

    # fix problem with multiplu delays
    article_text = re.sub("(<break time=\"[0-9]*ms\"/>\n){3,}", "<break time=\"1s\">\n", article_text)
    article_text = re.sub("(<break time=\"[0-9]*ms\"/>\n){2,}", "<break time=\"500ms\">\n", article_text)

    #  article_text = re.sub("<break time=\"[0-9]*ms\"/>\n<break time=\"[0-9]*ms\"/>\n", "<break time=\"1s\">\n", article_text)

    #  print(article_text)
    # return modified text
    return article_text
# END: generate_ssml()












##########################################################
# Process each URLs
#
def process_url(url):
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

    # decide which web novel source and how to extract text 
    #   and a useful output filename to use
    if re.search(r"royalroad\.com", url, re.IGNORECASE):
        if DEBUG: print("  > Royal Road article found")
        (content, meta) = extract_txt_royalroad(site_code)
    elif( re.search(r'meta name="generator" content="WordPress.com"', html_content, re.IGNORECASE)):
        if DEBUG: print("  > WordPress article found")
        (content, meta) = extract_txt_wordpress(site_code)
    else:
        print("  > Unknown web-novel type for\'", url, "'")
        print("Skipping...")
        return


    # process each line for basic correction to make tts better with less 
    # incorrect speach
    article_ssml = generate_ssml(content)
    article_text  = re.sub('<[^>]+>', '', article_ssml) # remove any tags

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

    return meta['filename']
# END: process_url()




####################################################
# Main
#
def main():
    
    # Process command line args
    global args 
    args = parse_args()

    # Load config file
    load_config()

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
# END: def main()
      



######################################################
# Start it up
if __name__ == "__main__":
   main()
