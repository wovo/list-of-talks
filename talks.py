# ===========================================================================
#
# File      : talks.py
# Part of   : the Free C++ Talks List (FCTL)
# Copyright : wouter van ooijen 2021# home      
# repo      : https://www.github.com/wovo/fctl
#
# This code is distributed under the Boost Software License, Version 1.0.
# (See accompanying boost.txt file or copy at 
# http://www.boost.org/LICENSE_1_0.txt)
#
# dependecies: request, pafy, youtube-dl
#
# C:\Python39\lib\site-packages\pafy\backend_youtube_dl.py", line 53
# changed to [] to get( .., 0 )
# same for dislikes
#
# ===========================================================================

import sys, glob, os, json, urllib.request, re, pafy

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
   "ö": "o",
   "Č": "C",
   "ć": "c",
   "ä": "a",
   "ë": "e",
   "ó": "o",
   "ś": "s",
   "ę": "e",
   "ź": "z",
   "î": "i",
   "ą": "a",
   "ă": "a",
   "ț": "t",
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
         identifier  : str, 
         meeting     : str, 
         edition     : str,
         title       : str,
         speakers    : str, 
         video       : str, 
         thumbnail   : str, 
         duration    : str,
         tags        : list[ str ] = [],
         level       : int = 0,
         language    : str = "english"
   ):
      self.identifier  = identifier
      self.meeting     = meeting
      self.edition     = edition
      self.title       = title
      self.speakers    = speakers
      self.video       = video
      self.thumbnail   = thumbnail
      self.duration    = duration
      self.tags        = tags
      self.level       = level
      self.language    = language
      
   def to_json( self ):
      return json.dumps( self, 
         default = lambda o: o.__dict__, 
         sort_keys = True, 
         indent = 3 )      
      
      
def pipo():      
      
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
      self.meetings     = set()
      self.editions     = set()
      self.speakers     = set()
      self.tags         = set()
      self.languages    = set()
      if file_name != None:
         self.read_json( file_name )
         
   def add( self, talk ):
      """
      add a single talk
      """   
      if talk.identifier in self.dict:
         print( "snark: duplicate identifier [%s]" % talk.identifier )
         exit( -1 )
      self.list.append( talk )
      self.dict[ talk.identifier ] = talk
      self.meetings.add( talk.meeting )      
      self.editions.add( talk.edition )
      self.speakers.update( talk.speakers ) 
      self.tags.update( talk.tags )  
      self.languages.update( talk.language )  

   def write_html( self, file_name = "index.html" ):
      """
      write the talks to a simple html file
      """   
      file = open( file_name, "w" )
      for talk in self.list:
         file.write( "<img src='%s' height=100><BR>\n" % ( talk.thumbnail ))
         file.write( "%s<BR>\n" % ( talk.identifier ))
         file.write( "<A HREF='%s' target=_blank>%s</A><BR>\n" % ( talk.video, talk.title ))
         file.write( "%s<BR>\n" % ( ", ".join( talk.speakers )))
         file.write( "<BR>\n" )
      file.close()      
      
   def write_json( self, file_name = "talks.json" ):
      """
      write the talks to a json file
      """   
      file = open( file_name, "w" )
      file.write( "{ \"list\": [" )
      separator = ""
      for talk in self.list:
         file.write( separator )
         separator = ","
         file.write( talk.to_json() )
      file.write( "]}" )     
      file.close()  
      
   def read_json( self, file_name = "talks.json" ):
      """      
      read and add talks from a json file
      """
      file = open( file_name, "r" )
      x = json.loads( file.read() )
      file.close()
      for t in x[ "list" ]:
         self.add( talk(
            t[ "identifier" ],
            t[ "meeting" ],
            t[ "edition" ],
            t[ "title" ],
            t[ "speakers" ],
            t[ "video" ],
            t[ "thumbnail" ],
            t[ "duration" ],
            t[ "tags" ],
            t[ "level" ],
            t[ "language" ],
         ) )
      

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

def search_youtube( s ):
   s = ( "+".join( s ) ).replace( " ", "+" )
   html = urllib.request.urlopen( 
      "https://www.youtube.com/results?search_query=" + s )
   video_ids = re.findall( r"watch\?v=(\S{11})", html.read().decode() )
   return video_ids

# ===========================================================================   

