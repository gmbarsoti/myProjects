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
        print(self.communication_lines[3462])
        
    def get_communication(self):
        return self.communication_lines

def generate_xml(cap_file):
    data_folder = Path("D:/sand_box/")
    program_path = data_folder / "ProtocolAnalyzerSaveXml.exe"
    
    data_folder = Path("D:/sand_box/")
    
    cap_path = data_folder / cap_file
    print(program_path)
    print (cap_path)
    run([str(program_path),str(cap_path)], stdout=PIPE)



def xml_treatment():
    data_folder = Path("D:/sand_box/")
    program_path = data_folder /  "InitGscan.xml"
    
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
    
    
def main():
    
    cap_file = "InitGscan.ctec"
    generate_xml(cap_file)
    
    xml_dict, com_list = xml_treatment()
    a_class = captured_config(xml_dict, com_list)
    a_class.printInfo()
    
    # Putting communication in a file
    if not os.path.isdir("D:/sand_box/output"):
        print("Creating directory output...")
        os.makedirs("D:/sand_box/output")
        
    f = open("D:/sand_box/output/cap.txt","a")
    l = a_class.get_communication()
    line_to_write = (l[0]["Time"] + " " + l[0]["Count"] + " "  + 
                     l[0]["Format"] + " "  + l[0]["Id"] + " "  + 
                     str(l[0]["Data"]).replace(',','.') + "\n") 
    f.write(line_to_write)
    f.close()
    
if __name__ == "__main__":
    main()