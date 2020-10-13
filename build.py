# ===========================================================================
#
# This script builds a list C++ talks that were held on a set of conferences.
#
# ===========================================================================

import sys, time, glob, os

#try:
#   from youtube_search import YoutubeSearch
#except:
#   print( "install youtube_search: pip [-m] install youtube-search" )
#   exit( -1 )


# ===========================================================================
#
# from https://github.com/joetats/youtube_search
#
# ===========================================================================

import requests, urllib.parse, json

class YoutubeSearch:
    def __init__(self, search_terms: str, max_results=None):
        self.search_terms = search_terms
        self.max_results = max_results
        self.encoded_search = urllib.parse.quote(self.search_terms)
        self.BASE_URL = "https://youtube.com"
        self.url = f"{self.BASE_URL}/results?search_query={self.encoded_search}"
        self.videos = self.search()

    def search(self):
        self.response = requests.get(self.url).text
        while 'window["ytInitialData"]' not in self.response:
            self.response = requests.get(self.url).text
        self.response = force_ascii( self.response )
        results = self.parse_html(self.response)
        if self.max_results is not None and len(results) > self.max_results:
            return results[: self.max_results]
        return results

    def parse_html(self, response):
        results = []
        start = (
            response.index('window["ytInitialData"]')
            + len('window["ytInitialData"]')
            + 3
        )
        end = response.index("};", start) + 1
        json_str = response[start:end]
        data = json.loads(json_str)

        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"
        ]["contents"][0]["itemSectionRenderer"]["contents"]

        for video in videos:
            res = {}
            if "videoRenderer" in video.keys():
                video_data = video.get("videoRenderer", {})
                res["id"] = video_data.get("videoId", None)
                res["thumbnails"] = [thumb.get("url", None) for thumb in video_data.get("thumbnail", {}).get("thumbnails", [{}]) ]
                res["title"] = video_data.get("title", {}).get("runs", [[{}]])[0].get("text", None)
                res["long_desc"] = video_data.get("descriptionSnippet", {}).get("runs", [{}])[0].get("text", None)
                res["channel"] = video_data.get("longBylineText", {}).get("runs", [[{}]])[0].get("text", None)
                res["duration"] = video_data.get("lengthText", {}).get("simpleText", 0)
                res["views"] = video_data.get("viewCountText", {}).get("simpleText", 0) 
                res["url_suffix"] = video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
                results.append(res)
        return results

    def to_dict(self):
        return self.videos

    def to_json(self):
        return json.dumps({"videos": self.videos})

   
# ===========================================================================

def time_in_minutes( time ):
   # https://stackoverflow.com/questions/10663720
   return sum( x * int(t) for x, t in zip([60, 1], time.split(":")))

def time_as_time( n ):
   return "%d:%02d" % ( n // 60, n % 60 )
   
def write_to_file( file, text ):
   f = open( file, "w" )
   f.write( text )
   f.close
   
def force_ascii( s ):
   r = ""
   for c in s:
      if ord(c) < 128: r += c
   return r   

# ===========================================================================

nn = 0

def youtube_find( s ):
   """
   use YoutubeSearch to find the recording of a talk.
   Using exponentially increasing pauses seems to be needed.
   """
   global nn
   n = 1
   sleep = 1
   while n <= 2:
      time.sleep( sleep )
      raw = YoutubeSearch( s, max_results = 2 )
      results = raw.to_dict()
      nn += 1
      write_to_file( str( nn ) + ".txt", s + "\n\n" + raw.response )
      if len( results ) > 0: return results
      print( 
         "youtube search attempt failed attempt=%d delay=%d search=[ %s ]" 
         % ( n, sleep, s ))
      n += 1
      sleep *= 2
   return results


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
         search = title + " " + conference + " " + year + " " + " ".join( speakers )
         match = youtube_find( search )
         if len( match ) > 0:
            match = match[ 0 ]
            self.duration = time_in_minutes( match[ "duration" ] )
            self.video = "https://youtube.com" + match[ "url_suffix" ]
         else:
            print( "definitely not found [%s]" % search )
      
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
   file_name = "cppcon/" + year + ".txt"
   for line in open( file_name, "r", encoding='utf-8', errors='replace' ).readlines():
      nr = nr + 1
      line = make_ascii( line )
      if progress:
         sys.stdout.write( "\rCppCon %s line %d     " % ( year, nr ))
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

   
# ===========================================================================

def process( processor, conference, year ):
   if year == "*":
      files = []
      for file in glob.glob( conference + "/20*.txt" ):
         files.append( file )
      talks = processor( year, progress = progress, google = google )
      file = conference + "/index.html"
   else:
      talks = processor( year, progress = progress, google = google )
      file = conference + "/" + year + ".html"     
   write_talks( file, talks )   

if __name__ == "__main__":
   progress = True
   google = True
   if len( sys.argv ) < 3:
      print( "usage: build <conference> <edition>" )
      exit( -1 )
      
   if sys.argv[ 1 ] == "cppcon":
      process( cppcon, sys.argv[ 1 ], sys.argv[ 2 ] )

   else:
      print( "unknown conference '%s'", sys.argv[ 1 ] )
      
