import requests
import json
from bs4 import BeautifulSoup
import unicodedata
import pandas as pd
import re
import DebugScrip2

campus_int = 6
campus_num = str(campus_int)
unique_tags = set()
word_key = set()
word_key2 = set()
"""
Returns a namedtuple("name", "age") object.
Also returns dict('name', 'age') if arg `d` is True

Arguments:
name  first name, must be string
age  age of person, must be int
d     to return Person as `dict` (default=False)

"""




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



#Function is not used when Just prints out all the names of tags and its children
def get_tag_structure_recursive(element, level=0):              #Works great i think i can be called within a tag, element 
    for child in element.find_all(recursive=False):
        print(" ->" * level + "[" + child.name +"]")            # Print the tag name with appropriate indentation
        if child.find():                                        # If the child has children, call the function recursively
           
            get_tag_structure_recursive(child, level + 2)       # Increase the level for children "2" is just for indentation, can be any int
        
#find all the tags that appear in every listing on every campus used to create the dictionary of tags 
def tag_global_set(element, level=0):
    global unique_tags
    for child in element.find_all(recursive=False):   #maybe if this is set to true it will also get the grandchildren , but the false recursive is useful when printing out structure 
        if child.name not in unique_tags:              #of the tags 
            unique_tags.add(child.name)
            print("new tag found", child.name)
        if child.find():
            tag_global_set(child, level + 1)
        
  

def find_tags_recursive2(element, level=0):
    children = element.find_all(recursive=False)
    if children:
        child_names = [child.name for child in children]
        grandchildren_names = [[grandchild.name for grandchild in child.find_all(recursive=False)] for child in children]
        print(" " * level + element.name + " --> " + str(child_names) + " --> " + str(grandchildren_names))
        for child in children:
            find_tags_recursive(child, level + 2)
    else:
        print(" " * level + element.name + " --> []")




#strong_tags = soup.find_all('strong')

                # Extract the text content of each <strong> tag and convert to all caps
                #strong_text_list = [tag.get_text().upper() for tag in strong_tags]

                # Print the list of all-caps text
                #print("Strong text list",strong_text_list)


def create_tag_structure(element, tag_structure=None):
    if tag_structure is None:
        tag_structure = {}

    
    for child in element.children:
        if child.name in ['h1', 'h2', 'h3', 'h4', 'u', 'em']:
            text = child.get_text().strip()
            if text in tag_structure:
                if child.name in tag_structure[text]:
                    tag_structure[text][child.name] += 1
                else:
                    tag_structure[text][child.name] = 1
            else:
                tag_structure[text] = {child.name: 1}
        if child.find():
            tag_structure = create_tag_structure(child, tag_structure)
    return tag_structure







def get_Keywords(element):
    global word_key
    list_keywords =['strong','h1', 'h2', 'h3', 'h4', 'u', 'em']
    
    for k_word in list_keywords:


        strong_tags = element.find_all(k_word)
        
        for tag in strong_tags:
            # word = tag.get_text()
            #print ("checking current tag", tag)
            text = tag.text.strip()
            if text != "" :
                word_list = text.split()
                num_words = len(word_list)
                if num_words <= 15:
                    pair = (tag.name , text)
                    if pair not in word_key:
                        #print("KEY TAG WORD WITH 1ST KEYWORDS", text, "at tag", tag.name)
                        word_key.add(pair)



def get_other_kwords(element):
    
    global word_key2
    for tag in element.find_all():
        #print ("checking current tag FOR :", tag)
        if ':' in tag.text:
            tag_text = tag.text.strip()
            
            substring = tag_text[:tag_text.index(':')+1]
            if substring !="":
                word_list = substring.split()
                num_words = len(word_list)
                if num_words < 15:
                    pair = (tag.name , substring)
                    if pair not in word_key2:
                        word_key2.add(pair)
        
        tag_text = tag.text.strip()
        words = re.findall(r'\b[A-Z]{3,}\b', tag_text)
        #print(" UPPER")
        if words :
            #print(" UPPER found", words)
            combined_words = ' '.join(words)

            pair = (tag.name , combined_words)
            if pair not in word_key2:
                #print("Uppercase words found:", combined_words)
                word_key2.add(pair)

    tags = element.find_all(attrs={"style": "text-decoration:underline;"})
    for tag in tags:
        #print("found a style tag", tag)
        text = tag.text.strip()
        if text != "" :
                word_list = text.split()
                num_words = len(word_list)
                if num_words <= 15:
                    pair = (tag.name , text)
                    if pair not in word_key2:
                        #print("STYLE WORD FOUND ", text, "at tag", tag.name)
                        word_key2.add(pair)
    

