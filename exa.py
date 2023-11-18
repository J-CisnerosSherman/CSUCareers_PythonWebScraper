# Your string representation of a dictionary (example)
string_representation = "key1:value1, key2:value2, key3:value3"

# Split the string by ',' to get key-value pairs
pairs = string_representation.split(', ')

# Create an empty dictionary
dictionary = {}

# Parse key-value pairs and add them to the dictionary
for pair in pairs:

    key, value = pair.split(':')
    dictionary[key] = value
    print( "what key ",key, "type",type(key))
    print( "what value ",value, "type",type(value))

# Now 'dictionary' contains the parsed dictionary
print(dictionary)