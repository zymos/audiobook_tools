"""
Loads config file
stores config data and args into one variable
config = load_config(config_filename,args)
config_filename is not full path, just the files name
"""

import pprint # for debugging
import os
import re
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
def load_config(config_filename, args, tmp_dir):
    """
    Get config file location
    priority is [CLI args] - > [local config] -> [default config]
    """


    # config_file = configparser.RawConfigParser()
    config = {}

    # set app name and gets config location
    appname = "audiobook-tools"
    appauthor = "audiobook-tools"

    config_file = os.path.join(user_config_dir(appname, appauthor), config_filename)
    global_config_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config_files', config_filename)
    default_config_file = os.path.join(os.path.dirname(__file__), '..', '..', 'config_files', 'DEFAULT', 'DEFAULT-' + config_filename)


    if args.debug:
        print("Local config file:", config_file)
        print("Global config file:", global_config_file)
        print("Default config file:", default_config_file)

    cfg_found = 0
    cfg_default_found = 0
    cfg_global_found = 0
    if os.path.isfile(config_file):
        #  print("Using local config file:", config_file)
        config_file_used = config_file
        cfg = configparser.RawConfigParser()
        cfg.read(config_file)
        cfg_found = 1
    if os.path.isfile(global_config_file):
        cfg_global = configparser.RawConfigParser()
        cfg_global.read(default_config_file)
        cfg_global_found = 1
    if os.path.isfile(default_config_file):
        cfg_default = configparser.RawConfigParser()
        cfg_default.read(default_config_file)
        cfg_default_found = 1
        if not cfg_found:
            print("Using default config file:", default_config_file)
    if cfg_found == 0 and cfg_default_found == 0 and cfg_global_found:
        print("Config file not found.")
        print(" Not:", config_file)
        print(" Not:", global_config_file)
        print(" Not:", default_config_file)
        exit(1)



    # Create config dictionary (from default config) (lowest priority)
    if cfg_default_found:
        # Load config with defaults
        config = {s:dict(cfg_default.items(s)) for s in cfg_default.sections()}

        # Overwrite with global config var's defaults using local config (med priority)
        if cfg_global_found:
            for s in cfg_global.sections():
                if not s in config:
                    config.update({s: {'set': 1}})
                for op in cfg_global.items(s):
                    if not op in config[s]:
                        config[s].update({op[0]: op[1]})
                    else:
                        config[s][op[0]] = op[1]
                    # if args.debug: print("local config:", s, " - ", op[0], " = ", op[1])
        
        # Overwrite with local config
        if cfg_found:
            for s in cfg.sections():
                if not s in config:
                    config.update({s: {'set': 1}})
                for op in cfg.items(s):
                    if not op in config[s]:
                        config[s].update({op[0]: op[1]})
                    else:
                        config[s][op[0]] = op[1]

    elif cfg_global_found:
        # no default, global only
        config = {s:dict(cfg_global.items(s)) for s in cfg_global.sections()}

        # Overwrite with local config
        if cfg_found:
            for s in cfg.sections():
                if not s in config:
                    config.update({s: {'set': 1}})
                for op in cfg.items(s):
                    if not op in config[s]:
                        config[s].update({op[0]: op[1]})
                    else:
                        config[s][op[0]] = op[1]
    else:
        # no default or global, using local
        config = {s:dict(cfg.items(s)) for s in cfg.sections()}

    # overwrite with global vars TODO (Check)
    #  if cfg_global_found:
    #      config = {s:dict(cfg_global.items(s)) for s in cfg_global.sections()}
    #
    #  # overwrite with local TODO (check)
    #  if cfg_found:
    #      config = {s:dict(cfg.tems(s)) for s in cfg.sections()}
    #

    # Add args to config var for conveonce of a single var
    config.update({'ARGS': {'set': 1}})
    for setting in vars(args):
        #  if args.debug: print("ARGS to config:", setting, " - ", vars(args)[setting])
        #config.update({setting: vars(args)[setting]})
        config['ARGS'].update({setting:vars(args)[setting]})



    ####################
    # Preferred Settings

    # create the 'preferred' key
    config.update({'preferred':{'set': 1}})

    # Preferred vars
    # priority is lowest to highest -> default_config, local_config, args

    # go through each setting

    # web-novel-to-text.py config
    if config_filename == "web-novel-to-text.conf":
        preferred_vars = ('delay_between_requests', 'format', 'speak_asterisk', 'dont_remove_quotes', 'dont_emphasize',
                          'dont_remove_asterisk', 'filename_format', 'debug', 'output_filename', 'test', 
                          'remove_all_bad_chars', 'remove_bad_char', 'remove_non_eu_chars', 'remove_non_latin1_chars',
                          'remove_non_ascii_chars', 'retries', 'timeout')
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
        # storage of changing vars TODO, create second var instead of config
        config.update({'VARS':{'file_number': args.first_file_number}})
        # config['GENERAL'].update({'start_number': args.start_number})

    # audiobook_reencoder config
    elif config_filename == "audiobook-reencoder.conf":
        preferred_vars = ('disable_extract_cover_art', 'disable_embed_cover_art', 'only_extract_cover_art', 'disable_reencode', 
                          'only_reencode', 'disable_split_chapters', 'disable_delete_unneeded_files', 'only_delete_unneeded_files', 
                          'disable_add_id3_genre', 'only_add_id3_genre', 'force_add_cover_art', 'delete_image_file_after_adding', 
                          'audio_output_format', 'bitrate', 'samplerate', 'threads', 'keep_original_files', 'test', 'disable_normalize', 
                          'disable_add_id3_encoded_by', 'ignore_errors', 'disable_id3_change', 'force_normalization', 
                          'delete_non_audio_files', 'delete_non_audio_image_files', 'debug', 'force_reencode','save_files_with_error')
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
        # storage of changing vars TODO, create second var instead of config


    # audiobook-tts.py programs config
    elif config_filename == "audiobook-tts.conf":
        preferred_vars = ('tts_service', 'voice', 'profile', 'locale', 'gender', 'key', 'input_format', 'gtts_lang', 
                          'gtts_tld', 'url_parameters', 'delay_between_requests', 'max_charactors','speaking_rate', 'debug', 'test', 
                          'remove_all_bad_chars', 'remove_bad_chars', 'remove_non_eu_chars', 'remove_non_ascii_chars',         
                          'remove_non_latin1_chars', 'audio_settings', 
                          'audio_format', 'bitrate', 'samplerate', 'read_speed')

        if config.get(config['GENERAL']['tts_service']) is None :
            print("Error: tts serivce \"" + config['GENERAL']['tts_service'] +
            "\" is set in config, yet the section does not exist.  Fix the [GENERAL] \"tts_service\" setting, or add a new section named \"" +
            config['GENERAL']['tts_service'] , "\" an create a file in 'APIs' folder named \"" + config['GENERAL']['tts_service'] + ".py\"")
            exit(1)

        # TTS Service (profiles are not implimented)
        #  if args.profile :
            #  if config[args.profile].get('tts_service') is not None:
                #  config['preferred']['tts_service'] = config[args.profile]['tts_service']
            #  else:
                #  config['preferred']['tts_service'] =  config['GENERAL']['tts_service']
        #  else:
            #  config['preferred']['tts_service'] =  config['GENERAL']['tts_service']
        
        # Set preferred setting
        for setting in preferred_vars:
            config['preferred'].update({setting: ''})
            # if args.debug: print("Config settings:", setting)
            if setting in vars(args).keys(): # var exists
                #  print("argv tts: " + str(vars(args)['tts_service']) + "setting" + str(config[vars(args)['tts_service']].get(setting)))
                if vars(args)[setting]: # var is set
                    #if args.debug: print("vars",vars(args)[setting] )
                    config['preferred'][setting] = vars(args)[setting]
                elif vars(args)['tts_service'] is not None and config[vars(args)['tts_service']].get(setting) is not None: # If the tts_service is set via ARGS and setting is set in config under the selected tts_service
                    config['preferred'][setting] = config[  vars(args)['tts_service'] ][setting]
                elif config[config['GENERAL']['tts_service']].get(setting) is not None:
                    config['preferred'][setting] = config[ config['GENERAL']['tts_service'] ][setting]
                elif config['GENERAL'].get(setting) is not None:
                    config['preferred'][setting] = config['GENERAL'][setting]
            elif vars(args)['tts_service'] is not None and config[vars(args)['tts_service']].get(setting) is not None: # If the tts_service is set via ARGS and setting is set in config under the selected tts_service
                config['preferred'][setting] = config[  vars(args)['tts_service'] ][setting]
            elif config[config['GENERAL']['tts_service']].get(setting) is not  None:
                config['preferred'][setting] = config[config['GENERAL']['tts_service']][setting]
                #  print("asdasdasdasda", setting)

        # set some hard defaults
        if config['preferred']['max_charactors'] == '':
            config['preferred']['max_charactors'] = int(1000)

 
    # online-tts.py programs config
    elif config_filename == "online-tts.conf":
        preferred_vars = ('voice', 'profile', 'locale', 'gender', 'key', 'input_format', 'audio_format', 'audio_settings', 'gtts_lang', 
                          'gtts_tld', 'url_parameters', 'delay_between_requests', 'max_charactors','speaking_rate', 'debug', 'test', 
                          'remove_all_bad_chars', 'remove_bad_chars', 'remove_non_eu_chars', 'remove_non_ascii_char')

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
            # if args.debug: print("Config settings:", setting)
            if setting in vars(args).keys(): # var exists
                if vars(args)[setting]: # var is set
                    #if args.debug: print("vars",vars(args)[setting] )
                    config['preferred'][setting] = vars(args)[setting]
                elif config[config['GENERAL']['tts_service']].get(setting) is not None:
                    config['preferred'][setting] = config[config['GENERAL']['tts_service']][setting]
            elif config[config['GENERAL']['tts_service']].get(setting) is not  None:
                config['preferred'][setting] = config[config['GENERAL']['tts_service']][setting]
                #  print("asdasdasdasda", setting)

        # set some hard defaults
        if config['preferred']['max_charactors'] == '':
            config['preferred']['max_charactors'] = int(1000)

    # TODO: add audiobook-tools

    # Unknown config file
    else:
        print("Error unknown config file, should be 'web-novel-to-text.conf' or 'online-tts.conf' or audiobook-reencoder.conf")
        exit(1)


    # add Places to store changing variables (place holders) (maybe dont use)
    config.update({'INPUT':{'filename': ''}})
    config['INPUT'].update({'text': ''})
    config['INPUT'].update({'text_ssml': ''})
    config['INPUT'].update({'text_chunk': ''})
    config.update({'OUTPUT':{'filename': ''}})
    config.update({'TMP':{'tmp_dir': tmp_dir}})
    
    config.update({'DEBUG':{'debug': args.debug}}) # legacy, TODO remove all instances

    # Correct some posible problems
    for section in config:
        for param in config[section]:
            if type(config[section][param]) == str: # only alter strings
                #  if config['ARGS']['debug']: print("config", section, param, config[section][param])
                # remove leading quotes
                config[section][param] = re.sub(r"^[\"']", '', config[section][param])
                # remove trailing quotes
                config[section][param] = re.sub(r"[\"']$", '', config[section][param])
                # covert true to 1
                if config[section][param].lower() == 'true' or config[section][param] == '1':
                    config[section][param] = True 
                elif  config[section][param].lower() == 'false' or config[section][param] == '0':
                    config[section][param] = False 

                #  config[section][param] = int(re.sub(r"true", '1', config[section][param], flags=re.IGNORECASE))
                # covert true to 0
                #  config[section][param] = int(re.sub(r"false", '0', config[section][param], flags=re.IGNORECASE))

    if args.debug:
        print("------------------------config------------------------")
        pprint.pprint(config)
        print("------------------------------------------------------")


    return config
# End load_config