def get_tags_text2(element, level = 0 ):
    print("\nTEXT Recursive = false and recursion  OF TAGS\n")

    for child in element.find_all(recursive=False):
        
        text = child.text.strip()
        clean_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        
        if child.name is not None:
            parent_name = child.name
            print("->"*level+ "[" + parent_name+ "]")


        if child.find():                                        # If the child has children, call the function recursively
            get_tag_structure_recursive(child, level + 2)       # Increase the level for children "2" is just for indentation, can be any int
        
        else:
            
            text = child.text.strip()
            clean_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8') 
            return clean_text 


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


def get_tags_text3(element):
    for tag in element.find_all(recyrsive=False):
        print( "Txt reading got here ")


        tags = element.find_all()



def unwrap_tags(element):
    
    
    tags = element.find_all( recursive=False)
    for tag in tags:

        #for br_tag in tag.find_all('br'):           #two lines added recently just delte them if doesnt run 
            #br_tag.replace_with('\n')


        
        if tag.find():
            print("unwrapping f called on ", tag.name)
            unwrap_tags(tag)

        else:
            if tag.name == 'div':
                
                tag.unwrap()
                #parent_tag = tag.parent
                if tag.contents:
                    tag.parent.extend(tag.contents)
                else:
                    tag.decompose()
        
def unwrap_tags2(element):
    div_tags = element.find_all('div')
    for div_tag in div_tags:
        if div_tag.string is None:
            div_tag.unwrap()
            div_tag.parent.extend(div_tag.contents)
            


def get_tags_text(element):
    string_obj =""

    element  = replace_br(element)
    element = remove_nbsp(element)
    #new_element = clean_n(new_element)

    print("\nTEXT OF TAGS\n")

            # finds all tags in the element

    div_tags = element.find_all('div')
    for div_tag in div_tags:
        if div_tag.string:
            
            #print ("attras of dv", div_tag.attrs)
            
            break
        else:
            div_tag.unwrap()

    
    tags = element.find_all(recursive = False)            
    #p_tags = element.find_all()                           #using this one actually prints the string twice     
    for tag in tags:
    # extract the text content of the <p> tag
    # text = p_tag.get_text()
        #div_tag = None

        #this one is just to text if the case in chico works.           
       
        #for br_tag in p_tag.find_all('br'):           #two lines added recently just delte them if doesnt run 
            #br_tag.replace_with('\n')
                    
        #if p_tag.find():                              # If the child has children, call the function recursively
            #find_tags_recursive(p_tag, level + 2)
        
        """  
        tags_with_nbsp = p_tag.find_all(lambda tag: '\xa0' in tag.text)
        for tag in tags_with_nbsp:
            if tag.text.strip() == '&nbsp;':
                tag.replace_with('\n')
        else:
            tag.string = tag.string.replace('\xa0', ' ')
        
        """

        
        text = tag.text.strip()
        #print("text type " , type(text))
        # remove all non-ascii characters from the text
        clean_text = unicodedata.normalize('NFKD', text)

        # Remove any non-ASCII characters from the string
        clean_text = re.sub(r'[^\x00-\x7F]+', '', clean_text)

        # Encode the string as ASCII and decode it as UTF-8
        clean_text = clean_text.encode('ASCII', 'ignore').decode('utf-8')

        #clean_text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
        
        #print("tifja ",type(clean_text))
        #tag.string.replace_with(clean_text)
            #tag.string.replace_with(clean_text)
        string_obj += clean_text + "\n"
        # remove all the newlines from the text        
        #within_strong_tag = any(text in strong_tag.stripped_strings for strong_tag in p_tag.find_all('strong'))
                    
        #print( "CleanString",clean_string)

        #if within_strong_tag:
            #clean_string = f'<strong>{clean_string}</strong>' #dont know what it does yet saved it to check lol 
            #clean_text = clean_text.upper()
                        

                    
                    # do some processing with the clean text
                    # for example, convert all the text to uppercase
                    #processed_text = clean_text.upper()
                    #within_strong_tag = any(string in strong_tag.stripped_strings for strong_tag in description_span.find_all('strong'))
                    # print the processed text
     
    return string_obj
        
    #tag_frequency(element)
    #get_tag_structure_recursive(element)



