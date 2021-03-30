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
def remove_nonstandard_chars(text):
    """
    Removes non-standard charactors
    Ref: https://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python
    """

    # remove all non-unicode
    text = bytes(text, 'utf-8').decode('utf-8', 'ignore')

    import sys # for sys.maxunicode

    # build a table mapping all non-printable characters to None
    NOPRINT_TRANS_TABLE = {
        i: None for i in range(0, sys.maxunicode + 1) if not chr(i).isprintable()
    }
    # remove non-printable chars
    text.translate(NOPRINT_TRANS_TABLE)

    return text
# End: remove_nonstandard_chars()




#############################################################################
# Convert Text to SSML
#
def text2ssml(text):
    """
    Converts text to ssml
    input str
    """
    ssml_text = text
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
    #text = ssml_text
    return text
# End: ssml2text()



#############################################################################
# Clean Text
#
def clean_text(text, dont_remove_asterisk, dont_remove_quotes, input_format):
    """
    Cleans up text to avoid weird noises
    """
    
    import re
    # strip leading/trailing whitespace
    text = text.strip()
    #print("ddddd")
    
    # remove all non-standard chars
    text = remove_nonstandard_chars(text)

    # convert html escape code
    #  ssml_text = unescape(ssml_text)

    # remove spoken asterisk
    if not dont_remove_asterisk:
        text = re.sub('\*', '', text)

    # remove spoken quotes   FIXME!!!!!!! dont remove quotes in tags
    if not input_format == 'ssml':
        if not dont_remove_quotes:
            text = re.sub('[“”„“‟”"❝❞⹂〝〞〟＂]', '', text)
        else:
            text = re.sub('[“”„“‟”"❝❞⹂〝〞〟＂]', '"', text)
        # ssml_text = re.sub("['\''’‚‘´\`]", "’", ssml_text)
        
        # sed 's/['\''’‚‘´\`]/’/g' |\
        # sed 's/[“”„“‟”"❝❞⹂〝〞〟＂]/"/g' |\
        # sed 's/…/\.\.\. /g' |\
        # sed 's/[–]/-/g'  `</speak>"
    # —


    # 2+ white space
    text = re.sub("[ \t][ \t]*", " ", text)
    
    # fix single quotes
    text = re.sub("['\''’‚‘´\`']", "’", text)


    # white space + newline
    text = re.sub("[ \t]*\n", "\n", text)

    # 2+ new line
    text = re.sub("[\n][\n]*", "\n", text)


    # 2+ single quote
    text = re.sub("[’][’]*", "’", text)
    text = text.replace('’’', '')
    

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
    ssml_text = re.sub('<\/?speak[^>]+>', '', ssml_text)
    ssml_text = re.sub('<\/speak>', '', ssml_text)
    ssml_text = ssml_text.strip()
    #print(ssml_text)
    
    # add <prosody ...> tag if needed, otherwise assume corrent
    if not re.search('<prosody ', ssml_text):
        if DEBUG: print("    Adding <prosody> tag.")
        ssml_text = '<prosody rate="' + speaking_rate + '">' + ssml_text + '</prosody>'

    # add <voice ...> tag if needed, otherwise assume corrent
    if not re.search('<voice ', ssml_text):
        if DEBUG: print("    Adding <voice> tag")
        ssml_text = '<voice name="' + voice + '">' + ssml_text + '</voice>'
    
    # fixes breaks with out closing char "/"
    ssml_text = re.sub("<break time=\"([a-zA-Z0-9]*)\">", 
                       r'<break time="\1"/>', ssml_text)
    
    # fix problem with multiplu delays
    ssml_text = re.sub(r"(<break time=\"[a-zA-Z0-9]*\"[ ]?\/?>\s){2,}", 
                       "<break time=\"1s\"/>", ssml_text)
    
    
    # fix non-matched <p></p> (havnt really tested this)
    if (re.search("<p>", ssml_text) and not re.search("<\/p>", ssml_text)) or (not re.search("<p>", ssml_text) and re.search("<\/p>", ssml_text)):
        ssml_text = re.sub('<\/p>', '', ssml_text)
        ssml_text = re.sub('<p>', '', ssml_text)
        
        
    
    # adding the <speak> tag
    ssml_text = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="string">' + ssml_text + '</speak>'
    
    
    #print("@@@@@@@@@@@@@@@@@@@@@@clean_ssml @@@@@@@@@@@@@@@@@@@@")
    #print(ssml_text)
    #print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    return ssml_text

# End: clean_ssml()



