# Guestbook

Guestbook is an Apache access log anaylzer. It can retrieve information about a site's most popular visitors by IP address, their page breakdown, as well as geolocation data about that IP address. 

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