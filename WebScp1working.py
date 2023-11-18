import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import re
import CleanScript1
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
        'campusList': ['1'],
        'jobposted': '0',
        'timebase': '4',
        'appttype': '1',
        'bgunit': 'R03',
        'disciplineList': None,
    }

    # Convert the data dictionary to JSON 
    data_json = json.dumps(data)
    print("The type of data_json :",type(data_json) )
    
    try:
        # Send the POST request (Inspect -> Network -> Header Request )
        response = requests.post(url, data=data_json, headers=headers)
        print("The type of response here :",type(response) )
        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            result = response.json()
            print("The type of result :",type(result))
            # Extract and process the job listings from the 'result' JSON object
            #What appears under -> Network -> Response 
            job_listings = result['d']
            print("The type of job_listings is:",type(job_listings)) 
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

#job is a dictionary
def get_job_details(job):
    # Extract PositionID from the job data
    position_id = job.get('PositionID')
    print("The type of job :",type(job)) 
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
            print("The type of soup :",type(soup)) 
            # Find the span element by ID
           
            #To retrive dicipline as a string
            dicipline_span = soup.find(id='ctl00_CareersContent_CatDiscP')
            dicipline = dicipline_span.text.strip() if dicipline_span else "Description not found."
            print("The type of dicipline_span :",type(dicipline), dicipline) 
            #description_span = soup.find(id='ctl00_CareersContent_DescriptionP')
            jobnum_span = soup.find(id='ctl00_CareersContent_JobIDP')
            print("The type of jobnum_span :",type(jobnum_span)) 
           
            # Extract the text under the span
            #id="ctl00_CareersContent_JobIDP"
            job_num = jobnum_span.text.strip() if jobnum_span else "Description not found."
            print("The type of job_num :",type(job_num)) 
            time_span = soup.find(id = 'ctl00_CareersContent_TimeBaseSpan')
            time = 'Time Base:' + time_span.text.strip() if time_span else "Description not found."
            print("The type of tim_span :",type(time), time) 

            description_span = soup.find(id = 'ctl00_CareersContent_DescriptionP')
            description_html = description_span.prettify() if description_span else "Description not found."
            description = description_span.text.strip() if description_span else "Description not found."
            #print("The description:",type(description), description) 
            print("html content ",description_html)
            soup = BeautifulSoup(description_html, 'html.parser')
            text_content = soup.get_text()
            print("TTTEEXXTTT ext content ",text_content) 

            #campus_span = soup.find(id ='ctl00_CareersContent_CampusP')
            #campus = campus_span.text.strip() if campus_span else "Description not found."
            
            # Print or process the job description
            #print(f"Details for PositionID: {position_id}")
            #print(job_num)
           # return #dicinary for details 
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
    





# ... (rest of the code, including search_job_list function)
# Perform the job search
results = search_job_list()
#results its a list returned from the fucntion 




# to write to excel file 
#df = pd.DataFrame(results)
# 
#df.to_excel('chekd.xlsx', sheet_name='Sheet1', index=False)


#List_2_dic = []
# Print the results (you can process them further as needed)

if results:
    for job in results:
        # Visit the job detail page for each job
        #print(job)
        #getjobdetails returns a string to be added to new function 
        #print("Callin the dictionary 1")
        #here call update created funntion to delete or keys not wanted 
        update_job_dt(job)
        print(job)
        str_to_pass = get_job_details(job)
        #print("Callin the dictionary 1"+ str_to_pass)
        pairs = str_to_pass.split('# ')
        num_elements = len(pairs)
        print("Number of dics in list ",num_elements)
        print("list 0 element  ",pairs[0])
        print("list 0 element  ",pairs[1])
        #print("list 0 element  ",pairs[2]) would prinnt the description
        
        
        dictionary5 = {}
        for pair in pairs:
            key, value = pair.split(':', 1)
            dictionary5[key] = re.sub(r'\s+', ' ', value).strip()
        #note that dictionary 5 is the one containing all 3 extra details now
        #print("strfrom  HERE details content : " , dictionary5)
        job.update(dictionary5)
        print("it was added to  job dic", job)

        #List_2_dic.append(dictionary5)    


        #dictionary4 = json.loads(json_str_to_pass)
        #return dictionary5
        #print("strfrom  HERE details content : " , dictionary4)
        print("The type of pairs :",type(pairs))
        #pairs is a list 


        #print("Callin the dictionary 2")
        #new_dicti = create_job_dictionary(str_to_pass)
        #print("dictORNHFJ  content : " , new_dicti)
        #List_2_dic.append(new_dicti)
        #print("adding to list 2 of dicts : " , List_2_dic)
#It prints out everything in list 


#This one print every dictionary int he results list
#for dictionary in results:
#    print(" Dic in esta in  ", dictionary)       






#num_elements = len(List_2_dic) 
#print("num of thihgs in list", num_elements)      

        