import os

def cleanup():
    #removing xml and txt files from the last execution 
    origin_dir = os.getcwd()
    above_dir = os.path.dirname(origin_dir)
    check_path = above_dir + "\\cap_files"
    os.chdir(check_path)
    
    
    #xml files in cap_files dir
    os.system("del /f *.xml")
    
    
    #txt files in txt_files dir
    os.chdir(check_path + "\\txt_files")
    os.system("del /f *.txt")
    
    
    #xml files in xml_files dir
    os.chdir(check_path + "\\xml_files")
    os.system("del /f *.xml")
    
    os.chdir(origin_dir)



if __name__ == "__main__":
     
    cleanup()