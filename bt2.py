import spacy
import re
from spacy.tokens import  Span
import random

# Load the spaCy model
#nlp = spacy.load("en_core_web_sm")
from spacy.matcher import Matcher

import spacy
from spacy.training.example import Example

# Load a pre-trained spaCy model (e.g., 'en_core_web_sm')
nlp = spacy.load("custom_ner_model")


with open("note3.txt", "r", encoding='utf-8') as file:
        text = file.read()


def clean_text_with_number_sequences(text):
   # Use regular expression to find and separate number sequences
    #cleaned_text = re.sub(r'(\d+-\d+)', r'\1 ', text)
    
    
    #cleaned_text = cleaned_text.replace(":", "xxxx")
    cleaned_text = re.sub(r'[^\w\s@:.,-]', '', text)
    cleaned_text = re.sub(r'\u2022', '-', text)
    cleaned_text = re.sub(r'\n+', '\n', text)    #removes multiple new lines
    
    #cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # Remove special characters
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)    # Replace multiple spaces with a single space
    cleaned_text = cleaned_text.strip()                 # Remove leading and trailing spaces

   
    # Use regular expression to separate lowercase and capital letters but only if "@" is not present
    #cleaned_text = re.sub(r'([^@a-z])([A-Z])', r'\1 \2', cleaned_text)
    #cleaned_text = re.sub(r'([a-z])([A-Z])', r'\1 \2', cleaned_text)
    
    # Strip leading and trailing spaces
    #cleaned_text = cleaned_text.strip()
    
    # Replace multiple consecutive whitespace characters with a single space
    #cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    
    return cleaned_text


c_text = clean_text_with_number_sequences(text)
doc = nlp(c_text)
print ("cleaned text ", c_text)
matcher = Matcher(nlp.vocab)

def extract_full_name(nlp_doc):
    pattern = [{"POS": "PROPN"}, {"POS": "PROPN"}]
    matcher.add("FULL_NAME", [pattern])
    matches = matcher(nlp_doc)
    for _, start, end in matches:
        span = nlp_doc[start:end]
        yield span.text

for ent in doc.ents:
        print(f"Entity: {ent.text}, Label: {ent.label_}")
    # Define a Matcher with custom patterns

