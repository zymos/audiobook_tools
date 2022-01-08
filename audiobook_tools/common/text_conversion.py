# -*- coding: utf-8 -*-
"""
Functions for converting text

ssml_text = text2ssml(text)
text = ssml2text(ssml_text)
ssml_text = ssml_clean(ssml_text)
text = clean_text(text)
ssml_text = clean_ssml(ssml_text)
text = remove_nonstandard_chars(text)
"""

#############################################################################
# Remove non-standard charactors
#
def remove_nonstandard_chars(text, config):
    """
    Removes non-standard charactors
    Ref: https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python
    """

    # remove non-european chars (non latin-1)
    if config['preferred']['remove_non_eu_chars']:
        text.encode('latin-1', 'ignore').decode('utf-8', 'ignore')

    # remove non-ASCII chars
    if config['preferred']['remove_non_ascii_char']:
        text.encode('ascii', 'ignore').decode('utf-8', 'ignore')

    
    # remove all non-unicode
    text = bytes(text, 'utf-8').decode('utf-8', 'ignore')

    # FIXME, way too slow
    #  import unicodedata, re, itertools, sys
    #
    #  all_chars = (chr(i) for i in range(sys.maxunicode))
    #  categories = {'Cc'}
    #  control_chars = ''.join(c for c in all_chars if unicodedata.category(c) in categories)
    #  # or equivalently and much more efficiently
    #  control_chars = ''.join(map(chr, itertools.chain(range(0x00,0x20), range(0x7f,0xa0))))
    #
    #  control_char_re = re.compile('[%s]' % re.escape(control_chars))
    #
    #  text = control_char_re.sub('', text)



    #  import sys # for sys.maxunicode
    #
    #  # build a table mapping all non-printable characters to None
    #  NOPRINT_TRANS_TABLE = {
    #      i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()
    #  }
    #  # remove non-printable chars
    #  text.translate(NOPRINT_TRANS_TABLE)

    return str(text)
# End: remove_nonstandard_chars()




#############################################################################
# Convert Text to SSML TODO
#
def text2ssml(text):
    """
    Converts text to ssml
    input str
    """
    ssml_text = ''
    return ssml_text
# End: text2ssml()


#############################################################################
# Convert SSML to Text
#
def ssml2text(ssml_text):
    """
    Converts ssml to plain text
    input/output str
    """
    import re
    text = re.sub('<[^>]+>', '', ssml_text)

    # remove blank lines
    text = re.sub(r'\n\s*\n', r'\n', text)

    #text = ssml_text
    return text
# End: ssml2text()



#############################################################################
# Clean Text
#
def clean_text(text, config):
    """
    Cleans up text to avoid weird noises
    dont_remove_asterisk, dont_remove_quotes, input_format
    """
    
    import re
    from html import unescape 
    import pprint

    # enable removal of bad chars
    bad_chars = ()
    remove_char = {'double_quote': False,
                   'paren': False, 
                   'bracket': False,
                   'asterisk': False,
                   'slash': False,
                   'underscore': False}
    if 'remove_bad_char' in config['preferred'].keys():
        bad_chars = config['preferred']['remove_bad_char'].split(',')
        for char in bad_chars:
            if char.lower() == 'q' or config['preferred']['remove_all_bad_chars']:
                remove_char['double_quote'] = True 
            if char.lower() == 'p' or config['preferred']['remove_all_bad_chars']:
                remove_char['paren'] = True 
            if char.lower() == 'b' or config['preferred']['remove_all_bad_chars']:
                remove_char['bracket'] = True 
            if char.lower() == 'a' or config['preferred']['remove_all_bad_chars']:
                remove_char['asterisk'] = True 
            if char.lower() == 's' or config['preferred']['remove_all_bad_chars']:
                remove_char['slash'] = True 
            if char.lower() == 'u' or config['preferred']['remove_all_bad_chars']:
                remove_char['underscore'] = True 


    #  pprint.pprint(remove_char)
    # Creating vars
    #  if "dont_remove_asterisk" in config['ARGS']:
        #  dont_remove_asterisk = config['ARGS']['keep_asterisk']
    #  else:
        #  dont_remove_asterisk = 0
    if "input_format" in config['preferred']:
        input_format = config['preferred']['input_format']
    elif "format" in config['preferred']:
        input_format = config['preferred']['format']
    else:
        input_format = 'txt'
    #  if "dont_remove_quotes" in config['ARGS']:
        #  dont_remove_quotes = config['ARGS']['keep_quotes']
    #  else:
        #  dont_remove_quotes = 0
    #  if "keep_bad_chars" in config['preferred']:
        #  keep_bad_chars = config['preferred']['keep_bad_chars']
    #  else:
        #  keep_bad_chars = 0
