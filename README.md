# Arch Linux Mirror Server Viewer

This is a Python app I developed for my CS 399 course. It gets information
about the various mirror servers for Arch Linux (found 
[here](https://archlinux.org/mirrors/status/)). This app specifically uses
the JSON data returned by the website from this URL:
https://archlinux.org/mirrors/status/json/

The app is built using [Streamlit](https://streamlit.io/) and is hosted at
https://archlinux-mirror-viewer.streamlit.app/ using the Streamlit community
cloud.

The website has 3 pages.
- The Mirror Comparer page allows a user to compare numerical statistics for 
  various mirrors.
- All Mirrors has a sortable table of all mirrors with a nonzero score. Users
  can select which pieces of information they wish to see. (Nonzero score is
  the app's way of confirming that a mirror server is actually working).
- Finally, the Mirror Inspector provides a way to view all data for a specific
  mirror.

This repository also includes various tests (using `pytest`). These tests
check the operation of the data collection functions used by the app.