#it prints out the 

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


#Not used just an example and for loop is how to use it not part of the function
def surrounded_by_strings(tag):
    return (isinstance(tag.next_element, NavigableString)
            and isinstance(tag.previous_element, NavigableString))

    #for tag in soup.find_all(surrounded_by_strings):
        #print tag.name
    # p
    # a
    # a
    # a
    # p




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
            # Parse the response.content. this content not connected to bs4
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
            details['URL'] = job_detail_url
            details['Dicipline'] = dicipline
            details['Time'] = time

            
            # print("The type of details obtained so far :",type(details), details)
            
            description_span = soup.find(id='ctl00_CareersContent_DescriptionP')
            if description_span:
                
                #children_tags = description_span.children
                #print("original tag structure")
                description_span = clean_n(description_span)
                description_span = remove_nbsp(description_span)
                description_span = replace_br(description_span)



                #description_span = remove_nbsp(description_span)
                #tag_frequency(description_span)  

                #get_tag_structure_recursive(description_span)
                #print("Unwrapping div tags")
                #unwrap_tags2(description_span)

                #print("new tags")
                #get_tag_structure_recursive(description_span)
                get_Keywords(description_span)
                get_other_kwords(description_span)

                print("CURRENT Entry key words")
                for key in word_key:
                    print(key)

                print("CURRENT Entry key words")
                for key in word_key2:
                    print(key)



                print("Complete string  \n" + get_tags_text(description_span))

               
                #print("\n\n\n\UPDATED TAGS\n\n\n[])
                #get_Keywords(description_span)
                #print("\n\nFETCHING TAGS\n\n")

                #tag_frequency(description_span)  
                #get_tag_structure_recursive(description_span)
                #clean_htmlchars(description_span)
                #print(" removing bullshit from file")

                #remove_nbsp(description_span)
                #print("Complete string  \n" + get_tags_text(description_span))
                #get_Keywords(description_span)
                #get_other_kwords(description_span)
                #print("cleaned text description " ,des_text   )
                #print("Complete string  \n" + get_tags_text(description_span))
                #print("getting llaves in text ")
                #get_Keywords(description_span)
                #print("getting other llaves in text ")
                #get_other_kwords(description_span)
                
                #tag_global_set(description_span)


                           
                
            #print("details",details)
            return details
        
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




#it prints out the 










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
        
            print("\n\n\nJOB DETAILS HERE  :",job)
            #str_to_pass = get_job_details(job)
            new_dic = get_job_details(job)
            #job.update(new_dic)
            #print("\n\n\nJOB DETAILS HERE  :",job)
            #pairs = str_to_pass.split('# ')
            # num_elements = len(pairs)
        print("DICTIONARY for campus +++++++++++", campus_name , "++++++++++\n\n" )
        print("\nDICTIONARY ONE\n")
        for key in word_key:
            print(key)
        print("\nDICTIONARY TWO\n")
        for key in word_key2:
            print(key)
        word_key.clear()
        word_key2.clear()

else:
    print("No Job listings found.")


#print("\n\nALL TAGS FOUND IN ALL LISTINGS\n\n",unique_tags)






"""
    




## TO RUN SEARCH CAMPUS BY CAMPUS

results = search_job_list('2')


# If there are results to return then it will enter loop and process them 
if results:
    for job in results:
        #print("the job details are :",job)
        update_job_dt(job)
        
        print("JOB DETAILS HERE  :",job)
        #str_to_pass = get_job_details(job)
        new_dic = get_job_details(job)
        #pairs = str_to_pass.split('# ')
        # num_elements = len(pairs)

    print ("GLOBAL KEYWORDS BY campus")
    for key in word_key:
            print(key)
else:
    print("No Job listings found.")

#print ("campus numm",type(campus_num),campus_num)

#"""