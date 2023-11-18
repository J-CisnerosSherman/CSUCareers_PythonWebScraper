
patterns = {
    0: [
        [{"TEXT": "Department"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"},
         {"POS": "ADP", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "+"}]
    ],
    1: [
        [{"TEXT": "Location"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"},
         {"POS": "ADP", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "+"}]
    ],
    2: [
        [{"TEXT": "College"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"}],
        [{"TEXT": "College"}, {"ORTH": ":"}, {"POS": "PROPN", "is_title": True, "OP": "+"},
         {"POS": "ADP", "OP": "*"}, {"POS": "PROPN", "is_title": True, "OP": "+"}]
    ],
    3: [
        [{"LOWER": "deadline"}],
        [{"LOWER": "review"}],
        [{"LOWER": "consideration"}]
    ],
    4: [
        [{"LOWER": "chair"}],
        [{"LOWER": "committee"}],
        [{"LOWER": "search committee"}]
    ],
    5: [
        [{"LOWER": "contact"}],
        [{"LOWER": "questions"}],
        [{"LOWER": "inquiries"}]
    ]
    }

# Access the key at index 1
index = 1
key_at_index_1 = patterns.get(index)  #gets the value of the key not the key itself

if key_at_index_1 is not None:
    print(key_at_index_1)
else:
    print("Key not found for index 1")



# NEW HIRING DEP FUNCTION

def get_hiring_dep(doc, pattern_num):
        
