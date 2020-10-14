FCTL : the Free C++ Talks List 

(2020-10-14) work in progress, come back later!

Start: https://isocpp.org/wiki/faq/conferences-worldwide

license: 
   - MIT for search.py
   - Boost for the other Python files
   - as for the data: I am not sure

This is my attempt to create a list of free (english language) 
conference talks that are publicly available on youtube.
I hope this helps to access this great source of information
and education.
I can't pretend to be a great front-end developer,n so 
beside the simple web interface the list
is (also) available in python for anyone to use.

Tho build this list, I downloaded a text copy (web cut-n-paste)
of the as-held schedules of the conferences I deemed interesting,
in a subdirectory for each conference, in a text file <edition>.txt
In most cases the edition is the year, but there are exceptions
like accu which has a 2019-autumn conference.
In each schedulke file, I added identifier lines (starting with a #)
that uniquely identify each talk. These must never be changed,
but can be removed, or new ones can be added later, provided that
they remain in alphabetical order.

Next I wrote a Python function for each conference that extracts
the talks. 


ToDo
   - more conferences
   - check correctness
   - find way to ID individual talks - year + sequence#?
   - sanitize the list of speakers (spelling errors)
   - number when no numbers yet #00001
   - meetingcpp 2015 different format, earlier not found
   - also non-conferences??
   - additional information, like sheets?
   
Process
   - command summary: build.py test|process|talks conference edition|*
   - find and download the schedule of each edition
   - write or check the processor (test command)
   - edit the schedule with ##edition and #0001 identifiers
   - process the schedule to create the .talks file(s) (process command)
   - create the all-in-one *.talks file and the index.html interface
  
Interesting caveats found:
   - some conferences are held more than once a year (accu, corehard)
   - on some conferences, some but not all talks are C++-related (fosdem)
   - not all texts (authors names, and even titles) are in ASCII
   - the python YoutubeSearch has a bug that pops up (only) occasionally
   - not all conferences have all schedules available
   - to add tags later, each talk must have a identifier that never changes
   