#      text = '<s>"Fascinating."</s> \
#  <s>"Yeah. Why are we whispering?"</s> \
#  <s>Grimalkin and Chaldion both turned to look at Saliss. The third Drake paused.</s>\
#  <s>"I mean<break time="200ms" /> Chaldion’s using his ring. Why are we whispering?"</s>\
#  <s>i""""""The other two Drakes stared at the [Alchemist]. ’Annoyed’ was a mild word to describe how they felt about Saliss. Resigned, aggravated<break time="200ms" /> you had to combine descriptors. But the Named Adventurer was the best [Alchemist] in all of Pallass, perhaps the world. He was more useful than he looked. And<break time="200ms" /> well, he was also hard to get rid of \'\'\'\'.</s> \
#  <s>Moreover, he was amid equals, in a sense. Grimalkin, the [Sinew Magus], and Chaldion, [Grand Strategist] in charge of Pallass’ armies were both famed and influential. If anything, Grimalkin was the lesser figure here. If anyone was being a stickler for the exact nuance of rank.</s> '
#
#      print('***********************************************')
#      print(text)
#      print('----------------------------------------------')
#      print(input_format)
    #  text = re.sub(r'\[', '#', text)


    # strip leading/trailing whitespace
    text = text.strip()
    
    # convert html escape code to Unicode/ASCII
    text = unescape(text)
 
    # Non-Standard Chars: remove all non-standard chars FIXME speed?
    text = remove_nonstandard_chars(text, config)

    textold = text
    # Fix Single Quotes
    text = re.sub(r"['\''’‚‘´\`']", "’", text)
    
    # Remove 2+ single quote
    text = re.sub("[’][’]*", "’", text)
    text = text.replace('’’', '') 

    # Remove Double Quote: remove spoken quotes
    if remove_char['double_quote']:
        if input_format == 'ssml':
            #  from bs4 import BeautifulSoup
            #  bstext = BeautifulSoup(text)
            #  for sentance in bstext.find_all('s'):
                #  sentance.string.replaceWith(re.sub(r'[“”„“‟”"❝❞⹂〝〞〟＂"]', '', bstext.string))
                #  print('bs')
            text = re.sub(r'[“”„“‟”"❝❞⹂〝〞〟＂]', '"', text) # FIXME in ssml, no quotes removed due to tags
        else:
            text = re.sub(r'[“”„“‟”"❝❞⹂〝〞〟＂]', '', text)
            #  print('nbs')
    else:
        #  print('nrm')
        text = re.sub(r'[“”„“‟”"❝❞⹂〝〞〟＂]', '"', text)

    # Remove 3+ quotes in a row
    text = re.sub(r'"{3,}', '', text)

    # Remove paren
    if remove_char['paren']:
        text = re.sub(r'[\(\)]', '', text)
 
    # Remove brackets
    if remove_char['bracket']:
        text = re.sub(r'[\[\]]', '', text)
 
    # Remove Asterisk
    if remove_char['asterisk']:
        text = re.sub(r'\*', '', text)
  
    # Remove slashes
    if remove_char['slash']:
        text = re.sub(r'[\\]', '', text)
    if remove_char['slash'] and not input_format == 'ssml': # FIXME
        text = re.sub(r'[\/]', '', text)
 
    # Remove Asterisk
    if remove_char['underscore']:
        text = re.sub(r'\_', ' ', text)
    
    # Remove whitespace
    # White Space: 2+ white space
    text = re.sub(r"[ \t][ \t]*", " ", text)
    # white space + newline
    text = re.sub("[ \t]*\n", "\n", text)
    # 2+ new line
    text = re.sub("[\n][\n]*", "\n", text)


    #  print(text)
    #  print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    #  exit()
    #  text = 'a'
    #  import difflib

    #  differences = difflib.ndiff(textold, text)
    #  for difference in differences:
        #  print(difference, "")
    return text
