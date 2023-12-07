import logging
import time
import multiprocessing

class profilesupervisor():

    def __init__(self,profilesfile):
        self.profilesfile = profilesfile

    def run(self):
        while True:
            time.sleep(10)
