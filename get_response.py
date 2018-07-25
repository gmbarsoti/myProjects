from request_responses_classes import response_interface_pack
from aux_functions import list_ended, is_a_response, is_negative_response, is_response_pending, is_a_request


def get_response(full_list, list_index):
    
    response_interface_obj = response_interface_pack([],list_index)
    
    if list_ended(full_list, list_index):
        # list has ended
        response_interface_obj.responses.append('cap_file_ended')
        return response_interface_obj
    
    
    line = full_list[list_index]
    
    if not is_a_response(line):
        # resquest without response
        response_interface_obj.responses.append('no_response_-_the_following_communication_is_also_a_request!')
        return response_interface_obj
    
    # found a response
    response_interface_obj.responses.append(line[2])
    
    # skipping negative pending response and tester present communication
    res_or_req = line[2]
    resp_pending = False
    
    if is_negative_response(line):
        if is_response_pending(line):
            # response pending
            resp_pending = True
    
    list_not_ended = True
    
    while resp_pending and list_not_ended:
        # case that response have to wait (response 7F.XY.78 - 78 means response is pending) and skip its tester present communication    
        list_index += 1 # go to next line
        
        if list_ended(full_list, list_index):
            # list has ended
            response_interface_obj.responses.append('cap_file_ended')
            list_not_ended = False
            
        else:
            
            line = full_list[list_index]
            res_or_req = line[2]

            if res_or_req == '3E.01.': 
                # ignoring tester present
                pass
        
            elif not res_or_req[0:2] == '7F':
                
                #print('Pending response found')
                response_interface_obj.responses.append(res_or_req)
            
                resp_pending = False
                
                list_index += 1
            
            elif is_a_request(line):
                #print('Pending response not found')
                resp_pending = False
                # resquest without response
                response_interface_obj.responses.append('no_response_-_the_following_communication_is_also_a_request!')
                # don't go to the next list item        
    
    response_interface_obj.list_index = list_index
    
    return response_interface_obj
