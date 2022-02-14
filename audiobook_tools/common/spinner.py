
#
#  import sys
#  import time
#  #
#  #  def main():
#  #
#  #      spinner = Spinner()
#  #      for x in range(20):
#  #          time.sleep(0.2)
#  #          spinner.update()
#  #      spinner.done()
#  #
#  class Spinner:
#      HIDE_CURSOR = '\x1b[?25l'
#      SHOW_CURSOR = '\x1b[?25h'
#      #_phases = ['⎺', '⎻', '⎼', '⎽', '⎼', '⎻']
#      _phases = ['•••  ', ' ••• ', '  •••', '•  ••', '••  •']
#      _status = 0
#      _spinner_length = 5
#
#      def __init__(self):
#          sys.stdout.write(self.HIDE_CURSOR)
#          sys.stdout.flush()
#
#      def update(self):
#          new_status = self._phases[self._status]
#          sys.stdout.write('\b' * self._spinner_length)
#          sys.stdout.write(new_status)
#          sys.stdout.flush()
#          if self._status == len(self._phases) - 1:
#              self._status = 0
#          else:
#              self._status += 1
#
#      def done(self):
#          sys.stdout.write('\b' * self._spinner_length)
#          sys.stdout.write(' ' * self._spinner_length)
#          sys.stdout.write('\b' * self._spinner_length)
#          sys.stdout.write(self.SHOW_CURSOR)
#          sys.stdout.flush()
#

#
#  import sys
#  import time
#
#  import threading
#
#
#  class Spinner(threading.Thread):
#
#      def __init__(self):
#          super().__init__(target=self._spin)
#          self._stopevent = threading.Event()
#
#      def stop(self):
#          self._stopevent.set()
#
#      def _spin(self):
#
#          while not self._stopevent.isSet():
#              for t in '|/-\\':
#                  sys.stdout.write(t)
#                  sys.stdout.flush()
#                  time.sleep(0.1)
#                  sys.stdout.write('\b')
#
#
#



#
#  # -*- coding: utf-8 -*-
#
#  import threading
#  import sys
#  import time
#  import os
#
#  spinner="▏▎▍▌▋▊▉█▉▊▌▍▎" #utf8
#
#  #convert the utf8 spinner string to a list
#  chars=[c.encode("utf-8") for c in spinner]
#
#  class Spinner(threading.Thread):   # not sure what to put in the brackets was (threading.Thread, but now im not sure whether to use processes or not)
#
#      def __init__(self):
#          super(Spinner,self).__init__() # dont understand what this does
#          self._stop = False
#
#      def run (self):
#          pos=0
#          while not self._stop:
#              sys.stdout.write("\r"+chars[pos])
#              sys.stdout.flush()
#              time.sleep(.15)
#              pos+=1
#              pos%=len(chars)
#
#      def cursor_visible(self):
#          os.system("tput cvvis")
#      def cursor_invisible(self):
#          os.system("tput civis")
#      def stop(self):
#          self._stop = True  #the underscore makes this a private variable ?
#      def stopped(self):
#          return self._stop == True
#
#
#  if __name__ == "__main__":
#      s = Spinner()
#      s.cursor_invisible()
#      s.start()
#      #  a = raw_input("")
#      s.stop()
#      s.cursor_visible()
#
#
#
#
#




# From https://stackoverflow.com/questions/4995733/how-to-create-a-spinning-command-line-cursor
#
from itertools import cycle
import threading
import time


class Spinner:
    #  __default_spinner_symbols_list = ['|-----|', '|#----|', '|-#---|', '|--#--|', '|---#-|', '|----#|']
    __default_spinner_symbols_list = ['[|] ', '[/] ', '[-] ', '[\\] ', '[|] ', '[/] ','[-] ','[\\] ']

    def __init__(self, spinner_symbols_list: [str] = None):
        spinner_symbols_list = spinner_symbols_list if spinner_symbols_list else Spinner.__default_spinner_symbols_list
        self.__screen_lock = threading.Event()
        self.__spinner = cycle(spinner_symbols_list)
        self.__stop_event = False
        self.__thread = None

    def get_spin(self):
        return self.__spinner

    def start(self, spinner_message: str):
        self.__stop_event = False
        time.sleep(0.3)

        def run_spinner(message):
            while not self.__stop_event:
                print("\r{message} {spinner}".format(message=message, spinner=next(self.__spinner)), end="")
                time.sleep(0.3)

            self.__screen_lock.set()

        self.__thread = threading.Thread(target=run_spinner, args=(spinner_message,), daemon=True)
        self.__thread.start()

    def stop(self):
        self.__stop_event = True
        if self.__screen_lock.is_set():
            self.__screen_lock.wait()
            self.__screen_lock.clear()
            print("\r", end="")

        print("\r", end="")

if __name__ == '__main__':
    import time
    # Testing
    spinner = Spinner()
    spinner.start("Downloading")
    # Make actions
    time.sleep(5) # Simulate a process
    #
    spinner.stop()


