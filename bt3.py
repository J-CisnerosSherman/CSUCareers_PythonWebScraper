import spacy
from spacy.matcher import Matcher

# Load the spaCy English language model
nlp = spacy.load("en_core_web_sm")

# Process the input text
text = "Contact: John Doe, Email: john.doe@example.com, Phone: 123-456-7890"
doc = nlp(text)

# Define a Matcher with the pattern
matcher = Matcher(nlp.vocab)
pattern = [{"LOWER": "contact:"}, {"IS_TITLE": True, "OP": "+"}]
matcher.add("CONTACT_NAME", [pattern])

# Find matches in the text
matches = matcher(doc)

# Extract and print the full names
for match_id, start, end in matches:
    contact_name = doc[start:end]
    print(f"Contact Name: {contact_name.text}")