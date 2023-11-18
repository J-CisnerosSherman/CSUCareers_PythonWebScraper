import spacy
import re
from spacy.matcher import Matcher
from spacy.tokens import  Span
# Load English tokenizer, tagger, parser and NER
#Note it could be ("en_core_web_sm")
nlp = spacy.load("en_core_web_trf")


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

# Selects a group of patters from the list of patterns based on index number 
# Returns the selected patterns
def select_patterns(pattern_number):
    all_patterns = [
        [#Pattern 0
            [{"TEXT": "Department"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},
             {"LOWER": "and", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "*"}],
            [{"TEXT": "Department"},{"ORTH": "/"},{"TEXT":"School"},{"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"},
             {"ORTH": "&", "OP": "*"},{"LOWER": "and", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
            [{"TEXT": "Department"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"},
             {"ORTH": "&", "OP": "*"},{"LOWER": "and", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "+"}]     
        ],
        [#Pattern 1 
            [{"TEXT": "Location"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"POS": "ADP", "OP": "*"},
             {"ORTH": "&", "OP": "*"},{"LOWER": "and", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "+"}]
        ],
        [#Pattern 2
            [{"TEXT": "College"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},
             {"LOWER": "and", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "*"}],
            [{"TEXT": "College"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},
             {"LOWER": "and", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "*"}]
             
        ],
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
        ]      
    ]

    if 0 <= pattern_number < len(all_patterns):
        return all_patterns[pattern_number]
    else:
        print(f"Invalid pattern number: {pattern_number}")
        return None        
    


def extract_hiring_department_infoo(doc,pattern_number):
    
    matcher = Matcher(nlp.vocab)                        # creates a matcher object
    patterns = select_patterns(pattern_number)          # Selects patterns based on the number
    department_info = {}                                # Create an empty dictionary to store the results
    
    for pattern in patterns:                            # Add patterns to the matcher (Can delete once completed)
        matcher.add("KEY INFO", [pattern])
        print ("added pattern ", pattern)               # Can delete when done
    
    matches = matcher(doc)                              # Find matches in the text over all text

    if len(matches) == 0:                               # Condtion checks if there are any matches, Exits if no matches 
        print("No matches found")
        department_info[keys_menu[pattern_number]] = None
        print ("department_info", department_info[keys_menu[pattern_number]])
        return department_info                          # if no matches ( len(matches)= 0) returns empty dictionary 
    
    print ("matches ", matches)                         # Can delete when done 
    
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
            pair = (start_index, ends_index)            # Creates pair by using the last saved start index and its largest index 
            print("The pair with previous start and largest end ", pair)
             
            if pair not in pairs:                       # Checks if the pair is already in the list, if not then adds pair
                pairs.append(pair)
            start_index = matches[i][1]                 # Reset the start and index to the new start and end index
            ends_index = matches[i][2]
            print("New Values",start_index, "matches[i][1]", matches[i][1])
    
    pair = (start_index, ends_index)                    # If all matches had same id only one pair will be added
    print("The pair with same id ", pair)               # Can delete when done
    
    if pair not in pairs:
        pairs.append(pair)

    for pair in pairs:                                  # Loop through all the pairs HERE CAN CHECK IF MORE THAN ONE PAIR FOUND WHAT TO DO WITH THEM 
        print(pair)
        
        first_num = pair[0]                             # Gets first number of the pair, which is start
        end_num = pair[1]                               # Gets second number of the pair, which is end  
        
        keyword = doc[first_num]
        print ("key word",keyword, "Start", first_num, "match_id")
       
        department_name = doc[first_num +2 :end_num ]      #Sets value of key to start after the original Text  this could have been one but its two to avoid ":"
        print ("dept nae here ", department_name)

        if keyword.text not in department_info:
            #department_info[keyword.text] = department_name.text
            department_info[keys_menu[pattern_number]] = department_name.text
            print("Added to department_info:", keyword.text, ":", department_name.text) 
            return department_info
 
            #break this was before the return
    return department_info



# This function calls all the other functions and returns a dictionary with all the info to WebScriptFile
def parse_text(text):
    c_text = clean_text(text)               # Given Text, calls clean_text function and returns cleaned text
    doc = nlp(c_text)                       # Sets doc to the cleaned text
    print("How text is being processed", c_text)             
    Total_info = {}                         # Creates an empty dictionary to store all the info
    
    #Loops through all the patterns in order to obtain required fields
    for pattern_number in range(6):
    
        selected_patterns = select_patterns(pattern_number)                     # Returns a list of patterns based on pattern number which changes in every iteration
        print ("selected patterns ", selected_patterns)
        print ("pattern number ", pattern_number)
        
        if pattern_number <= 2:                                                 # For pattern 0 (Department) ,1 (Location) , 2 (College) calls extract_hiring_department_infoo function
            dept = extract_hiring_department_infoo(doc,pattern_number)          # Returns a dictionary with the key and value 
            Total_info.update(dept)                                             # Returns a dictionary with the key and value will add pattern 0,1,2 to Total_info in order
        else:                                                                   # For the rest of the patterns
            indexli = extract_keyword_indexlist(doc, pattern_number)            # Returns a list of index where the keyword ( 3,4,5) was found according to pattern  number
            print("index list ", indexli, "For pattern ", pattern_number)
            
            #Find_near_entity function requires a doc, the index list and current pattern number  
            Added_dic = find_near_entity(doc, indexli, pattern_number)          # Returns a dictionary with the key and value starts at Deadline and ends at Contact
            print("updating total info ", Added_dic)
            
            value = Added_dic.get(keys_menu[pattern_number])                    # Gets the value of the Keyword at indicated index = pattern_number
            print("The value of the adajdfa is ", value)                        # To check if Value is None ( Not the case for date)       
            #is_one_token = len(value) == 1                                      # Checks if the value is one token long
            print ("vaule type", type(value))


            if value == None :                                                   # If the value of Contact or Chair is None it means it didnt find anything 
                Secon_dic = get_Contact_info( doc,  indexli , pattern_number)                                                     # Call additional function to attempt to find missing info
                if Secon_dic:                                                   #  if  matches found means second dic has these values  
                    print ("dic is empty for hre ")
                    for key, value in Secon_dic.items():                        # Loop through the second dictionary 
                        # Check if the key is already in the first dictionary
                        print("key was adddedffadfa For second dic", key, "value ", value)
                        Added_dic[key] = value                              # Add the key and value to the first dictionary
                #else:
                    #print("No matches found for second dic")
                    #Added_dic[keys_menu[pattern_number]] = None
                    #Secon_dic = {keys_menu[pattern_number]: None}
                
                print("Second dictionary ", Secon_dic)

            Total_info.update(Added_dic)                                        # Updates the dictionary with the new key and value
            
            if isinstance(value, spacy.tokens.span.Span):
                # Get the text of the span
                span_text = value.text

                # Split the span text into tokens
                tokens = span_text.split()

                # Find the number of tokens
                num_tokens = len(tokens)
                print("num_tokens in the key", num_tokens)
                if num_tokens == 1:
                    Secon_dic = get_Contact_info( doc,  indexli , pattern_number)                                                     # Call additional function to attempt to find missing info
                    if Secon_dic:                                                   #  if  matches found means second dic has these values  
                        print ("dic is empty for hre ")
                        for key, value in Secon_dic.items():                        # Loop through the second dictionary 
                            # Check if the key is already in the first dictionary
                            print("key was adddedffadfa For second dic", key, "value ", value)
                            Added_dic[key] = value                              # Add the key and value to the first dictionary
                
                    print("Second dictionary +++ ", Secon_dic)

                Total_info.update(Added_dic) 
                    

    print("Total info ", Total_info)                                            # By the time it gets here it should have all the info
    return Total_info



















def parse_text2(text):
    c_text = clean_text(text)
    doc = nlp(c_text)
    print("How text is being processed", c_text)
    total_info = []
    for pattern_number in range(6):
        selected_patterns = select_patterns(pattern_number)
        print("selected patterns ", selected_patterns)
        print("pattern number ", pattern_number)
        
        if pattern_number <= 2:
            dept = extract_hiring_department_infoo(doc, pattern_number)
            total_info.append(("Department" if pattern_number == 0 else "Location" if pattern_number == 1 else "College", dept))
        else:
            indexli = extract_keyword_indexlist(doc, pattern_number)
            print("index list ", indexli, "For pattern ", pattern_number)
            
            added_info = find_near_entity(doc, indexli, pattern_number)
            print("updating total info ", added_info)
            
            value = added_info.get(keys_menu[pattern_number])
            print("The value of the adajdfa is ", value)
            print("value type", type(value))

            if value is None:
                secon_info = get_Contact_info(doc, indexli, pattern_number)
                if secon_info:
                    print("dic is empty for hre ")
                    for key, value in secon_info.items():
                        print("key was adddedffadfa For second dic", key, "value ", value)
                        total_info.append((keys_menu[pattern_number], {key: value}))
                
                print("Second dictionary ", secon_info)

            if isinstance(value, spacy.tokens.span.Span):
                span_text = value.text
                tokens = span_text.split()
                num_tokens = len(tokens)
                print("num_tokens in the key", num_tokens)
                if num_tokens == 1:
                    secon_info = get_Contact_info(doc, indexli, pattern_number)
                    if secon_info:
                        print("dic is empty for hre ")
                        for key, value in secon_info.items():
                            print("key was adddedffadfa For second dic", key, "value ", value)
                            total_info.append((keys_menu[pattern_number], {key: value}))
                
                    print("Second dictionary +++ ", secon_info)

            total_info.append((keys_menu[pattern_number], added_info))
                    
    print("Total info ", total_info)
    return total_info


