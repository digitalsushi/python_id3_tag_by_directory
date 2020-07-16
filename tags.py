#!/usr/bin/env python3
import argparse,glob,os
from mp3_tagger import MP3File, VERSION_1, VERSION_2, VERSION_BOTH
from threading import Thread
from queue import *

#stuff
class TaskQueue(Queue):
  def __init__(self, num_workers=1):
    Queue.__init__(self)
    self.num_workers = num_workers
    self.start_workers()

  def add_mp3(self, file):
    self.put(file)
    print("processing " + file)

  def start_workers(self):
    for i in range(self.num_workers):
      t = Thread(target=self.worker)
      t.daemon = True
      t.start()

  def worker(self):
    while True:
      item = self.get()
      process(item)
      self.task_done()
#/stuff

def process(file):
  print(file)
  mp3=MP3File(file)
  parts=file.split('/')
  mp3.set_version(VERSION_2)
  mp3.genre=parts[0]
  mp3.artist=parts[1]
  mp3.album=parts[2]
  mp3.song=parts[3]

def worker(dirs):
   print("i am a worker function, neat")
   print(dirs)
   q = TaskQueue(num_workers=10)
   for d in dirs:
     print(d)
     os.chdir(d)
     for file in glob.iglob("**/*.mp3",recursive=True):
       q.add_mp3(file)
   q.join()
   print("finished everything")

def showtime():
  parser = argparse.ArgumentParser(description="do some stuff")
  parser.add_argument('--foo', help='foo help')
  parser.add_argument('-d','--dir', nargs='+', dest='music_dirs', help='<Required> Set flag', required=True)
  args = parser.parse_args()
  worker(args.music_dirs)

if __name__ == "__main__":
  showtime()
