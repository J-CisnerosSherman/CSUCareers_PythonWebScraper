import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import re
import DebugScrip2

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
        'campusList': ['4'],              #['1'],                    # Campus number if 1 = Bakersfield (if None means no campus selected returns all campuses)
        'jobposted': '0',                      # it only works with 0(all of them ),10,20 increment of 10 no other days work
        'timebase': '4',                        # Full Time jobs
        'appttype': '1',                        # Tenure Track
        'bgunit': 'R03',
        'disciplineList': None,
    }

    # Convert the data dictionary to JSON 
    data_json = json.dumps(data)
    #print("The type of data_json :",type(data_json) )
    
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
            # You can now work with the job listings as needed

            return job_listings
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None



#this one wil return a dictionary to add to the job listing 
def get_details(job):
    
    position_id = job.get('PositionID')
    details = { 'Dicipline':None,
                'Time':None,
                'Description':None
    }       

    # Construct the URL for the job detail page
    job_detail_url = f'https://careers.calstate.edu/detail.aspx?pid={position_id}'
    try:
        # Send a GET request to the job detail page with the new headers
        response = requests.get(job_detail_url, headers=job_detail_headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            # empty dictionary to store details
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # print("The type of soup :",type(soup)) 
            # Find the span element by ID
        
            #To retrive dicipline as a string
            dicipline_span = soup.find(id='ctl00_CareersContent_CatDiscSpan')
            dicipline = dicipline_span.text.strip() if dicipline_span else "Dicipline not found."
            print("The type of dicipline_span :",type(dicipline), dicipline)

            
            #To retrive time as a span 
            time_span = soup.find(id = 'ctl00_CareersContent_TimeBaseSpan')
            time = time_span.text.strip() if time_span else "Time not found."
            print("The type of tim_span :",type(time), time) 


            #To retrive the Description 
            # Find the <strong> element with the specified text
            # Find the span element by ID
            description_span = soup.find(id='ctl00_CareersContent_DescriptionP')
            
            if description_span:
                # Find the <strong> element within  the specified span object
                description_strong = description_span.find('strong', text='Description:')

                if description_strong:
                    # Extract the <strong> element and its contents
                    extracted_html = str(description_strong)
                    print ("what text is to be extracted from des.span", extracted_html)
                    # Remove the <strong> element from the description_span
                    description_strong.extract()

                    description_html = description_span.encode_contents().decode('utf-8')


                    # Print or do further processing with 'extracted_html'
                    print(" remaining code  ", description_html)
                else:
                    print("Description not found.")
            else:
                print("Description span not found.")
            
          
           
            



          

            #return f"{time}# {dicipline}# {description}"
        else:
            print(f"Failed to retrieve details for PositionID: {position_id}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching details for PositionID {position_id}: {str(e)}")






#job is a dictionary which is called for each job in the list of results 
def get_job_details(job):
    
    # Extract PositionID from the job data
    position_id = job.get('PositionID')
    #print("The type of job :",type(job)) 
    #job type 'dict'

    # Construct the URL for the job detail page
    job_detail_url = f'https://careers.calstate.edu/detail.aspx?pid={position_id}'
    
    try:
        # Send a GET request to the job detail page with the new headers
        response = requests.get(job_detail_url, headers=job_detail_headers)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content
            
            soup = BeautifulSoup(response.text, 'html.parser')
            #print("The type of soup :",type(soup)) 
            # Find the span element by ID
        
            #To retrive dicipline as a string
            dicipline_span = soup.find(id='ctl00_CareersContent_CatDiscP')
            dicipline = dicipline_span.text.strip() if dicipline_span else "Description not found."
            #print("The type of dicipline_span :",type(dicipline), dicipline) 
            #description_span = soup.find(id='ctl00_CareersContent_DescriptionP')
            jobnum_span = soup.find(id='ctl00_CareersContent_JobIDP')
            #print("The type of jobnum_span :",type(jobnum_span)) 
           
            # Extract the text under the span
            #id="ctl00_CareersContent_JobIDP"
            job_num = jobnum_span.text.strip() if jobnum_span else "Description not found."
            #print("The type of job_num :",type(job_num)) 
            time_span = soup.find(id = 'ctl00_CareersContent_TimeBaseSpan')
            time = 'Time Base:' + time_span.text.strip() if time_span else "Description not found."
            #print("The type of tim_span :",type(time), time) 

            
            description_span = soup.find(id = 'ctl00_CareersContent_DescriptionP')
            description_html = description_span.prettify() if description_span else "Description not found."
            
            #print ("DESCRIPTION HTML", description_html)
            #soup = BeautifulSoup(description_html, 'html.parser')

            description = soup.get_text()
            
            print ("DESCRIPTION SOUP TEXT", description)
            
            description = description.encode('utf-8')
            # Encode the text in UTF-8
            print ("DESCRIPTION encode ", description)
            
            description = description.strip()
            print ("DESCRIPTION STRIP", description)

            return f"{time}# {dicipline}# {description}"
        else:
            print(f"Failed to retrieve details for PositionID: {position_id}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching details for PositionID {position_id}: {str(e)}")



def update_job_dt(job):
    job.pop('__type')
    job.pop('campusAbbr')
    job.pop('jobID')
    job.pop('rssParam')
    job.pop('campusCode')

results = search_job_list()

# If there are results to return then it will enter loop and process them 
if results:
    for job in results:
        update_job_dt(job)
        
        
        str_to_pass = get_job_details(job)
        print ("STR TO PASS", str_to_pass)
        #get_details(job)
        #pairs = str_to_pass.split('# ')
        # num_elements = len(pairs)
        
