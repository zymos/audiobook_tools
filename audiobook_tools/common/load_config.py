"""
Loads config file 
stores config data and args into one variable
config = load_config(config_filename,args)
config_filename is not full path, just the files name
"""

import pprint # for debugging
import os
try:
    import configparser
except:
    print("Error: module 'configparser' not installed")
    print("Install: pip install configparser")
    exit(1)
try:
    from appdirs import user_config_dir
except:
    print("Error: module 'appdirs' not installed")
    print("Install: pip install appdirs")
    exit(1)


##################################################
# Config file
#
def load_config(config_filename, args, tmp_dir, DEBUG, TEST):
    """
    Get config file location
    priority is [CLI args] - > [local config] -> [default config]
    """
    
    #Load modules
    # debug


    config_file = configparser.ConfigParser()
    config = {}

    # set app name and gets config location
    appname = "audiobook-tools"
    appauthor = "audiobook-tools"
    config_file = os.path.join(user_config_dir(appname, appauthor), config_filename)
    default_config_file = os.path.join(os.path.dirname(__file__), '..', '..', config_filename)
    
    #print(os.path.dirname(__file__))
    # read config file
    # if DEBUG:
        # print("Local config file:", config_file)
        # print("Default config file:", default_config_file)
    cfg_found = 0
    cfg_default_found = 0
    if os.path.isfile(config_file):  
        print("Local config file:", config_file)
        cfg = configparser.ConfigParser()
        cfg.read(config_file)
        cfg_found = 1
    if os.path.isfile(default_config_file):
        print("Default config file:", default_config_file)
        cfg_default = configparser.ConfigParser()
        cfg_default.read(default_config_file)
        cfg_default_found = 1
    if cfg_found == 0 and cfg_default_found == 0:
        print("Config file not found.")
        print(" Not:", config_file)
        print(" Not:", default_config_file)
        exit(1)



    # create dictionary (from default config) (lowest priority)
    if cfg_default_found:
        config = {s:dict(cfg_default.items(s)) for s in cfg_default.sections()}  
        # overwrite config var's defaults using local config (med priority)
        if cfg_found:
            for s in cfg.sections():
                if not s in config:
                    config.update({s: {'set': 1}})
                for op in cfg.items(s):
                    if not op in config[s]:
                        config[s].update({op[0]: op[1]})
                    else:
                        config[s][op[0]] = op[1]
                    if DEBUG: print("local config:", s, " - ", op[0], " = ", op[1])
    else:
        # no default, local only
        config = {s:dict(cfg.items(s)) for s in cfg.sections()}  


    # Add args to config var for conveonce of a single var
    config.update({'ARGS': {'set': 1}})
    for setting in vars(args):
        if DEBUG: print("ARGS to config:", setting, " - ", vars(args)[setting])
        #config.update({setting: vars(args)[setting]})
        config['ARGS'].update({setting:vars(args)[setting]})

    # Set Prefered settings

    #  Overrides via commandline
    #  voice
    #  config.update({'preferred':{'voice': ''}})
    #  if( args.voice ):
        #  config['preferred']['voice'] = args.voice
    #  elif config[config['GENERAL']['tts_service']].get('voice') is not None:
        #  config['preferred']['voice'] = config[config['GENERAL']['tts_service']]['voice'] 

    #print(config[config['GENERAL']['tts_service']])


    ####################
    # Preferred Settings
    
    # create the 'preferred' key
    config.update({'preferred':{'set': 1}})

    # Preferred vars 
    # priority is lowest to highest -> default_config, local_config, args
    # if DEBUG: print("pref vars")

    # go through each setting

    # web-novel-to-text.py config
    if config_filename =="web-novel-to-text.conf":
        # print("TODO: not enabled yet")
        preferred_vars = ('delay_between_requests', 'format', 'speak_asterisk', 'dont_remove_quotes', 'dont_emphasize','filename_format')
        # go through each setting
        for setting in preferred_vars:
            config['preferred'].update({setting: ''}) 
            if setting in vars(args).keys(): # var exists
                if vars(args)[setting]: # var is set
                    config['preferred'][setting] = vars(args)[setting]
                elif config['GENERAL'].get(setting) is not None:
                    config['preferred'][setting] = config['GENERAL'][setting]    
            elif config['GENERAL'].get(setting) is not None:
                config['preferred'][setting] = config['GENERAL'][setting]

    # online-tts.py programs config
    elif config_filename == "online-tts.conf":
        preferred_vars = ('voice', 'profile', 'locale', 'gender', 'key', 'input_format', 'audio_format', 'audio_settings', 'gtts_lang', 'gtts_tld', 'url_parameters', 'delay_between_requests', 'max_charactors','speaking_rate')

        if config.get(config['GENERAL']['tts_service']) is None :
            print("Error: tts serivce \"" + config['GENERAL']['tts_service'] + 
            "\" is set in config, yet the section does not exist.  Fix the [GENERAL] \"tts_service\" setting, or add a new section named \"" +
            config['GENERAL']['tts_service'] , "\" an create a file in 'APIs' folder named \"" + config['GENERAL']['tts_service'] + ".py\"")
            exit(1)
        # TTS Service
        if args.profile :
            if config[args.profile].get('tts_service') is not None:
                config['preferred']['tts_service'] = config[args.profile]['tts_service']
            else:
                config['preferred']['tts_service'] =  config['GENERAL']['tts_service']
        else:
            config['preferred']['tts_service'] =  config['GENERAL']['tts_service']

        for setting in preferred_vars:
            config['preferred'].update({setting: ''}) 
            # if DEBUG: print("Config settings:", setting)
            if setting in vars(args).keys(): # var exists
                if vars(args)[setting]: # var is set
                    #if DEBUG: print("vars",vars(args)[setting] )
                    config['preferred'][setting] = vars(args)[setting]
                elif config[config['GENERAL']['tts_service']].get(setting) is not None:
                    config['preferred'][setting] = config[config['GENERAL']['tts_service']][setting] 
            elif config[config['GENERAL']['tts_service']].get(setting) is not  None:
                config['preferred'][setting] = config[config['GENERAL']['tts_service']][setting] 
                #  print("asdasdasdasda", setting)

        # set some hard defaults
        if config['preferred']['max_charactors'] == '':
            config['preferred']['max_charactors'] = 1000
    
    # Unknown config file
    else:
        print("Error unknown config file, should be 'web-novel-to-text.conf' or 'online-tts.conf'")
        exit(1)



    # save Debugging and testing vars
    config.update({'DEBUG':{'debug': False}})
    config['DEBUG'].update({'test': False})
    if DEBUG:
        config['DEBUG']['debug'] = True
    if TEST:
        config['DEBUG']['test'] = True

    #  pprint.pprint(vars(args)[profile])
    #  if( args.key ):
        #  config.update({'OVERRIDE':{'key': args.key}}) 
    #  elif config[config['GENERAL']['tts_service']]['key']:
        #  config.update({'preferred':{'key': config[config['GENERAL']['tts_service']]['key']}}) 
    #  else:
        #  config.update({'preferred':{'key': ''}}) 
    # input format
    #  config['preferred'].update({'input_format': ''}) 
    #  if( args.input_format ):
        #  config['preferred']['input_format'] = args.input_format
    #  elif config[config['GENERAL']['tts_service']].get('input_format') is not None:
        #  config['preferred']['input_format'] = config[config['GENERAL']['tts_service']]['input_format'] 


    #  if( args.input_format ):
        #  config.update({'OVERRIDE':{'input_format': args.input_format}}) 
        #  #  config['OVERRIDE']['input_format'] = args.input_format
    #  # PROFILE
    #  if( args.profile ):
        #  config.update({'OVERRIDE':{'profile': args.profile}}) 
    #  # URL_PARAMETERS
    #  if( args.url_parameters ):
        #  config.update({'OVERRIDE':{'url_parameters': args.url_parameters}}) 

    # add Places to store changing variables (place holders)
    config.update({'INPUT':{'filename': ''}}) 
    config['INPUT'].update({'text': ''}) 
    config['INPUT'].update({'text_ssml': ''}) 
    config['INPUT'].update({'text_chunk': ''}) 
    config.update({'OUTPUT':{'filename': ''}}) 
    config.update({'TMP':{'tmp_dir': tmp_dir}})

    if DEBUG: 
        print("------------------------config------------------------")
        pprint.pprint(config)
        print("------------------------------------------------------")

  
    return config
# End load_config
