# -*- coding: utf-8 -*-

import subprocess
import importlib
import os
import sys
import pprint


project_dir = "/home/zymos/Documents/Projects/audiobook_tools/online-tts"
prog = os.path.join(project_dir, "online-tts.py")

workingin_dir = "/home/zymos/tmp/wanderinginn/4/"

input_file = 'testing.ssml'

scripts_dir = os.path.dirname(os.path.realpath(__file__))

main_prog = os.path.join(scripts_dir, '../online-tts.py')

input_file_full = os.path.join(workingin_dir,input_file)
    
params = ''

test_command =['python',
               main_prog,
               params,
               input_file]


command_line_exe = [main_prog, input_file]


if __name__ == "__main__":

    
    print("workingin_dir = ", workingin_dir )

    print("input_file  = ", input_file)

    print("scripts_dir  = ", scripts_dir)

    print("main_prog = ", main_prog)

    print("input_file_full = ", input_file_full)
    print("program = ", test_command)  
    
    os.chdir(workingin_dir)
    #sys.path.insert(0, '..')   
    pprint.pprint(sys.path)

    sys.path.append(project_dir)
    pprint.pprint(sys.path)
    
    #import unittest
    #import mock
    from unittest.mock import patch
    
    print("loading args")
    with patch('sys.argv', command_line_exe):
        
        pprint.pprint(sys.argv)
        print("loading main program")
        #import importlib
        #importlib.import_module('online_tts')
        #t = __import__("../online_tts.py")
        #t.main()        
        #import online_tts
        #main()
        import re
        
        #test = 'I just thought this might be a blacksmith so I<break time="200ms" /> <break time="200ms"/> <break time="500ms"> Adding <prosody> tag.'
        #print(test)
        #test = re.sub("<break time=\"[a-zA-Z0-9]*\">\s*<break time=\"[a-zA-Z0-9]*\">", 
                       #"&&", test)

        #test = re.sub(r"(<break time=\"[a-zA-Z0-9]*\"[ ]?/?>\s){2,}", 
                       #"++++", test)
        #print("-----")
        #print(test)
        #exit()
        
        #exec(open(prog).read())
        
        #import runpy 
        #runpy.run_path(prog)
    
    
    
    #p = importlib.import_module(command)
    #print(main_prog)
    p = subprocess.Popen(test_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    print(p.communicate()[0])
    
    
    print("test done")
    exit()
    #print(p.communicate())