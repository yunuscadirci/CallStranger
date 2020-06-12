from setuptools import setup
from os import path

current_directory = path.abspath(path.dirname(__file__))
with open(path.join(current_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='CallStranger',
    version='1.0.3',
    packages=['upnpy', 'upnpy.soap', 'upnpy.ssdp', 'upnpy.upnp'],
    keywords=['upnp', 'upnpy'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    url='https://www.callstranger.com',
    license='MIT',
    author='Yunus Çadırcı',
    author_email='yunuscadirci@yunuscadirci.com',
    description='This script created by Yunus Çadırcı (https://twitter.com/yunuscadirci) to checkagainst CallStranger (CVE-2020-12695) vulnerability. An attacker can use this vulnerability for:\n* Bypassing DLP for exfiltrating data\n* Using millions of Internet-facing UPnP device as source of amplified reflected TCP DDoS / SYN Flood\n* Scanning internal ports from Internet facing UPnP device\nYou can find detailed information on https://www.callstranger.com\n https://github.com/5kyc0d3r/upnpy used for base UPnP communication',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
