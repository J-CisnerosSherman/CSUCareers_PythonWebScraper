import requests
import json
from bs4 import BeautifulSoup
import pandas as pd

#Headers to connect to the 
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
        'Cookie': 'ASP.NET_SessionId=1uwya2tzfmybyf23yjtzrwzv',  # Set the correct session ID
        'X-Requested-With': 'XMLHttpRequest'
}


#headers for the details url of each job listing
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

    # Define the headers here our outside 
   
    # Define the data payload using the provided criteria
    data = {
        'keywords': '',
        'zipcode': '',
        'jobtype': '1',
        'dist': '20',
        'campusList': ['8'],
        'jobposted': '0',
        'timebase': '4',
        'appttype': '1',
        'bgunit': 'R03',
        'disciplineList': None,
    }

    # Convert the data dictionary to JSON 
    data_json = json.dumps(data)
    
    try:
        # Send the POST request (Inspect -> Network -> Header Request )
        response = requests.post(url, data=data_json, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            #print("The type of result :",type(result) )
            # Extract and process the job listings from the 'result' JSON object
            #What appears under -> Network -> Response 
            job_listings = result['d']
            #print("The type of job list is:",type(job_listings)) 
            #job_listing type is list
            

            #To know what type of variable it is 
            # You can now work with the job listings as needed

            return job_listings
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def get_job_details(job):
    # Extract PositionID from the job data
    position_id = job.get('PositionID')
    # print("The type of job :",type(job)) 
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
            
            # Find the span element by ID
            #description_span = soup.find(id='ctl00_CareersContent_DescriptionP')
            jobnum_span = soup.find(id='ctl00_CareersContent_JobIDP')
           
           
            # Extract the text under the span
            #id="ctl00_CareersContent_JobIDP"
            job_num = jobnum_span.text.strip() if jobnum_span else "Description not found."
            
            # Print or process the job description
            print(f"Details for PositionID: {position_id}")
            print(job_num)
        else:
            print(f"Failed to retrieve details for PositionID: {position_id}, Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching details for PositionID {position_id}: {str(e)}")


# ... (rest of the code, including search_job_list function)
# Perform the job search
results = search_job_list()





# to write to excel file 
df = pd.DataFrame(results)
# jupyter 
df.to_excel('chekd.xlsx', sheet_name='Sheet1', index=False)





# Print the results (you can process them further as needed)
if results:
    for job in results:
        # Visit the job detail page for each job
        print(job)
        get_job_details(job)

        