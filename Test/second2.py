'''
Created on 12 de jun de 2018

@author: 155 X-MX
'''
from pathlib import Path
import os.path
from os import listdir
from os.path import isfile

class request_response:
    request = ''
    response = ''
    def __init__(self, req, resp):
        self.request = req
        self.response = resp
        
    def print_req_resp(self):
        print("Request: ", self.request)
        print("Response: ", self.response)

class request_responses:
    request = ''
    responses = []
    def __init__(self, req, resp):
        self.request = req
        self.responses = resp
        
    def print_req_resp(self):
        print("Request: ", self.request)
        print("Responses: ")
        for resp in self.responses:
            print(resp)
        
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


def occurred_cases3(req_res_class_list):
    
    ''' Returna list with just an occurrence of each service request 
    that is made in a comunication list'''
    filtered_req_res_list = [] # list that returns a once occurred request and its response
    services_occurred = [] # list to store services that have already been found
    
    for item in req_res_class_list:
        req = item.request # getting just the service
        if not req in services_occurred: # if service was not found yet
            services_occurred.append(req) # record this service occurrence
            
            filtered_req_res_list.append(item) # store request and response
       
    return filtered_req_res_list


def occurred_cases4(req_res_class_list2):
    
    ''' Returna list with just an occurrence of each service request 
    that is made in a comunication list'''
    filtered_req_res_list = [] # list that returns a once occurred request and its response
    services_occurred = [] # list to store services that have already been found
    
    for item in req_res_class_list2:
        
        req = item.request # getting just the service
    
        if req in services_occurred: # if service was already found
            if req == '19.02.20.':
                print(req)
            elem_pos = services_occurred.index(req) # getting position
            resp = item.responses[0]
            # Appending different response to a request 
            if not resp in filtered_req_res_list[elem_pos].responses:
                filtered_req_res_list[elem_pos].responses.append(resp)
        
        if not req in services_occurred: # if service was not found yet
            services_occurred.append(req) # record this service occurrence
            
            filtered_req_res_list.append(item) # store request and response
            
        
       
    return filtered_req_res_list



def req_and_res(full_vector):
    """Return a list with a request and a response per item in list"""
    
    ret_vector = []
    aux = []
    
    # getting just even positions Ex: 0,2,4,...
    only_requests = full_vector[::2]
    
    # getting just odd positions Ex: 1,3,5,...
    only_responses = full_vector[1::2]
    
    # creating a list with requests and its corresponding responses per item in list
    for position, request_element in enumerate(only_requests):
        aux.append(request_element)
        aux.append(only_responses[position])
        ret_vector.append(list(aux))
        # Cleaning aux
        del aux[:]
        
    
    return ret_vector

def is_a_request(line):
    request_response_id = line[2][0]
    requests_values = ['0','1','2','3','8','9','A','B']
    if request_response_id in requests_values:
        return True
    else:
        return False

def is_a_response(line):
    return not is_a_request(line)

def list_ended(list_lenght, list_index):
    if list_index < list_lenght:
        return False
    else:
        return True


def req_and_res_2(full_list):
    """Return a list with a request and a response per item in list
    Based in if third bit is set or not"""

    request_response_list = []
    
    list_index = 0
    list_lenght = len(full_list)
    
    while not list_ended(list_lenght, list_index):
        
        request_response_object = request_responses("",[])
        
        line = full_list[list_index]
        data = line[2]
        
        if is_a_request(line):
            # it is a request
            request_response_object.request = data
            
            list_index += 1
            if list_ended(list_lenght, list_index):
                # list has ended
                request_response_object.responses.append('list_ended')
                pass
            
            else:
                line = full_list[list_index]
            
                if is_a_response(line):
                    
                    data = line[2]
                    
                    # skipping pending responses and tester present
                    while (data == '7F.10.78.' or data == '3E.01.') and (not list_ended(list_lenght, list_index)):
                        # case that response have to wait (response 7F.10.78 - 78 means response is pending) and its tester present communication
                        list_index += 1
                        
                        if list_ended(list_lenght, list_index):
                            pass
                        else:
                            line = full_list[list_index]
                            data = line[2]
                            
                    if list_ended(list_lenght, list_index):   
                        request_response_object.responses.append('list_ended')
                        pass
                    else:
                        response = data
                        request_response_object.responses.append(response)
                        list_index += 1
                
                    
                else:
                    request_response_object.responses.append('no_response_-_the_following_communication_is_also_a_request!')
        else:
            list_index += 1
            # ignoring intial lines thar are not requests
            pass
            
        request_response_list.append(request_response_object)
    
    for i in request_response_list:
        i.print_req_resp()
        print("")
             
    return  request_response_list
               
                                   
                

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
    response_values = ['4','5','6','7','C','D','E','F'] # values with third bit enable Ex: 0101
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

