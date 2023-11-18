import spacy
import re
from spacy.matcher import Matcher
from spacy.tokens import  Span
from datetime import datetime
import dateutil.parser
import json
# Load English tokenizer, tagger, parser and NER
#Note it could be ("en_core_web_sm")("en_core_web_trf")
nlp = spacy.load("en_core_web_sm")


def get_pattern_of_colon_keywords(pattern_number):
    all_patterns = [
        [#Pattern 0  Corresponds to College: in output_dictionary 
            [{"LOWER": "college"}, {"IS_SPACE": True, "OP": "?"}, {"ORTH": ":"}]  #the ? means 0 or more times
        ],
        [#Pattern 1 Corresponds to Department: in output_dictionary
            [{"LOWER": "department"},{"IS_SPACE": True, "OP": "?"}, {"ORTH": ":"}],
            [{"LOWER": "department"}, {"ORTH": "/"}, {"LOWER": "school"},{"IS_ALPHA": True, "OP": "?"},{"IS_SPACE": True, "OP": "?"}, {"ORTH": ":"}],
            [{"LOWER": "school"},{"ORTH": "/"},{"LOWER": "department"},{"IS_ALPHA": True, "OP": "?"},{"IS_SPACE": True, "OP": "?"}, {"ORTH": ":"}]
        ],
        [#Pattern 3  Corresponds to Program: in output_dictionary
            [{"LOWER": "location"},{"IS_SPACE": True, "OP": "?"},{"ORTH": ":"}],
            [{"LOWER": "program"},{"IS_SPACE": True, "OP": "?"},{"ORTH": ":"}]
        ]            
    ]

    if 0 <= pattern_number < len(all_patterns):
        return all_patterns[pattern_number]
    else:
        print(f"Invalid pattern number: {pattern_number}")
        return None 





