# Scripts for Security
This is a collection of different scripts used for security purposes.

#### File Integrity Checker
Name: file_intregity_checker.py <br>
Description: Checks a directory for any changes, including modified or deleted files by storing a list of files and their hashes. <br>
Usage: Create a baseline with the following command: <br>
> python3 file_integrity_checker.py create path/to/directory

Then to verify a directory with its baseline measures, simply change from 'create' to 'verify'

> python3 file_integrity_checker.py verify path/to/directory

#### Connection Tracker
Name: connection_tracker.py <br>
Description: Checks all active IPv4 and IPv6 connections on device.
Usage: You can choose to display connections in the terminal or save to a JSON file.

>python3 connection_tracker.py view

>python3 connection_tracker.py save