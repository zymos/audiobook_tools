# -*- coding: utf-8 -*-

import subprocess
import importlib
import os
import sys
import pprint


#  project_dir = "/home/zymos/Documents/Projects/audiobook_tools/online-tts"
#  prog = os.path.join(project_dir, "online-tts.py")

workingin_dir = "tmp/"

if __name__ == "__main__":

    print(os.getcwd())
    sys.path.insert(0, os.getcwd())
    #  exit()
    try:
        # python 3.4+ should use builtin unittest.mock not mock package
        from unittest.mock import patch
    except ImportError:
        from mock import patch

    from audiobook_tools.online_tts import online_tts
     
    os.chdir(workingin_dir)
    print("TESTING cwd:", os.getcwd())
    sys.path.insert(0, os.path.dirname(__file__))
    
    print('TESTING sys.path:', sys.path[0], sys.path)
    # Command line args
    testargs = ['online-tts', '--debug', '2019-03-02 - Interlude.ssml']
    #  exit()
    # emulate CLI args
    with patch.object(sys, 'argv', testargs):
        # Run the prog
        online_tts.main()
    
    exit()
    #
    #
    #  print("workingin_dir = ", workingin_dir )
    #
    #  print("input_file  = ", input_file)
    #
    #  print("scripts_dir  = ", scripts_dir)
    #
    #  print("main_prog = ", main_prog)
    #
    #  print("input_file_full = ", input_file_full)
    #  print("program = ", test_command)
    #
    #  #sys.path.insert(0, '..')
    #  pprint.pprint(sys.path)
    #
    #  sys.path.append(project_dir)
    #  pprint.pprint(sys.path)
    #
    #  #import unittest
    #  #import mock
    #  from unittest.mock import patch
    #
    #  print("loading args")
    #  with patch('sys.argv', command_line_exe):
    #
    #      pprint.pprint(sys.argv)
    #      print("loading main program")
    #      #import importlib
    #      #importlib.import_module('online_tts')
    #      #t = __import__("../online_tts.py")
    #      #t.main()
    #      #import online_tts
    #      #main()
    #      import re
    #
    #      #test = 'I just thought this might be a blacksmith so I<break time="200ms" /> <break time="200ms"/> <break time="500ms"> Adding <prosody> tag.'
    #      #print(test)
    #      #test = re.sub("<break time=\"[a-zA-Z0-9]*\">\s*<break time=\"[a-zA-Z0-9]*\">",
    #                     #"&&", test)
    #
    #      #test = re.sub(r"(<break time=\"[a-zA-Z0-9]*\"[ ]?/?>\s){2,}",
    #                     #"++++", test)
    #      #print("-----")
    #      #print(test)
    #      #exit()
    #
    #      #exec(open(prog).read())
    #
    #      #import runpy
    #      #runpy.run_path(prog)
    #
    #
    #
    #  #p = importlib.import_module(command)
    #  #print(main_prog)
    #  p = subprocess.Popen(test_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    #  print(p.communicate()[0])
    #
    #
    #  print("test done")
    #  exit()
    #  #print(p.communicate())
