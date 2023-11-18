import spacy
from spacy.matcher import Matcher

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
        #[{"TEXT": "Departments"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
        [{"TEXT": "Location"},{"POS": "PROPN", "is_title": True, "OP": "+"}],
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

# Example usage:

text = """
The Department of Computer Science at XYZ University is hiring. Location Nursing School of Natural Sciences The College of Engineering has an opening. Departments Mathematics And Science
"""
result = extract_hiring_department_info(text)
print(result)
