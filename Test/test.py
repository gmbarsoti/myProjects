def line_adjust(line):
    ''' Return a list without specific separators'''
    # Getting symbol of empty that is in the lines
    items = line.split(' ')
    
    separator = items[1]
    new_list = []
    if len(separator) >1:
        # There is no separator
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
print(line_adjust("740.   2. 3E.01."))
print(line_adjust("Sd 745.02.10.C0.00.00.00.00.00."))
