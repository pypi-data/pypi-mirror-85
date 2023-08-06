Matchlight Offline Document Fingerprinting
==========================================

This folder contains an example project demonstrating how the Matchlight Python SDK can be used to separately fingerprint and then upload Matchlight Document record types. For example, if for security reasons the documents you are uploading are stored on a machine without external Internet access you could use this pattern to first fingerprint the files on the restricted machined, transfer the files to an Internet enabled machine, and then upload the fingerprints.

These example scripts outline the recommended best practices for the Matchlight Python SDK in this use case. The scripts are fully functional as-written but are intended to be modified by the 3rd party developer to meet their specific needs.

There are 3 scripts in this project:

1. `format-input-data.py` (offline) - This script is a convenience script that takes semi-formatted data of unrestricted document length and generates a new set of formatted data of no more than 840 characters per record. If your data can easily be directly formatted and you do not wish to do so programatically you can skip this step.

2. `fingerprint-documents.py` (offline) - This script take a CSV of formatted data and generates Matchlight document fingerprints and metadata saved as a CSV.

3. `upload-fingerprints.py` (online) - This script takes the fingerprints produced by `fingerprint-documents.py` and uploads them to Matchlight.