import requests
import json
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
import re

import NewKeySearch

colon_lines_all = set() #Lines end with colon : {(colon_lines)
unique_strings_all = set()  # Lines with col but dont end with one : 

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
    #print("\nFrequency of Children tags in description\n")
        # print the tag counts
    #for tag_name, count in chamacos.items():
        #print(f"{tag_name}: {count}")    

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
    #print("removing nbsp")
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
    #tag_frequency(element)

    if len(element.find_all()) > len(element.find_all('strong')):
        element  = replace_br(element)
        #element = remove_nbsp(element)
        #new_element = clean_n(new_element)

        #print("\nTEXT OF TAGS\n")

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

                #print("Description Updated")
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


ALLcampus_num_lines_per_entry= set()
ALLcampus_num_of_end_colon_lines = set()
ALLcampus_colon_end_lines = set()
ALLcampus_num_possible_heading_lines_no_colon = set()
ALLcampus_possible_heading_lines_no_col = set()
ALLcampus_num_lines_with_colon_but_dont_end= set()
ALLcampus_col_lines_dont_end = set()
ALLcampus_lines_after_colon = set()



#my_list = []


for campus_num, campus_name in campus_dict.items():             #for loop to

    campus_num_lines_per_entry= set()
    campus_num_of_end_colon_lines = set()
    campus_colon_end_lines = set()
    campus_num_possible_heading_lines_no_colon = set()
    campus_possible_heading_lines_no_col = set()
    campus_num_lines_with_colon_but_dont_end= set()
    campus_col_lines_dont_end = set()
    campus_lines_after_colon = set()
    

    results = search_job_list(campus_num)
    print("\n\n\n\n\n\n\n\n\n#######################", campus_name,"#######################\n\n\n\n")
    if results:
        entry_count = 0

        for job in results:
            entry_count += 1
            #print("the job details are :",job)
            output_list_description =[]
            
            output_dict = {} 
            
            update_job_dt(job)
            #new_dic = {}
            print("\n\nWITHOUT LINES ",entry_count,"\n\n")
            str_to_pass = get_job_details(job)
            output_dict = NewKeySearch.parse_text(str_to_pass)
            
            #new_dic = get_job_details(job)
            #job.update(new_dic)
            #print("\n\n\nJOB DETAILS HERE  :",job)

            num_lines = 0
            if "num_lines_in_list" in output_dict:
                num_lines = output_dict["num_lines_in_list"]
                print("num_lines_in_list :",num_lines)
                campus_num_lines_per_entry.add(num_lines)
            else:
                print("Key 'num_lines_in_list' not found in output_dict")
            
            
            num_h_col_lines = 0
            if "num_of_end_colon_lines" in output_dict:
                
                num_h_col_lines = output_dict["num_of_end_colon_lines"]
                print("num_header_col_lines:",num_h_col_lines)
                campus_num_of_end_colon_lines.add(num_h_col_lines)
            else:
                print("Key 'num_of_end_colon_lines' not found in output_dict")

            if "colon_end_lines" in output_dict:
                colon_e_lines = output_dict["colon_end_lines"]
                print("colon_end_lines\n")
                campus_colon_end_lines.update(colon_e_lines)
                for line in colon_e_lines:
                    print(line)
            else:
                print("Key 'colon_end_lines' not found in output_dict")


            num_p_h_lines_n_col = 0
            if "num_possible_heading_lines_no_col" in output_dict:
                num_p_h_lines_n_col = output_dict["num_possible_heading_lines_no_col"]
                print("num_p_h_lines_n_col :",num_p_h_lines_n_col)
                campus_num_possible_heading_lines_no_colon.add(num_p_h_lines_n_col)
            else:
                print("Key 'num_possible_heading_lines_no_col' not found in output_dict")


            if "possible_heading_lines_no_col" in output_dict:
                possible_h_no_col = output_dict["possible_heading_lines_no_col"]
                print("possible_headings_no_col\n")
                campus_possible_heading_lines_no_col.update(possible_h_no_col)
                for line in possible_h_no_col:
                    print(line)
            else:
                print("Key 'possible_heading_lines_no_col' not found in output_dict")
     
            
            num_lines_col_dont_end = 0
            if "num_lines_with_colon_but_dont_end" in output_dict:
                
                num_lines_col_dont_end = output_dict["num_lines_with_colon_but_dont_end"]
                print("num_lines_col_dont_end\n")
                campus_num_lines_with_colon_but_dont_end.add(num_lines_col_dont_end)
            else:
                print("Key 'num_lines_with_colon_but_dont_end' not found in output_dict")

            if "col_lines_dont_end_" in output_dict:
                col_lines_dont_end = output_dict["col_lines_dont_end_"]
                print("col_lines_dont_end]\n")
                campus_col_lines_dont_end.update(col_lines_dont_end)
                for line in col_lines_dont_end:
                    print(line)
            else:
                print("Key 'col_lines_dont_end_' not found in output_dict")
          
            if "lines_after_colon" in output_dict:
                lines_a_colon = output_dict["lines_after_colon"]
                print("lines_after_colon\n")
                campus_lines_after_colon.update(lines_a_colon)
                for line in lines_a_colon:
                    print(line)
            else:
                print("Key 'lines_after_colon' not found in output_dict")
        
            if "output_list" in output_dict:
                output_list_description= output_dict["output_list"]
                print("\n\n output_list",entry_count,"\n\n")
                for line in output_list_description:
                    print(line)
            else:
                print("Key 'output_list' not found in output_dict")
            
         



            #pairs = str_to_pass.split('# ')
            # num_elements = len(pairs)
    
    print("\n\nENTIRE STATS BY CAMPUS\n\n")
    print("campus_num_lines_per_entry\n ",campus_num_lines_per_entry)
    ALLcampus_num_lines_per_entry.update(campus_num_lines_per_entry)
    #campus_num_lines_per_entry.clear()

    print("campus_num_of_end_colon_lines\n ",campus_num_of_end_colon_lines)
    ALLcampus_num_of_end_colon_lines.update(campus_num_of_end_colon_lines)
    #campus_num_of_end_colon_lines.clear()

    print("campus_colon_end_lines \n")
    for line in campus_colon_end_lines:
        print(line)
    ALLcampus_colon_end_lines.update(campus_colon_end_lines)
    #campus_colon_end_lines.clear()


    print("campus_num_possible_heading_lines_no_colon\n ",campus_num_possible_heading_lines_no_colon)
    ALLcampus_num_possible_heading_lines_no_colon.update(campus_num_possible_heading_lines_no_colon)
    #campus_num_possible_heading_lines_no_colon.clear()
    
    print("campus_possible_heading_lines_no_col \n")

    for line in campus_possible_heading_lines_no_col:
        print(line)
    ALLcampus_possible_heading_lines_no_col.update(campus_possible_heading_lines_no_col)
    #campus_possible_heading_lines_no_col.clear()

    print("campus_num_lines_with_colon_but_dont_end \n",campus_num_lines_with_colon_but_dont_end)
    ALLcampus_num_lines_with_colon_but_dont_end.update(campus_num_lines_with_colon_but_dont_end)
    #campus_num_lines_with_colon_but_dont_end.clear()

    print("campus_col_lines_dont_end \n")
    for line in campus_col_lines_dont_end:
        print(line)

    ALLcampus_col_lines_dont_end.update(campus_col_lines_dont_end)
    #campus_col_lines_dont_end.clear()

    print("campus_lines_after_colon \n")
    for line in campus_lines_after_colon:
        print(line)
    ALLcampus_lines_after_colon.update(campus_lines_after_colon)
    #campus_lines_after_colon.clear()
    #print("output_list_description ",output_list_description)

    
    #print("CAMPUS TOTALLINES  end with colon\n",colon_lines_all)
    #print("CAMPUS TOTAL with col but dont end with one\n",unique_strings_all)
