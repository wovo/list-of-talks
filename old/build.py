# ===========================================================================
#
# File      : build.py
# Part of   : the Free C++ Talks List (FCTL)
# Copyright : wouter van ooijen 2020
# home      : https://www.github.com/wovo/fctl
#
# This script builds a list C++ talks that 
# were held on one or more conferences, 
# by extracting this info from the text form of the published schedules,
# and using a youtube search to find the corresponding videos.
#
# This code is distributed under the Boost Software License, Version 1.0.
# (See accompanying BOOST-license.txt file or copy at 
# http://www.boost.org/LICENSE_1_0.txt)
#
# ===========================================================================

import sys, glob, os
import talks, search

   
# ===========================================================================

def time_in_minutes( time ):
   # from https://stackoverflow.com/questions/10663720
   return sum( x * int(t) for x, t in zip([60, 1], time.split(":")))

def time_as_time( n ):
   return "%d:%02d" % ( n // 60, n % 60 )
   
def write_to_file( file, text ):
   f = open( file, "w" )
   f.write( text )
   f.close
   
   
# ===========================================================================

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
         level       = level      
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
      
def main( args ):
        
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
      args = args[ 1 : ]      
      
   if len( args ) != 2:
      print( "usage: build [options] <conference> <edition>" )
      print( "options: -noyoutube, -noprogress" )
      exit( -1 )
      
   if args[ 0 ] in [ "accu", "cppcon" ]:
      process( process_title_author, args[ 0 ], args[ 1 ], youtube, progress )

   else:
      print( "unknown conference type [%s]", args[ 0 ] )
      
if __name__ == "__main__":
   main(  sys.argv[ 1 : ] )