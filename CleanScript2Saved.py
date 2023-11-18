import spacy
import re
from spacy.matcher import Matcher
from spacy.tokens import  Span
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")


keys_menu  = ['Department', 'Location', 'College', 'Deadline', 'Chair', 'Contact'] 

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
            [{"TEXT": "Department"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"}]     
        ],
        [#Pattern 1 
            [{"TEXT": "Location"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"},
             {"POS": "ADP", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "+"}]
        ],
        [#Pattern 2
            [{"TEXT": "College"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
            [{"TEXT": "College"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"},
             {"POS": "ADP", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "+"}]
        ],
        #[#Pattern 3
            #[{"TEXT": "Contact"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"}]     
        #]
        [#Pattern 3
            [{"LOWER": "deadline"}],
            [{"LOWER": "review"}],
            [{"LOWER": "consideration"}]
        ],
        [#Pattern 4
            [{"LOWER": "chair"}],
            [{"LOWER": "committee"}],
            [{"LOWER": "search committee"}]
        ],
        [#Pattern 5
            [{"LOWER": "contact"}],
            [{"LOWER": "questions"}],
            [{"LOWER": "inquiries"}]
        ],
        [#Pattern 6  #Can add other patterns that didnt find something after this one 
            [{"TEXT": "Contact"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"}]
            
        ]      
    ]

    if 0 <= pattern_number < len(all_patterns):
        return all_patterns[pattern_number]
    else:
        print(f"Invalid pattern number: {pattern_number}")
        return None  # Return None for an invalid pattern number


#This one begins the search one token after the keyword
#As soon as it finds a match its returned with the corresponding Keyword 
def extract_hiring_department_infoo(doc,pattern_number):
    
    matcher = Matcher(nlp.vocab)                        # creates a matcher object
    
    patterns = select_patterns(pattern_number)          # Selects patterns based on the number
    
    for pattern in patterns:                            # Add patterns to the matcher (Can delete once completed)
        matcher.add("KEY INFO", [pattern])
       
        print ("added pattern ", pattern)
    
   
    department_info = {}                                # Create an empty dictionary to store the results
    matches = matcher(doc)                              # Find matches in the text 

    
    #Condtion check if there are any matches if not exits and returns empty dictionary 
    if len(matches) == 0:
        print("No matches found")
        department_info[keys_menu[pattern_number]] = None
        return department_info
    
    print ("matches ", matches)    #Can delete when done 
    # matches[0] accesses the first tuple in the list, 
    # #and [1] retrieves the start component of that tuple. 
    #start_of_first_tuple = matches[0][1]
    #[0] -> match_id, [1] -> start, [2] -> end
    num_matches = len(matches)                          # sets the number to loop through 
    print("num_matches", num_matches)
    pairs = []                                          # To save the pairs of start and end index
    start_index = matches[0][1]                         # initialized to the first start index of the first match
    ends_index = matches[0][2]                          # initialized to the first end index of the first match


    for i in range(num_matches):                        # Loop through all the matches

        if start_index == matches[i][1]:                # The case where initial ID Matches the current ID    
            print("start index",start_index, "matches[i][1]", matches[i][1])
            if matches[i][2] >= ends_index:
                ends_index = matches[i][2]              # Update the ends index to the largest end index
        
        elif start_index != matches[i][1]:              # The case where initial ID does not match the current ID
            
            pair = (start_index, ends_index)            # Create pair by using the last saved start index and its largest index 
            print("The pair with previous start and largest end ", pair)
             
            if pair not in pairs:                       # Check if the pair is already in the list
                pairs.append(pair)
            start_index = matches[i][1]                 # Reset the start and index to the new start and end index
            ends_index = matches[i][2]
            print("New Values",start_index, "matches[i][1]", matches[i][1])
            

    pair = (start_index, ends_index)                    # If all matches had same id only one pair will be added
    print("The pair with same id ", pair)
    
    if pair not in pairs:
        pairs.append(pair)

    for pair in pairs:                 # Loop through all the pairs HERE CAN CHECK IF MORE THAN ONE PAIR FOUND WHAT TO DO WITH THEM 
        print(pair)
        
        first_num = pair[0]             # Gets first number of the pair, which is start
        end_num = pair[1]               # Gets second number of the pair, which is end  
        
        keyword = doc[first_num]
        #print ("key word",keyword, "Start", first_num, "match_id")
       
        department_name = doc[first_num + 2:end_num]      #Sets value of key to start after the original Text  this could have been one but its two to avoid ":"
        print ("dept nae here ", department_name)

        if keyword.text not in department_info:
            #department_info[keyword.text] = department_name.text
            department_info[keys_menu[pattern_number]] = department_name.text
            print("Added to department_info:", keyword.text, ":", department_name.text) 
            return department_info
 
            #break this was before the return
    return department_info





def extract_keyword_indexlist(doc, pattern_number):

    matcher = Matcher(nlp.vocab)                        # Creates a matcher object
    patterns = select_patterns(pattern_number)          # Selects patterns based on the number

    
    for pattern in patterns:                            # Add patterns to the matcher (Can delete once completed)
        matcher.add("Index_INFO", [pattern])
        print ("added pattern ", pattern)               # Can delete when done
    
    reviewdate_info = {}                                # Create an empty dictionary to store the results       
    indexlist =[]                                       # Create an empty list to store the index of the keyword
    
    matches = matcher(doc)                              # Find matches in the text
    print ("matches for THIS ", matches)          # Can delete when done
    
    for match_id, token_start,token_end in matches:
        
        keyword_index = token_start                     # Sets the keyword index to the start of the match
        keyword = doc[keyword_index]                    # Sets keyword to the token at the index
        
        if keyword_index not in indexlist:              # Check if the keyword index was found and get its token index
            
            indexlist.append(keyword_index)
            print(f"Token index of KEY WORD FOUND: {keyword_index}")   # Can delete when done
            
    return indexlist




def find_near_entity(doc, indexlist, pattern_num):
    
    review_info = {}                                                # Initialize an empty dictionary to store review_info

    if pattern_num == 3 :                                           # To find Date entity
        
        for index_point in indexlist:                               # Loops through the list of Indeces 
            
            start_token = max(0, index_point - 20)                  # Calculate start_token and end_token with a buffer of 20 tokens
            end_token = index_point + 20                            # Calculate End_token 
            print( "start ", start_token, "end ", end_token)        # Can delete later 
            
            min_difference = float('inf')                                    # Initialize with a large value
            
            # Extract entities within the specified boundaries                                                        
            selected_entities = [ent for ent in doc.ents if start_token <= ent.start < end_token]
            closest_entity = None                                            #  Creates empty Entity to save the closest one                                                      


            for ent in selected_entities:                           # Loops through the entities            
                if ent.label_ == "DATE":                            # Checks if the entity is a DATE entity
                    start_index = ent.start                         # Get the start index of the DATE entity
                    difference = abs(start_index - index_point)     # Calculate the difference between indeces of Date and Keyword 
                
                    if difference < min_difference:
                        min_difference = difference
                        closest_entity = ent                        # most finish loop to get closest entity

            keyword = doc[index_point]                              # Points Keyword at the index_point
            keyword_text = keys_menu[pattern_num]
            
            if keyword_text not in review_info:
                # Add the keyword text as a key to review_info and set its value as the closest_date_entity
                review_info[keys_menu[pattern_num]] = closest_entity   # Sets the Value of key to the closest entity
                return review_info                                     # Returns the dictionary with the key and value as soon as it finds one 
                
        return review_info                                             # if no entity found returns empty dictionary
        
    elif pattern_num == 4 or pattern_num == 5:   #To find Person entity 
        
        for index_point in indexlist:
            
            start_token = max(0, index_point - 30)                     # Calculate start_token and end_token with a buffer of 30 tokens
            end_token = index_point + 30                               # Calculate End_token
            print( "start ", start_token, "end ", end_token)

            min_difference = float('inf')                              # Initialize with a large value
             
            selected_entities = [ent for ent in doc.ents if start_token <= ent.start < end_token]   # Extract tokens within the specified boundaries
            closest_entity = None                                      # Creates empty Entity to save the closest one

            for ent in selected_entities:
                if ent.label_ == "PERSON":                              # Checks if the entity is a PERSON entity                    
                    start_index = ent.start                             # If ent is a PERSON, Get the start index of the PERSON entity
                    difference = abs(start_index - index_point)         # Calculate the difference between indeces of PERSON and Keyword
                
                    if difference < min_difference:
                        min_difference = difference
                        prev_token = doc[ent.start-1]
                        
                        if prev_token.text in ("Dr", "Dr.", "Professor", "Professor.", "Prof", "Prof.", "PhD", "Ph.D.", "Ph.D", "Phd", "Phd."):
                            
                            closest_entity = Span(doc, ent.start-1, ent.end, label="PERSON")
                            print("Found a person entity 1:", closest_entity.text)
                            
                        else:
                            closest_entity = ent
                            print("Found a person entity 2 :", closest_entity.text)
            
            keyword = doc[index_point]                                  # Points Keyword at the index_point
            keyword_text = keys_menu[pattern_num]                       # Sets keyword_text to the keyword_text at the index_point  
            
            if keyword_text not in review_info:
                # Add the keyword text as a key to review_info and set its value as the closest_date_entity
                review_info[keys_menu[pattern_num]] = closest_entity   # Sets the Value of key to the closest entity
                
            # get indeces of all the positive entities
            Email_phone_info = extract_contact_info(doc, start_token, end_token, pattern_num-3)
            review_info.update(Email_phone_info)

        return review_info                 
        
            
            
def get_Contact_info(doc, indexlist, pattern_num):          
    contact_info = {}
    
    matcher = Matcher(nlp.vocab)  
    # pattern = [{"POS": "PROPN", "is_title": True}]
    # tag = doc[start_t].text
    #pattern = [{"POS": "PROPN", "is_title": True, "OP": "+"}, {"ORTH": ".", "OP": "*"}, {"TEXT": ","}]
    #matcher.add("Name pattern ", [pattern])
    #print ("added patter ", pattern) 
    
    for index_point in indexlist:
        start_t = index_point +1                      # Calculate start_token 
        end_t = index_point + 20                    # Calculate End_token
        tag = doc[index_point].text
        print( "start ", start_t, "Word :", tag, "end ", end_t)     
        
        selected_text = doc[start_t: end_t].text       # Extract tokens within the specified boundaries
        #print ("selected text ", selected_text)
        pattern = [{"POS": "PROPN", "is_title": True, "OP": "+"}, {"ORTH": ".", "OP": "*"}, {"TEXT": ","}]
        matcher.add("Name pattern2 ", [pattern])
        #print ("added patter2 ", pattern) 
        #selected_tokens = doc[start_t: end_t]

        doc2 = nlp(selected_text)
        matches = matcher(doc2)
         
        print ("for index point    ", index_point, "matches   ", matches)
        
        if len(matches) == 0:                   #If not matches are found returns empty dictionary 
            print("No matches found")
            contact_info[keys_menu[pattern_num]] = None
            return contact_info
        
        num_matches = len(matches)                          # sets the number to loop through 
        print("num_matches", num_matches)
        pairs = []                                          # To save the pairs of start and end index
        start_index = matches[0][1]                         # initialized to the first start index of the first match
        ends_index = matches[0][2]
        
        for i in range(num_matches):                        # Loop through all the matches
            if ends_index == matches[i][2]:                # The case where initial ID Matches the current ID   
                print("end index",ends_index, "matches[i][2]", matches[i][2])
                if matches[i][1] <= start_index:
                    start_index = matches[i][1]
        
            elif ends_index != matches[i][2]:              # The case where initial ID does not match the current ID
                pair = (start_index, ends_index) 
                print("The pair with previous start and largest end ", pair)
                if pair not in pairs:                       # Check if the pair is already in the list
                    pairs.append(pair)
                    start_index = matches[i][1]                 # Reset the start and index to the new start and end index
                    ends_index = matches[i][2]
                    print("New Values",ends_index, "matches[i][2]", matches[i][2])
        
        pair = (start_index, ends_index)                    # If all matches had same id only one pair will be added
        print("The pair ends ind3ex ", pair)
        if pair not in pairs:
            pairs.append(pair)
        for pair in pairs:                 # Loop through all the pairs HERE CAN CHECK IF MORE THAN ONE PAIR FOUND WHAT TO DO WITH THEM 
            print(pair)
        
            first_num = pair[0]             # Gets first number of the pair, which is start
            end_num = pair[1]               # Gets second number of the pair, which is end  
        
            #keyword = doc2[first_num]
            keyword = doc[index_point]
            #print ("key word",keyword, "Start", first_num, "match_id")
       
            contact_name = doc2[first_num :end_num]      #Sets value of key to start after the original Text  this could have been one but its two to avoid ":"
            print ("contact nae here ", contact_name)

        if keyword.text not in contact_info:
            #department_info[keyword.text] = department_name.text
            contact_info[keys_menu[pattern_num]] = contact_name.text
            print("Added to contact_info:", keyword.text, ":", contact_name.text) 
            return contact_info
 
            #break this was before the return
    return contact_info


           
def get_Contact_info2(doc, indexlist, pattern_num):          
    contact_info = {}
    matcher = Matcher(nlp.vocab)  
    pattern = [{"POS": "PROPN", "is_title": True}]

    matcher.add("Name pattern ", [pattern])
    print ("added patter ", pattern) 
    
    for index_point in indexlist:
        start_t = index_point                       # Calculate start_token 
        end_t = index_point + 20                    # Calculate End_token
        print( "start ", start_t, "Word :", doc[start_t].text, "end ", end_t)     
        selected_text = doc[start_t: end_t].text       # Extract tokens within the specified boundaries
        doc2 = nlp(selected_text)
        matches = matcher(doc2)
        print ("for index point ", index_point, "matches ", matches)

        for match_id, start, end in matches:
            text = doc2[start:end].text
            print("priting words that match ", text)
        #print ("matches in the index thnbgy  ", matches)


def extract_cc_infoo(doc, pattern_number):
    # Create a matcher object
    matcher = Matcher(nlp.vocab)
    # Select patterns based on the number
    patterns = select_patterns(pattern_number)
    
    # Add patterns to the matcher
    for pattern in patterns:
        matcher.add("DEPARTMENT_INFO", [pattern])
        print("Added pattern ", pattern)
    
    # Initialize a dictionary to store department information
    department_info = {}
    
    # Find matches in the text
    matches = matcher(doc)
    
    for match_id, start, end in matches:
        keyword = doc[start]
        print("Key word", keyword, "Start", start, "match_id", match_id)
        department_name = doc[start + 1:end]
        print("Dept name here ", department_name)
        
        # Check if the location (start) is already in department_info
        if keyword.text not in department_info:
            department_info[keyword.text] = []
        
        # Append the department name to the list associated with this location
        department_info[keyword.text].append(department_name.text)
        print("Added to department_info:", keyword.text, ":", department_name.text)
    
    # After processing all matches, join the lists of department names into single strings
    for location, names in department_info.items():
        department_info[location] = ' '.join(names)
       
    return department_info





#Working like expected 
def extract_contact_info(doc, start_token, end_token, ind):
    
    
    matcher = Matcher(nlp.vocab)
    
    pattern = [{"ORTH": "("},{"SHAPE": "ddd"},{"ORTH": ")"},{"SHAPE": "ddd"},{"ORTH": "-", "OP": "?"},{"SHAPE": "dddd"}]


    matcher.add("Phone number", [pattern])
       
    print ("added patter ", pattern) 
    
    contact_info = {}

    selected_tokens = doc[start_token: end_token]
    
    
    closest_entity = None
    closest_ent = None
    #keyword_text = None
    keyword_text = "Phone_"+ str(ind)
    keyword_text2 = "Email_"+ str(ind)
    
    
    matches = matcher(selected_tokens)
    
   
    for match_id, start, end in matches:
        #keyword = selected_tokens[start]
        span = selected_tokens[start:end]
        
        closest_ent = span.text
       
        if keyword_text not in contact_info:
            contact_info[keyword_text] = closest_ent
            break

    

    for token in selected_tokens:
        if token.like_email:
            
            closest_entity = token
            #keyword_text2 = "Email"
            
            if keyword_text2 not in contact_info:
                contact_info[keyword_text2] = closest_entity
                break
        
    
    #contact_info["Email"] = closest_entity.text if closest_entity else "None"
    #contact_info["Phone"] = closest_ent if "Phone" not in contact_info else contact_info["Phone"]
    return contact_info




#last_key, last_value = list(my_dict.items())[-1]

#with open("note4.txt", "r") as file:
    #text = file.read()

#c_text = clean_text(text)
#print("CLEAN TEXT ", c_text)
#doc = nlp(c_text)
#Total_info = {}

#Total_info = extract_hiring_department_infoo(doc,0)
#print("Total info ", Total_info)



def parse_text(text):

    c_text = clean_text(text)

    #doc with the cleaned text
    doc = nlp(c_text)
    print("clean text", c_text)
    Total_info = {}
    #pattern_number = 1
    #Loops through all the patterns in order to obtain nessary fields
    for pattern_number in range(6):
    
        selected_patterns = select_patterns(pattern_number)
        print ("selected patterns ", selected_patterns)
        print ("pattern number ", pattern_number)
        if pattern_number <= 2:
            dept = extract_hiring_department_infoo(doc,pattern_number)
            Total_info.update(dept)
        else:
            indexli = extract_keyword_indexlist(doc, pattern_number)            # Returns a list of index where the keyword was found 
            print("index list ", indexli, "For pattern ", pattern_number)
            
            Added_dic = find_near_entity(doc, indexli, pattern_number)          # Returns a dictionary with the key and value
            print("updating total info ", Added_dic)
            
            value = Added_dic.get(keys_menu[pattern_number])                    # Gets the value of the Keyword at indicated index = pattern_number
            print("The value of the adajdfa is ", value)                        # Can delete later       
            
            if value == None:                                                   # If the value of Contact or Chair is None it means it didnt find anything 
                Secon_dic = get_Contact_info( doc, indexli,pattern_number)                                                     # Call additional function to attempt to find missing info
                print("Second dictionary ", Secon_dic)

            Total_info.update(Added_dic)                                        # Updates the dictionary with the new key and value
            

    print("Total info ", Total_info)                                            # By the time it gets here it should have all the info
    return Total_info




            
            
