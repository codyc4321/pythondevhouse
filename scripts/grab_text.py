#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
from my_scripting_library import write_content, append_content, read_content

AD_REPO = '/home/cchilders/devhouse_ad.txt'

# myrequest = requests.get('http://pythondevhouse.com')

content = read_content('/home/cchilders/projects/pythondevhouse/app/templates/index.html')

soup = BeautifulSoup(content)

p_tags = soup.find_all('p')

"""
http://makble.com/parsing-and-traversing-dom-tree-with-beautifulsoup
"""

write_content(AD_REPO, '')

for tag in p_tags:
    append_content(AD_REPO, tag.text.strip())
    append_content(AD_REPO, '\n\n')
    
headers = soup.find_all('h2')

append_content(AD_REPO, '\n\nheaders: \n')

for header in headers:
    append_content(AD_REPO, header.text)
    append_content(AD_REPO, '\n\n')