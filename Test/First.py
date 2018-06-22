'''
Created on 7 de jun de 2018

@author: 155 X-MX
'''

#Fixing file path and opening file

from pathlib import Path

class capture_header:
    captor = "Unknow" #who did the capture
    user = "Unknow" 
    os = "Unknow" # Operating System used to do the capture
    date = "Unknow"
    time = "Unknow"
    
    def __init__(self, **cap_info):
        if len(cap_info) == 0:
            print("Missing parameters to class capture")
        else:
            if 'captor' in cap_info: 
                self.captor = cap_info['captor']
            if 'user' in cap_info:
                self.user = cap_info['user']
            if 'os' in cap_info:
                self.os = cap_info['os']
            if 'date' in cap_info:
                self.date = cap_info['date']
            if 'time' in cap_info:
                self.time = cap_info['time']
            
    def printInfo(self):
        print("Captor: ", self.captor)
        print("User: ", self.user)
        print("Operating System: ", self.os)
        print("Date: ", self.date)
        print("Time: ", self.time)
    
def fileLines():
    data_folder = Path("C:/Users/155 X-MX/Desktop")
     
    file_to_open = data_folder / "captura.txt"
     
    f = open(file_to_open,"r")
     
    if not file_to_open.exists():
        print("Oops, file doesn't exist!")
    else:
        print("Yay, the file exists!")
         
    #f.seek(0)
    # Getting all lines    
    all_lines = f.readlines()
    return all_lines


def main():

    # Getting file lines
    all_lines = fileLines()
    
    # Getting header
    firstLines = all_lines[0]
    
    # Getting data from headers
    words = firstLines.split(" ")
    date = words[3]
    time = words[4]
    user = words[7] + " " + words[8]
    captor = words[10]
    os = words[12]
    
    cap = capture_header(user = user, captor = captor, os = os, date = date, time = time)
    cap.printInfo()
    
    # Communication lines
    # Ex: Sd 7E0.02.3E.01.00.00.00.00.00.
    addr_pattern = all_lines[1].split(" ")[0]
    bytes_sent = all_lines[1].split(" ")[1]
    data_list = bytes_sent.split(".")
    addr_sender = data_list[0]
    num_of_bytes = data_list[1]
    print (addr_pattern)
    print (addr_sender)
    print (num_of_bytes[0])
    
    # Data size rules
    if num_of_bytes[0] == "0":
        # Next nibble is the num of data
        position_of_last_data = int(num_of_bytes[1]) + 1
        data = data_list[2:position_of_last_data] # 2:-1 to get only data
        print (data)    
        
    #===========================================================================
    # cap_info = []
    # cap_info.append(captor)
    # cap_info.append(user)
    # cap_info.append(os)
    # print (cap_info[1])
    # #print (cap_info)
    #===========================================================================
    #===========================================================================
    # cap = capture(cap_info)
    # cap.printInfo() 
    # print(os)
    # print (words)
    # print (firstLines)
    #===========================================================================
    
if __name__== "__main__":
    main()
