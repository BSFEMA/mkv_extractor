# mkv_extractor
Python mkv extractor for mkvextract (MKVToolNix) for Linux

Purpose:  I couldn't find a good mkvextract frontend for Linux, so I decided to make my own and used this as an oppertunity to learn python subprocess and json.  This currently exports all tracks (audio, video, subtitles) as well as chapters and attachments.  I have never used mkv [tags, CUE sheets, timestamps, cues], so I'm not going to bother with them here.

Application:  mkv_extractor

Author:  BSFEMA

Started:  2008-10-18

Prerequisites:  You need to have MKVToolNix installed:  https://mkvtoolnix.download/downloads.html  Try running "mkvmerge --version" in terminal.  If that works, then you are good to go, otherwise install MKVToolNix

Command Line Parameters:  There is just 1:  It is the folder path that will be used to start looking at the *.mkv files from.  If this value isn't provided, then the starting path will be where this application file is located.  The intention is that you can call this application from a context menu from a file browser (e.g. Nemo) and it would automatically load up that folder.

Resources:  https://mkvtoolnix.download/doc/mkvextract.html
