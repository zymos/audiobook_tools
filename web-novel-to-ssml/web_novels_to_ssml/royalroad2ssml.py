#!/usr/bin/python
# -*- coding: latin-1 -*-



##############################
# 
# Source: royalroad.com 
#
# title: <meta property="og:title" content="*****title*****"/>
# 
# Text start: <div class="chapter-inner chapter-content">
# Text end: </div>
#
# Output file name: [TITLE].ssml


##########################
# imports
#
import re
import sys
import getopt

import urllib3
from lxml import html

from lxml import etree

import requests
from html.parser import HTMLParser

import argparse

# for sleep func debug
import time

############################
# Main
#
def main():
    # argv = sys.argv[1:]
    
    # CLI Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('URL', type=str, help='URL to a royalroad post')
    parser.add_argument('--format', help='Format of each file')
    parser.add_argument('-a', '--speak-asterisk', help='Speaks out asterisk[*] (off by default)', action="store_true")
    parser.add_argument('-q', '--dont-remove-quotes', help='Leave quotes in place and may or may not be spoken (off by default)', action="store_true")
    args = parser.parse_args()


    url = args.URL
    
    # url = 'https://www.royalroad.com/fiction/31429/cinnamon-bun/chapter/533652/chapter-sixty-seven-fairness'

    # print('ARGV      :', url)

    # response = urllib2.urlopen(url)
    # page_text = str(response.read())
    try:
        #  response = urllib3.urlopen(url)
        response = requests.get(url)
    except:
        print("URL is invalid: " + url)
        exit(1)
    # page = requests.get(url)
    # tree = html.fromstring(page.content)

    html_content = response.text
    # tree = html.fromstring(html_content)
    # print "Get all data: ", html

    # post_title = tree.xpath('//h1[@class="entry-title"]/text()')[0]
    # post_date = tree.xpath('//div[@class="entry-content"]/p/text()')

    article_text = ""
    article_title = ''
    article_date = ''
    article_write = 0
    line_cnt=0
    # TAG_RE = re.compile(r'<[^>]+>')
    
    h = HTMLParser()


    tree = html.fromstring(response.text)

    #  <meta property="og:title" content="*****title*****"/>
    article_title = tree.xpath('//meta[@property="og:title"]/@content')[0]

    # pages contents (found between <div class="chapter-inner chapter-content">
    content = tree.xpath('//div[@class="chapter-inner chapter-content"]')

    for line in content:
    #  for line in html_content.split('\n'):


        # line_mod is the output
        line_mod = etree.tostring(line).decode('utf-8')

        print(line_mod)
        print(type(line_mod))
        #  break








        # text line adds break
        line_mod = re.sub('<p>', '', line_mod)




        line_mod = re.sub('</p>', '@!@!@!@!break time="200ms"/!@!@!@!@', line_mod)

        # nbsp space
        line_mod = re.sub('&nbsp;', '@!@!@!@!break time="200ms"/!@!@!@!@', line_mod)
        
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
        line_mod = re.sub("['\''’‚‘´\`]", "’", line_mod)

        # emphasised text
        line_mod = re.sub('<strong>', '@!@!@!@!emphasis level="moderate"!@!@!@!@', line_mod)
        line_mod = re.sub('</strong>', '@!@!@!@!/emphasis!@!@!@!@', line_mod)

        line_mod = re.sub('<em>', '@!@!@!@!emphasis level="moderate"!@!@!@!@', line_mod)
        line_mod = re.sub('</em>', '@!@!@!@!/emphasis!@!@!@!@', line_mod)

        line_mod = re.sub('<[^>]+>', '', line_mod) # remove any html tags
        
        
        # Extra breaks
        # ': ', '…', '—' '—-' '—'
        line_mod = re.sub('—-', '@!@!@!@!break time="200ms"/!@!@!@!@ ', line_mod)
        line_mod = re.sub('—', '@!@!@!@!break time="200ms"/!@!@!@!@ ', line_mod)
        line_mod = re.sub('…', '@!@!@!@!break time="200ms"/!@!@!@!@ ', line_mod)
        # add pause for colon "Speaking: Words"
        if re.search('[a-zA-Z]: [a-zA-Z]', line_mod): 
            line_mod = re.sub(': ', '@!@!@!@!break time="200ms"/!@!@!@!@ ', line_mod)

        # print line_mod

        # line_mod = re.sub('<p>', '', line_mod)
        # line_mod = re.sub('<p>', '', line_mod)
        # line_mod = re.sub('<p>', '', line_mod)
        # line_mod = re.sub('<p>', '', line_mod)
        
        # Avoid removing ssml tags
        line_mod = re.sub('@!@!@!@!', '<', line_mod)
        line_mod = re.sub('!@!@!@!@', '>', line_mod)
        
        # Add line to text
        article_text += line_mod + "\n"

        # Article has started
        #  if re.search('<div class="entry-content">', line):
            #  article_write = 1
            #  article_text += article_title + "<break time=\"1s\" />\n\n"
       
    # print article_text.encode('utf-8')
    #  article_text = "<speak>\n<!--\nWordpress articles post: Metadata\n   <meta property=\"og:title\" content=\"\" />\n    <meta property=\"og:url\" content=\"\" />\n    <meta property=\"article:published_time\" content=\"\" />\n    <meta property=\"og:site_name\" content=\"\" />\n    <meta property=\"og:image\" content=\"\" />\n-->\n    <metadata>\n        <dc:date><dc:date>\n        <dc:publisher></dc:publisher>\n        <dc:source></dc:source>\n     <dc:title></dc:title>\n    </metadata>\n" + article_text
    
    print(article_text)
    filename = article_title + ".ssml"
    print("Saving to filename: " + filename)

    file = open(filename, "w")
    #  file.write(article_text.encode('utf-8'))
    file.write(article_text)
    file.close()

    
# def main() ...end...
      



#################################
# Start it up
if __name__ == "__main__":
   main()
