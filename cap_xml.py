from subprocess import run, PIPE
from pathlib import Path
import xml.etree.ElementTree as ET
import os
import shutil
from request_responses_classes import captured_config



def generate_xml(cap_file):
    
    root_path = Path("./")
    program_path = root_path / "ProtocolAnalyzerSaveXml.exe"
    
    
    cap_files_path = Path("./../cap_files/")
    cap_path = cap_files_path / cap_file
    
    run([str(program_path),str(cap_path)], stdout=PIPE)



def xml_treatment(xml_file_name):
    #print("Parsing XML file: ", xml_file_name)
    
    data_folder = Path("./../cap_files/xml_files/")
    file_path = data_folder /  xml_file_name
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    #===========================================================================
    # print(xml_file_name)
    # node = root.find('Config').find('CAN').find('Filter').findall('Item')
    # for info_addr in node:
    #     print(info_addr.find('Id').text)
    # 
    #===========================================================================
    
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
    
    if data_node == None:
        return xml_dict, com_list
    
    for item_node in data_node:
        for child_node in item_node:
            one_com_dict[child_node.tag] = child_node.text
        com_list.append(dict(one_com_dict)) 
        
    return xml_dict, com_list


def cap_files():
    ''' Return a list with all path to cap files from a specific directory'''
    
    if not os.path.isdir("./../cap_files"):
        print("Missing cap_file directory...")
        print("Missing captured files...")
        print("Creating directory cap_files...")
        os.makedirs("./../cap_files")
   
    all_itens_on_directory = os.listdir("./../cap_files")
    all_cap_path = []
    
    for item in all_itens_on_directory:
        path_to_check = "./../cap_files/" + item
        if os.path.isfile(path_to_check):
            all_cap_path.append(item)
    
    
    return all_cap_path


def xml_files():
    ''' Return a list with all path to xml files from a specific directory'''
   
    all_cap_path = os.listdir("./../cap_files/xml_files")
    return all_cap_path


def move_xml_files():
    if not os.path.isdir("./../cap_files/xml_files"):
        print("Missing xml_files directory...")
        print("Missing xml files...")
        print("Creating directory xml_files...")
        os.makedirs("./../cap_files/xml_files")
            
    dir_files = os.listdir("./../cap_files")
    
    for item in dir_files:
        if item[-3:] == "xml":
            shutil.move("./../cap_files/" + item, "./../cap_files/xml_files/" + item)
            
def custom_filter_insert():

    scanner_addr = input("Please insert SCANNER address:\n")
    module_addr = input("Please insert MODULE address:\n")
    
    scanner_addr = scanner_addr.upper()
    module_addr = module_addr.upper()
    
    scanner_module_addr_code = [scanner_addr,module_addr]
    
    
    return scanner_module_addr_code
    
    
    
def choose_filter():
    """ Choose a specific filter to get a specific communication from cap files """
    choice = ''
    valid_list = ['0','1','2','3','4','5','6','7']
    while not choice in valid_list:
        choice = input("Choose a filter to use:\n\n" +
                       "0 - Insert custom filter\n"+
                       "1 - body - 745, 765\n" +
                       "2 - engine - 7E0, 7E8\n" +
                       "3 - cluster - 743, 763\n" +
                       "4 - steering - 742, 762\n" +
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
    
    if choice == '0':
        communication_filter = custom_filter_insert()
    elif choice == '1':
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


def cap_to_txt_xml():
     
    all_cap_files = cap_files()
    
    # Generating all XML files from cap files
    print("Creating XML files...")
    for cap_file in all_cap_files:
        generate_xml(cap_file)
     
    # Moving files to xml directory
    move_xml_files()
     
    # Create a .txt file from each xml file
    
    all_xml_files =  xml_files()
    
    cap_object_list = []
    
    print("\n\nParsing XML files.\n")
    
    for xml_file in all_xml_files:
        xml_dict, com_list = xml_treatment(xml_file)
        cap_object_list.append(captured_config(xml_dict, com_list))
    
    # Putting communication in a file
    
    # Creating output dir
    if not os.path.isdir("./../output"):
        print("Creating directory output...")
        os.makedirs("./../output")

    txt_file_list = []
    
    if not os.path.isdir("./../cap_files/txt_files"):
        print("Creating directory txt_files...")
        os.makedirs("./../cap_files/txt_files")
        
    # Open a .txt file to each xml file 
    for cap_file in all_cap_files:
        txt_file_list.append(open("./../cap_files/txt_files/" + cap_file[:-4] + 'txt',"w"))
    
    # Choose of address communication filter to select specific module from captured files
    communication_filter = choose_filter()
    
    # Writing communication (requests and responses) to each .txt file        
    for i, txt_file in enumerate(txt_file_list):
        communication = cap_object_list[i].get_communication()
        # Putting all lines into txt file
        for com in communication:
            if com["Id"] in communication_filter: 
                line_to_write = (com["Format"] + " "  + com["Id"] + "."  + 
                                 str(com["Data"]).replace(',','.') + "\n")
                
                txt_file.write(line_to_write)
        txt_file.close()  
    
    print("\nAll .txt files from cap files were created!")   

 
if __name__ == "__main__":
    cap_to_txt_xml()