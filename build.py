# ===========================================================================
#
# This script builds a list C++ talks that were held on a set of conferences.
#
# ===========================================================================

from youtube_search import YoutubeSearch
import sys

def time_in_minutes( time ):
   # https://stackoverflow.com/questions/10663720/how-to-convert-a-time-string-to-seconds
   return sum( x * int(t) for x, t in zip([3600, 60, 1], time.split(":")))


# ===========================================================================

class talk:
    """
    A talk object has the information about one talk 
    (all are strings, unless noted):
    - conference : "cppcon" etc.
    - year : the year the conference took place
    - title: the title of the talk
    - speakers : (python list of strings) the speaker(s)
    - video: url of the video (on youtuibe)
    - duration: (int) length of the video in minutes
    """

   def __init__( self, title, conference, year, speakers, google ):
      self.conference = conference
      self.year = year
      self.title = title
      self.speakers = speakers
      self.video = None
      self.duration = 0
      
      if google and ( self.video == None ):
         search = title + " " + conference + " " + year + " ".join( speakers )
         match = YoutubeSearch( search, max_results = 1 ).to_dict()
         if len( match ) > 0:
            match = match[ 0 ]
            self.duration = time_in_minutes( match[ "duration" ] )
            self.video = "https://youtube.com" + match[ "url_suffix" ]
         else:
            print( "not found [%s]" % search
      
   def __str__( self ):
      return "%s : [%s]" % ( self.speakers, self.title )
      
   def html( self ):
      s = ""
      s += '%s %s (%s)<BR>\n' % ( self.conference, self.year, self.duration )
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
      
def is_ascii(s):
    return all(ord(c) < 128 for c in s)      
      
      
# ===========================================================================

def cppcon( year, progress, google ):
   """
   Return the list of talks for the cppcon year (or years).
   """

   talks = []
   if not isinstance( year, str ):
      for y in year:
         talks.extend( cppcon( y, progress, google ))  
      return talks      
   state = 0
   nr = 0
   file_name = year + ".txt"
   for line in open( file_name, "r", encoding='utf-8', errors='replace' ).readlines():
      nr = nr + 1
      line = make_ascii( line )
      if progress:
         sys.stdout.write( "\rCppCon %s %d     " % ( year, nr ))
         sys.stdout.flush()
      if 0: print( state, line )
      if not is_ascii( line ):
         print( "%s:%d : non ascii : [%s]" % ( file_name, nr, line ))
      if ( state == 2 ) and line.strip().endswith( ")" ):
         # 2016 and earlier had room lines
         pass
      elif state == 1:
         title = line.strip()
         state = 2
      elif state == 2:
         speakers = line.strip()
         state = 1
         if 0: print( speakers, title )         
         if speakers != '' and not title.startswith( "Book Signing" ):
            talks.append( talk( 
               conference = "CppCon",
               year = year,
               title = title, 
               speakers = speakers.split( '@' ),
               google = google
            ))
      if line.strip().endswith( "MDT" ) or line.strip().endswith( "PDT" ) : 
         state = 1
      if line.strip() == "": 
         state = 0
   return talks
   
def write_talks( file_name, talks ):
   f = open( file_name, "w" )
   for t in talks: 
      f.write( t.html() )
   f.close()   
    
talks = cppcon( [ "2014", "2015", "2016", "2017", "2018", "2019" ], progress = True, google = True )      
write_talks( "index.html", talks )