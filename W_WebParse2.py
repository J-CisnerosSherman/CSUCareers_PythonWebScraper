import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import re
import W_CleanScript2

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
        'campusList': None,              #['1'],                    # Campus number if 1 = Bakersfield (if None means no campus selected returns all campuses)
        'jobposted': '10',                      # it only works with 0,10,20 increment of 10 no other days work
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
            soup = BeautifulSoup(description_html, 'html.parser')
            
            description = soup.get_text()
            print("The type of description :",type(description), description)
            #description = description.encode('utf-8')
            
            description = description.strip()

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
    


# EXECUTION STARTS HERE 


# Perform the job search and get the results
#results its a list of dictionaries returned from the fucntion search_job_list()
results = search_job_list()

# If there are results to return then it will enter loop and process them 
if results:
    for job in results:
        update_job_dt(job)
        str_to_pass = get_job_details(job)
        
        pairs = str_to_pass.split('# ')
        num_elements = len(pairs)
        
        dictionary5 = {}
        for pair in pairs:
            key, value = pair.split(':', 1)
            dictionary5[key] = re.sub(r'\s+', ' ', value).strip()
       
        job.update(dictionary5)
        texttoparse = job['Description'] 
    
        dictionary6 = {}
        dictionary6 = CleanScript2.parse_text(texttoparse)
        job.pop('Description')
        job.update(dictionary6)
        print("Final Listing Entry " , job)


#df = pd.DataFrame(results)                      # to write to excel file

modified_results = []

selected_columns = ['PositionID','datePosted','closingDate', 'jobTitle', 'apptType', 'location', 'jobType',
'Time Base', 'Discipline','Department', 'Location', 'College', 'Deadline', 'Chair', 'Phone_1', 'Email_1', 'Contact', 'Phone_2', 'Email_2']

for result in results:
    modified_dict = {col: result.get(col, None) for col in selected_columns}
    modified_results.append(modified_dict)

df = pd.DataFrame(modified_results)

excel_file = 'Searchtrf15wp2E.xlsx'

#df.columns = custom_col_names

df.to_excel(excel_file, sheet_name='Sheet1', index=False)
  

        
