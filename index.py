# ===========================================================================
#
# File      : index.py
# Part of   : the Free C++ Talks List (FCTL)
# Copyright : wouter van ooijen 2020
# home      : https://www.github.com/wovo/fctl
#
# Update the comprehensive all.talks file
#
# This code is distributed under the Boost Software License, Version 1.0.
# (See accompanying BOOST-license.txt file or copy at 
# http://www.boost.org/LICENSE_1_0.txt)
#
# ===========================================================================

import talks

file = open( "index.html", "w" )
for talk in talks.talks( "all.talks" ).list:
   file.write( "<img src='%s' height=100><BR>\n" % ( talk.thumbnail ))
   file.write( "%s<BR>\n" % ( talk.identifier ))
   file.write( "<A HREF='%s'>%s</A><BR>\n" % ( talk.video, talk.title ))
   file.write( "%s<BR>\n" % ( ", ".join( talk.speakers )))
   file.write( "<BR>\n" )
file.close()