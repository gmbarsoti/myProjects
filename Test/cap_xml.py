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



def xml_treatment():
    data_folder = Path("D:/sand_box/")
    program_path = data_folder /  "Leitutas.xml"
    
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
    print(data_node[0][0].tag)
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
   
    all_cap_path = os.listdir("D:/sand_box/cap_files")
    return all_cap_path

def move_xml_files():
    dir_files = os.listdir("D:/sand_box/cap_files")
    
    for item in dir_files:
        if item[-3:] == "xml":
            os.rename("D:/sand_box/cap_files/" + item, "D:/sand_box/cap_files/xml_files/" + item)

def main():
    
    #cap_file = "Leitutas.ctec"
    
    all_cap_file = cap_files()
    
    for cap_file in all_cap_file:
        print(cap_file)
        generate_xml(cap_file)
    
    move_xml_files()
    input()
    cap_file = "Leitutas.ctec"    
    generate_xml(cap_file)
    
    xml_dict, com_list = xml_treatment()
    a_class = captured_config(xml_dict, com_list)
    a_class.printInfo()
    
    # Putting communication in a file
    if not os.path.isdir("D:/sand_box/output"):
        print("Creating directory output...")
        os.makedirs("D:/sand_box/output")
    
    
    
    for cap_file in all_cap_file:
        f = open("D:/sand_box/output/" + cap_file,"a")
        
    f = open("D:/sand_box/output/cap.txt","a")
    communication = a_class.get_communication()
    
    
    
    # Putting all lines to the main file
    for com in communication:
        line_to_write = (com["Format"] + " "  + com["Id"] + "."  + 
                     str(com["Data"]).replace(',','.') + "\n") 
        f.write(line_to_write)
    f.close()
    #===========================================================================
    # line_to_write = (l[0]["Time"] + " " + l[0]["Count"] + " "  + 
    #                  l[0]["Format"] + " "  + l[0]["Id"] + " "  + 
    #                  str(l[0]["Data"]).replace(',','.') + "\n") 
    #===========================================================================
if __name__ == "__main__":
    main()