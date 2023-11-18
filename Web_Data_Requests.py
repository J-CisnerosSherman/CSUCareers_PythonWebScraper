import requests
import json
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
import re
import Extract_Position_Details
import HMTL_To_Text_Processing


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
        'campusList': [campus_num],             # ['1'] (See list in comment block above), None (All)                   
        'jobposted': '120',                     # it only works with 0 (All postings ava.),'10',20 increment of 10 no other days work
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
            result = response.json()                                    # Parse the JSON response 
            #What appears under -> Network -> Response 
            job_listings = result['d']                                  #Extract and process the job listings from the 'result' JSON object
            return job_listings
        else:
            print(f"Request __failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    


def update_job_dt(job):         # function eliminates the fields that are not needed
    job.pop('__type')
    job.pop('campusAbbr')
    job.pop('jobID')
    job.pop('rssParam')
    job.pop('campusCode')


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
            #DIPLINE FIELD  
            dicipline_span = soup.find(id='ctl00_CareersContent_CatDiscSpan')
            dicipline = dicipline_span.text.strip() if dicipline_span else "Dicipline not found."
           
            #TIME BASED FIELD
            time_span = soup.find(id = 'ctl00_CareersContent_TimeBaseSpan')
            time = time_span.text.strip() if time_span else "Time not found."
           
            # Update the details dictionary with the values of dicipline and time
            details['URL'] = job_detail_url
            details['Dicipline'] = dicipline
            details['Time'] = time

            #DESCRIPTION FIELD
            description_span = soup.find(id='ctl00_CareersContent_DescriptionP')

            if description_span:
                print ("removing rare chars")
                description_span_updated =  HMTL_To_Text_Processing.remove_rare_chars(description_span)
                print ("removing br tags")
                description_span_updated = HMTL_To_Text_Processing.remove_br_tags(description_span_updated)
                print ("getting tags text")
                description_text = HMTL_To_Text_Processing.get_tags_text(description_span_updated)
                print ("updating last Dic ")
                job.update(details)
            
            return  description_text
        
        else:
            print(f"Failed to retrieve details for PositionID: {position_id}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching details for PositionID {position_id}: {str(e)}")





#EXECUTION STARTS HERE

df = pd.DataFrame()
for campus_num, campus_name in campus_dict.items():             # Loops through every campus in the dictionary
    results = search_job_list(campus_num)                       # list of jobs for each campus (dicionary)
    if results:
        for job in results:
            final_output_dict = {} 
            update_job_dt(job)                                  # remove unecessary keys from dictionary
            str_to_pass = get_job_details(job)
            final_output_dict = Extract_Position_Details.extract_all_details(str_to_pass)
            job.update(final_output_dict)
                     
        result_df = pd.DataFrame(results)
        df = pd.concat([df, result_df], ignore_index=True)
    else:
        
        print("No Job listings found.")


excel_file = 'Last120daysPostings.xlsx'
df.to_excel(excel_file, index=False)
