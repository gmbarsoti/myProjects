class data_packet():
    def __init__(self, data_length, data, source_address):
        self.data_length = data_length
        self.data = data
        self.source_address = source_address
        self.is_complete = False
    

def get_next_frame(frames_list, frames_list_index):
    
    end_of_list_reached = False
    frame = ''
                
    #checking if end of list was reached
    try:
        frame = frames_list[frames_list_index[0]]
    except IndexError:
        end_of_list_reached = True
        
    if not end_of_list_reached:
        frames_list_index[0] += 1
        return frame.split('.')
    else:
        #end of file was reached
        return -1


def is_request_first_frame(frame):
    req_or_res = ''
    requests_values = ['0','1','2','3','8','9','A','B']
    frame_length = 0
    
    #first size byte can be 0X, 1X, 2X or 3X
    frame_type = frame[2][0]
    
    #===========================================================================
    # Single frame          0
    # First frame           1
    # Consecutive frame     2
    # Flow control frame    3
    #===========================================================================
    
    if (frame_type == '0'):
        # Single frame 
        req_or_res = frame[3]
        frame_length = int(frame[2][1],16)
    elif (frame_type == '1'):
        # First frame      
        req_or_res = frame[4]
        # Length of 3 nibbles
        frame_length = int(frame[2][1]+frame[3][0]+frame[3][1],16)
    else:
        #this frame is not a initial frame of a request or response
        return (False,frame_length)
    
    #first nibble of a request or a response
    request_response_id = req_or_res[0]
    
    if (request_response_id in requests_values) or not (request_response_id in requests_values):
        return (True,frame_length)
    else:
        return (False,frame_length)
    
    
    
def get_consecutive_frame(frames_list, frames_list_index, data_packet_length):
    internal_frames_index = frames_list_index
    end_of_file = False
    bytes_per_frame = 6
    amount_of_frames_to_find = 0 
    all_frames_found = False
    rest_of_data = []
    
    
    # five is the amount of data that is in the first frame
    last_frame_bytes_amount = (data_packet_length - 5) % bytes_per_frame
    if (last_frame_bytes_amount > 0):
        amount_of_frames_to_find = ((data_packet_length - 5)//bytes_per_frame) + 1
    else:
        amount_of_frames_to_find = ((data_packet_length - 5)//bytes_per_frame)
    
    
    while((not end_of_file) and (not all_frames_found)):
        
        frame = get_next_frame(frames_list, internal_frames_index)
        
        if (frame == -1):
            end_of_file = True
        else:
            #checking if it is consecutive frame 2X
            if (frame[2][0] == '2'):
                #one consecutive frame found

                # concatenating frames
                if (amount_of_frames_to_find == 1):
                    rest_of_data+=frame[3:last_frame_bytes_amount+3] #-1 removes \n
                else:
                    rest_of_data+=frame[3:-1] #-1 removes \n
                
                
                #checking if all frames were gotten
                amount_of_frames_to_find-=1 
                if amount_of_frames_to_find == 0:
                    all_frames_found = True                                        
    
    if all_frames_found:
        return rest_of_data
    
    if end_of_file:
        return -1 


def find_first_request(frames_list, frames_list_index):
    end_of_file = False
    req_found = False
    first_frame = ''
    data_packet_length = 0
    data_from_data_packet = []
    addr = ''
    first_frame_data = ''
    
    
    while((not end_of_file) and (not req_found)):
        first_frame = get_next_frame(frames_list, frames_list_index)
        if (first_frame == -1):
            end_of_file = True
        else:
            ret = is_request_first_frame(first_frame)
            verification = ret[0]
            data_packet_length = ret[1]
            if(verification):
                req_found = True
    

    if req_found:
        if data_packet_length <= 6:
            first_frame_data = first_frame[3:data_packet_length+3]
            data_from_data_packet = first_frame_data
            
        else:
            first_frame_data = first_frame[4:-1]
            #necessary to get the rest of data
            rest_of_data = get_consecutive_frame(frames_list, frames_list_index, data_packet_length)
            if rest_of_data == -1:            
                #end_of_file was reached
                return -1 
            else:
                data_from_data_packet = first_frame_data + rest_of_data
        
           
    
        addr = first_frame[0]+'.'+first_frame[1]+'.'        
        return (addr, data_packet_length, data_from_data_packet)
    else:
        #file ended and request not found
        return -1 
    
    
def invalid_initial_communication(line):
    print(line)
    size_byte = line[2]
    first_size_byte = int(size_byte,16)
    
    if first_size_byte > 0x1F:
        return True
    else:
        return False
    
def framesCAN_extended_address():
    
    frames_list_index = [0]
    
    f = open('captura.txt','r')
    frames = f.readlines()
    
    with open('dados.txt','w') as output_file:
        
        ret  = find_first_request(frames, frames_list_index)
        while not ret == -1:
            
            data_in_str = ''
            if not ret == -1:
                for byte_data in ret[2]:
                    data_in_str += byte_data+'.'
                
                    framesCAN_line = ret[0][3:-3]+' '+str(ret[1])+'. '+data_in_str+'\n'
            
                #print(framesCAN_line, end='')
                output_file.write(framesCAN_line)
            ret  = find_first_request(frames, frames_list_index)
        
            
if __name__ == "__main__":
    framesCAN_extended_address()