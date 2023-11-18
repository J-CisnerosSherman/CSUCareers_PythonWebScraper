import requests
import json
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
import re
import Extract_Position_Details



def remove_br_tags(element):
    
    br_tags = element.find_all('br')
    for br_tag in br_tags:
        br_tag.replace_with('\n')
    
    sup_tags = element.find_all('sup') 
    for sup_tag in sup_tags:
        sup_tag.decompose()

    return element



def remove_rare_chars(element):   # Find and replace &nbsp; within HTML tags
    
    for tag in element.find_all():
        
        if tag.string is not None and '\u25cf' in tag.string:
            tag_text = tag.text.strip()
            cleaned_text = tag_text.replace('\u25cf', '')
            tag.string.replace_with(cleaned_text)


        if tag.string is not None and '\xa0' in tag.string: 
            tag_text = tag.text.strip()
            cleaned_text = tag_text.replace('\xa0', ' ')
            tag.string.replace_with(cleaned_text)
        

        if tag.string is not None and '\u2010' in tag.string: 
            tag_text = tag.text.strip()
            cleaned_text = tag_text.replace('\u2010', ' ')
            tag.string.replace_with(cleaned_text)

    return element


def get_tags_text(element):
    string_obj =""
    
    if len(element.find_all()) > len(element.find_all('strong')):
        #element  = replace_br(element)
       
        if element.find_all('div'):
            div_tags = element.find_all('div')
            for div_tag in div_tags:
                if div_tag.string:
                    break
            else:
                div_tag.unwrap()

    
        tags = element.find_all(recursive = False)   

        for tag in tags:
            text = tag.text.strip()
            clean_text = unicodedata.normalize('NFKD', text)
            clean_text = re.sub(r'[^\x00-\x7F]+', '', clean_text)       # Remove any non-ASCII characters from the string
            clean_text = clean_text.encode('ASCII', 'ignore').decode('utf-8')   # Encode the string as ASCII and decode it as UTF-8
            string_obj += clean_text + "\n"
    else:# Process the element as shown in the second code snippet
        
        for string in element.stripped_strings:
            clean_string = unicodedata.normalize('NFKD', string)
            clean_string = re.sub(r'[^\x00-\x7F]+', '', clean_string)
            clean_string = clean_string.encode('ASCII', 'ignore').decode('utf-8')
            string_obj += clean_string + "\n"
     
    return string_obj
        
   