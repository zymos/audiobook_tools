# Create an python file to the 'APIs' folder with the name of your new API
the main function in the file should be 
<pre>
get_tts_audio(text_in, config, args)
</pre>
-*** the input is string 'text_in'
- should return binary audio (prefered mp3 format)
- to get debug output use 'DEBUG = config['DEBUG']['debug']'
- to use settings from config file use variables 'config['prefered']['VARIABLE_NAME']'

# Add API to config file
- edit 'config_files/DEFAULT/DEFAULT-audiobook-tts.conf'
- add section for your API, named the same as your APIs filename without the '.py'
- use common variables if posible.  
                           ('voice', 'profile', 'locale', 'gender', 'key', 'input_format', 'gtts_lang', 
                          'gtts_tld', 'url_parameters', 'delay_between_requests', 'max_charactors','speaking_rate', 'debug', 'test', 
                          'remove_all_bad_chars', 'remove_bad_chars', 'remove_non_eu_chars', 'remove_non_ascii_char', 'audio_settings', 
                          'format', 'bitrate', 'samplerate', 'read_speed')
- if you need to add a new option you will need to add it to 'audiobook_tools/common/load_config.py' in the variable 'preferred_vars' under the line 'elif config_filename == "audiobook-tts.conf":'

- edit  'config_files/audiobook-tts.conf'
- copy your section with all options commented out
=Documend you API in the 'docs/audiobook_tts.md'=
- Describe your API and its options

 




