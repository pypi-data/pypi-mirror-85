TV Series Renamer
=================

Simple script in python3 that download and organize subtitles from
`OpenSubtitles <http://www.opensubtitles.org>`__. The purpose of the
program is to make easier for user to get every subtitle associated with
its related video.

How does it work
----------------

This program works in ~/Downloads (default) or in a directory passed as
argument.

1. It takes every *subdirectory*, *video*, *archive* and *subtitle* file
   in folder that looks like it’s a tv-series related file.
2. After that it move archives in the corrisponding folder or extracts
   their contents if the video file is in the same directory of the
   archive.
3. If a video file and a subtitle file are related (same tv-shows name
   and same season and episode) the program renames the subtitle the
   same as the video.

Configure OpenSubtitle account
------------------------------

Configure **opensubtitles.json** file as show in
**opensubtitles.json.example** and put it into
**~/.opensubtitles_downloader**. If you want to use it anonymously don’t
insert any username, otherwise use your account on
`OpenSubtitles <http://www.opensubtitles.org>`__.

– opensubtitles.json.example –

.. code:: json

   {
       "username": "username",
       "password": "password",
       "language": "eng",
       "useragent": "mistalbo"
   }

Install package from pip
------------------------

.. code:: bash

   pip install --user opensubtitles-downloader

How to use it
-------------

Launch it with ~/Downloads directory as target:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   $ opensubtitles_downloader

Launch it with user input directory as target:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   $ opensubtitles_downloader -d <directory>

Launch it with user input file as target:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   $ opensubtitles_downloader -f <filename>

Launch it with clean option:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   $ opensubtitles_downloader -c

When this option is activated, the script looks for all subtitles for
which there is no video file related and for all empty directories, then
it put them in trash. Using the clean option doesn’t prevent the program
from downloading subtitles, it’s intended as an extra action and not as
an alternative to regular actions.

Contribute
----------

Read **CONTRIBUTING.md**.
