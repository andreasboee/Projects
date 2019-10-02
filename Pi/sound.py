#pip install setuptools
#pip install cffi
#pip install sounddevice

import os
import sounddevice as sd
import numpy as np

class Sound:

    total = 0
    samples = 0
    avg = 0

    duration = 120000 #12000 msec = 120 seconds

    def __init__(self):
        self.check_sound()
    
    def record_sound(self, indata, outdata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        self.total = self.total + volume_norm
        self.samples = self.samples + 1
        self.avg = self.total / self.samples

    def get_status(self):
        return self.status

    def check_sound(self):
        self.avg = 0
        self.total = 0
        self.samples = 0

        with sd.Stream(callback=self.record_sound):
            sd.sleep(self.duration)

        return round(self.avg, 2)
