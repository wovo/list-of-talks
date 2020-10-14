# ===========================================================================
#
# File      : renumber.py
# Part of   : the Free C++ Talks List (FCTL)
# Copyright : wouter van ooijen 2020
# home      : https://www.github.com/wovo/fctl
#
# This script renumbers the #....DDDD lines in a file.
# Use this only once, before the file enters the list!
#
# This code is distributed under the Boost Software License, Version 1.0.
# (See accompanying BOOST-license.txt file or copy at 
# http://www.boost.org/LICENSE_1_0.txt)
#
# ===========================================================================

import sys

def renumber( file_name ):
   result = []
   
   file = open( file_name, "r", encoding='utf-8', errors='replace' )
   nr = 0
   for line in file.readlines():
      if line.startswith( "#" ):
         line = line[ : -1 ]
         nr += 1
         while line[ -1 ] in "01234567890":
            line = line[ : -1 ]
         line += "%04d\n" % nr
      result.append( line )
   file.close()
   
   file = open( file_name + "x", "w", encoding='utf-8', errors='replace' )
   for line in result:
      file.write( line )
   file.close()   
      
if __name__ == "__main__":
   renumber( sys.argv[ 1 ] )
   