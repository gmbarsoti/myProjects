class captured_config:
    Type = "Unknow" 
    PinX = "Unknow" 
    PinY = "Unknow"
    BaudRate = "Unknow"
    Info = "Unknow"
    Total_lines = "Unknow"
    communication_lines = []
    
    def __init__(self, xml_dict, com_list):
        if 'Type' in xml_dict:
            self.Type = xml_dict["Type"]
        if 'PinX' in xml_dict:
            self.PinX = xml_dict["PinX"]
        if 'PinY' in xml_dict:
            self.PinY = xml_dict["PinY"]
        if 'BaudRate' in xml_dict:
            self.BaudRate = xml_dict["BaudRate"]
        if 'Info' in xml_dict:
            self.Info = xml_dict["Info"]
        if 'Total_lines' in xml_dict:
            self.Total_lines = xml_dict["Total_lines"]
        self.communication_lines = com_list
        
            
    def printInfo(self):
        print("Type: ", self.Type)
        print("PinX: ", self.PinX)
        print("PinY: ", self.PinY)
        print("BaudRate: ", self.BaudRate)
        print("Info: ", self.Info)
        print("lines number: ", self.Total_lines)
        print(self.communication_lines[1])
        #print(self.communication_lines[3462])
        
    def get_communication(self):
        return self.communication_lines


class request_responses:
    request = ''
    responses = []
    def __init__(self, req, resp):
        self.request = req
        self.responses = resp
        
    def print_req_resp(self):
        print("Request: ", self.request)
        resp_str = ''
        for resp in self.responses:
            resp_str += resp + ' - '
        resp_str = resp_str[:-3]
        print("Responses: ", resp_str, "\n")
        
        
class response_interface_pack:
    responses = []
    list_index = 0
    def __init__(self, resp, lst_ind):
        self.responses = resp
        self.list_index = lst_ind
    