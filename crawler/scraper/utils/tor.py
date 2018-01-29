'''
Python script to connect to Tor via Stem and Privoxy, requesting a new connection (hence a new IP as well) as desired.
'''
import time
import urllib.request
import requests

from stem import Signal
from stem.control import Controller 

# initialize some HTTP headers for later usage in URL requests
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent}
ipify = 'https://api.ipify.org?format=text'

# initialize some holding variables
oldIP = "0.0.0.0"
newIP = "0.0.0.0"

# seconds between IP address checks
secondsBetweenChecks = 2

# request a URL 
def request(url):
    # communicate with TOR via a local proxy (privoxy)
    def _set_urlproxy():
        proxy_support = urllib.request.ProxyHandler({'http' : 'http://127.0.0.1:8118'})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
    _set_urlproxy()
    request = urllib.request.Request(url, None, headers)
    return urllib.request.urlopen(request).read()

def rx_tx_bytes(): 
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password = 'mypassword')
        bytes_read = controller.get_info("traffic/read")
        bytes_written = controller.get_info("traffic/written")
        print("My Tor relay has read %s bytes and written %s." % (bytes_read, bytes_written))

# signal TOR for a new connection
def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password = 'mypassword')
        controller.signal(Signal.NEWNYM)

def new_connection(): 
    with Controller.from_port(port = 9051) as controller:
      controller.authenticate(password = 'mypassword')
      controller.signal(Signal.NEWNYM)
      import ipdb; ipdb.set_trace()
      pass

def change_ip(): 
    # if it's the first pass
    global newIP
    global oldIP
    if newIP == "0.0.0.0":
        # renew the TOR connection
        renew_connection()
        # obtain the "new" IP address
        newIP = request(ipify).decode('utf-8')
    # otherwise
    else:
        oldIP = newIP
        # refresh the TOR connection
        renew_connection()
        # obtain the "new" IP address
        newIP = request(ipify).decode('utf-8')

    # zero the 
    # elapsed seconds    
    seconds = 0
    # loop until the "new" IP address
    # is different than the "old" IP address,
    # as it may take the TOR network some
    # time to effect a different IP address
    while oldIP == newIP:
        # sleep this thread
        # for the specified duration
        time.sleep(secondsBetweenChecks)
        # track the elapsed seconds
        seconds += secondsBetweenChecks
        # obtain the current IP address
        newIP = request(ipify).decode('utf-8')
        # signal that the program is still awaiting a different IP address
        print ("%d seconds elapsed awaiting a different IP address." % seconds)
    print ("newIP: %s" % newIP)