def make_talk(
      identifier,
      meeting,
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
         search_terms = speakers + [ meeting, edition, title2 ]
         #print( "search %s" % " ".join( search_terms ) )
         match = search_youtube( search_terms )
         #print( "done" )
         if len( match ) == 0:
            # try without the speakers
            search_terms = [ meeting, edition, title2 ]
            #print( "search 2" )
            match = search_youtube( search_terms )
            #print( "done 2" )
            if len( match ) == 0:
               print( "video not found for [ %s ]" % " ".join( search_terms ))   
            
      if len( match ) > 0:
         video       = "https://youtube.com/watch?v=%s" % match[ 0 ]
         thumbnail   = "http://img.youtube.com/vi/%s/0.jpg" % match[ 0 ]
         duration    = pafy.new( video ).length
          
      return talk(
         identifier  = identifier,
         meeting     = meeting, 
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
   
def process_marker_title_author( meeting, edition, lines, youtube, progress ):
   found_talks = []    
   state = 0
   found = {}
   for nr, line in lines:
      if line.startswith( "#locked" ):
         pass
         
      elif ( state == 0 ) and line.startswith( "#" ):
         state = 1
         identification = line[:].replace( "marker", meeting + "-" + edition )
         
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
            
         found_talks.append( make_talk( 
            identifier  = identification,
            meeting     = meeting,
            edition     = edition,
            title       = title, 
            speakers    = speakers.split( '@' ),
            youtube     = youtube
         ))
         
   return found_talks   
   
   
# ===========================================================================

def add_talks( talks, files, youtube, progress ):

   n_files = 0
   tags = []
   meeting = None
   edition = None
   language = None
   for file_name in glob.glob( files ):
   
      n_files += 1
      file = open( file_name, "r", encoding='utf-8', errors='replace' )
      nr = 0
      lines = []
      for line in file.readlines():
         nr += 1
         line = make_ascii( line.strip() )
         if not is_ascii( line ):
            print( "%s:%d : non ascii" % ( file_name, nr ))         
            for c in line:
               if not is_ascii( c ):
                  print( "[%s]" % c )
            exit( -1 )
         lines.append( [ nr, line ] )
         if line.startswith( "$add" ):
            split = line.split( " " )[ 1 : ]
            if split[ 0 ] == "meeting":
               meeting = split[ 1 ]
            elif split[ 0 ] == "edition":
               edition = split[ 1 ]
            elif split[ 0 ] == "language":
               language = split[ 1 ]
            elif split[ 0 ] == "tags":
               tags.extend( split[ 1 : ] )      
            else:
               print( "unknow $add [%s]" % line )
               exit( -1 )
         
      if meeting == None or edition == None or language == None:
         print( "no meeting, edition, language set" )
         exit( -1 )
         
      new_talks = process_marker_title_author( meeting, edition, lines, youtube, progress )
      for t in new_talks:
         t.tags.extend( tags )
         if language != None: t.language = language
         talks.add( t )
      
      
# ===========================================================================

def command_line_command( args, c, f ):
   if len( args ) > 0 and args[ 0 ] == c:
      youtube = True
      progress = True
      args.pop( 0 )
      while ( len( args ) > 0 ) and args[ 0 ].startswith( "-" ):
         if args[ 0 ] == "-noyoutube":
            youtube = False
         elif args[ 0 ] == "-noprogress":  
            progress = False
         else:
            print( "unknown option [%s]" % args[ 0 ] )
            exit( -1 )
         args.pop( 0 ) 
      if len( args ) > 0:
         print( "do %s %s" % ( c, args[ 0 ] ))
         f( args[ 0 ], youtube, progress )    
         args.pop( 0 )
      else:
         print( "%s command needs a <file>" % ( s ) )
         exit( -1 )
      
      
# ===========================================================================

if __name__ == "__main__":
   """
   command line interface
   """
   args = sys.argv[ 1 : ]
   if args == []:
      print( """commands:
         renumber <text_file>
         read_json <json_file>
         write_json <json_file>
         write_html <html_file>
      """ )   
      exit( -1 )
   
   t = talks()
   while args != []:
      old_args = args[ : ]
      
      command_line_command( args, "renumber",    lambda f, y, p: renumber( f ) )
      command_line_command( args, "read_json",   lambda f, y, p: t.read_json( f ) )
      command_line_command( args, "write_json",  lambda f, y, p: t.write_json( f ) )
      command_line_command( args, "write_html",  lambda f, y, p: t.write_html( f ) )
      command_line_command( args, "add",         lambda f, y, p: add_talks( t, f, y, p ) )
               
      if args == old_args:
         print( "unknown command %s" % args[ 0 ] )
         exit( -1 )
      
