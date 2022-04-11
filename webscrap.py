#! /usr/bin/python3

'''
This script will scrape the following web pages to get the current user count on the
webvpn appliance.

http://$HOSTNAME/dana-na/healthcheck/healthcheck.cgi?status=all

This page has output that looks like:

Health check details:
CPU-UTILIZATION=2;
SWAP-UTILIZATION=0;
DISK-UTILIZATION=18;
SSL-CONNECTION-COUNT=742;
USER-COUNT=718;
MAX-LICENSED-USERS-REACHED=NO;
VPN-TUNNEL-COUNT=710;

The xml of the out looks like:
<?xml version="1.0" encoding="utf-8"><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML Basic 1.0//EN""http://www.w3.org/TR/xhtml-basic/xhtml-
basic10.dtd"><html xmlns="http://www.w3.org/1999/xhtml" lang="en-US"><head><title>HealthCheck</title></head><body><h1>Health check d
etails:</h1>CPU-UTILIZATION=2;
<br>SWAP-UTILIZATION=0;
<br>DISK-UTILIZATION=18;
<br>SSL-CONNECTION-COUNT=723;
<br>USER-COUNT=697;
<br>MAX-LICENSED-USERS-REACHED=NO;
<br>VPN-TUNNEL-COUNT=686;
<br></body></html>

We are solely interested in the USER-COUNT info.

We will be logging this to syslog on the system this runs on in order to get it into
Splunk logs so that we can create a visualation on a dashboard.

'''

import requests
import syslog
import sys
from bs4 import BeautifulSoup as bs
from datetime import datetime

# need to create a date stamp to append to the output file name
# define a timestamp format you like
FORMAT = '%Y-%m-%d-%H-%M-%S'

date_time_stamp = datetime.now().strftime(FORMAT)

response = requests.get("http://150.125.56.5/dana-na/healthcheck/healthcheck.cgi?status=all").text

soup = bs(response, 'html.parser')
###print(soup)

body = (soup.find('body').text)

output_list = body.split(';')

###print(output_list[4])

(_, count) = output_list[4].split('=')

syslog_message = "webvpn user count data - " + date_time_stamp + "  ###  " + count + "\n"

###print(syslog_message)

syslog.openlog(sys.argv[0])
syslog.syslog(syslog.LOG_WARNING, syslog_message)

syslog.closelog()
