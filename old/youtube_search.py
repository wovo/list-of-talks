# ===========================================================================
#
# File      : youtube_search.py
# Part of   : the Free C++ Talks List (FCTL)
# Copyright : joe tats 2019, wouter van ooijen 2020
# home      : https://www.github.com/wovo/fctl
#
# from https://github.com/joetats/youtube_search,
# modified to avoid occasional problems
#
# license: MIT (see accompanying MIT-license.txt file)
#
# ===========================================================================

import requests
import urllib.parse, json

nn = 0

def force_ascii( s ):
   r = ""
   for c in s:
      if ord(c) < 128: r += c
   return r   

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
        # self.response = force_ascii( self.response )
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

        if 0: # debugging
           global nn
           nn += 1
           open( str( nn ) + "-log.txt", "w" ).write( force_ascii( json_str ))

        # this and next part modified
        videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
            "sectionListRenderer"]["contents"]
        # [0]["itemSectionRenderer"]["contents"]
        
        for content in videos:
          if "itemSectionRenderer" in content:
           for video in content["itemSectionRenderer"]["contents"]:
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
