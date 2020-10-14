# ===========================================================================
#
# File      : talks.py
# Part of   : the Free C++ Talks List (FCTL)
# Copyright : wouter van ooijen 2020
# home      : https://www.github.com/wovo/fctl
#
# This code is distributed under the Boost Software License, Version 1.0.
# (See accompanying BOOST-license.txt file or copy at 
# http://www.boost.org/LICENSE_1_0.txt)
#
# ===========================================================================

import glob, os, pickle


# ===========================================================================

class talk:
   """
   A talk object has the information about one talk 
   (all are strings, unless noted):
      - identifier  : the unique indentifier for this talk
      - conference  : conference name 
      - edition     : (list of strings) the edition (often just the year) of the conference
      - title       : the title of the talk
      - speakers    : (python list of strings) the speaker(s)
      - video       : url of the video (probably on youtube)
      - thumbnail   : url of a thumbnail of the video (probably also on youtube)
      - duration    : (int) length of the video in minutes
      - tags        : (list of strings) the tags of the talk
      - level       : (int) the level of the talk (1 novice, 10 expert, 0 unknow)
   """

   def __init__( self, 
         identifier, 
         conference, 
         edition,
         title,
         speakers, 
         video, 
         thumbnail, 
         duration,
         tags = [],
         level = 0
   ):
      self.identifier = identifier
      self.conference = conference
      self.edition = edition
      self.title = title
      self.speakers = speakers
      self.video = video
      self.thumbnail = thumbnail
      self.duration = duration
      self.tags = tags
      self.level = level
      
   def __str__( self ):
      return "%s : [%s]" % ( self.speakers, self.title )
      
   def html( self ):
      s = ""
      s += '%s %s (%s)<BR>\n' % \
         ( self.conference, self.year, time_as_time( self.duration ))
      if self.video == None:
         s += '[no video] %s <BR>\n' % self.title
      else:
         s += '<A HREF="%s">%s</A><BR>\n' % ( self.video, self.title )
      separator = ""
      for speaker in self.speakers:
         s += separator + speaker
         separator = ", "
      s += "<BR>\n<BR>\n"   
      return s

      
# ===========================================================================

class talks:
   """
   A talks object has all the talks, and some aggregates information:
      - list        : the list of all talks
      - dict        : the dictionary of all talks, indexed by indetifier
      - conferences : the set of all conferences
      - editions    : the set of all editions
      - speakers    : the set of all speakers
      - tags        : the set of all tags
   """
   
   def __init__( self, file_name = None ):
      """
      create an empty talks object, optionally reading its content from a file
      """
      self.list = []
      self.dict = dict()
      self.conferences = set()
      self.editions = set()
      self.speakers = set()
      self.tags = set()
      if file_name != None:
         file = open( file_name, "rb" )
         for t in pickle.load( file ).list:
            self.add( t )
         file.close()
      
   def add( self, talk ):
      """
      add a single talk
      """   
      self.list.append( talk )
      if talk.identifier in self.dict:
         print( "snark: duplicate identifier [%s]" % talk.identifier )
         exit( -1 )
      self.dict[ talk.identifier ] = talk
      self.conferences.add( talk.conference )      
      self.editions.add( talk.edition )
      self.speakers.update( talk.speakers ) 
      self.tags.update( talk.tags )  

   def write( self, file_name ):
      """
      write the talks object to a file
      """   
      file = open( file_name, "wb" )
      pickle.dump( self, file )
      file.close()      
      
   # read and write tags and other extra info?

      
# ===========================================================================

def all_talks( selection = "*/*.talks"):
   all = talks()
   for file in glob.glob( selection ):
      for talk in talks( file ).list:
         all.add( talk )
   return all
