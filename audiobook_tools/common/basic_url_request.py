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

    error = ''
    max_retries = 5 #config["preferred"]['retries']
    trys = 0
    if config["DEBUG"]['debug']:
        print("URL=" + url)
    while True:
        try:
            response = requests.get(url, 10) #, timeout=60) #config["preferred"]["timeout"])
            #  out = 1/0
        except Exception as e:
            trys += 1
            error = e
            print("!", end="", flush= True)
        else:
            #  break
            return response.content
        #  if trys == 0:
        #      return response.content
        #  elif trys == max_retries:
        #      print("Error: Conversion failed. " + e)
        #      exit(1)
        if trys == 4:
            print("\nError: Conversion failed. " + str(error))
            exit(1)


    #  try:
    #      response = requests.get(url, timeout=6) #config["preferred"]["timeout"])
    #  except Exception as e:
    #      print("Error: Conversion failed. " + e)
    #      exit(1)
    #      #  trys += 1
    #      #  error = e
    #      print("!", end="")
    #
    #  trys = 1
    # try a couple of times
    #  while 1:
    #      # Send request to server
    #      is_set = 0
    #      try:
    #          response = requests.get(url, timeout=3)
    #          response.raise_for_status()
    #      except requests.exceptions.HTTPError as errh:
    #          print ("Http Error:",errh)
    #          exit(1)
    #      except requests.exceptions.ConnectionError as errc:
    #          print ("Error Connecting:",errc)
    #          trys += 1
    #          is_set = 1
    #      except requests.exceptions.Timeout as errt:
    #          print ("Timeout Error:",errt)
    #          trys += 1
    #          is_set = 1
    #      except requests.exceptions.RequestException as err:
    #          print ("Error: Something Else",err)
    #          exit(1)
    #
    #      # Check for errors
    #      if( re.search('ERROR', response.text, re.IGNORECASE) ):
    #          print("Error response text: ")
    #          print("  ", response.text)
    #          print("URL (without text): " + url)
    #          print("Trying again(" + str(trys) + ")")
    #          is_set = 1
    #          trys += 1
    #      elif( int(response.status_code) >= 400 ):
    #          print("Error: HTTP response status code: "+str(response.status_code))
    #          print("Error response code:", response.status_code)
    #          #  print( response.text)
    #          #  print("URL (without text): " + url_sans_text)
    #          print("Trying again(" + str(trys) + ")")
    #          is_set = 1
    #          trys += 1
    #
    #      # everything is ok
    #      if not is_set:
    #          break
    #
    #      # Give up after 3 tries, and exit
    #      #  if trys >= int(config['preferred']['max_retries']) + 1:
    #      if trys >= max_retries +1:
    #          print("Conversion failed, exiting.")
    #          exit(1)
    #
    #      time.sleep(float(config['preferred']['delay_between_requests']) # dont clobber
    #  # End of try loop


    # return response (audio out, binary)
    #  return response.content
# End: basic_url_request()
