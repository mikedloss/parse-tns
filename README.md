# parse-tns
A small script used to parse a tnsnames.ora file in Python 2.7. It's purpose is to 'clean up' any python scripts that use the cx_Oracle library to be able to just connect to a database. Python 3 will be coming Soon™.

## How-to

This little script reads in either a file ('tnsnames.ora') or a stringified version of 'tnsnames.ora' and will return a dictionary of all databases and their respective connection strings.

Since I don't have a setup.py file, just throw this into %python%\Lib\site-packages\ .

> import parse-tns

or

> from parse-tns import parse_tns

parse_tns is the main function here, reading in 2 optional variables:
* **var** = used for the file 'tnsnames.ora' object or stringified version of 'tnsnames.ora'. If nothing is passed in for **var**, then it will default to looking at your 'TNS_ADMIN' system variable and try to find 'tnsnames.ora' through there. If var is default, errors will be thrown if either your 'TNS_ADMIN' system variable or 'tnsnames.ora' file cann't be found
* **specific** = used after parsing your tnsnames.ora file. If you want a smaller dictionary returned that has a specific list of entries that you already know exist, then use this. Input string should be delimited with commas. All commas and spaces are removed, and the script uses something like the SQL 'like' statement to find keys. Something similar to this:

> SELECT * FROM TABLE WHERE COL1 LIKE '%SPECIFIC%';

**DISCLAIMER**: This script reads the tnsnames.ora file and expects each entry to be shown as "DATABASE.SOMETHING" (like DB.WORLD). It does handle entries like DB.WORLD,DB , though, but who does that??