# End: clean_text()



##########################################################################
# Clean SSML text
#

def clean_ssml(ssml_text, voice, speaking_rate):
    """
    Clean up ssml, corrects for some errors
    makes sure <speak> tags are in place
    """
    
    import re
    
    DEBUG = 0
        
    # Modifying ssml file
    #   ssml requires voices set,
    #   and is the only place to alter speaking rate
    # SSML, adding basic tags if needed
        # remove <speak> tags, will add later
    ssml_text = re.sub(r'<\/?speak[^>]+>', '', ssml_text)
    ssml_text = re.sub(r'<\/speak>', '', ssml_text)
    ssml_text = ssml_text.strip()
    #print(ssml_text)
    
    # add <prosody ...> tag if needed, otherwise assume corrent
    if not re.search('<prosody ', ssml_text) and not speaking_rate == '':
        if DEBUG: print("    Adding <prosody> tag.")
        ssml_text = '<prosody rate="' + speaking_rate + '">' + ssml_text + '</prosody>'

    # add <voice ...> tag if needed, otherwise assume corrent
    if not re.search(r'<voice ', ssml_text) and not voice == '':
        if DEBUG: print("    Adding <voice> tag")
        ssml_text = '<voice name="' + voice + '">' + ssml_text + '</voice>'
    
    # fixes breaks with out closing char "/"
    ssml_text = re.sub("<break time=\"([a-zA-Z0-9]*)\">", 
                       r'<break time="\1" />', ssml_text)
    
    # fix problem with multiplu delays
    ssml_text = re.sub(r"(<break time=\"[a-zA-Z0-9]*\"[ ]?\/?>\s){2,}", 
                       "<break time=\"1s\" />", ssml_text)
    
    # replace '\x02/p>' not sure is this is a one off or a bug
    # 2018-07-21\ -\ 5.03.ssml
    ssml_text = re.sub(r"\\x02/p>", r"</s>", ssml_text) 
    
    # fix non-matched <p></p> (havnt really tested this)
    if (re.search(r"<p>", ssml_text) and not re.search(r"<\/p>", ssml_text)) \
            or (not re.search(r"<p>", ssml_text) and re.search(r"<\/p>", ssml_text)):
        ssml_text = re.sub(r'<\/p>', '', ssml_text)
        ssml_text = re.sub(r'<p>', '', ssml_text)        
        
    # remove blank sentences
    ssml_text = re.sub(r'<s>\s</s>', '', ssml_text)        
    ssml_text = re.sub(r'<s></s>', '', ssml_text)   
    
    # adding the <speak> tag
    ssml_text = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="string">' + ssml_text + '</speak>'
    
    
    #print("@@@@@@@@@@@@@@@@@@@@@@clean_ssml @@@@@@@@@@@@@@@@@@@@")
    #print(ssml_text)
    #print("@@@@@@@@@@@@@@@@@ clean_ssml (end) @@@@@@@@@@@@@@@@@@@@@@")
    return ssml_text

# End: clean_ssml()



