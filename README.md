romfilter
==============
A simple Python 3.8 application for filtering roms.

General Usage
-------------

Tkinter GUI Python 3.8 scripts. Used to filter out files by file extension and tags denoted by "()" and "[]". 
A more comprehensive list of tags and their meaning can be found on https://www.emuparadise.me/help/romnames.php .

Has the option to remove duplicates by name devoid of tags and file extensions, 
therefor it cannot see the difference between 'game (x)[y].exe' and 'game [z][a].txt'. This is intended behaviour to filter same name roms with different versions. It is recommended to only remove duplicates when the folder contains a single file extension.

The default behaviour is to only keep files where all selected tags match every tag the file contains. 
Ticking 'Match Single Tag' will override this behaviour and keep a file if even a single tag matches.

Binary File
------

A binary file containing this projects scripts has been made using pyinstaller. https://www.pyinstaller.org/
