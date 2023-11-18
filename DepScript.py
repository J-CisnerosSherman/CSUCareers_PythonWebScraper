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
    #cleaned_text = cleaned_text.replace(":", "")
    
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
        [{"TEXT": "Location"},{"ORTH":":"},{"POS": "PROPN", "is_title": True, "OP": "+"}],
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




def extract_hiring_department_infoo(text):
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
        #[{"TEXT": "Departments"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
        #[{"TEXT": "Location"},{"POS": "PROPN", "is_title": True, "OP": "+"}],
        [{"TEXT": "Location"},{"ORTH":":"},{"POS": "PROPN", "is_title": True, "OP": "+"}],
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

        if keyword.text not in department_info:
            department_info[keyword.text] = department_name.text
            print("Added to department_info:", keyword.text, ":", department_name.text)  
       
    return department_info
    
  



dept = extract_hiring_department_infoo(c_text)
print("fjj ", dept)




with open("output3.txt", "a") as f:
    print("Hello, world!", file=f)
    print(c_text,file=f)



# Analyze synta
    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])
    print ( " uuuj ",dept )
    





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



