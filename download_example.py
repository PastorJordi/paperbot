#!/usr/bin/env python
# coding: utf-8

# In[1]:


# test with my own

# url = 
# source can be found in the iframe: <iframe src="https://zero.sci-hub.se/2531/adca58daebf712bd194f67367fc5b828/pastor-ciurana2014.pdf#view=FitH" id="pdf"></iframe>

import os
import requests
from bs4 import BeautifulSoup

# DOI = '10.1016/j.bbr.2014.02.028'
baseurl = 'https://www.sci-hub.se/'

def download_by_doi(DOI):
    """grabs a pdf from scihubs iframe,
    wont work if a captcha pops up
    
    if it works, return True, +localpath, else returns False, and exception"""
    # Requests URL and get response object
    response = requests.get(baseurl+DOI)
    
    # Parse text obtained
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        pdfurl = soup.find('iframe')['src'].split('#view')[0]


        fname = pdfurl.split('/')[-1]
        abpth = os.path.abspath(f'./downloads/{fname}')
        with open(abpth, 'wb') as f:
            f.write(requests.get(pdfurl).content)

        return True, abpth
    except Exception as e:
        return False, str(repr(e))


