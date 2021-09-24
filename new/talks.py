# ===========================================================================
#
# File      : talks.py
# Part of   : the Free C++ Talks List (FCTL)
# Copyright : wouter van ooijen 2021# home      
# repo      : https://www.github.com/wovo/fctl
#
# This code is distributed under the Boost Software License, Version 1.0.
# (See accompanying BOOST-license.txt file or copy at 
# http://www.boost.org/LICENSE_1_0.txt)
#
# ===========================================================================

import sys, glob, os, json, youtube_search

def time_in_minutes( time ):
   # from https://stackoverflow.com/questions/10663720
   return sum( x * int( t ) for x, t in zip( [ 60, 1 ], time.split( ":" )))

def time_as_time( n ):
   return "%d:%02d" % ( n // 60, n % 60 )
   
def write_to_file( file, text ):
   with open( file, "w" ) as f:
      f.write( text )

replacements = {
   "•": "@",
   "í": "i",
   "á": "a",
   "é": "e",
   "á": "a",
   "ł": "l",
   "ñ": "n",
   "’": "'",
   "＜": "<",
   "＞": ">",
   "ň": "n",
   "ř": "r",
   "ý": "y",
   "ń": "n",
   "=": "=",
   "ü": "u",
   "“": "\"",
   "”": "\"",
   "ç": "c",
   "–": "-",
   "ć": "c",
   "Á": "A",
   "Ł": "L",
   "x": "x",
   "x": "x",
   "x": "x",
   "x": "x",
   "x": "x",
   "x": "x",
}   
      
def make_ascii( s ):
   """
   returns the string with the non-ascii characters 
   replaced by an ascii equivalent.
   """
   
   result = ""
   for c in s:
      c = replacements.get( c, c )   
      result += c
   return result   
      
def is_ascii( s ):
    return all( ord( c ) < 128 for c in s )         
   
def force_ascii( s ):
   r = ""
   for c in s:
      if ord(c) < 128: r += c
   return r   
      

# ===========================================================================

class talk:
   """
   the information of a single talk (all strings are ascii):
      - identifier  : unique indentifier for this talk
      - meeting     : meeting name 
      - edition     : edition (often just the year) of the meeting
      - title       : title of the talk
      - speakers    : the speaker(s)
      - video       : video url (probably on youtube)
      - thumbnail   : video thumbnail url (probably also on youtube)
      - duration    : length of the video in minutes
      - tags        : tags of the talk
      - level       : level of the talk (1 novice, 10 expert, 0 unknow)
      - thumbnail   : language of the talk (for now, only "english")
   """

   def __init__( self, 
         identifier  : string, 
         meeting     : string, 
         edition     : string,
         title       : string,
         speakers    : string, 
         video       : string, 
         thumbnail   : string, 
         duration    : string,
         tags        : List[ string ] = [],
         level       : int = 0,
         language    : string = "english"
   ):
      self.identifier  = identifier
      self.conference  = conference
      self.edition     = edition
      self.title       = title
      self.speakers    = speakers
      self.video       = video
      self.thumbnail   = thumbnail
      self.duration    = duration
      self.tags        = tags
      self.level       = level
      self.language    = language
      
   def __str__( self ):
      return "(%s) %s : [%s]" % ( self.identifier, self.speakers, self.title )
      
   def html_line( self ):
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
   all the talks, and some aggregate information:
      - list        : (list of talks) the list of all talks
      - dict        : (dict of string:talk) dictionary of all talks, indexed by indentifier
      - meetings    : (list of strings) set of all meetings
      - editions    : (list of strings) set of all editions
      - speakers    : (list of strings) set of all speakers
      - tags        : (list of strings) set of all tags
      - languages   : (list of strings) set of all languages
   """
   
   def __init__( self, file_name = None ):
      """
      create an empty talks object, optionally reading its content from a json file
      """
      self.list         = []
      self.dict         = dict()
      self.conferences  = set()
      self.editions     = set()
      self.speakers     = set()
      self.tags         = set()
      self.languages    = set()
      if file_name != None:
         self.read_json( file_name )
         
   def read_json( self, file_name = "talks.json" ):
      """      
      read and add talks from a json file
      """
      file = open( file_name, "r" )
      list = json.loads( fileObject.read() )
      file.close()
      for talk in list:
         self.add( talk )
      
   def add( self, talk ):
      """
      add a single talk
      """   
      if talk.identifier in self.dict:
         print( "snark: duplicate identifier [%s]" % talk.identifier )
         exit( -1 )
      self.list.append( talk )
      self.dict[ talk.identifier ] = talk
      self.conferences.add( talk.conference )      
      self.editions.add( talk.edition )
      self.speakers.update( talk.speakers ) 
      self.tags.update( talk.tags )  
      self.language.update( talk.language )  

   def write_json( self, file_name = "talks.json" ):
      """
      write the talks to a json file
      """   
      file = open( file_name, "w" )
      file.write( json.dumps( self.list )
      file.close()  
      
   def write_html( self, file_name = "index.html" ):
      """
      write the talks to a simple html file
      """   
      file = open( "index.html", "w" )
      for talk in self.talks( "all.talks" ).list:
         file.write( "<img src='%s' height=100><BR>\n" % ( talk.thumbnail ))
         file.write( "%s<BR>\n" % ( talk.identifier ))
         file.write( "<A HREF='%s' target=_blank>%s</A><BR>\n" % ( talk.video, talk.title ))
         file.write( "%s<BR>\n" % ( ", ".join( talk.speakers )))
         file.write( "<BR>\n" )
      file.close()      
      

# ===========================================================================

def renumber( file_name ):
   """
      renumber the #....DDDD lines in a file.
      Use this only once, before the file enters the list, because
      a number must be and remain unique.
      Place a '#locked' line in the file after adding it to the list.
   """
   result = []
   
   file = open( file_name, "r", encoding='utf-8', errors='replace' )
   nr = 0
   for line in file.readlines():
      if line.startswith( "#locked" ):
         print( "file has a #locked line - not renumbered" )
         exit( -1 )
      if line.startswith( "#" ):
         line = line[ : -1 ]
         nr += 1
         while line[ -1 ] in "01234567890":
            line = line[ : -1 ]
         line += "%04d\n" % nr
      result.append( line )
   file.close()
   
   file = open( file_name, "w", encoding='utf-8', errors='replace' )
   for line in result:
      file.write( line )
   file.close()   
   
   
# ===========================================================================   

def make_talk(
      identifier,
      conference,
      edition,
      title,
      speakers,
      youtube
   ):
      """   
      return a talk object from the info found in a conference schedule
      """
   
      video = ""
      thumbnail = ""
      duration = ""
      tags = []
      level = 0
      match = []
      language = "english"
      
      title2 = title
      if title2.endswith( " I" ): title2 = '"%s"' % title2
      if title2.endswith( " II" ): title2 = '"%s"' % title2
      
      if youtube:
         search_terms = speakers + [ conference, edition, title2 ]
         match = search.YoutubeSearch( " ".join( search_terms ) ).to_dict()
         if len( match ) == 0:
            # try without the speakers
            search_terms = [ conference, edition, title2 ]
            match = search.YoutubeSearch( " ".join( search_terms ) ).to_dict()
            if len( match ) == 0:
               print( "video not found for [ %s ]" % " ".join( search_terms ))   
            
      if len( match ) > 0:
         match = match[ 0 ]
         video       = "https://youtube.com" + match[ "url_suffix" ]
         thumbnail   = match[ "thumbnails" ][ 0 ].split( "?" )[ 0 ]
         duration    = time_in_minutes( match[ "duration" ] )
          
      return talks.talk(
         identifier  = identifier,
         conference  = conference, 
         edition     = edition,
         title       = title,
         speakers    = speakers, 
         video       = video,
         thumbnail   = thumbnail,
         duration    = duration,
         tags        = tags,
         level       = level,
         language    = language
      )
      
      
# =========================================================================== 
   
def process_title_author( conference, edition, lines, youtube, progress ):
   found_talks = talks.talks()     
   state = 0
   found = {}
   for nr, line in lines:
      if line.startswith( "#locked" ):
         pass
         
      elif ( state == 0 ) and line.startswith( "#" ):
         state = 1
         identification = line[:]
         
      elif state == 1:
         state = 2
         title = line[:]
         
      # ccpcon 2016 has title-room-speakers
      elif state == 2 and not line.endswith( ")" ):         
         speakers = line[:]
         state = 0
         
         if progress:
            sys.stdout.write( "\r%s   " % identification )
            sys.stdout.flush()
            
         key = title + " " + speakers
         if key in found:
            print( "duplicate: %s %s" % ( found[ key ], identification ))
         found[ key ] = identification   
            
         found_talks.add( make_talk( 
            identifier  = identification,
            conference  = conference,
            edition     = edition,
            title       = title, 
            speakers    = speakers.split( '@' ),
            youtube     = youtube
         ))
   return found_talks   
   
   
# ===========================================================================

def process( processor, conference, edition, youtube , progress ):

   n_files = 0
   for file_name in glob.glob( conference + "/" + edition + ".txt" ):
   
      n_files += 1
      file = open( file_name, "r", encoding='utf-8', errors='replace' )
      nr = 0
      lines = []
      for line in file.readlines():
         nr += 1
         line = make_ascii( line.strip() )
         if not is_ascii( line ):
            print( "%s:%d : non ascii" % ( file_name, nr ))         
            exit( -1 )
         lines.append( [ nr, line ] )
         
      talks = processor( conference, edition, lines, youtube, progress )
      talks.write( file_name.replace( ".txt", ".talks" ))
      
   if progress:
      print( "%d file(s) processed" % n_files )
      
      
# ===========================================================================

def process( files ):    
      
   if len( args ) != 2:
      print( "usage: build [options] <conference> <edition>" )
      print( "options: -noyoutube, -noprogress" )
      exit( -1 )
      
   if args[ 0 ] == "cppcon":
      process( process_title_author, args[ 0 ], args[ 1 ], youtube, progress )

   else:
      print( "unknown conference type [%s]", args[ 0 ] )


def command_line_command( n, c, f ):
   if sys.argv[ n ] == c:
      n += 1
      youtube = True
      progress = True
      while ( len( args ) > 0 ) and args[ 0 ].startswith( "-" ):
         if args[ 0 ] == "-noyoutube":
            youtube = False
         elif args[ 0 ] == "-noprogress":  
            progress = False
      else:
         print( "unknown option [%s]" % args[ 0 ] )
         exit( -1 )
      if sysn.argc > n:
         f( sys.argv[ n ] )    
         n += 1
      else:
         print( "%s <file>", ( s ) )
         exit( -1 )
   return n            
      
if __name__ == "__main__":
   """
   command line interface
   """
   if sys.argc == 0:
      print( """commands:
         renumber <text_file>
         read_json <json_file>
         write_json <json_file>
         write_html <html_file>
      """ )   
   else:
      n = 1
      t = talks()
      while sys.argc >= n:
         q = n
      
         n = command_line_command( n,  "renumber",    renumber )
         n = command_line_command( n,  "read_json",   read_json )
         n = command_line_command( n,  "write_json",  write_json )
         n = command_line_command( n,  "write_html",  write_json )
         n = command_line_command( n,  "process",     process )
               
         if q == n:
            print( "unknown command %s", sys.argv[ n ] )
            exit( -1 )
      
      
# ===========================================================================

def all_talks( selection = "*/*.talks"):
   all = talks()
   for file in glob.glob( selection ):
      for talk in talks( file ).list:
         all.add( talk )
   return all

def bla:
 all = talks.talks()
 n = 0
 for file_name in glob.glob( "*/*.talks" ):
   print( file_name )
   n += 1
   for t in talks.talks( file_name ).list:
      all.add( t )
 print( "%d file(s) gathered" % n )
 all.write( "all.talks"       )   
