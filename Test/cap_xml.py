'''
Created on 25 de jun de 2018

@author: 155 X-MX
'''
from subprocess import run, PIPE
from pathlib import Path
import xml.etree.ElementTree as ET
import os



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

def generate_xml(cap_file):
    
    root_path = Path("D:/sand_box/")
    program_path = root_path / "ProtocolAnalyzerSaveXml.exe"
    
    
    cap_files_path = Path("D:/sand_box/cap_files/")
    cap_path = cap_files_path / cap_file
    
    run([str(program_path),str(cap_path)], stdout=PIPE)



def xml_treatment(xml_file_name):
    print("Parsing XML file: ", xml_file_name)
    
    data_folder = Path("D:/sand_box/cap_files/xml_files/")
    program_path = data_folder /  xml_file_name
    
    tree = ET.parse(program_path)
    root = tree.getroot()
    
    
    xml_dict = {}
    config_node = root.find('Config')
    for iterator_note in config_node[1].iter():
        if not str(iterator_note.text) == "None":
            xml_dict[iterator_note.tag] = iterator_note.text
    # Number of lines
    xml_dict["Total_lines"] = config_node.find("Total").text
    
    # Get communication lines
    
    data_node = root.find("Data")
    
    # list to store communication lines
    com_list = []
    # list to store one communication
    one_com_dict = {}
    
    for item_node in data_node:
        for child_node in item_node:
            one_com_dict[child_node.tag] = child_node.text
        com_list.append(dict(one_com_dict)) 
        
    return xml_dict, com_list


def occurred_cases2(full_vector):
    ''' Return a list with just an occurrence of each service request 
    that is made in a comunication list'''
    ret_vector = [] # list that returns a once occurred request and its response
    services_occurred = [] # list to store services that have already been found
    
    for item in full_vector:
        service = item[0][2] # getting just the service
        if not service in services_occurred: # if service was not found yet
            services_occurred.append(service) # record this service occurrence
            ret_vector.append(item) # store request and response
       
    return ret_vector  

def cap_files():
    ''' Return a list with all path to cap files from a specific directory'''
    
    if not os.path.isdir("D:/sand_box/cap_files"):
        print("Missing cap_file directory...")
        print("Missing captured files...")
        print("Creating directory cap_files...")
        os.makedirs("D:/sand_box/cap_files")
   
    all_itens_on_directory = os.listdir("D:/sand_box/cap_files")
    all_cap_path = []
    
    for item in all_itens_on_directory:
        path_to_check = "D:/sand_box/cap_files/" + item
        if os.path.isfile(path_to_check):
            all_cap_path.append(item)
    
    
    return all_cap_path


def xml_files():
    ''' Return a list with all path to xml files from a specific directory'''
   
    all_cap_path = os.listdir("D:/sand_box/cap_files/xml_files")
    return all_cap_path


def move_xml_files():
    if not os.path.isdir("D:/sand_box/cap_files/xml_files"):
        print("Missing xml_files directory...")
        print("Missing xml files...")
        print("Creating directory xml_files...")
        os.makedirs("D:/sand_box/cap_files/xml_files")
            
    dir_files = os.listdir("D:/sand_box/cap_files")
    
    for item in dir_files:
        if item[-3:] == "xml":
            os.rename("D:/sand_box/cap_files/" + item, "D:/sand_box/cap_files/xml_files/" + item)
            
            
def choose_filter():
    """ Choose a specific filter to get a specific communication from cap files """
    choice = ''
    valid_list = ['1','2','3','4','5','6','7']
    while not choice in valid_list:
        choice = input("Choose a filter to use:\n" +
                       "1 - body - 745, 765\n" +
                       "2 - engine - 7E0, 7E8\n" +
                       "3 - cluster - 743, 763\n" +
                       "4- steering - 742, 762\n" +
                       "5 - ABS - 740, 760\n" +
                       "6 - airbag - 752, 772\n"+
                       "7 - ABS_volvo_xc60 - 760, 768\n")
        if not choice in valid_list:
            print("\nChoose a valid option!\n")
    
    
    # Creating a filter to get specific communications
    body = ["745","765"] # Carroceira in Portuguese
    engine = ["7E0","7E8"] # Motor in Portuguese
    cluster = ["743","763"] # Painel in Portuguese
    steering = ["742","762"] # Direcao in Portuguese
    ABS = ["740","760"] 
    airbag = ["752","772"]
    ABS_volvo_xc60 = ["760","768"]
    
    communication_filter = []
    
    if choice == '1':
        communication_filter = body
    elif choice == '2':
        communication_filter = engine
    elif choice == '3':
        communication_filter = cluster
    elif choice == '4':
        communication_filter = steering
    elif choice == '5':
        communication_filter = ABS
    elif choice == '6':
        communication_filter = airbag
    elif choice == '7':
        communication_filter = ABS_volvo_xc60 
        
    return communication_filter

def main():
    
     
    all_cap_files = cap_files()
    
    # Generating all XML files from cap files
    print("Creating XML files from:\n")
    for cap_file in all_cap_files:
        print(cap_file)
        generate_xml(cap_file)
     
    # Moving files to xml directory
    move_xml_files()
     
    # Create a .txt file from each xml file
    
    all_xml_files =  xml_files()
    
    cap_object_list = []
    
    print("\n\nParsing XML files:\n")
    
    for xml_file in all_xml_files:
        xml_dict, com_list = xml_treatment(xml_file)
        cap_object_list.append(captured_config(xml_dict, com_list))
    
    # Putting communication in a file
    
    # Creating output dir
    if not os.path.isdir("D:/sand_box/output"):
        print("Creating directory output...")
        os.makedirs("D:/sand_box/output")

    txt_file_list = []
    
    if not os.path.isdir("D:/sand_box/cap_files/txt_files"):
        print("Creating directory txt_files...")
        os.makedirs("D:/sand_box/cap_files/txt_files")
        
    # Open a .txt file to each xml file 
    for cap_file in all_cap_files:
        txt_file_list.append(open("D:/sand_box/cap_files/txt_files/" + cap_file[:-4] + 'txt',"w"))
    
    # Choose of address communication filter to select specific module from captured files
    communication_filter = choose_filter()
    
    # Wrinting communication (requests and responses) to each .txt file        
    for i, txt_file in enumerate(txt_file_list):
        communication = cap_object_list[i].get_communication()
        # Putting all lines into txt file
        for com in communication:
            if com["Id"] in communication_filter: 
                line_to_write = (com["Format"] + " "  + com["Id"] + "."  + 
                                 str(com["Data"]).replace(',','.') + "\n")
                
                txt_file.write(line_to_write)
        txt_file.close()  
    
        
    input("All .txt files were created!\nPress enter to Continue.")
    
if __name__ == "__main__":
    main()