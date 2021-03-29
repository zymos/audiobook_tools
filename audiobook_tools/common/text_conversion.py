"""
Functions for converting text

ssml_text = text2ssml(text)
text = ssml2text(ssml_text)
ssml_text = ssml_clean(ssml_text)
text = clean_text(text)
ssml_text = clean_ssml(ssml_text)
"""


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
    
    # remove all non-unicode
   #  for line in text:
    text = bytes(text, 'utf-8').decode('utf-8', 'ignore')
    # convert html escape code
    #  line_mod = unescape(line_mod)

    # remove spoken asterisk
    if not dont_remove_asterisk:
        text = re.sub('\*', '', text)

    # remove spoken quotes   FIXME!!!!!!! dont remove quotes in tags
    if not input_format == 'ssml':
        if not dont_remove_quotes:
            text = re.sub('[“”„“‟”"❝❞⹂〝〞〟＂]', '', text)
        else:
            text = re.sub('[“”„“‟”"❝❞⹂〝〞〟＂]', '"', text)
        # line_mod = re.sub("['\''’‚‘´\`]", "’", line_mod)
        
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