import spacy
import re
from spacy.matcher import Matcher
from spacy.tokens import  Span
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")





def clean_text(text):
   # Use regular expression to find and separate number sequences
    cleaned_text = re.sub(r'(\d+-\d+)', r'\1 ', text)
    # Use regular expression to separate lowercase and capital letters but only if "@" is not present
    cleaned_text = re.sub(r'([^@a-z])([A-Z])', r'\1 \2', cleaned_text)
    cleaned_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', cleaned_text)
    # Strip leading and trailing spaces
    cleaned_text = cleaned_text.strip()
    # Replace multiple consecutive whitespace characters with a single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    return cleaned_text


#Selects a patters from the list of patterns based on index number 
#Returns the selected pattern and the index number
def select_patterns(pattern_number):
    all_patterns = [
        [#Pattern 0
            [{"TEXT": "Department"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"},
             {"POS": "ADP", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
            [{"TEXT": "Department/School"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"},
             {"POS": "ADP", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
            [{"TEXT": "Location"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"},
             {"POS": "ADP", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
            [{"TEXT": "Department"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
            [{"TEXT": "College"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"}]
        ],
        [#Pattern 1
            [{"LOWER": "deadline"}],
            [{"LOWER": "review"}],
            [{"LOWER": "consideration"}]
        ],
        [#Pattern 2
            [{"LOWER": "chair"}],
            [{"LOWER": "committee"}],
            [{"LOWER": "search committee"}],
        ],
        [#Pattern 3
            [{"LOWER": "contact"}],
            [{"LOWER": "questions"}],
            [{"LOWER": "inquiries"}]
        ]
        

        
    ]

    if 0 <= pattern_number < len(all_patterns):
        return all_patterns[pattern_number]
    else:
        print(f"Invalid pattern number: {pattern_number}")
        return None  # Return None for an invalid pattern number

# Example usage:
 # Change this number to select a different list of patterns
#selected_patterns = select_patterns(pattern_number)

#if selected_patterns:
    #print("Selected Patterns:")
    #for pattern in selected_patterns:
        #print(pattern)
#else:
    #print("Invalid pattern number.")


#This one begins the search one token after the keyword
def extract_hiring_department_infoo(doc,pattern_number):
    #creates a matcher object
    matcher = Matcher(nlp.vocab)
    #Selects patterns based on the number
    patterns =select_patterns(pattern_number)
    
    # Add patterns to the matcher
    for pattern in patterns:
        matcher.add("DEPARTMENT_INFO", [pattern])
       
        print ("added pattern ", pattern)
    
    # Initialize a dictionary to store department information
    department_info = {}
    #print("Dictonary creation " , department_info)
    # Find matches in the text
    matches = matcher(doc)
    #print ("matches ", matches)
    
    for match_id, start, end in matches:
       
        keyword = doc[start]
        print ("key word",keyword, "Start", start, "match_id", match_id)
        department_name = doc[start + 1:end]
        print ("dept nae here ", department_name)

        if keyword.text not in department_info:
            department_info[keyword.text] = department_name.text
            print("Added to department_info:", keyword.text, ":", department_name.text)  
       
    return department_info


def extract_keyword_indexlist(doc, pattern_number):
    #extracted_date = None
    
    # Initialize a matcher to find the keyword "Deadline"
    matcher = Matcher(nlp.vocab)
    patterns =select_patterns(pattern_number)

    # Define a pattern with the label "Deadline" and the text "Deadline"
    for pattern in patterns:
        matcher.add("Index_INFO", [pattern])
        print ("added pattern ", pattern)
    

    reviewdate_info = {}
    indexlist =[]
    #print("Dictonary creation " , reviewdate_info)
    
    matches = matcher(doc)
    print ("matches for review date", matches)
    
    for match_id, token_start,token_end in matches:
        # Store the token index where "Deadline" is found
        keyword_index = token_start
        keyword = doc[keyword_index] #sets keyword to the token at the index
        # Check if the keyword was found and get its token index
        if keyword_index not in indexlist:
            
            indexlist.append(keyword_index)
            print(f"Token index of 'Deadline': {keyword_index}")
             # Stop searching once the keyword is found

    # Iterate through entities just to print them out
    #for ent in doc.ents:
        #print(f"Entity: {ent.text}, Label: {ent.label_}, Start: {ent.start}, End: {ent.end}")
    
    return indexlist



#Working like expected 
def extract_contact_info(doc, start_token, end_token):
    matcher = Matcher(nlp.vocab)
    pattern = [{"ORTH": "("},{"SHAPE": "ddd"},{"ORTH": ")"},{"SHAPE": "ddd"},{"ORTH": "-", "OP": "?"},{"SHAPE": "dddd"}]


    matcher.add("Phone number", [pattern])
       
    print ("added patter ", pattern) 
    
    contact_info = {}
    selected_tokens = doc[start_token: end_token]
    closest_entity = None
    closest_ent = None
    keyword_text = None
    keyword_text2 = None
    matches = matcher(selected_tokens)
    
    for match_id, start, end in matches:
        keyword = selected_tokens[start]
        span = selected_tokens[start:end]
        keyword_text = "Phone"
        closest_ent = span.text
       
        if keyword_text not in contact_info:
            contact_info[keyword_text] = closest_ent
       
    
    for token in selected_tokens:
        if token.like_email:
            
            closest_entity = token
            keyword_text2 = "Email"
            
    if keyword_text2 not in contact_info:
        contact_info[keyword_text2] = closest_entity
        
  
    #contact_info["Email"] = closest_entity.text if closest_entity else "None"
    #contact_info["Phone"] = closest_ent if "Phone" not in contact_info else contact_info["Phone"]
    return contact_info




def find_near_entity(doc, indexlist, pattern_num):
    # Initialize an empty dictionary to store review_info
    review_info = {}

    if pattern_num == 1 :
        
        for index_point in indexlist:
            # Calculate start_token and end_token with a buffer of 20 tokens
            start_token = max(0, index_point - 20)
            end_token = index_point + 20
            print( "start ", start_token, "end ", end_token)
            # Extract entities within the specified boundaries
            min_difference = float('inf')  # Initialize with a large value
            selected_entities = [ent for ent in doc.ents if start_token <= ent.start < end_token]
            closest_entity = None


            for ent in selected_entities:
                if ent.label_ == "DATE":  #DATE #Person
                    start_index = ent.start  # Get the start index of the DATE entity
                    difference = abs(start_index - index_point)  # Calculate the difference
                
                    if difference < min_difference:
                        min_difference = difference
                        closest_entity = ent

            keyword = doc[index_point]
            keyword_text = keyword.text
            if keyword_text not in review_info:
            # Add the keyword text as a key to review_info and set its value as the closest_date_entity
                review_info[keyword_text] = closest_entity
        return review_info 
    
    elif pattern_num == 2 or pattern_num == 3:   #To find Person entity 
        
        for index_point in indexlist:
            # Calculate start_token and end_token with a buffer of 20 tokens
            start_token = max(0, index_point - 30)
            end_token = index_point + 30
            print( "start ", start_token, "end ", end_token)
            #Check here if it can get any emails or phone numbers signal the index_point used to identify them 

            #Email_phone_info = extract_contact_info(doc, start_token, end_token)

            min_difference = float('inf')  # Initialize with a large value
             # Extract tokens within the specified boundaries
            selected_entities = [ent for ent in doc.ents if start_token <= ent.start < end_token]
           
            closest_entity = None

            for ent in selected_entities:
                if ent.label_ == "PERSON":  #DATE #Person
                    start_index = ent.start  # Get the start index of the DATE entity
                    difference = abs(start_index - index_point)  # Calculate the difference
                
                    if difference < min_difference:
                        min_difference = difference
                        prev_token = doc[ent.start-1]
                        if prev_token.text in ("Dr", "Dr.", "Professor", "Professor.", "Prof", "Prof.", "PhD", "Ph.D.", "Ph.D", "Phd", "Phd."):
                            
                            closest_entity = Span(doc, ent.start-1, ent.end, label="PERSON")
                            print("Found a person entity:", closest_entity.text)
                            break
                        
                        closest_entity = ent

            keyword = doc[index_point]
            keyword_text = keyword.text
            if keyword_text not in review_info:
                review_info[keyword_text] = closest_entity
            
            

            # get ideces of all the positive entities
            Email_phone_info = extract_contact_info(doc, start_token, end_token)
            review_info.update(Email_phone_info)
        return review_info

 
#THIS IS WHERE EXECUTION BEGINS
# Read the contents of the text file of description for each job listing
#with open("note1.txt", "r") as file:
    #text = file.read()

def parse_text(text):

    c_text = clean_text(text)

    #doc with the cleaned text
    doc = nlp(c_text)
    print(c_text)
    Total_info = {}
    #pattern_number = 1
    #Loops through all the patterns in order to obtain nessary fields
    for pattern_number in range(4):
    
        selected_patterns = select_patterns(pattern_number)
        print ("selected patterns ", selected_patterns)
        print ("pattern number ", pattern_number)
        if pattern_number == 0:
            dept =extract_hiring_department_infoo(doc,pattern_number)
            Total_info.update(dept)
        else:
            indexli = extract_keyword_indexlist(doc, pattern_number)
            Added_dic = find_near_entity(doc, indexli, pattern_number)
            print("updating total info ", Added_dic)
            Total_info.update(Added_dic)

    print("Total info ",Total_info)
    return Total_info
     



















