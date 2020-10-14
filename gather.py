# ===========================================================================
#
# File      : gather.py
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

import glob
import talks

all = talks.talks()
n = 0
for file_name in glob.glob( "*/*.talks" ):
   print( file_name )
   n += 1
   for t in talks.talks( file_name ).list:
      all.add( t )
print( "%d file(s) gathered" % n )
all.write( "all.talks"       )