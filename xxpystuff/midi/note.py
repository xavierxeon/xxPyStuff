#!/usr/bin/env python3

class MidiNote:

   class Duration:

      def __init__(self, tempo = 120):

         self._quartersPerSecond = tempo / 60

      def half(self):

         return self._duration(0.5)

      def quarter(self):

         return self._duration(1)

      def eighth(self):

         return self._duration(2)

      def sixteenth(self):

         return self._duration(4)

      def _duration(self, notePerQaurter):

         notesPerSecond =  notePerQaurter * self._quartersPerSecond 
         secondsPerNote = 1/ notesPerSecond
         return secondsPerNote

   @staticmethod
   def convert(note):

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