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




#===============================================================================
# def get_next_line():
#     global next_line_index 
# 
#     if next_line_index>total_lines-1:
#         print('end_of_file')
#         return -1
#     line = lines[next_line_index]
#     next_line_index+=1
#     return line.split('.')
#     
#===============================================================================
    
    
#===============================================================================
# def get_all_data_sent(data_sent, bytes_lenght, line):
#     global max_data_bytes_in_frame
#     
#     #all data got from the flow
#     got_data = 0
#     
#     #getting the firsts five bytes
#     for byte in line[4:9]:
#         data_sent.append(byte)
#         
#     got_data+=5
#     
#     # all missing data to still be got    
#     data_to_get = bytes_lenght - got_data
#     
#     # looking for first frame from data flow with starts with '20'
#     while not line[2] == '20':
#         line = get_next_line() #skip line with control flow
#     
#     # calculating how many frames/lines will come in data flow
#     num_lines_to_check = 0
#     
#     #there are 6 bytes per frame/line
#     if data_to_get%max_data_bytes_in_frame > 0:
#         # plus one if the last frame has less than 6 bytes of data
#         num_lines_to_check = int(data_to_get/max_data_bytes_in_frame) + 1
#     else:  
#         num_lines_to_check = int(data_to_get/max_data_bytes_in_frame)
#    
# 
#     frame_bytes = 0
#     if (data_to_get) > max_data_bytes_in_frame:
#         frame_bytes = max_data_bytes_in_frame
#     else:
#         frame_bytes = bytes_lenght - got_data
#         
#     if not (num_lines_to_check+next_line_index) > total_lines:
#         for num_line_to_check in range(num_lines_to_check):
#                     
#             for byte in line[3:3+(frame_bytes)]:
#                 data_sent.append(byte)
#                 
#             data_to_get-=frame_bytes
#             
#             got_data+=frame_bytes
#             
#             if (data_to_get) > max_data_bytes_in_frame:
#                 frame_bytes = max_data_bytes_in_frame
#             else:
#                 frame_bytes = data_to_get
#                 
#             # get next line only while it will be used inside this function
#             if  not num_line_to_check == num_lines_to_check-1:  
#                 line = get_next_line()
#     else:
#         return -1
#===============================================================================
        
#===============================================================================
# class communication():    
#     def __init__(self, com_standard, sender_addr, addr_byte, size_byte, line):
#         self.com_standard = com_standard
#         self.sender_addr = sender_addr
#         self.addr_byte = addr_byte
#         self.size_byte = size_byte
#         self.data_sent = []
#         self.first_size_byte = int(size_byte,16)
#         self.bytes_lenght = 0
#         self.byte_lenght(line)
#         self.get_data_sent(line)
#         
#         
#     def byte_lenght(self, line):
#         if self.first_size_byte < 0x10:
#             # it is the only size byte
#             self.bytes_lenght = self.first_size_byte
#         else:
#             # 3 size nibbles
#             first_nibble = line[2][1]
#             second_and_third_nibbles = line[3]
#             three_nibbles = first_nibble + second_and_third_nibbles 
#             self.bytes_lenght = int(three_nibbles,16)
#         
#     def get_data_sent(self, line):
#         # Analysing first size byte
#         # isn't flow control
#         if self.first_size_byte < 0x10:
#             # it is the only size byte
#             for byte in line[3:3+self.bytes_lenght]:
#                 self.data_sent.append(byte)
#             line = get_next_line()
#             print('next: ',line)
#             if line == -1:
#                 return -1    
#         # it is a flow of data bytes
#         else:
#             # 3 size nibbles
#             get_all_data_sent(self.data_sent, self.bytes_lenght, line)
#===============================================================================

        
def invalid_initial_communication(line):
    print(line)
    size_byte = line[2]
    first_size_byte = int(size_byte,16)
    
    if first_size_byte > 0x1F:
        return True
    else:
        return False
             
        
#===============================================================================
# def mount_obj_communication(line):
# 
#     while invalid_initial_communication(line):
#         line = get_next_line()
#         if line == -1:
#             return -1
#     
#      
#     print('valid: ', line)
#     #open txt file created from xml
#     
#     #lines pattern
#     #Xd 18CEFA21.F1.23.00.00.00.00.00.00.
#     
#     #xd is the communication standard
#     com_standard = line[0][:2]
#     #18CEFA21 is address that set the following bytes
#     sender_addr = line[0][3:]
#     # F1 is a address byte
#     addr_byte = line[1]
#     # 23 is size byte or multiple frame byte controller (bytes from 20 to 29 and 30)
#     data_sent = []
#     
#     size_byte = line[2]
#     first_size_byte = int(size_byte,16)
#     
#     com_obj = communication(com_standard, sender_addr, addr_byte, size_byte, line)
#     
#     print('data lenght: ',com_obj.bytes_lenght)
#     
#     print('dados enviados: ', com_obj.data_sent)
#     
#     return com_obj
#===============================================================================

#===============================================================================
# 
# def main():
# 
#     f = open('test.txt','r')
#     
#     # global variables
#     max_data_bytes_in_frame = 6
#     next_line_index = 0
#     
#     lines = []
#     lines = f.readlines()
#     
#     total_lines = len(lines)
#     
#     first_line = lines[next_line_index].split('.')
#     
#     end_of_file = False
#     
#     com_obj_list = []
#     
#     while not end_of_file:
#         print('first: ', first_line)
#         com_obj = mount_obj_communication(first_line)
#         
#         
#         if (com_obj == -1) or (next_line_index == total_lines):
#             end_of_file = True
#             print('End of file')
#         else:
#             com_obj_list.append(com_obj)
#             first_line = lines[next_line_index-1].split('.')
#             
#     with open('output.txt','w') as output_file: 
#         for com_obj in com_obj_list:
#             output_file.write(com_obj.sender_addr + '. ' + str(com_obj.bytes_lenght) + '. ')
#             for byte in com_obj.data_sent:
#                 output_file.write(byte + '.')
#             output_file.write('\n')
#             
#===============================================================================

def main2():
    
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
    main2()