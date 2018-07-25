def list_ended(list_to_test, list_index):
    if list_index < len(list_to_test):
        return False
    else:
        return True

def is_a_request(line):
    request_response_id = line[2][0]
    requests_values = ['0','1','2','3','8','9','A','B']
    if request_response_id in requests_values:
        return True
    else:
        return False

def is_a_response(line):
    return not is_a_request(line)

def is_negative_response(response):    
    if response[2][0:2] == '7F':
        return True
    else:
        return False
        
def is_response_pending(response):
    if response[2][-3:-1] == '78':
        return True
    else:
        return False