# Arch Linux Mirror Score Viewer

This is a Python app I developed for my CS 399 course. It gets information
about the various mirror servers for Arch Linux (found 
[here](https://archlinux.org/mirrors/status/)). This app specifically uses
the JSON data returned by the website from this URL:
https://archlinux.org/mirrors/status/json/

The website has 3 pages.
The Mirror Comparer page allows a user to compare
numerical statistics for various mirrors.
All Mirrors has a sortable table of all mirrors with a nonzero score - this is
my rough check for a mirror that is actually working. Users can select which
pieces of information they wish to see.
Finally, the Mirror Inspector provides a way to view all data for a specific
mirror.
