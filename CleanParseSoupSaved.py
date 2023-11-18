import requests
import json
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
import re
import Spacy_CleanScript2


#{'br', 'a', 'img', 'h4', 'tbody', 'sup', 'ins', 'ul', 'span', 'strong', 'h2The value of x² is 4 when x is equal to 2.', 'li', 'em', 'ol', 'td', 'h3', 'h1', 'p', 'div', 'tr', 'table', 's', 'u'}

campus_dict = {

    '1':'Bakersfield',
    '2':'Chico',
    '4':'Chanel Islands',
    '5':'Maritime Academy',
    '6':'Dominguez Hills',
    '7':'Fresno',
    '8':'Fullerton',
    '9':'East bay',
    '10':'Humboldt',
    '11':'Los Angeles',
    '12':'Long Beach',
    '13':'Monterrey Bay',
    '14':'Northridge',
    '15':'Pomona',
    '16':'Sacramento',
    '17':'San Bernardino',
    '18':'San Diego',
    '19':'San Francisco',
    '20':'San Jose',
    '21':'San Luis Obispo',
    '22':'San Marcos',
    '23':'Sonoma',
    '24':'Stanislaus'
    
}


#Headers to connect to the AJAX request 
# CreateJobList -> Network -> Headers
# In firefox this all appears under Response Headers
headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,es-MX;q=0.7,ca-Es-VALENCIA;q=0.6,ca;q=0.5',
        'Connection': 'keep-alive',
        'Host': 'careers.calstate.edu',
        'Origin': 'https://careers.calstate.edu',
        'Referer': 'https://careers.calstate.edu/',
        #'Cookie': 'ASP.NET_SessionId=1uwya2tzfmybyf23yjtzrwzv',  # Set the correct session ID
        'Cookie': 'ASP.NET_SessionId=jsjbpy5k0yvlknkmf3d2bhbc',
        'X-Requested-With': 'XMLHttpRequest'
}


#headers for the details url of each job listing
#from careers.calstate.edu -> Network -> Headers
#detail.aspx?pid=xxxxx
job_detail_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,es;q=0.8,es-MX;q=0.7,ca-Es-VALENCIA;q=0.6,ca;q=0.5',
    'Connection': 'keep-alive',
    'Host': 'careers.calstate.edu',
    'Referer': 'https://careers.calstate.edu/',
    'Sec-Ch-Ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.36',
}



def search_job_list(campus_num):
    # Define the URL for the AJAX request the URL for actual jobsite doesnt work here
    url = 'https://careers.calstate.edu/AjaxMethods.aspx/CreateJobList'  # Use the correct URL

    # Define the data payload using the provided criteria
    # This is where user makes selection of detail of search (Change Campus list)
    data = {
        'keywords': '',
        'zipcode': '',
        'jobtype': '1',                         # Instructional Faculty
        'dist': '20',                           # No distance limit
        'campusList': [campus_num],                   # ['1'] (See list in comment block above), None (All)                   
        'jobposted': '0',                       # it only works with 0 (All postings ava.),'10',20 increment of 10 no other days work
        'timebase': '4',                        # Full-Time 
        'appttype': '1',                        # Tenure Track
        'bgunit': 'R03',
        'disciplineList': None,
    }

    # Convert the data dictionary to JSON 
    data_json = json.dumps(data)
    try:
        # Send the POST request (Inspect -> Network -> Header Request )
        response = requests.post(url, data=data_json, headers=headers)
       
       
        if response.status_code == 200:                                 # Check if the request was successful
            # Parse the JSON response
            result = response.json()                                    # Parse the JSON response
            #Extract and process the job listings from the 'result' JSON object
            #What appears under -> Network -> Response 
            job_listings = result['d']                                
            return job_listings
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def tag_frequency(element):       

    children_tags = element.children
    chamacos = {}       # edit to return this dic and takes description.span as argument

    for child in children_tags:
        #if child.name:
        if child.name is not None:
            tag_name = child.name
            if tag_name in chamacos:
                chamacos[tag_name] += 1
            else:
                chamacos[tag_name] = 1
            """
            nietos_tags = child.contents
            if nietos_tags:
            nieto_names = [nieto.name for nieto in nietos_tags if nieto.name is not None]
            print(f"{tag_name} --> {nieto_names}")
            """   
    print("\nFrequency of Children tags in description\n")
        # print the tag counts
    for tag_name, count in chamacos.items():
        print(f"{tag_name}: {count}")    

