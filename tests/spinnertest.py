#!/usr/bin/env python

"""
Main program for audiobook-reencoder

calls the functions in audiobook_tools/audiobook_reencoder/audiobook_reencoder.py
"""

#  if __name__ == "__main__" :
import sys
sys.path.append("..")

from audiobook_tools.common.spinner import Spinner

if __name__ == '__main__':
    import time
    # Testing
    spinner = Spinner()
    spinner.start("Downloading")
    # Make actions
    time.sleep(5) # Simulate a process
    #
    spinner.stop()


    #  audiobook_reencoder.main()
