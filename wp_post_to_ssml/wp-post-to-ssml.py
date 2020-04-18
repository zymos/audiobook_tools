#!/usr/bin/python
# -*- coding: latin-1 -*-


##########################
# imports
#
import re
import sys
import getopt

import urllib2
from lxml import html

from lxml import etree

import requests
from HTMLParser import HTMLParser

import argparse


############################
# Main
#
def main():
    # argv = sys.argv[1:]
    
    # CLI Arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('URL', type=str, help='URL to a Wordpress post')
    parser.add_argument('--format', help='Format of each file')
    parser.add_argument('-a', '--speak-asterisk', help='Speaks out asterisk[*] (off by default)')
    parser.add_argument('-q', '--dont-remove-quotes', help='Leave quotes in place and may or may not be spoken (off by default)')
    args = parser.parse_args()


    url = args.URL
    
    # url = 'https://wanderinginn.com/2016/11/27/1-28/'

    # print('ARGV      :', url)

    # response = urllib2.urlopen(url)
    # page_text = str(response.read())
    try:
        response = urllib2.urlopen(url)
    except:
        print "URL is invalid: " + url
        exit(1)
    # page = requests.get(url)
    # tree = html.fromstring(page.content)

    html_content = response.read()
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


    for line in html_content.split('\n'):
        line_cnt += 1
        # pages_line = line
        # print str(article_write) + "/" + str(line_cnt) + ": " + line

        # Get publish date
        if re.search('<meta property="article:published_time"', line):
            article_date = re.sub('<meta property="article:published_time" content="', '', line)
            article_date = re.sub('T[0-2].*', '', article_date)

        # Get posts title
        if re.search('<meta property="og:title"', line):
            article_title = re.sub('<meta property="og:title" content="', '', line)
            article_title = re.sub('".*', '', article_title)
            article_title = h.unescape(article_title.decode('utf-8',errors='ignore'))

        
        # article has ended
        if re.search('<!-- .entry-content -->', line):
            article_write = 0
            article_text += "</speak>"
        
        # Adding article text
        if article_write:
            line_mod = line

            # text line adds break
            line_mod = re.sub('<p>', '', line_mod)
            line_mod = re.sub('</p>', '@!@!@!@!break time="200ms"/!@!@!@!@', line_mod)
            
            # remove spoken asterisk
            if not args.speak_asterisk:
                line_mod = re.sub('\*', '', line_mod)

            # remove spoken quotes
            if not args.dont_remove_quotes:
                line_mod = re.sub('[“”„“‟”"❝❞⹂〝〞〟＂]', '', line_mod)

            # emphasised text
            line_mod = re.sub('<em>', '@!@!@!@!emphasis level="moderate"!@!@!@!@', line_mod)
            line_mod = re.sub('</em>', '@!@!@!@!/emphasis!@!@!@!@', line_mod)

            line_mod = re.sub('<[^>]+>', '', line_mod) # remove any html tags
            
            # Removes Previous Chapter Next Chapter
            line_mod = re.sub('Previous Chapter\s*Next Chapter', '', line_mod)
            
            # Extra breaks
            # ': ', '…', '—' '—-' '—'
            line_mod = re.sub('—-', '@!@!@!@!break time="200ms"/!@!@!@!@', line_mod)
            line_mod = re.sub('—', '@!@!@!@!break time="200ms"/!@!@!@!@', line_mod)
            line_mod = re.sub('…', '@!@!@!@!break time="200ms"/!@!@!@!@', line_mod)     
            if re.search('[a-zA-Z]: [a-zA-Z]', line_mod): 
                line_mod = re.sub(': ', '@!@!@!@!break time="200ms"/!@!@!@!@', line_mod)

            # print line_mod

            # line_mod = re.sub('<p>', '', line_mod)
            # line_mod = re.sub('<p>', '', line_mod)
            # line_mod = re.sub('<p>', '', line_mod)
            # line_mod = re.sub('<p>', '', line_mod)
            
            # Avoid removing ssml tags
            line_mod = re.sub('@!@!@!@!', '<', line_mod)
            line_mod = re.sub('!@!@!@!@', '>', line_mod)
            
            line_mod = h.unescape(line_mod.decode('utf-8',errors='ignore'))

            # line_mod = unescape(line_mod)
            article_text += line_mod + "\n"

        # Article has started
        if re.search('<div class="entry-content">', line):
            article_write = 1
            article_text += article_title + "<break time=\"1s\" />\n"
       
    # print article_text.encode('utf-8')
    article_text = "<speak>\n<!--\nWordpress articles post: Metadata\n   <meta property=\"og:title\" content=\"\" />\n    <meta property=\"og:url\" content=\"\" />\n    <meta property=\"article:published_time\" content=\"\" />\n    <meta property=\"og:site_name\" content=\"\" />\n    <meta property=\"og:image\" content=\"\" />\n-->\n    <metadata>\n        <dc:date><dc:date>\n        <dc:publisher></dc:publisher>\n        <dc:source></dc:source>\n     <dc:title></dc:title>\n    </metadata>\n" + article_text
    filename = article_date + " - " + article_title + ".ssml"
    print "Saving to filename: " + filename

    file = open(filename, "w")
    file.write(article_text.encode('utf-8'))
    file.close()

    
# def main() ...end...
      



#################################
# Start it up
if __name__ == "__main__":
   main()
