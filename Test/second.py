'''
Created on 12 de jun de 2018

@author: 155 X-MX
'''
from pathlib import Path
import os.path


def fileLines(path_to_folder, file_name):
    '''return a list with all lines of a txt file'''
    #data_folder = Path("C:/Users/155 X-MX/Desktop/Preenche Servicos")
    data_folder = Path(path_to_folder)
    file_to_open = data_folder / file_name
     
    f = open(file_to_open,"r")
     
    if not file_to_open.exists():
        print("Oops, file doesn't exist!")
    else:
        print("Yay, the file exists!")
         
    # Getting all lines    
    all_lines = f.readlines()
    #print('lines len: ', str(len(all_lines)))
    return all_lines

def occurred_cases(full_vector):
    ''' Returna list with just an occurrence of each item from a initial list'''
    ret_vector = []
    
    for item in full_vector:
        if not item[2] in ret_vector:
            ret_vector.append(item[2])
            
    return ret_vector


def occurred_cases2(full_vector):
    ''' Returna list with just an occurrence of each service request 
    that is made in a comunication list'''
    ret_vector = [] # list that returns a once occurred request and its response
    services_occurred = [] # list to store services that have already been found
    
    for item in full_vector:
        service = item[0][2] # getting just the service
        if not service in services_occurred: # if service was not found yet
            services_occurred.append(service) # record this service occurrence
            ret_vector.append(item) # store request and response
       
    return ret_vector



def req_and_res(full_vector):
    
    ret_vector = []
    aux = []
    # getting just even positions Ex: 0,2,4,...
    only_requests = full_vector[::2]
    # getting just odd positions Ex: 1,3,5,...
    only_responses = full_vector[1::2]
    
    #===========================================================================
    # ''' List fix: Remove last line if there is more requests
    # than responses'''
    # 
    # if not len(only_requests) == len(only_responses):
    #     print('Full vec size: ' + str(len(full_vector)))
    #     print('requests vec size: ' + str(len(only_requests))+ '  '+ 'responses vec size: ' + str(len(only_responses))) 
    #     print("different lists sizes")
    #     print("removeing last position from requests vector (cap file)")
    #     only_requests.pop()
    #===========================================================================
        
    
    # creating a list with request and its corresponding response per list item
    for position, request_element in enumerate(only_requests):
        #print (request_element)
        #print (only_responses[position])
        aux.append(request_element)
        aux.append(only_responses[position])
        ret_vector.append(list(aux))
        # Cleaning aux
        del aux[:]
        
    
    return ret_vector

def line_adjust(line):
    ''' Return a list without not useful separators'''
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


def adjust_list(list_to_adjust):
    '''Sometimes list is a bad format.
    Thus, is necessary to treat it in manner to make it useful to extract 
    data from it'''

    ''' Remove first line if it is not a service or valid line
    In this case it is checking if first char is a number.
    If it does not, remove first line'''
    # if the first line from file dados.txt is not valid pop it
    if not list_to_adjust[0][0].isdigit(): # Check if the first position in first line is a digit Ex: . (first line is just a point)
        list_to_adjust.pop(0) # if not pop the first line


    ''' Check if first line is a service or a response. If it is a response pop it.'''
        
    new_first_line = line_adjust(list_to_adjust[0])
    response_values = ['4','5','6','7'] # values with third bit enable Ex: 0101
    if new_first_line[2][0] in response_values: # Check if the first position in first line is a request
        list_to_adjust.pop(0) # if not pop the first line
    
    ''' Check if list has a even number of positions. If not even, pop last position '''    
    if len(list_to_adjust)%2:
        print("different lists sizes")
        print("removeing last position from requests vector (cap file)") 
        list_to_adjust.pop()
    
    print("Size....: ", len(list_to_adjust))    
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

##########

def main():
    
    # Giving directory path and file name
    path_to_directory = "C:/Users/155 X-MX/Desktop/Preenche Servicos"
    file_name = "dados.txt"
    
    # Getting all lines from file dados.txt
    lines = fileLines(path_to_directory, file_name)
    
    # Leaving list in a treatable format
    lines = adjust_list(lines)
    
    # Lists
    cleaned_line = []
    positions = []
    
    # List of lists. Each position is a list that contains line informations from dados.txt 
    #===============================================================================
    # for i in lines:
    #     print (i)
    #===============================================================================
    
    
    final_list = clean_all_lines(lines)
    
    print("Linhas a serem analisadas:")
    for b,i in enumerate(final_list):
        print (i,b)
    
    ######
    
    # getting just even positions Ex: 0,2,4,...
    only_requests = final_list[::2]
    # getting just odd positions Ex: 1,3,5,...
    only_responses = final_list[1::2]
    
    
        
    
    #####
    vec_req_and_res = req_and_res(final_list)
    if vec_req_and_res == 0:
        print('finishing app....')
        quit()
        
    vec_req_and_res = occurred_cases2(vec_req_and_res)
    req_vector = []
    
    for i in vec_req_and_res:
        req_vector.append(i[0][2])
        #print (i[0][2])
    
    for i in req_vector:
        print (i)    
    
    # Getting requests that already occurred
    # open file
    data_folder = Path("C:/Users/155 X-MX/Desktop/")
    file_to_open = data_folder / "occurred requests.txt"
    requests_already_got = []
    #checking if the file already exists
    if os.path.isfile(file_to_open): 
        f = open(file_to_open,"r")
        
        # Getting all lines    
        requests_already_got = f.readlines()
        
        f.close() 
    
    # recording cases in a file
    
    # open file
    data_folder = Path("C:/Users/155 X-MX/Desktop/")
    file_to_open = data_folder / "occurred requests.txt"
    f = open(file_to_open,"a")
     
    for line in req_vector:
        # checking if the request already occurred
        # if not, insert this request at file occurred requests.txt
        if not line+'\n' in requests_already_got:
            # wrinting line to the file
            str_line = line + '\n'
            f.write(str_line)
     
    # closing file
    f.close() 
    
    
    # open file
    #occurred_cases2(vec_req_and_res)
    data_folder = Path("C:/Users/155 X-MX/Desktop/")
    file_to_open = data_folder / "req_res.txt"
    f = open(file_to_open,"a")
     
    for line in vec_req_and_res:
        # wrinting line to the file
        if not str(line[0][2])+'\n' in requests_already_got:
            str_line = 'req: '+str(line[0][2])+' res: '+str(line[1][2])+'\n'
            print('Inserting: ',line[0][2])
            f.write(str_line)
     
    # closing file
    f.close()  

if __name__ == "__main__":
    main()
        
