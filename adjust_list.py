from aux_functions import is_a_request

def line_adjust(line):
    ''' Return a list without unnecessary separators'''
    # Getting symbol of empty that is in the lines
    items = line.split(' ')
    
    separator = items[1]
    new_list = []
    if len(separator) >1:
        # There is no separator
        # removing \n from the last list item
        items[2] =  items[2][:-1]
        return items
        pass
    else:
        # There is a separator
        # creating new line list without separator
        for item in items:
            if item != separator:
                new_list.append(item)
            
        # removing \n from the last list item
        new_list[2] = new_list[2][:-1]
        return new_list


def adjust_list(list_to_adjust):
    '''Sometimes list is a bad format.
    Thus, is necessary to treat it in manner to make it useful to extract 
    data from it'''

    ''' Remove first line if it is not a service or valid line
    In this case it is checking if first char is a number.
    If it does not, remove first line'''
    
    
    # if the first line from file dados.txt is not valid pop it
    while not list_to_adjust[0][0].isdigit(): # Check if the first position in first line is a digit Ex: . (first line is just a point)
        list_to_adjust.pop(0) # if not pop the first line


    ''' Check if first line is a service or a response. If it is a response pop it.'''
        
    new_first_line = line_adjust(list_to_adjust[0])

    if not is_a_request(new_first_line):# Check if the first position in first line is a request
        list_to_adjust.pop(0) # if not pop the first line
    
    #print("Size....: ", len(list_to_adjust))    
    return list_to_adjust


def clean_all_lines(lines_list):
    all_lines = []
    for line in lines_list:
        # Cleaning line
        cleaned_line = line_adjust(line)
         
        # appending processed line to a final list        
        all_lines.append(list(cleaned_line))
         
        # cleaning list, makes the list be empty
        del cleaned_line[:]
    return all_lines