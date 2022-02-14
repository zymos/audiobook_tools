#!/usr/bin/python
# -*- coding: utf-8 -*-

from queue import Queue
from threading import Thread
from random import random 
import time


def do_stuff(q):
  while True:
    time.sleep(10*random())
    print(q.get())
    q.task_done()



q = Queue(maxsize=0)
num_threads = 10

for i in range(num_threads):
  worker = Thread(target=do_stuff, args=(q,))
  worker.setDaemon(True)
  worker.start()

for y in range (10):
  for x in range(10):
    q.put(x + y * 10)
  #  print("Batch " + str(y) + " Done")


q.join()
