import spacy
import re
# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

# Read the contents of the text file
with open("note1.txt", "r") as file:
        text = file.read()


def clean_text_with_number_sequences(text):
   # Use regular expression to find and separate number sequences
    cleaned_text = re.sub(r'(\d+-\d+)', r'\1 ', text)
    #cleaned_text = cleaned_text.replace(":", "xxxx")
    
    # Use regular expression to separate lowercase and capital letters but only if "@" is not present
    cleaned_text = re.sub(r'([^@a-z])([A-Z])', r'\1 \2', cleaned_text)
    cleaned_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', cleaned_text)
    
    # Strip leading and trailing spaces
    cleaned_text = cleaned_text.strip()
    
    # Replace multiple consecutive whitespace characters with a single space
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    return cleaned_text


c_text = clean_text_with_number_sequences(text)

print(c_text)
doc = nlp(c_text)

from spacy.matcher import Matcher
matcher = Matcher(nlp.vocab)

def extract_full_name(nlp_doc):
    pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]
    matcher.add("FULL_NAME", [pattern])
    matches = matcher(nlp_doc)
    for _, start, end in matches:
        span = nlp_doc[start:end]
        yield span.text


def extract_hiring_department_info(text):
    # Load the spaCy English language model
    nlp = spacy.load("en_core_web_sm")
    
    # Process the input text
    doc = nlp(text)
    
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")
    # Define a Matcher with custom patterns
    matcher = Matcher(nlp.vocab)
    
    # Define patterns for keywords and their corresponding department information
   

    patterns = [
        [{"TEXT": "The Department"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
        #[{"TEXT": "Departments"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
        [{"TEXT": "Locationxxxx"},{"POS": "PROPN", "is_title": True, "OP": "+"}],
        #[{"POS": "PUNCT", "TEXT": ":"}, {"TEXT": "Location"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
        #[{"TEXT": {"in": ["Department:", "Location:"]}}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
        #[{"TEXT": {"regex": "Location:"}}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
        [{"TEXT": "Department"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
        [{"TEXT": "College"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"}]
    ]
    
    # Add patterns to the matcher
    for pattern in patterns:
        matcher.add("DEPARTMENT_INFO", [pattern])
        print ("added patter ", pattern)
    
    # Initialize a dictionary to store department information
    department_info = {}
    print("Dictonary creation " , department_info)
    # Find matches in the text
    matches = matcher(doc)
    print ("matches ", matches)
    
    for match_id, start, end in matches:
       
        keyword = doc[start]
        print ("key word",keyword, "Start", start, "match_id", match_id)
        department_name = doc[start + 1:end]
        print ("dept nae here ", department_name)
        department_info[keyword.text] = department_name.text
        print("dep info " , department_info)
    
    return department_info


def extract_hiring_department_infoo(doc):
   
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")
    # Define a Matcher with custom patterns
    matcher = Matcher(nlp.vocab)
    
    # Define patterns for keywords and their corresponding department information
   

    patterns = [
        
        [{"TEXT": "Department"},{"ORTH": ":"},{"POS": "PROPN", "is_title": True, "OP": "+"},{"POS": "ADP", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "+"}],
        [{"TEXT": "Department/School"},{"ORTH": ":"},{"POS": "PROPN", "is_title": True, "OP": "+"},{"POS": "ADP", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "+"}],
        [{"TEXT": "Location"},{"ORTH": ":"},{"POS": "PROPN", "is_title": True, "OP": "+"},{"POS": "ADP", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "+"}],
        [{"TEXT": "Department"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
        [{"TEXT": "College"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"}]
    ]
    
    # Add patterns to the matcher
    for pattern in patterns:
        matcher.add("DEPARTMENT_INFO", [pattern])
       
        print ("added patter ", pattern)
    
    # Initialize a dictionary to store department information
    department_info = {}
    print("Dictonary creation " , department_info)
    # Find matches in the text
    matches = matcher(doc)
    print ("matches ", matches)
    
    for match_id, start, end in matches:
       
        keyword = doc[start]
        print ("key word",keyword, "Start", start, "match_id", match_id)
        department_name = doc[start + 1:end]
        print ("dept nae here ", department_name)

        if keyword.text not in department_info:
            department_info[keyword.text] = department_name.text
            print("Added to department_info:", keyword.text, ":", department_name.text)  
       
    return department_info




dept = extract_hiring_department_infoo(doc)
print("fjj ", dept)


def extract_deadline_date_with_entity(doc):
    #extracted_date = None
    
    # Initialize a matcher to find the keyword "Deadline"
    matcher = Matcher(nlp.vocab)
    
    patterns = [
        [{"LOWER": "Deadline"}],
        [{"LOWER": "Review"}],
        [{"LOWER": "Consideration"}]
        ]
    # Define a pattern with the label "Deadline" and the text "Deadline"
    for pattern in patterns:
        matcher.add("Deadline_INFO", [pattern])
        print ("added patter ", pattern)
    
    reviewdate_info = {}
    indexlist =[]
    print("Dictonary creation " , reviewdate_info)
    matches = matcher(doc)
    print ("matches for review date", matches)
    
    for match_id, token_start, token_end in matches:
        # Store the token index where "Deadline" is found
        keyword_index = token_start
        keyword = doc[keyword_index]
        # Check if the keyword was found and get its token index
        if keyword_index not in indexlist:
            
            indexlist.append(keyword_index)
            print(f"Token index of 'Deadline': {keyword_index}")
             # Stop searching once the keyword is found

    # Iterate through entities
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}, Start: {ent.start}, End: {ent.end}")
    
    return indexlist



def find_closest_date_entity(doc, indexlist, label, pattern_num):
    # Initialize an empty dictionary to store review_info
    review_info = {}


    for index_point in indexlist:
        # Calculate start_token and end_token with a buffer of 20 tokens
        start_token = max(0, index_point - 20)
        end_token = index_point + 20
        print( "start ", start_token, "end ", end_token)
        # Extract entities within the specified boundaries
        min_difference = float('inf')  # Initialize with a large value
       
       
       
        selected_entities = [ent for ent in doc.ents if start_token <= ent.start < end_token]
        closest_date_entity = None
       




        #Add If statement for the use of entity in loop 
        # Iterate through the selected entities depending on the label given "DATE"
        for ent in selected_entities:
            if ent.label_ == label:
                start_index = ent.start  # Get the start index of the DATE entity
                difference = abs(start_index - index_point)  # Calculate the difference
                
                if difference < min_difference:
                    min_difference = difference
                    closest_date_entity = ent
        


        #Add if statment for the use of tokens in loop 



        # Check if the keyword at the current index in indexlist is not in review_info
        keyword = doc[index_point]
        keyword_text = keyword.text
        if keyword_text not in review_info:
            # Add the keyword text as a key to review_info and set its value as the closest_date_entity
            review_info[keyword_text] = closest_date_entity
    return review_info
    
 

# Call extract_deadline_date_with_entity with the doc as an argument
indexli = extract_deadline_date_with_entity(doc)
print("List of index matching keywords:", indexli)

# Check if indexlist is not empty
if indexli:
    # Initialize an empty dictionary to store review_info
    review_info = find_closest_date_entity(doc, indexli)

    if review_info:
        # Iterate through the review_info dictionary and print information for each keyword
        for keyword, closest_date_entity in review_info.items():
            print(f"Keyword: {keyword}")
            print(f"Closest DATE Entity: {closest_date_entity.text}")
            print(f"Start Index of Closest DATE Entity: {closest_date_entity.start}")
    else:
        print("No DATE Entities found in the document for any of the keywords in indexlist.")
else:
    print("The indexlist is empty or 'Deadline' keywords were not found in the document.")


print ("dic of review", review_info)


def extract_contact_info(doc):
    print("Extracting contact info...")
    matcher = Matcher(nlp.vocab)
    
    patterns = [
        [{"LOWER": "contact"}],
        [{"LOWER": "questions"}],
        [{"LOWER": "inquiries"}],
        ]
    
    for pattern in patterns:
        matcher.add("Contact_INFO", [pattern])
        print ("added patter ", pattern)

    contact_info = {}
    indexlist =[]
    print("Dictonary creation " , contact_info)
    matches = matcher(doc)
    print ("matches for contact", matches)
    for match_id, token_start, token_end in matches:
        # Store the token index where "Deadline" is found
        keyword_index = token_start
        keyword = doc[keyword_index]
        # Check if the keyword was found and get its token index
        if keyword_index not in indexlist:
            
            indexlist.append(keyword_index)
            print(f"Token index of 'contact': {keyword_index}")
             # Stop searching once the keyword is found

    # Iterate through entities
    for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}, Start: {ent.start}, End: {ent.end}")
    
    return indexlist















with open("output3.txt", "a") as f:
    print("Hello, world!", file=f)
    print(c_text,file=f)



# Analyze synta
   # print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
   # print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
   # print ( " uuuj ",dept )
    





# Find named entities, phrases and concepts
#for entity in doc.ents:
    #print(entity.text, entity.label_)
    
#This is what bingchat said
# Import the Matcher from spaCy

# Define a function to extract full names




#with open("output3.txt", "a") as f:

    #print("          Noun phrases:", [chunk.text for chunk in doc.noun_chunks], file=f)
    #print("          Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"], file=f)
    #print("THIS IOF THJE NAME ", next(extract_full_name(doc)))
    #for entity in doc.ents:
        #print(entity.text, entity.label_, file=f)
        #print(entity.text, entity.label_)



