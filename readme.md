PCTL : the Public C++ Talks List 

license: Boost

wouter van ooijen

(2021-09-23) work in progress, come back later!

This is a list of C++ related talks that are publicly available on youtube.

I created the list by semi-automated processing of the
published schedules of conferences that I deemed interesting,
and searching for the combination of conference, title and speakers on youtube.
This mostly seems to work, but there are bound to be errors.
In the process, I converted all text to ascii (sorry speakers...).
The trags are still rudimentary.

I don't pretend to be a front-end developer, so 
beside the very spartan web page the list
is available in Json format, with a Python interface for
maybe slightly easier use.
If you create you own interface, let me know!

Tho build the list, I downloaded a text copy (web cut-n-paste)
of the as-held schedules of the conferences I deemed interesting,
in a subdirectory (in input) for each conference, 
in a text file <edition>.txt
In most cases the edition is the year, but there are exceptions
like accu which has a 2019-autumn conference.
In each schedule file, I added some meta information ($add ...) lines,
and talk identifier lines (starting with a #). 
The latter must never be changed,
but can be removed, or new ones can be added later, provided that
they remain in alphabetical order.
The renumber command makes this somewhat easier, but
don't forget to put a #locked line in the file once it has
its identifiers.

Often some hand processing is needed, like replacing special chars,
swapping first name and surname, combining multiple speakers (separated by @),
and elimination lignting talks (which don't have a distinct name)
and talks that can't be found on youtube.

Start: https://isocpp.org/wiki/faq/conferences-worldwide

todo:
- cppcon 2014 closing - no more description :( should be? Jon Kalb "Exception-Safe Code, Part III"
code-dive 2017 nog geen markers!

was cppcon 2020 live?? others too

done: cppcon, accu, c++-on-sea, code-dive
working on: 
backburner: c++now 15/16/17 - has no speakers?? 18/19 does have 'm

https://archive.fosdem.org/2020/schedule/xml
https://conference.accu.org/previous/2019_autumn/sessions/ - has no video links
https://cppcon.org/cppcon-2019-program/ - difficult to parse?
   
tags (0 or more)
   C++
   naming
   templates
   panel
   talk
   lightning
   keynote   

ToDo
   - more conferences
   - check correctness
   - number when no numbers yet #00001
   - meetingcpp 2015 different format, earlier not found
   - also non-conferences??
   - additional information, like sheets?
   - tags: C++
   - tags: live, ...                                     s
   - tags: conference, meetup, podcast
   - tags: talk, discussion, interview
  
Interesting caveats found:
   - on some conferences, some but not all talks are C++-related (accu, fosdem)
   - not all conferences have all schedules available
   - c++now schedule up to 2017 doesn't mention the speakers
   - meeting-c++ 2016 had a different schedule formatting
   - older schedules often not available, but sometimes a youtube playlist is!                      
   