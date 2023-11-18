import spacy
import re
from spacy.matcher import Matcher
from spacy.tokens import  Span
# Load English tokenizer, tagger, parser and NER
#Note it could be ("en_core_web_sm")
nlp = spacy.load("en_core_web_trf")


keys_menu  = ['Department', 'Location', 'College', 'Deadline', 'Chair', 'Contact'] 
#unique_strings = set()  # A set to hold the unique strings found in the text
#colon_lines = set()







# This function calls all the other functions and returns a dictionary with all the info to WebScriptFile
def parse_text(string):
    #string_list = Html_extracted_text.splitlines()
    
    
    
    
    
    output_dict = {
        "num_lines_in_list": 0,
        "num_of_end_colon_lines": 0,
        "colon_end_lines": [],
        "num_possible_heading_lines_no_col": 0,
        "possible_heading_lines_no_col": [],
        "num_lines_with_colon_but_dont_end": 0,
        "col_lines_dont_end_": [],
        "lines_after_colon": [],
        "output_list": []
    }



    if string is None:
        return output_dict
    
    my_list = [line.strip() for line in string.splitlines() if line.strip()]            #splits string into lines and removes empty lines
    
    possible_head_with_col = set()      #HAVE COL BUT TEXT AFTER TOO
    colon_end_lines = set()
    possible_headings = set()
    lines_after_colon = set()
    output_list = []
    num_header_colon_lines = 0 
    num_possible_heading_lines = 0



    for i, line in enumerate(my_list, start=0):
        
        words = line.split()            #splits by words 
        num_words = len(words)          #coutns how many words in a line 
        num_colons = line.count(":")    #counts how many colons in a line
           #if num_possible_heading_lines > 2:
        
        
        if num_colons == 0 and num_words <=10 : #if line has less than 6 words and 0 colon it will be considered a possible heading line
            num_possible_heading_lines += 1
            possible_headings.add(line)        #adds to set to makesure there is no repeating lines 

        
        if num_colons == 1 and  line.endswith(':') and num_words <= 20:  #if line has 1 colon and ends with it will be considered a heading line
            num_header_colon_lines += 1
            colon_end_lines.add(line)
       
        elif num_colons >= 1:  #if line has 1 colon and ends with it will be considered a heading line
    
            key, value = line.split(':', 1) 

            num_wkey = len(key.split())             #number of words before the colon
            if num_wkey <= 20:             #if line has less than 10 words it will be considered a heading line  
                possible_head_with_col.add(key.strip()+":")  # Add the LINES WITH COLON BUT DONT END WITH ONE
           
            num_word2 = len(value.split())         #number of words after the colon
            if num_word2 <= 30:             #if line has less than 10 words it will be considered a heading line
                lines_after_colon.add(value)   #adds to set to makesure there is no repeating lines
        
        
        output_string = f"Line {i}: {line} ({num_words} words)"
        output_list.append(output_string) 
        
        #print(f"Line {i}: {line} ({num_words} words)"
    
    list_len = len(my_list)
    output_dict = {

        "num_lines_in_list": list_len,
        "num_of_end_colon_lines": num_header_colon_lines,
        "colon_end_lines": list(colon_end_lines),
        "num_possible_heading_lines_no_col": num_possible_heading_lines,
        "possible_heading_lines_no_col": list(possible_headings),
        "num_lines_with_colon_but_dont_end": len(possible_head_with_col),
        "col_lines_dont_end_": list(possible_head_with_col),
        "lines_after_colon": list(lines_after_colon),
        "output_list": output_list
        #"my_list": my_list              #this one returns the list without any number or line info
    }
          



    #print(f"Number of strings in list: {len(my_list)}\n\n")
    #print(f"Number of lines ending with colon: {num_colon_lines}\n\n")
    #print(f"Lines with col but dont end with one : {(unique_strings)}\n\n")
    #print(f"Lines end with colon : {(colon_lines)}")


        

    return output_dict




            
            