else:
    print("No Job listings found.")


print("\n\n\n\n\n\n\n\n\n####################### ALL CAMPUS #######################\n\n\n\n")
print("ALLcampus_num_lines_per_entry\n")
for item in ALLcampus_num_lines_per_entry:
    print(item)


print("ALLcampus_num_of_end_colon_lines\n")
for item in ALLcampus_num_of_end_colon_lines:
    print(item)

print("ALLcampus_colon_end_lines \n")
for line in ALLcampus_colon_end_lines:
    print(line)


print("ALLcampus_num_possible_heading_lines_no_colon\n")
for item in ALLcampus_num_possible_heading_lines_no_colon:
    print(item)

print("ALLcampus_possible_heading_lines_no_col \n")
for line in ALLcampus_possible_heading_lines_no_col:
    print(line)

print("ALLcampus_num_lines_with_colon_but_dont_end \n")
for item in ALLcampus_num_lines_with_colon_but_dont_end:
    print(item)

print("ALLcampus_col_lines_dont_end \n")
for line in ALLcampus_col_lines_dont_end:
    print(line)

print("ALLcampus_lines_after_colon \n")
for line in ALLcampus_lines_after_colon:
    print(line)













"""
    



## TO RUN SEARCH CAMPUS BY CAMPUS

results = search_job_list('1')


# If there are results to return then it will enter loop and process them 
if results:
    for job in results:
        my_string_list = []
        update_job_dt(job)
        #new_dic = {}
        
        print("\n\nWITHOUT LINES\n\n")
            
        str_to_pass = get_job_details(job)

        my_string_list = NewKeySearch.parse_text(str_to_pass)

else:
    print("No Job listings found.")

#print ("campus numm",type(campus_num),campus_num)

#"""

