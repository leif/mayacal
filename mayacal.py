#!/usr/bin/env python

"""
This program converts Maya Long Count strings to and from Unix epoch seconds.

Example usage:

$ ./mayacal.py 0.0.0.0.0 # Mayan epoch in Unix time
-160384752000

$ ./mayacal.py -160384752000 # Mayan epoch, including Tzolk'in & Haab' dates
4 Ajaw 8 Kumk'u 0.0.0.0.0

$ ./mayacal.py 0 # Unix epoch as Maya Long Count date
13 Chikchan 3 K'ank'in 12.17.16.7.5

$ ./mayacal.py `date +%s -d 'Dec 20 2012 UTC'` # Last day of B'ak'tun 12
3 Kawak 2 K'ank'in 12.19.19.17.19

$ ./mayacal.py `date +%s -d 'Dec 21 2012 UTC'` # Happy New B'ak'tun!
4 Ajaw 3 K'ank'in 13.0.0.0.0

Disclaimer: Everything I know about Mayan calendars I learned from
Wikipedia while writing this. I recommend doing your own research before
relying on this software for your end-of-the-b'ak'tun planning.
Also, it does not account for leap seconds.
"""

__author__    = "Leif Ryge <leif@synthesize.us>"
__copyright__ = "4 Muluk 17 K'ank'in 12.19.19.0.9"
__license__   = "WTFPL"


DAY_NAMES = [ "Imix'", "Ik'", "Ak'b'al", "K'an", "Chikchan", "Kimi", "Manik'",
    "Lamat", "Muluk", "Ok", "Chuwen", "Eb'", "B'en", "Ix", "Men", "K'ib'",
    "Kab'an", "Etz'nab'", "Kawak", "Ajaw" ]

MONTH_NAMES = [ "Pop", "Wo'", "Sip", "Sotz'", "Sek", "Xul", "Yaxk'in'", "Mol",
    "Ch'en", "Yax", "Sak'", "Keh", "Mak", "K'ank'in", "Muwan'", "Pax",
    "K'ayab", "Kumk'u", "Wayeb'" ]

# Unix epoch (Jan 1 1970 CE) in Gregorian Serial Days (days since Jan 1, 1 CE)
UNIX_EPOCH_GSD = 719163

# Mayan Long Count epoch (Aug 11, 3114 BCE) in GSD
# (according to the "Goodman, Martinez, Thompson" correlation)
MAYA_EPOCH_GSD = -1137142

# Unix epoch in days since mayan epoch
UNIX_EPOCH_MSD = UNIX_EPOCH_GSD - MAYA_EPOCH_GSD

def unixSecondsToTzolkinDay( seconds ):
    day = UNIX_EPOCH_MSD + int( seconds / (24*60*60) )
    day += 3 # the world began on 4 Ajaw
    return "%s %s" % ( (day % 13) + 1, DAY_NAMES[ (day + 16) % 20 ] )

def unixSecondsToHaabDay( seconds ):
    day  = UNIX_EPOCH_MSD + int( seconds / (24*60*60) )
    day  += 348 # The world began on 8 Kumk'u, the 348th day of the year
    day  %= 365
    month = day / 20
    day  %= 20
    return "%s %s" % ( day, MONTH_NAMES[ month ] )

def unixSecondsToLongCount( seconds ):
    days   = UNIX_EPOCH_MSD + int( seconds / (24*60*60) )
    baktun = days / 144000
    days  %= 144000
    katun  = days / 7200
    days  %= 7200
    tun    = days / 360
    days  %= 360
    winal  = days / 20
    days  %= 20
    kin    = days
    return ".".join(map(str, [baktun, katun, tun, winal, kin]))

def longCountToUnixSeconds( longCount ):
    baktun, katun, tun, winal, kin = map(int,
            longCount.split(' ')[-1].split('.'))
    days = baktun*144000 + katun*7200 + tun*360 + winal*20 + kin
    return (days - UNIX_EPOCH_MSD) * (24*60*60)

def unixSecondsToFullLongCount( seconds ):
    return "%s %s %s" % (
            unixSecondsToTzolkinDay(seconds),
            unixSecondsToHaabDay(seconds),
            unixSecondsToLongCount(seconds))

if __name__ == "__main__":
    from sys import argv, exit
    if len(argv) != 2:
        exit( "usage: %s [unix-seconds|mayan-long-count]" % argv[0] )
    else:
        try:
            seconds = int( argv[1] )
        except ValueError:
            print longCountToUnixSeconds( argv[1] )
        else:
            print unixSecondsToFullLongCount( seconds )

