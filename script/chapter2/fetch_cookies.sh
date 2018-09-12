#!/bin/bash

#http://slacy.com/blog/2010/02/using-cookies-sqlite-in-wget-or-curl/

function cleanup {
rm -f $TMPFILE
exit 1
}

trap cleanup  SIGHUP SIGINT SIGTERM

# This is the format of the sqlite database:
# CREATE TABLE moz_cookies (id INTEGER PRIMARY KEY, name TEXT, value TEXT, host TEXT, path TEXT,expiry INTEGER, lastAccessed INTEGER, isSecure INTEGER, isHttpOnly INTEGER);

# We have to copy cookies.sqlite, because FireFox has a lock on it 
TMPFILE=`mktemp /tmp/cookies.sqlite.XXXXXXXXXX`
cat $1 >> $TMPFILE
sqlite3 -separator '	' $TMPFILE << EOF
.mode tabs
.header off
select host,
case substr(host,1,1)='.' when 0 then 'FALSE' else 'TRUE' end,
path,
case isSecure when 0 then 'FALSE' else 'TRUE' end,
expiry,
name,
value
from moz_cookies;
EOF
cleanup
