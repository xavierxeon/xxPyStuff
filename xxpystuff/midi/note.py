#!/usr/bin/env python3

class Note:

   Sixteenth = 1
   Eighth = 2
   Quarter = 4
   Half = 8
   Full = 16

   def __init__(self, pitch, duration, velocity = 127):

      self.pitch = pitch
      self.duration = duration
      self.velocity = velocity

   @staticmethod
   def pitch(note):

      noteValues = {
         'C': 0, 
         'C#': 1, 
         'D': 2, 
         'D#': 3, 
         'E' : 4, 
         'F': 5, 
         'F#': 6, 
         'G': 7,
         'G#': 8,
         'A': 9,
         'A#': 10,
         'B': 11
      }

      root = note[:-1]
      # 60 equals C4
      octave = int(note[-1:]) + 1
      value = noteValues[root] + (12 * octave)
      return value      

