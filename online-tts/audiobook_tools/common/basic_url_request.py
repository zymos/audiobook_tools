########################################################################
#
#   File for various online/cloud TTS APIs
#
#   Global variables:
#       config['preferred']['tts_service']
#       config['preferred']['voice']
#       config['preferred']['locale']
#       config['preferred']['audio_format']
#       config['preferred']['audio_settings']
#       config['preferred']['input_format']
#       config['preferred']['key']
#       config['preferred']['url_parameters']
#       config['preferred']['gtts_lang']
#       config['preferred']['gtts_tld']
#       config['preferred']['delay_between_requests']
#
#       config['DEBUG']['debug']
#
#
########################################################################



#####################################
# Function for general url requests
#
def basic_url_request(url, config):
    """
    Input: full url with all paramerters and text
    Output: audio data (byte)


    TODO seperate para, headers
    """
    import re # regex
    import pprint # debuging
    import requests # for sending request to server
    import time # for sleep


    trys = 1
    # try a couple of times
    while 1:
        # Send request to server
        is_set = 0
        try:
            response = requests.get(url) 
        except:
            # requests module failed
            print('Error: tts conversion request failed')
            #  print("URL (without text): " + url_sans_text)
            print("Trying again(" + str(trys) + ")")
            set = 1
            trys += 1

        # Check for errors
        if( re.search('ERROR', response.text, re.IGNORECASE) ):
            print("Error response text: ")
            print("  ", response.text)
            print("URL (without text): " + url)
            print("Trying again(" + str(trys) + ")")
            is_set = 1
            trys += 1
        elif( int(response.status_code) >= 400 ):
            print("Error: HTTP response status code: "+str(response.status_code))
            print("Error response code:", response.status_code)
            #  print( response.text)
            #  print("URL (without text): " + url_sans_text)
            print("Trying again(" + str(trys) + ")")
            is_set = 1
            trys += 1

        # everything is ok
        if not set:
            break

        # Give up after 3 tries, and exit
        if trys >= int(config['preferred']['max_retries']) + 1:
            print("Conversion failed, exiting.")
            exit(1)

        time.sleep(config['preferred']['delay_between_requests']) # dont clobber
    # End of try loop


    # return response (audio out, binary)
    return response.content
# End: basic_url_request()
