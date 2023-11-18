import requests
import json
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
import re
import DebugScrip2

campus_int = 4 
campus_num = str(campus_int)

"""
Bakersfield = 1
Chico = 2
Chancellor Office = 3
Chanel Islands = 4
Maritime Academy = 5
Dominguez Hills = 6
Fresno = 7
Fullerton = 8
east bay = 9
humboldt = 10
Los Angeles = 11
Long Beach = 12
Monterrey Bay = 13
Northridge = 14
Pomona = 15
Sacramento = 16
San Bernardino = 17
San Diego = 18
San Francisco = 19
San Jose = 20
San Luis Obispo = 21
San Marcos = 22
Sonoma = 23
Stanislaus = 24
"""





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



def search_job_list():
    # Define the URL for the AJAX request the URL for actual jobsite doesnt work here
    url = 'https://careers.calstate.edu/AjaxMethods.aspx/CreateJobList'  # Use the correct URL

   
    # Define the data payload using the provided criteria
    # This is where user makes selection of detail of search (Change Campus list)
    data = {
        'keywords': '',
        'zipcode': '',
        'jobtype': '1',                         # Instructional Faculty
        'dist': '20',                           # No distance limit
        'campusList': ['2'],                   # ['1'] (See list in comment block above), None (All)                   
        'jobposted': '0',                       # it only works with 0 (All postings ava.),'10',20 increment of 10 no other days work
        'timebase': '4',                        # Full-Time 
        'appttype': '1',                        # Tenure Track
        'bgunit': 'R03',
        'disciplineList': None,
    }

    # Convert the data dictionary to JSON 
    data_json = json.dumps(data)
    #print("The type of data_json :",type(data_json) )
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print("+++++++++++++++++++++++++++++++++++++++++   chico  ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ ")
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

    try:
        # Send the POST request (Inspect -> Network -> Header Request )
        response = requests.post(url, data=data_json, headers=headers)
        #print("The type of response here :",type(response) )
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            #print("The type of result :",type(result))
            # Extract and process the job listings from the 'result' JSON object
            #What appears under -> Network -> Response 
            job_listings = result['d']
            #print("The type of job_listings is:",type(job_listings)) 
            #job_listings type is list
            
            #To know what type of variable it is 
            #print(" You can now work with the job listings as needed")

            return job_listings
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None



#this one wil return a dictionary to add to the job listing 
def get_job_details(job):
    
    position_id = job.get('PositionID')

    details = { 'Dicipline':None,
                'Time':None
    }       

    # Construct the URL for the job detail page
    job_detail_url = f'https://careers.calstate.edu/detail.aspx?pid={position_id}'
    try:
        # Send a GET request to the job detail page with the new headers
        response = requests.get(job_detail_url, headers=job_detail_headers)
        
        # Check if the request was successful
        if response.status_code == 200:   #this is the url of each job listing dependig by campus ?
            # Parse the HTML content
            # empty dictionary to store details
            # Once you have a soup object, you can navigate and extract data from the HTML content. 
            soup = BeautifulSoup(response.content, 'html.parser')
               
            #print("The type of soup :",type(soup))
            #To retrive dicipline as a string
            dicipline_span = soup.find(id='ctl00_CareersContent_CatDiscSpan')
            dicipline = dicipline_span.text.strip() if dicipline_span else "Dicipline not found."
            #print("The type of dicipline_span :",type(dicipline), dicipline)

            #To retrive time as a span 
            time_span = soup.find(id = 'ctl00_CareersContent_TimeBaseSpan')
            time = time_span.text.strip() if time_span else "Time not found."
            #print("The type of tim_span :",type(time), time) 

            # Update the details dictionary with the values of dicipline and time
            details['Dicipline'] = dicipline
            details['Time'] = time

            print("The type of details obtained so far :",type(details), details)
            
            description_span = soup.find(id='ctl00_CareersContent_DescriptionP')
            if description_span:
                #strings: This generator extracts all the strings within the description_span element and its descendants, 
                # including any text within child elements. It returns each string as a separate element in 
                #print("BAKERSFIELD") 

                #strong_tags = soup.find_all('strong')

                # Extract the text content of each <strong> tag and convert to all caps
                #strong_text_list = [tag.get_text().upper() for tag in strong_tags]

                # Print the list of all-caps text
                #print("Strong text list",strong_text_list)
                
                print("\nTAGS\n")
                p_tags = description_span.find_all('p')
                
                for p_tag in p_tags:
                    # extract the text content of the <p> tag
                    # text = p_tag.get_text()
                    
                    for br_tag in p_tag.find_all('br'):           #two lines added recently just delte them if doesnt run 
                        br_tag.replace_with('\n')
                    
                    
                    
                    text = p_tag.text.strip()
                    # remove all non-ascii characters from the text
                    clean_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
                    
                    within_strong_tag = any(text in strong_tag.stripped_strings for strong_tag in p_tag.find_all('strong'))
                    
                    #print( "CleanString",clean_string)

                    if within_strong_tag:
                        #clean_string = f'<strong>{clean_string}</strong>' #dont know what it does yet saved it to check lol 
                        clean_text = clean_text.upper()
                        

                    
                    # do some processing with the clean text
                    # for example, convert all the text to uppercase
                    #processed_text = clean_text.upper()
                    #within_strong_tag = any(string in strong_tag.stripped_strings for strong_tag in description_span.find_all('strong'))
                    # print the processed text
                    print(clean_text)




                """ THIS ONE IS THE MOST BASIC JUST PRINTS THEMIN A SEPERATE STRING, WOULD HAVE TO CODE HOW TO SEPERATE THEM
                print("\nSTRINGS\n")
                for string in description_span.strings:
                    #just to print them as they are but not needed and doesnt work with texts that have non ascii characters
                    #print("STRINGS" ,string)

                    #Removes all the non ascii characters
                    clean_string = unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode('utf-8') 
                    print(clean_string)"""

                
                
                #THIS ESSESNTIALLY REMOVES ALL SPACES KINDA 
                #HMTLParse_Campus_num_Out.txt files shows the output of this








                print("\nSTRIPPED STRINGS\n")

                for string in description_span.stripped_strings:
                    #just to print them as they are but not needed and doesnt work with texts that have non ascii characters
                    #print("tHIS STRIPPED", string) 
                    
                    #Removes all the non ascii characters
                    #if not removed, it will return errors in CSUDH and others 
                    clean_string = unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore').decode('utf-8')
                    #print( "CleanString",clean_string)
                    # Check if the string is within a <strong> tag
                    within_strong_tag = any(string in strong_tag.stripped_strings for strong_tag in description_span.find_all('strong'))
                    #print( "CleanString",clean_string)

                    if within_strong_tag:
                        #clean_string = f'<strong>{clean_string}</strong>' #dont know what it does yet saved it to check lol 
                        clean_string = clean_string.upper()
                        
                    print(clean_string)

                    

                
                    

                #description = description_span.text.strip()
                #print("The type of description :",type(description), description)



            return details
        
        else:
            print(f"Failed to retrieve details for PositionID: {position_id}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching details for PositionID {position_id}: {str(e)}")
































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
results = search_job_list()



# If there are results to return then it will enter loop and process them 
if results:
    for job in results:
        print("the job details are :",job)
        update_job_dt(job)
        
        print("the updated job details are :",job)
        #str_to_pass = get_job_details(job)
        new_dic = get_job_details(job)
        #pairs = str_to_pass.split('# ')
        # num_elements = len(pairs)
else:
    print("No Job listings found.")

print ("campus numm",campus_num)