def get_pattern_of_key_phrases(pattern_number):
    all_patterns = [
        [#Pattern 0 
            [{"LOWER": "college"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},
             {"ORTH": "/", "OP": "*"},{"ORTH": ",", "OP": "*"},{"LOWER": "and", "OP": "*"},{"LOWER": "the", "OP": "*"}, 
             {"POS": "PROPN", "is_title": True, "OP": "*"}],
            [{"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},{"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},
             {"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"},{"LOWER": "Department"}]
        ],
        [#Pattern 1
            [{"LOWER": "department"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},
             {"ORTH": "/", "OP": "*"},{"ORTH": ",", "OP": "*"},{"LOWER": "and", "OP": "*"},{"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"}],
            [{"LOWER": "school"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},
             {"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},{"LOWER": "the", "OP": "*"},{"ORTH": ",", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"}],
            [{"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},{"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},
             {"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"},{"LOWER": "Department"}]
        ],
        [#Pattern 2
            [{"LOWER": "division"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},
             {"ORTH": "/", "OP": "*"},{"ORTH": ",", "OP": "*"},{"LOWER": "and", "OP": "*"},{"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"}],
            [{"LOWER": "program"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},{"ORTH": "/", "OP": "*"},
             {"LOWER": "and", "OP": "*"},{"ORTH": ",", "OP": "*"},{"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"}],
            [{"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},{"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},
             {"LOWER": "the", "OP": "*"},{"ORTH": ",", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"},{"LOWER": "Program"}],
            [{"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},{"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},
             {"LOWER": "the", "OP": "*"},{"ORTH": ",", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"},{"LOWER": "Division"}]
        ]     
    ]

    if 0 <= pattern_number < len(all_patterns):
        return all_patterns[pattern_number]
    else:
        print(f"Invalid pattern number: {pattern_number}")
        return None 





def get_pattern_of_key_words2(pattern_number):                      #patterns for review date
    all_patterns = [
        [#Pattern 0 
            [{"LOWER": "College"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},
             {"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},{"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"}],
            [{"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},{"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},
             {"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"},{"LOWER": "Department"}]
        ],
        [#Pattern 1
            [{"LOWER": "Department"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},
             {"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},{"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"}],
            [{"LOWER": "School"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},
             {"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},{"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"}],
            [{"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},{"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},
             {"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"},{"LOWER": "Department"}]
        ],
        [#Pattern 2
            [{"LOWER": "Division"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},
             {"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},{"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"}],
            [{"LOWER": "Program"}, {"LOWER": "of"}, {"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},{"ORTH": "/", "OP": "*"},
             {"LOWER": "and", "OP": "*"},{"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"}],
            [{"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},{"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},
             {"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"},{"LOWER": "Program"}],
            [{"POS": "PROPN", "is_title": True, "OP": "+"},{"ORTH": "&", "OP": "*"},{"ORTH": "/", "OP": "*"},{"LOWER": "and", "OP": "*"},
             {"LOWER": "the", "OP": "*"},{"POS": "PROPN", "is_title": True, "OP": "*"},{"LOWER": "Division"}]
        ]     
    ]

    if 0 <= pattern_number < len(all_patterns):
        return all_patterns[pattern_number]
    else:
        print(f"Invalid pattern number: {pattern_number}")
        return None 



def form_lists(string):                        #Given a String splits it into 3 lists based on the number of colons and the number of words in the line
    
    
    my_list = [re.sub(r'\s+', ' ', line.strip()) for line in string.splitlines() if line.strip()]  #creates a list of strings, one for each line in the text                         #removes all weird spacing from each line 
    
    sublist1 = []                               #sublist1 is the list of lines that have 1 colon and end with it
    sublist2 = []                               #sublist2 is the list of lines that have 1 colon but dont end with it
    sublist3 = []                               #sublist3 is the list of lines that have more than 1 colon

    for line in my_list:
        word_count = len(line.split())

        if line.count(':') == 1 and not line.endswith(':') and word_count <= 16:
            sublist1.append(line)
        elif ':' not in line and word_count <= 16:
            sublist2.append(line)
        elif word_count > 16:
            sublist3.append(line)

    return sublist1, sublist2, sublist3, my_list


def filter_matches(matches):
    match_dict = {}
    for match_id, start, end in matches:
        if start not in match_dict or end > match_dict[start][1]:
            match_dict[start] = (match_id, end)

    # Step 2: Convert the dictionary back to a list of tuples
    processed_matches = [(match_id, start, end) for start, (match_id, end) in match_dict.items()]

    return processed_matches



def dept_details(sublist1, sublist2, sublist3):
  
    int_to_out_list = ["College","Department","Program"]
    
    output_dict = {
        "College": None,
        "Department": None,
        "Program": None
    }

    #sublist1 is to find information in the first format such as College : 
    if sublist1:
        
        sublist_string1= '\n'.join(sublist1)                      #strings in list are joined together with a new line  
        
        doc1 = nlp(sublist_string1)                                 #creates a doc object based on the new sublist_string
        print("DOC WITH SPACES 1 ",doc1)


        for pattern_num in range(3):                              # Loop through the three different variables to find 
            
            matcher1 = Matcher(nlp.vocab)    
            #print ("numero de pattern",pattern_num)                                # creates a matcher object
            patterns = get_pattern_of_colon_keywords(pattern_num)           # Selects patterns based on the number 0 -> College         1 -> Department         2 -> Program
            #print ("patterns returned",patterns)                                        # Add patterns to the matcher (Can delete once completed)
            
            for pattern in patterns:                                        # Add patterns to the matcher (Can delete once completed)
                matcher1.add("KEY INFO", [pattern])
                #print ("added pattern ", pattern)  

            matches = matcher1(doc1)                              # finds matches in the doc object

            if matches:

                match_id, start, end = matches[0]               # get the first match of the corresponding pattern
                span = doc1[start:end]                           # get the matched span (until the colon)
                
                newline_token = None
                
                for token in doc1[end:]:
                    if token.text == '\n':
                        #print("found line space")
                        newline_token = token
                        break


                end_index = newline_token.i if newline_token else len(doc1)
                text_after_span = doc1[end:end_index].text

                # get the text after the span until the end of the line
                #print("text after span",text_after_span)
                #print("key choosen",int_to_out_list[pattern_num])
                output_dict[int_to_out_list[pattern_num]] = text_after_span  #set the corresponding key in the output dictionary to the text after the span    
                print("output dict",output_dict)


    if any(value is None for value in output_dict.values()):            #checks if any of the values are empty in the output dictionary
        #print("some values of dic are empty")

        if sublist2: 
            sublist_string2 = '\n'.join(sublist2)                        #strings in list are joined together with a new line   
            
            doc2 = nlp(sublist_string2) 
            
            #print("DOC WITH SPACES 2",doc2)
            
            matcher2 = Matcher(nlp.vocab)
            for key, value in output_dict.items():              
                
                if value is None:

                    #print("key is none",key)

                    matcher2 = Matcher(nlp.vocab)

                    patterns = get_pattern_of_key_phrases(int_to_out_list.index(key))        #selects patterns of those empty values
                    #print ("numero de pattern",int_to_out_list.index(key)) 
                    #print ("patterns returned",patterns)                                        # Add patterns to the matcher (Can delete once completed)
                    
                    for pattern in patterns:                                        # Add patterns to the matcher (Can delete once completed)
                        matcher2.add("KEY INFO", [pattern])
                        #print ("added pattern ", pattern) 
                    
                    matches2 = matcher2(doc2)                              # finds matches in the doc object
                    matches2B = filter_matches(matches2)
                    
                    #print("matches2",matches2B)
                    if matches2:
                        match_id, start, end = matches2B[0]
                        span2 = doc2[start:end]
                        #print("span2",span2)
                        output_dict[key] = span2.text
                        #print ("KEY HERE",key)
                        print("output dict",output_dict)
    

    if any(value is None for value in output_dict.values()):    
        print("some values of dic are empty still round 2")
        if sublist3: 

            sublist_string3 = '\n'.join(sublist3)                        #strings in list are joined together with a new line   
            doc3 = nlp(sublist_string3) 
        
            for key, value in output_dict.items():              
                if value is None:
                    matcher3 = Matcher(nlp.vocab)
                    patterns = get_pattern_of_key_phrases(int_to_out_list.index(key))        #selects patterns of those empty values
                    
                    for pattern in patterns:                                        # Add patterns to the matcher (Can delete once completed)
                        matcher3.add("KEY INFO", [pattern])
                        #print ("added pattern ", pattern) 
                    
                    matches3 = matcher3(doc3)                              # finds matches in the doc object
                    matches3B = filter_matches(matches3)
                    if matches3:
                        match_id, start, end = matches3B[0]
                        span = doc3[start:end]
                        output_dict[key] = span.text
    return output_dict
        


def review_date(sublist1, sublist2, sublist3):
    
    similar_words = ["review", "screening"]
    similar_words2 = ["application", "applications", "applicant", "applicants","documents"]
    similar_words3 = ["begin", "begins", "commences"]
    similar_words4 = ["by", "on", "in", "until","starting","beginning"]
    similar_words5 = ["received", "accepted", "reviewed", "completed"]
    similar_words6 = ["submit", "apply", "complete"]
    

    patterns = [#Pattern 0  Corresponds to College: in output_dictionary 
            [{"LOWER": "deadline"}, {"IS_SPACE": True, "OP": "?"}, {"ORTH": ":"}],  #the ? means 0 or more times
            [{"LOWER": "begins"},{"IS_SPACE": True, "OP": "?"}, {"ORTH": ":"}],
            [{"LOWER": "review"},{"IS_SPACE": True, "OP": "?"}, {"ORTH": ":"}], #add in case extra token before the colon
            [{"LOWER": "date"},{"IS_SPACE": True, "OP": "?"}, {"ORTH": ":"}]
        ] 

    patterns2 = [#Pattern 0  Corresponds to College: in output_dictionary 
            [{"LOWER": {"IN": similar_words}},{"LOWER": "of"},{"IS_ALPHA": True, "OP": "*"},{"LOWER": {"IN": similar_words2}},
             {"IS_ALPHA": True, "OP": "*"},{"LOWER": "will", "OP":"?"}, {"LOWER": {"IN": similar_words3}}],  #the ? means 0 or more times
            [{"LOWER": {"IN": similar_words2}},{"IS_ALPHA": True, "OP": "*"},{"LOWER": {"IN": similar_words5}},
             {"IS_ALPHA": True, "OP": "*"}, {"LOWER": {"IN": similar_words4}}],
            [{"LOWER": {"IN": similar_words6}},{"IS_ALPHA": True, "OP": "*"},{"LOWER": {"IN": similar_words2}, "OP": "?"},
             {"LOWER": {"IN": similar_words4}}],
            [{"LOWER": {"IN": similar_words}},{"LOWER": {"IN": similar_words3}}]            
        ]
    

    date_months = [
        "january", "jan","february", "feb","march", "mar","april", "apr","may", "may","june", "jun","july", "jul","august", "aug",
        "september", "sep","october", "oct","november", "nov","december", "dec"
    ]

    date_patterns = [

        [{"LOWER": {"IN": date_months}},
         {"IS_DIGIT": True, "LENGTH": {"in": [1, 2]}},  # Month (1 or 2 digits)
         {"ORTH": ",", "OP": "?"},
         {"IS_DIGIT": True, "LENGTH": {"in": [2, 4]}, "OP": "?"}],  # Year (2 or 4 digits)
        
        [{"SHAPE": "dd/dd/dddd"}],[{"SHAPE": "dd/dd/dd"}],[{"SHAPE": "d/d/dddd"}],[{"SHAPE": "dd/d/dd"}],[{"SHAPE": "d/dd/dd"}],
        [{"SHAPE": "dd-dd-dddd"}],[{"SHAPE": "dd-dd-dd"}],[{"SHAPE": "d-d-dddd"}],[{"SHAPE": "dd-d-dd"}],[{"SHAPE": "d-dd-dd"}],
      
        [{"IS_DIGIT": True, "LENGTH": {"in": [1, 2]}},
         {"ORTH": "/", "OP": "?"},{"ORTH": "-", "OP": "?"},
         {"IS_DIGIT": True, "LENGTH": {"in": [1, 2]}},  # Month (1 or 2 digits)
         {"ORTH": "/","OP": "?"},{"ORTH": "-", "OP": "?"},
         {"IS_DIGIT": True, "LENGTH": {"in": [2, 4]}, "OP": "?"},
         {"ORTH": ";","OP": "?"}]  # Year (2 or 4 digits)
        
    ]

    output_dict = {
        "ReviewDate": None
    }
    

    if sublist1:

        sublist_string1 = '\n'.join(sublist1)                      #strings in list are joined together with a new line  
        doc1 = nlp(sublist_string1)    

        matcher1 = Matcher(nlp.vocab)                                    # creates a matcher object
       
        for pattern in patterns:                                        # Add patterns to the matcher (Can delete once completed)
            matcher1.add("KEY INFO", [pattern])
            #print ("added pattern ", pattern)  

        
        matches1 = matcher1(doc1)
        #print("matches found in 1 for doc listf adf",matches1)
                    
        
        if matches1:
            matches1B = filter_matches(matches1)
            #print("matches date 1B  fdfa dfjadf ",matches1B)

            review_dates_docs = []
            for match_id, start, end in matches1B:             
                newline_token = None
                
                for token in doc1[end:]:
                    if token.text == '\n':
                        #print("found line space f3e3 ")
                        newline_token = token
                        break
                
                end_index = newline_token.i if newline_token else len(doc1)
                doc_dateA = doc1[end:end_index]  #whole sentences after key word
                review_dates_docs.append(doc_dateA)
                print("span date 1 dfaDFA ",doc_dateA)   
                
            #previous loop got a list of the docs
        
            if review_dates_docs:
                #print ("thre is  something in the review dates docs")
                #print("review dates docs que have ",review_dates_docs)
                review_dates = []


                for doc_date in review_dates_docs:
                    
                    matcher_date = Matcher(nlp.vocab)
                
                    for pattern in date_patterns:
                        matcher_date.add("DATE", [pattern])
                        #print("added pattern fd fffff",pattern) 
                    
                    matches_date = matcher_date(doc_date)
                    
                    if matches_date:
                        #print ("it got here and found a match")
                        matches_dateB = filter_matches(matches_date)
                        #print("matches 000000000000dfa dfjadf ",matches_dateB)
                        for match_id, start, end in matches_dateB:

                            span_date = doc_date[start:end] 
                            #span_date= doc1[start:end]
                            #print("span date 1 ERREF ",span_date)   #upto here got the correct date 
                            review_dates.append(span_date.text)
                            
                print("review dfas dfdfa dates",review_dates)
 
                if len(review_dates) == 1:            
                    output_dict["ReviewDate"] = review_dates[0]
                    #print("output dict 1 dateFDSF  ",output_dict)
                    
                elif len(review_dates) > 1:
                    date_objs = [dateutil.parser.parse(date) for date in review_dates]
                    #print("date objs dfsafasf df",date_objs)
                    earliest_date = min(date_objs)
                    earliest_date_str = earliest_date.strftime('%Y-%m-%d')
                    output_dict["ReviewDate"] = earliest_date_str
                    print("output dict 1 sec optionFDASF  date",output_dict)



    if output_dict["ReviewDate"] is None and sublist2:          #checks if any of the values are empty in the output dictionary              
        
        sublist_string2 = '\n'.join(sublist2)                      #strings in list are joined together with a new line  
        doc2 = nlp(sublist_string2)    
        #print("DOC WITH SPACES 23e3333",doc2)
        matcher2 = Matcher(nlp.vocab)                                    # creates a matcher object
       
        for pattern in patterns2:                                        # Add patterns to the matcher (Can delete once completed)
            matcher2.add("KEY INFO", [pattern])
            #print ("added pattern ", pattern)  

        
        matches2 = matcher2(doc2)
        #print("matches found in 1 for doc list fggggggggg",matches2)            #found no matches in the list with the single lines 
       
        if matches2:
            matches2B = filter_matches(matches2)            
            #print("matches date 17457815",matches2B)

            review_dates_docs2 = []

            for match_id, start, end in matches2B:             
                newline_token = None
                
                for token in doc2[end:]:
                    if token.text == '\n':
                        #print("found line fgfdgs space")
                        newline_token = token
                        break
                
                end_index2 = newline_token.i if newline_token else len(doc2)
                doc_date2 = doc2[end:end_index2]
                #print("doc date 1gdff ff ",doc_date2)
                review_dates_docs2.append(doc_date2)
                #print("span date 1gdfgfdgdfgfg77",doc_date2)
                
            #previous loop got a list of the docs
        
            if review_dates_docs2:
                review_dates2 = []

                for doc_date2 in review_dates_docs2:
                    matcher_date2 = Matcher(nlp.vocab)
                
                    for pattern in date_patterns:
                        matcher_date2.add("DATE", [pattern])
                        
                    matches_date2 = matcher_date2(doc_date2)
                    
                    if matches_date2:
                        
                        matches_date2B = filter_matches(matches_date2)
                        #print("matches date 2 hgfsgs fsere fda ",matches_date2B)
                        
                        for match_id, start, end in matches_date2B:

                            span_date3 = doc_date2[start:end]
                            #print("span date 1gfds  ",span_date3)
                            review_dates2.append(span_date3.text)
                            #print("srint apn span ",span_date3.text)
                            #print("output dict",output_dict)

                if len(review_dates2) == 1:            
                    output_dict["ReviewDate"] = review_dates2[0]
                    #print("output dictfg sfd       fdfggf  ",output_dict)
                    
                elif len(review_dates2) > 1:
                    #print("more than one mathchfhadshfhasd ")
                    date_objs = [dateutil.parser.parse(date) for date in review_dates2]
                    earliest_date2 = min(date_objs)
                    earliest_date_str2 = earliest_date2.strftime('%Y-%m-%d')
                    output_dict["ReviewDate"] = earliest_date_str2
                
        
    if output_dict["ReviewDate"] is None and sublist3:          #checks if any of the values are empty in the output dictionary              
        
        sublist_string3 = '\n'.join(sublist3)                      #strings in list are joined together with a new line  
        doc3 = nlp(sublist_string3)    

        matcher3 = Matcher(nlp.vocab)                                    # creates a matcher object
       
        for pattern in patterns2:                                        # Add patterns to the matcher (Can delete once completed)
            matcher3.add("KEY INFO", [pattern])
            #print ("added pattern ", pattern)  

        
        matches3 = matcher3(doc3)
        #print("matches found in 1 for doc listfff a",matches3)
        
        if matches3:
            matches3B = filter_matches(matches3)            

            #print("matches dafd 3333 date 1",matches3B)

            review_dates_docs3 = []

            for match_id, start, end in matches3B:             
                newline_token = None
                
                for token in doc3[end:]:
                    if token.text == '\n':
                        #print("found line space 788787 ")
                        newline_token = token
                        break
                
                end_index = newline_token.i if newline_token else len(doc3)
                doc_date3 = doc3[end:end_index]
                review_dates_docs3.append(doc_date3)
                #print("span date 1dfa dfdf  ",doc_date3)
                
            #previous loop got a list of the docs
        
            if review_dates_docs3:
                review_dates3 = []

                for doc_date3 in review_dates_docs3:
                    matcher_date3 = Matcher(nlp.vocab)
                
                    for pattern in date_patterns:
                        matcher_date3.add("DATE", [pattern])
                        
                    matches_date3 = matcher_date3(doc_date3)
                    
                    if matches_date3:
                        
                        matches_date3B = filter_matches(matches_date3)
                        #print("matches date 333bbbbbbbbb ",matches_date3B)
                        for match_id, start, end in matches_date3B:

                            span_date4 = doc_date3[start:end]
                            #print("span date 1666 56 665 ",span_date4)
                            review_dates3.append(span_date4.text)
                            #print("Revuew date list after append yw",review_dates3)
                            #print("output dict efwe ewf ",output_dict)

                if len(review_dates3) == 1:            
                    output_dict["ReviewDate"] = review_dates3[0]
                    
                elif len(review_dates3) > 1:
                    date_objs = [dateutil.parser.parse(date) for date in review_dates3]
                    #print("date objs 3 ____",date_objs)
                    earliest_date3 = min(date_objs)
                    #print("earliest date 3ffdfa ",earliest_date3)
                    earliest_date_str3 = earliest_date3.strftime('%Y-%m-%d')
                    #print("earliest date str 3 fgfgggggg",earliest_date_str3)
                    output_dict["ReviewDate"] = earliest_date_str3

 
    return output_dict






def contact_info(my_list):                      #Given a String splits it into 3 lists based on the number of colons and the number of words in the line
    
    similar_wordsA = ["address", "direct", "refer"]
    similar_wordsB = ["questions", "information", "inquiries", "requests"]
    similar_wordsC = ["directed", "addressed", "sent"]
    similar_wordsD = ["about", "regarding"]
    similar_wordsE = ["position", "recruitment"]
    similar_wordsF = ["contact", "call"]
    similar_wordsG = ["Dr", "Dr.", "Professor", "Professor.", "Prof", "Prof.", "PhD", "Ph.D.", "Ph.D", "Phd", "Phd.", "Ph.D."]

    pattern2 =[#Pattern 0  Corresponds to College: in output_dictionary 
            {"TEXT": {"IN": similar_wordsG},"OP": "?"},{"IS_UPPER": True, "LENGTH": 1,"OP": "?"},{"TEXT": ".","OP": "?"},{"POS": "PROPN", "IS_TITLE": True},
            {"IS_UPPER": True, "LENGTH": 1,"OP": "?"},{"TEXT": ".","OP": "?"},{"POS": "PROPN", "IS_TITLE": True, "OP": "+"},{"ORTH": ",", "OP": "?"}           
        ]
    
    pattern3 = [ #Pattern to recognize phone numbers  
            {"ORTH": "(","OP":"?"},{"SHAPE": "ddd"},{"ORTH": ")","OP":"?"},{"IS_SPACE": True, "OP": "?"},{"ORTH": ".","OP":"?"},{"ORTH": "-","OP":"?"},
            {"SHAPE": "ddd"},{"IS_SPACE": True, "OP": "?"},{"ORTH": ".","OP":"?"},{"ORTH": "-","OP":"?"},
            {"SHAPE": "dddd"}
        ]
    
    patterns = [#Pattern 0  Corresponds to College: in output_dictionary 
            [{"LOWER": "contact"}, {"IS_SPACE": True, "OP": "?"}, {"ORTH": ":"}],
            [{"LOWER": "phone"}, {"IS_SPACE": True, "OP": "?"}, {"ORTH": ":"}],
            [{"LOWER": "email"}, {"IS_SPACE": True, "OP": "?"}, {"ORTH": ":"}],
            [{"LOWER": "search"},{"IS_ALPHA": True, "OP": "?"}, {"IS_SPACE": True, "OP": "?"}, {"ORTH": ":"}],
            [{"LOWER": {"IN": similar_wordsA}},{"IS_ALPHA": True, "OP": "*"},{"LOWER": {"IN": similar_wordsB}},
             {"IS_ALPHA": True, "OP": "*"},{"LOWER": "to"}],
            [{"LOWER": {"IN": similar_wordsB}},{"IS_ALPHA": True, "OP": "*"},{"LOWER": {"IN": similar_wordsD}},
             {"IS_ALPHA": True, "OP": "*"},{"LOWER": {"IN": similar_wordsE}},{"IS_ALPHA": True, "OP": "*"},{"LOWER": {"IN": similar_wordsF}}],  #the ? means 0 or more times
            [{"LOWER": {"IN": similar_wordsB}},{"IS_ALPHA": True, "OP": "*"},{"LOWER": {"IN": similar_wordsC}},
             {"IS_ALPHA": True, "OP": "*"},{"LOWER": "to"}],
            [{"LOWER": "for"},{"LOWER": {"IN": similar_wordsB}}, {"LOWER": "and"},{"LOWER": {"IN": similar_wordsB}}]            
        ]
   
 
    output_dict = {

        "Contact_1": None,
        "Email_1": None,
        "phone_1": None,
        "Contact_2": None,
        "Email_2": None,
        "phone_2": None
    }


    if my_list:
        sublist_string = '\n'.join(my_list)                      #strings in list are joined together with a new line  
        doc = nlp(sublist_string)     
        matcher = Matcher(nlp.vocab)
        
        for pattern in patterns:                                        # Add patterns to the matcher (Can delete once completed)
            matcher.add("KEY INFO", [pattern])
            #print ("added pattern ", pattern) 
        
        matches = matcher(doc)                              #finds key words to find contact info
        matchesB = filter_matches(matches)
        if matches:

            sub_docs_to_check = []
            
            for match_id, start, end in matchesB:             # get the first match of the corresponding pattern
                
                indx_newline = []
                span = doc[start:end]
                # Find the first newline character after the patter
                newline_token = None
                
                for token in doc[end:]:

                    if token.text == '\n':
                        newline_token = token
                        indx_newline.append(newline_token.i)
                        
                        if len(indx_newline) == 8:    #collects the first 8 new line tokens          
                            break
                
                
                if len(indx_newline) == 0:

                    end_index = len(doc)
                    doc_sub = doc[end:end_index]
                    sub_docs_to_check.append(doc_sub)

                else:
                    doc_sub = doc[end:indx_newline[-1]]   
                    sub_docs_to_check.append(doc_sub)
                
        
            
            for doc_sub in sub_docs_to_check:  #for each doc that was formed from the new line tokens
                
                matcher2 = Matcher(nlp.vocab)
                matcher2.add("Contact Name", [pattern2])
                matches2 = matcher2(doc_sub)
                matches2B = filter_matches(matches2)



                if matches2:   
                    
                    if len(matches2B) == 1:               
                        match_id, start, end = matches2B[0]
                        span1 = doc_sub[start:end]
                        output_dict["Contact_1"] = span1.text
                        #print(span.text)
                    
                    elif len(matches2B) > 1:


                        match_id, start, end = matches2B[0]
                        span1 = doc_sub[start:end]
                        output_dict["Contact_1"] = span1.text
                        text1 = span1.text
                        text1 = text1.lower()
                        text1 = re.sub(r'[^\w\s]', '', text1)


                        match_id, startB, endB = matches2B[1]
                        span2 = doc_sub[startB:endB]
                        text2 = span2.text
                        text2 = text2.lower()
                        text2 = re.sub(r'[^\w\s]', '', text2)

                        if text1 != text2:

                            output_dict["Contact_2"] = span2.text


                emails = []

                for token in doc_sub:
                    if token.like_email:
                        e_mail = token
                        emails.append(e_mail)
                        
                if len(emails) == 1:

                    output_dict["Email_1"] = emails[0].text
                
                elif len(emails) > 1:
                    output_dict["Email_1"] = emails[0].text
                    output_dict["Email_2"] = emails[1].text


                
                matcher3 = Matcher(nlp.vocab)
                matcher3.add("Phone Number", [pattern3])
                matches3 = matcher3(doc_sub)
                matches3B = filter_matches(matches3)

                if matches3:
                    
                    
                    if len(matches3B) == 1:               
                        match_id, start, end = matches3B[0]
                        span1 = doc_sub[start:end]
                        output_dict["phone_1"] = span1.text
                        
                    elif len(matches3B) > 1:
                        
                        match_id, start, end = matches3B[0]
                        span1 = doc_sub[start:end]
                        output_dict["phone_1"] = span1.text
                        textA = span1.text
                        
                        match_id, startB, endB = matches3B[1]
                        span2 = doc_sub[startB:endB]
                        textB = span2.text

                        if textA != textB:
                            output_dict["phone_2"] = span2.text

    return output_dict



def extract_all_details(string):
    print("Extracting details from text...")
    
    details_output_dict = {}
    dic_1 = {}
    
    if string is None:
        details_output_dict2 = {}
        return  details_output_dict2 
    
    sublist1, sublist2, sublist3, my_list = form_lists(string)             #splits the list into 3 lists based on the number of colons and the number of words in the line to find key information

    dic_1 = dept_details(sublist1, sublist2, sublist3)             #splits the list into 3 lists based on the number of colons and the number of words in the line to find key information
    details_output_dict.update(dic_1)

    dic_2 = review_date(sublist1, sublist2, sublist3)              
    details_output_dict.update(dic_2)

    dic_3 = contact_info(my_list)             
    details_output_dict.update(dic_3)


    return details_output_dict





            
            