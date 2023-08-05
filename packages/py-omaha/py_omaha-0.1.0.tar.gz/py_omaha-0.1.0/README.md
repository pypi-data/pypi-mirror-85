# Python library for using the API of the TP-Link Omaha Wi-Fi Access Point Management system

This is a simple wrapper around Requests to log in to the Omaha HTTP API and then retrieve
device lists and manipulate devices. It was written for a simple Home Assistent integration but
can be used outside of it.

Patches welcome.


## Unit tests

For the unit tests to run the file tests/config_sample.py has to be copied to tests/config.py and the variables there set to an Omaha instance that is reachable.