#########################################################
# Correct articles text for better speach
#
def html_article2ssml(html_article, args): # maybe convert to config instead of args
    """
    html article converted to ssml
    not full website just the html for a post
    """
    import re
    from html import unescape 
    # to unescape html code

    # article_write = 0
    # line_cnt=0

    # print("----------------------html_text-------------------------------")
    # print(html_article)
    # print(type(html_article))
    # print("---------------------html_text (end)-------------------------")    
    # remore all non-standard chars, non-unicode, non-printable, etc
    ssml_text = str(remove_nonstandard_chars(html_article))
    # print("----------------------ssml_text-------------------------------")
    # print(ssml_text)
    # print(type(ssml_text))
    # print("---------------------ssml_text (end)-------------------------") 
    # for some reason it is a string with byte type chars around it b'gdsdfsdf-text-sdfsdfgds' so we remove it
    ssml_text = re.sub(r"^b'", r"", ssml_text) 
    ssml_text = re.sub(r"'$", r"", ssml_text)

    # convert html escape code
    ssml_text = unescape(ssml_text)

    # remove non-tab tabs (no need to real tabs ether)
    ssml_text = re.sub(r"\\t", r"", ssml_text) 

    # corrent the newlines that are not-new-lines
    ssml_text = re.sub(r"\\n", r"\n", ssml_text)

    # remove spoken asterisk
    if not args.speak_asterisk:
        ssml_text = re.sub(r'\*', '', ssml_text)

    # remove spoken quotes
    if not args.dont_remove_quotes:
        ssml_text = re.sub('[“”„“‟”"❝❞⹂〝〞〟＂]', '', ssml_text)
    else:
        ssml_text = re.sub('[“”„“‟”"❝❞⹂〝〞〟＂]', '"', ssml_text)
        # ssml_text = re.sub("['\''’‚‘´\`]", "’", ssml_text)
        
        # sed 's/['\''’‚‘´\`]/’/g' |\
        # sed 's/[“”„“‟”"❝❞⹂〝〞〟＂]/"/g' |\
        # sed 's/…/\.\.\. /g' |\
        # sed 's/[–]/-/g'  `</speak>"
    # —

    # fix single quotes
    ssml_text = re.sub("['\''’‚‘´\`']", "’", ssml_text)

    # 2+ white space
    ssml_text = re.sub("[ \t][ \t]*", " ", ssml_text)

    # fix single quotes
    ssml_text = re.sub("['\''’‚‘´\`']", "’", ssml_text)


    # 2+ single quote
    ssml_text = re.sub("[’][’]*", "’", ssml_text)
    ssml_text = ssml_text.replace('’’', '')
    
    # remove empty <p>paragraphs FIXME!! still isnt catching all
    ssml_text = re.sub(r'<p>[\s\n]*</p>', '', ssml_text)

    # text line adds break 
    ssml_text = re.sub('<p>', '@!@!@!@!s!@!@!@!@', ssml_text)
    ssml_text = re.sub('</p>', "@!@!@!@!/s!@!@!@!@", ssml_text)

    # nbsp space
    ssml_text = re.sub('&nbsp;', "@!@!@!@!break time=\"200ms\"/!@!@!@!@  ", ssml_text)
    
    # line breaks
    ssml_text = re.sub('<br ?[\/]?>', "@!@!@!@!break time=\"400ms\"/!@!@!@!@\n", ssml_text)


    # emphasised text
    ssml_text = re.sub('<strong>', "@!@!@!@!emphasis level=\"moderate\"!@!@!@!@", ssml_text)
    ssml_text = re.sub('</strong>', "@!@!@!@!/emphasis!@!@!@!@ ", ssml_text)

    ssml_text = re.sub('<em>', "@!@!@!@!emphasis level=\"moderate\"!@!@!@!@", ssml_text)
    ssml_text = re.sub('</em>', "@!@!@!@!/emphasis!@!@!@!@ ", ssml_text)

    ssml_text = re.sub('<[^>]+>', '', ssml_text) # remove any html tags codes not em, strong
    
    
    # Extra breaks
    # ': ', '…', '—' '—-' '—'
    ssml_text = re.sub('—-', "@!@!@!@!break time=\"200ms\"/!@!@!@!@ ", ssml_text)
    ssml_text = re.sub('—', "@!@!@!@!break time=\"200ms\"/!@!@!@!@ ", ssml_text)
    ssml_text = re.sub('…', "@!@!@!@!break time=\"200ms\"/!@!@!@!@ ", ssml_text)
    # add pause for colon "Speaking: Words"
    if re.search('[a-zA-Z]: [a-zA-Z]', ssml_text): 
        ssml_text = re.sub(': ', "@!@!@!@!break time=\"200ms\"/!@!@!@!@ ", ssml_text)
    

    # Removes Previous Chapter Next Chapter text sometimes used in article
    ssml_text = re.sub('Previous Chapter\s*Next Chapter', '', ssml_text)

    
    # Avoid removing ssml tags
    ssml_text = re.sub('@!@!@!@!', '<', ssml_text)
    ssml_text = re.sub('!@!@!@!@', '>', ssml_text)
    

    # final fixes
    # white space + newline
    ssml_text = re.sub("[ \t]*\n", r"\n", ssml_text)

    # 2+ new line
    ssml_text = re.sub("[\n][\n]*", r"\n", ssml_text)

    # fix problem with multiplu delays
    ssml_text = re.sub("(<break time=\"[0-9]*ms\"/>\n){3,}", "<break time=\"1s\">\n", ssml_text)
    ssml_text = re.sub("(<break time=\"[0-9]*ms\"/>\n){2,}", "<break time=\"500ms\">\n", ssml_text)

    ssml_text = '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="string">\n' + ssml_text + "\n</speak>"

    #  ssml_text = re.sub("<break time=\"[0-9]*ms\"/>\n<break time=\"[0-9]*ms\"/>\n", "<break time=\"1s\">\n", ssml_text)
    print("----------------------ssml_text-------------------------------")
    print(ssml_text)
    print(type(ssml_text))
    print("---------------------ssml_text (end)-------------------------") 
    #  print(ssml_text)
    # return modified text
    return ssml_text
# END: html_article2ssml()