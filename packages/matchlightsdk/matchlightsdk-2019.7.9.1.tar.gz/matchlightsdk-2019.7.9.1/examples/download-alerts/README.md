Matchlight Alert Downloading and Storage
========================================

This folder contains an example project demonstrating how the Matchlight Python SDK can be used to create a local cache of Matchlight Alerts. Creating a local data store of alerts may be useful for customers who are building an integration with the Matchlight platform. In many cases application performance can be improved by fetching new alerts just once time and storing a local copy for future access.

These example scripts outline the recommended best practices for the Matchlight Python SDK in this use case. The scripts are fully functional as-written but are intended to be modified by the 3rd party developer to meet their specific needs. Specifically, this scripts will require a Matchlight project with alerts in order to demonstrate their full functionality.

There are two scripts in this project:

1. `download-alerts-with-pagination.py` - This script downloads new alerts starting with the newest alert and working back until all alerts have been stored in an in-memory SQLite database.

2. `download-alerts-and-mark-seen.py` - This script downloads new alerts and changes their `seen` value from `False` to `True` starting with the newest alert and working back until all alerts have been stored in an in-memory SQLite database.