def get_new_services(file_name_after_framesCAN):
    
    # Path to data.txt directory
    path_to_directory_framesCAN = "./FramesCAN/FramesCAN_processed"
    data_txt_file = file_name_after_framesCAN
    
    # Getting all lines from file dados.txt
    lines = fileLines(path_to_directory_framesCAN, data_txt_file)
    
    # if list is empty
    if lines == []:
        return 0
    
    # Leaving lines list in a treatable format
    lines = adjust_list(lines)
    
    # Removing separators in each line
    final_list = clean_all_lines(lines)
    
    print("Lines to be analysed:")
    for b,i in enumerate(final_list):
        print (i,b)
        
        
    a = req_and_res_2(final_list)    
    occurred_cases3(a)
    
    # Organizing requests and responses in a list
    list_req_and_res = req_and_res_2(final_list)
    
    # Check if there was communication
    if list_req_and_res == 0:
        
        pass
        print('No communicaiton found in dados.txt file \nfinishing app....')
        
    else:
        
        # Get just one occurence of each service in communicaton from dados.txt file
        list_req_and_res2 = occurred_cases4(list_req_and_res)
        list_req_and_res = occurred_cases3(list_req_and_res)
        req_vector = []
        
        # Getting just requests
        for req_resp_object in list_req_and_res:
            req_vector.append(req_resp_object.request)#request[0][2])
        
        print("\nRequests occured:\n")
        for i in req_vector:
            print (i)    
        
        # Getting requests that already occurred
        data_folder = Path("./output")
        file_to_open = data_folder / "occurred_requests.txt"
        requests_already_got = []
        
        #checking if the file already exists
        if os.path.isfile(file_to_open): 
            
            # if occurred_requests.txt file exists let's read services already registered
            f = open(file_to_open,"r")
            
            # Getting all lines    
            requests_already_got = f.readlines()
            
            f.close() 
        
        # recording cases in a file
        data_folder = Path("./output")
        file_to_open = data_folder / "occurred_requests.txt"
        f = open(file_to_open,"a")
         
        for request in req_vector:
            # checking if the request already occurred
            # if not, insert this request at file occurred requests.txt
            if not request +'\n' in requests_already_got:
                # wrinting line to the file
                str_line = request + '\n'
                f.write(str_line)
         
        # closing file
        f.close() 
        
        
        # file with request and response per line
        data_folder = Path("./output")
        file_to_open = data_folder / "req_res.txt"
        f = open(file_to_open,"a")
         
        for req_and_resp_object in list_req_and_res:
            
            # wrinting line to the file if it doesn't occurred yet
            request = req_and_resp_object.request #str(req_and_resp[0][2])
            
            if not request + '\n' in requests_already_got:
                responses = req_and_resp_object.responses #str(req_and_resp[1][2])
                responses_str = ''
                for resp in responses:
                    responses_str = responses_str + resp + ' - '
                request_response_line = 'req: ' + request + ' res: ' + responses_str + '\n'
                print('Inserting: ', request)
                f.write(request_response_line)
         
        # closing file
        f.close()  


def services_occurrences():
    all_itens_names = listdir("./FramesCAN/FramesCAN_processed")       
    
    for item_name in all_itens_names:
        path_to_check = "./FramesCAN/FramesCAN_processed/" + item_name
        if isfile(path_to_check):
            get_new_services(item_name)
        


if __name__ == "__main__":
    services_occurrences()
        
    