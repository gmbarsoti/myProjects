'''
Created on 22 de jun de 2018

@author: 155 X-MX
'''

def line_adjust(line):
    ''' Return a list without not useful separators'''
    # Getting symbol of empty that is in the lines
    items = line.split(' ')
    print (items)
    
    separator = items[1]
    print(len(separator))
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


l = '760.  159. 59.02.7B.40.20.04.50.40.20.1C.50.C4.02.00.50.C1.01.00.50.40.40.64.50.51.51.55.50.50.50.04.50.C4.14.00.50.C4.23.00.50.40.10.01.50.40.14.01.50.40.18.01.50.40.1C.01.50.40.11.01.50.40.15.01.50.40.19.01.50.40.1D.01.50.F0.03.17.50.51.56.55.50.51.89.64.50.40.6B.92.50.40.6C.55.50.C0.01.00.50.F0.03.13.50.51.25.95.50.40.31.1D.50.40.31.38.50.40.30.97.50.40.34.1D.50.40.34.38.50.40.33.97.50.51.27.64.50.51.26.95.50.40.37.1D.50.40.37.38.50.40.36.97.50.40.3A.1D.50.40.3A.38.50.40.39.97.50.'

print(line_adjust(l))