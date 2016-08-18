# Guestbook

Guestbook is an Apache access log anaylzer. It can retrieve information about a site's most popular visitors by IP address, their page breakdown, as well as geolocation data about that IP address. 

### Usage
~~~~
guestbook.py [-h] [-agents AGENTS] [-times TIMES] [-cutoff CUTOFF]
                [-target TARGET] [-popular] [-track] [-breakdown]
                filePath

positional arguments:
  filePath        Filepath for access log

optional arguments:
  -h, --help      show this help message and exit
  -agents AGENTS  Show user agents for a given ip
  -times TIMES    Show page visits with timestamps for a particular IP address
  -cutoff CUTOFF  Minimum view count cutoff when showing results
  -target TARGET  Only show results for specified IP address
  -popular        Show IP addresses of most popular visits
  -track          Enable tracking IP geolocation. Results will be shown with
                  tracking data.
  -breakdown      Show page visit breakdown for each IP address

~~~~

### Usage Examples
~~~~ 
python guestbook.py access_logs.txt -popular 
~~~~
Show the most popular visitors by IP address.

~~~~ 
python guestbook.py access_logs.txt -popular -track
~~~~
Show the most popular visitors by IP address, and find Geolocation data for each IP address.


~~~~ 
python guestbook.py access_logs.txt -popular -track -cutoff=10
~~~~
Show the most popular visitors by IP address with viewcount equal to or greater than the cutoff, and find Geolocation data for each IP address. 

~~~~ 
python guestbook.py access_logs.txt -breakdown
~~~~
Shows the URL access breakdown for every visitor, as listed in the access log.

~~~~ 
python guestbook.py access_logs.txt -breakdown -target=a.b.c.d
~~~~
Shows the URL access breakdown for the target IP, as listed in the access log.

### Status
Beta - it works, but this isn't as polished up as it should be. 

### Authors
[Brian Lam] - Developer

### Tech

Guestbook runs on Python 2.7. It uses the freegeoip.net API to retrieve geolocation data. 

### Development

Feel free to contact me if you'd like to help develop this. 

### Todos

 - How do we analyze access logs that aren't in default format
 - Add argument parser
 - We should probably use a GET request library
 - I'm sure I'm missing some error handling, particularly with string encoding
 - Breakdown by day


License
----
MIT License

[Brian Lam]: <http://brianlam.me>