def replace_br(element):
    br_tags = element.find_all('br')
    for br_tag in br_tags:
        br_tag.replace_with('\n')
    
    sup_tags = element.find_all('sup')

    # loop through each sup tag and delete it
    for sup_tag in sup_tags:
        sup_tag.decompose()

    return element

def remove_nbsp(element):
    # Find and replace &nbsp; within HTML tags
    #clean_description_text = ""
    print("removing nbsp")
    for tag in element.find_all():
        



        if tag.string is not None and '\u25cf' in tag.string:
            tag_text = tag.text.strip()
            cleaned_text = tag_text.replace('\u25cf', '')
            tag.string.replace_with(cleaned_text)
        if tag.string is not None and '\xa0' in tag.string: 
            #print("got tehm")
            tag_text = tag.text.strip()
            #print("at tag", tag)
            #print("tag text", tag_text)
            cleaned_text = tag_text.replace('\xa0', ' ')



            #clean_text = unicodedata.normalize('NFKD', cleaned_text)
            # print("cleaned text", cleaned_text)
            #clean_text = clean_text.encode('ASCII', 'ignore').decode('utf-8')
            
            tag.string.replace_with(cleaned_text)
            #print("new tag", tag.name)

        if tag.string is not None and '\u2010' in tag.string: 
            print("got tehm 2")
            tag_text = tag.text.strip()
            #print("at tag", tag)
            #print("tag text", tag_text)
            cleaned_text = tag_text.replace('\u2010', ' ')
            #clean_text = unicodedata.normalize('NFKD', cleaned_text)
            #clean_text = clean_text.encode('ASCII', 'ignore').decode('utf-8')
            
            #print("cleaned text ", clean_text)
            tag.string.replace_with(cleaned_text)
            #print("new tag", tag.name)
        
        #in_text = tag.text.strip()
        #clean_text = unicodedata.normalize('NFKD', in_text)
        #clean_text = re.sub(r'[^\x00-\x7F]+', '', clean_text)
        #clean_text = clean_text.encode('ASCII', 'ignore').decode('utf-8')

    return element
        




    #return clean_description_text

def clean_n(element):           

    for tag in element.find_all():
        if tag.string is not None and '\xa0' in tag.string:
            tag.string.replace_with(tag.string.replace('\xa0', ' '))
        if tag.string is not None and '\u2010' in tag.string:
            tag.string.replace_with(tag.string.replace('\u2010', ' '))
        if tag.string is not None and '\u25cf' in tag.string:
            tag.string.replace_with(tag.string.replace('\u25cf', ''))
    return element

def get_tags_text(element):
    string_obj =""
    # Check if the element contains any tags
    tag_frequency(element)

    if len(element.find_all()) > len(element.find_all('strong')):
        element  = replace_br(element)
        #element = remove_nbsp(element)
        #new_element = clean_n(new_element)

        print("\nTEXT OF TAGS\n")

            # finds all tags in the element

        if element.find_all('div'):
            div_tags = element.find_all('div')
            for div_tag in div_tags:
                if div_tag.string:
            
                #print ("attras of dv", div_tag.attrs)
            
                    break
            else:
                div_tag.unwrap()

    
        tags = element.find_all(recursive = False)            
        for tag in tags:
            text = tag.text.strip()
            clean_text = unicodedata.normalize('NFKD', text)

        # Remove any non-ASCII characters from the string
            clean_text = re.sub(r'[^\x00-\x7F]+', '', clean_text)

        # Encode the string as ASCII and decode it as UTF-8
            clean_text = clean_text.encode('ASCII', 'ignore').decode('utf-8')


            string_obj += clean_text + "\n"
    else:
        # Process the element as shown in the second code snippet
        for string in element.stripped_strings:
            clean_string = unicodedata.normalize('NFKD', string)
            clean_string = re.sub(r'[^\x00-\x7F]+', '', clean_string)
            clean_string = clean_string.encode('ASCII', 'ignore').decode('utf-8')
                
               
            

            string_obj += clean_string + "\n"
     
    return string_obj
        
   



