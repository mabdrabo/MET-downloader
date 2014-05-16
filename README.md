MET-downloader
==============

a simple web crawler to automatically download all missing files and organizes them by "File type" according to MET website


Requirements:
=============
1. Firefox
2. Selenium: run-- $ pip install -U selenium (linux/mac might need 'sudo')

Steps:
======
1. open the file, and edit the part that says "EDIT"
2. open a terminal, enter-- $ python path/to/file (or just drag and drop the file to the terminal after writing python)
3. that's it, a small report will be printed at the end stating how many files were downloaded and where

Issues:
=======
1. [SOLVED] Since the max. allowed downloads at any given time is 10 files, if there are more than 10 that need to be downloaded only the first 10 will be downloaded then an exception will be thrown, then the script could be run again to download the rest (don't worry no duplicates)
2. [SOLVED] Courses that have their files password-protected, requires the student to be logged in, thus can not be downloaded for now
3. [In Progress] When logging-in is disabled, an exception is thrown when trying to download a password protected file
