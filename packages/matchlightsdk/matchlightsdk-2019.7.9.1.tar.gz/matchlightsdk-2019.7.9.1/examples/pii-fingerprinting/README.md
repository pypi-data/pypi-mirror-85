Matchlight PII Fingerprinting
=============================

This folder contains an example project demonstrating how the Matchlight Python SDK can be used to fingerprint and upload Matchlight Personally Identifiable Information (PII) record types. Using the Matchlight SDK to create an application integration for PII fingerprinting may be useful for customers who are want to keep their Matchlight data in sync with dynamic datasets that are frequently updated.

These example scripts outline the recommended best practices for the Matchlight Python SDK in this use case. The scripts are fully functional as-written but are intended to be modified by the 3rd party developer to meet their specific needs.

There is one script in this project:

1. `fingerprint-pii.py` - This script uploads 3 PII records to a Matchlight PII project and saves a local copy of the plaintext PII data with a `user_record_id` index value that can be used to connect Matchlight alerts to the source data.