#########################################################
# Correct articles text for better speach
#
def html_article2ssml(html_article, config, args): # maybe convert to config instead of args
    """
    html article converted to ssml
    not full website just the html for a post
    """
    import re

    # article_write = 0
    # line_cnt=0
    if config['DEBUG']['debug']:
        print("----------------------html_text-------------------------------")
        print(html_article)
        # print(type(html_article))
        print("---------------------html_text (end)-------------------------")

    # Clean the text up
    ssml_text = clean_text(html_article, config)

    # Remove Byte type text left overs
    #  for some reason it is a string with byte type chars around it b'gdsdfsdf-text-sdfsdfgds' so we remove it
    ssml_text = re.sub(r"^b'", r"", ssml_text) 
    ssml_text = re.sub(r"'$", r"", ssml_text)
    # remove non-tab tabs (no need to real tabs ether)
    ssml_text = re.sub(r"\\t", " ", ssml_text)
    # corrent the newlines that are not-new-lines
    ssml_text = re.sub(r"\\n", "\n", ssml_text)
    # replace '\x02/p>' not sure is this is a one off or a bug
    # 2018-07-21\ -\ 5.03.ssml
    ssml_text = re.sub(r"\x02/p>", r"</p>", ssml_text) 
    

    #
    #  # convert html escape code
    #  ssml_text = unescape(ssml_text)
    #
    #  # remove non-tab tabs (no need to real tabs ether)
    #  ssml_text = re.sub(r"\\t", r"", ssml_text)
    #
    #  # corrent the newlines that are not-new-lines
    #  ssml_text = re.sub(r"\\n", r"\n", ssml_text)
    #
    #  # remove spoken asterisk
    #  if config['GENERAL']['speak_asterisk']:
    #      ssml_text = re.sub(r'\*', '', ssml_text)
    #
    #  # remove spoken quotes
    #  if config['GENERAL']['dont_remove_quotes']:
    #      ssml_text = re.sub('[“”„“‟”"❝❞⹂〝〞〟＂]', '', ssml_text)
    #  else:
    #      ssml_text = re.sub('[“”„“‟”"❝❞⹂〝〞〟＂]', '"', ssml_text)
    #      # ssml_text = re.sub("['\''’‚‘´\`]", "’", ssml_text)
    #
    #      # sed 's/['\''’‚‘´\`]/’/g' |\
    #      # sed 's/[“”„“‟”"❝❞⹂〝〞〟＂]/"/g' |\
    #      # sed 's/…/\.\.\. /g' |\
    #      # sed 's/[–]/-/g'  `</speak>"
    #  # —



    #
    #  # fix single quotes
    #  ssml_text = re.sub(r"['\''’‚‘´\`']", "’", ssml_text)
    #
    #  # 2+ white space
    #  ssml_text = re.sub(r"[ \t][ \t]*", " ", ssml_text)
    #
    #  # fix single quotes
    #  ssml_text = re.sub(r"['\''’‚‘´\`']", "’", ssml_text)
    #
    #
    #  # 2+ single quote
    #  ssml_text = re.sub(r"[’][’]*", "’", ssml_text)
    #  ssml_text = ssml_text.replace('’’', '')
    #


    #  ssml_text =  ': , …, —, —-, —, &nbsp;, ___,    <s>—-</s><s>—-</s>'

    # remove empty <p>paragraphs FIXME!! still isnt catching all
    ssml_text = re.sub(r'<p>\s*</p>', '', ssml_text)

    # text line adds break (convert <p> to <s>)
    ssml_text = re.sub(r'<p>', r'˫@!@!@!@!s˧!@!@!@!@', ssml_text)
    ssml_text = re.sub(r'</p>', r"˫@!@!@!@!/s˧!@!@!@!@", ssml_text)


    # emphasised text
    #   emphasise sounds horible for ms_azure i think its slowwer rate
    #   so only increase volume, recomend disable by default
    #   needs testing
    if config['GENERAL']['no_emphasis']:
        emph_tag = "˫@!@!@!@!prosody volume=\"10%\"˧!@!@!@!@"
        emph_tag_end = r"˫@!@!@!@!/prosody˧!@!@!@!@"
        ssml_text = re.sub('<strong>', emph_tag, ssml_text)
        ssml_text = re.sub('</strong>', emph_tag_end, ssml_text)
        ssml_text = re.sub('<em>', emph_tag, ssml_text)
        ssml_text = re.sub('</em>', emph_tag_end, ssml_text)
        #ssml_text = re.sub('<strong>', "@!@!@!@!emphasis level=\"moderate\"!@!@!@!@", ssml_text)
        #ssml_text = re.sub('</strong>', "@!@!@!@!/emphasis!@!@!@!@", ssml_text)
        #ssml_text = re.sub('<em>', "@!@!@!@!emphasis level=\"moderate\"!@!@!@!@", ssml_text)
        #ssml_text = re.sub('</em>', "@!@!@!@!/emphasis!@!@!@!@", ssml_text)
    
    # Remove all other html tags
    ssml_text = re.sub('<[^>]+>', '', ssml_text) 
    
    # Add pauses
    # ': ', '…', '—' '—-' '—' '&nbsp;' '___'    <s>—-</<s>—-</s>
    ssml_text = re.sub(r'—-', "˫@!@!@!@!break time=\"200ms\" /˧!@!@!@!@ ", ssml_text)
    ssml_text = re.sub(r'—', "˫@!@!@!@!break time=\"200ms\" /˧!@!@!@!@ ", ssml_text)
    ssml_text = re.sub(r'…', "˫@!@!@!@!break time=\"200ms\" /˧!@!@!@!@ ", ssml_text)
    # nbsp space
    ssml_text = re.sub('&nbsp;', "˫@!@!@!@!break time=\"200ms\" /˧!@!@!@!@  ", ssml_text)
    # line breaks
    ssml_text = re.sub(r'<br ?[\/]?>', "˫@!@!@!@!break time=\"400ms\" /˧!@!@!@!@\n", ssml_text)
    # add pause for colon "Speaking: Words"
    if re.search('[a-zA-Z]: [a-zA-Z]', ssml_text): 
        ssml_text = re.sub(': ', "˫@!@!@!@!break time=\"200ms\" /˧!@!@!@!@ ", ssml_text)
    # Multiple underscores
    ssml_text = re.sub(r'\_{3,}', "˫@!@!@!@!break time=\"500ms\" /˧!@!@!@!@ ", ssml_text)


    # Removes Previous Chapter Next Chapter text sometimes used in article
    ssml_text = re.sub(r'Previous Chapter\s*Next Chapter', '', ssml_text)

    
    # Avoid removing ssml tags
    ssml_text = re.sub('˫@!@!@!@!', '<', ssml_text)
    ssml_text = re.sub('˧!@!@!@!@', '>', ssml_text)

    # final fixes
    # white space + newline
    ssml_text = re.sub("[ \t]*\n", r"\n", ssml_text)

    # 2+ new line
    ssml_text = re.sub("[\n][\n]*", r"\n", ssml_text)

    # fix problem with multiplu delays
    ssml_text = re.sub("(<break time=\"[0-9]*ms\"/>\n){3,}", "<break time=\"1s\" />\n", ssml_text)
    ssml_text = re.sub("(<break time=\"[0-9]*ms\"/>\n){2,}", "<break time=\"500ms\" />\n", ssml_text)



  
    # clean up the ssml code
    ssml_text = clean_ssml(ssml_text, "", "")

    # clean up text
    ssml_text = clean_text(ssml_text, config)
 
    # Re-Add <speak> tags
    #  ssml_text = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="string">\n' + ssml_text + "\n</speak>"

    #  ssml_text = re.sub("<break time=\"[0-9]*ms\"/>\n<break time=\"[0-9]*ms\"/>\n", "<break time=\"1s\">\n", ssml_text)
    # print("----------------------ssml_text-------------------------------")
    # print(ssml_text)
    # print(type(ssml_text))
    # print("---------------------ssml_text (end)-------------------------") 
    #  print(ssml_text)
    # return modified text
    return ssml_text
# END: html_article2ssml()