#this one wil return a dictionary to add to the job listing 
def get_job_details(job):
    
    position_id = job.get('PositionID')

    details = { 
        'URL':None,
        'Dicipline':None,
        'Time':None
    }       

    # Construct the URL for the job detail page
    job_detail_url = f'https://careers.calstate.edu/detail.aspx?pid={position_id}'
    try:
        # Send a GET request to the job detail page with the new headers
        response = requests.get(job_detail_url, headers=job_detail_headers)
        
        # Check if the request was successful
        if response.status_code == 200:   #this is the url of each job listing dependig by campus ?
            
            soup = BeautifulSoup(response.content, 'html.parser')
               
            dicipline_span = soup.find(id='ctl00_CareersContent_CatDiscSpan')
            dicipline = dicipline_span.text.strip() if dicipline_span else "Dicipline not found."
           
            #To retrive time as a span 
            time_span = soup.find(id = 'ctl00_CareersContent_TimeBaseSpan')
            time = time_span.text.strip() if time_span else "Time not found."
           

            # Update the details dictionary with the values of dicipline and time
            details['URL'] = job_detail_url
            details['Dicipline'] = dicipline
            details['Time'] = time

        
            description_span = soup.find(id='ctl00_CareersContent_DescriptionP')

            if description_span:
                
                description_span_updated = clean_n(description_span)
                description_span_updated = remove_nbsp(description_span_updated)
                description_span_updated = replace_br(description_span_updated)

                print("Description Updated")
                description_text = get_tags_text(description_span_updated)
                
                #description_details = {}
                #description_details= Spacy_CleanScript2.parse_text(description_text)
                #details.update(description_details)
                job.update(details)
            return  description_text
        
        else:
            print(f"Failed to retrieve details for PositionID: {position_id}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching details for PositionID {position_id}: {str(e)}")





#doesnt work yet
def get_description_details(soup):
    
    # Find the description span element by ID, get the list of all tags in the span element
    text_contents =[]

    description_span = soup.find(id='ctl00_CareersContent_DescriptionP')
    
    if description_span:

        description = soup.get_text()  
    else:
        print("Description not found.")
    


def update_job_dt(job):
    job.pop('__type')
    job.pop('campusAbbr')
    job.pop('jobID')
    job.pop('rssParam')
    job.pop('campusCode')



#EXECUTION STARTS HERE


#GETS THE DICTIONARY OF EVERY LISTING AND CONTAINS THE POSITION ID TO CREATE THE URL FOR EACH JOB LISTING 
#IN NEXT FUNCTION

#"""    

for campus_num, campus_name in campus_dict.items():
    
    results = search_job_list(campus_num)
    print("\n\n\n\n\n\n\n\n\n#######################", campus_name,"#######################\n\n\n\n")
    if results:
        for job in results:
            #print("the job details are :",job)
            update_job_dt(job)
            #new_dic = {}
            #print("\n\n\nJOB DETAILS HERE  :",job)
            
            str_to_pass = get_job_details(job)
            #new_dic = get_job_details(job)
            #job.update(new_dic)
            print("\n\n\nJOB DETAILS HERE  :",job)
            print("Text Description" , str_to_pass)
            #pairs = str_to_pass.split('# ')
            # num_elements = len(pairs)
        
else:
    print("No Job listings found.")



"""
    



## TO RUN SEARCH CAMPUS BY CAMPUS

results = search_job_list('1')


# If there are results to return then it will enter loop and process them 
if results:
    for job in results:
        #print("the job details are :",job)
        update_job_dt(job)
        
        print("JOB DETAILS HERE  :",job)
        str_to_pass = get_job_details(job)
        print("\n\n\nJOB DETAILS HERE  :",job)
        print("Text Description" , str_to_pass)
        #job.update(new_dic)
        #pairs = str_to_pass.split('# ')
        # num_elements = len(pairs)

else:
    print("No Job listings found.")

#print ("campus numm",type(campus_num),campus_num)

#"""

