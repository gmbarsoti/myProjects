import os


def creating_dirs():
        
    if not os.path.isdir("./../cap_files"):
        print("Missing cap_file directory...")
        print("Missing captured files...")
        print("Creating directory cap_files...")
        os.makedirs("./../cap_files")
    
    
    if not os.path.isdir("./../cap_files/xml_files"):
        print("Missing xml_files directory...")
        print("Missing xml files...")
        print("Creating directory xml_files...")
        os.makedirs("./../cap_files/xml_files")
            

    if not os.path.isdir("./../cap_files/txt_files"):
        print("Creating directory txt_files...")
        os.makedirs("./../cap_files/txt_files")
        
    if not os.path.isdir("./../output"):
        print("Creating directory output...")
        os.makedirs("./../output")


 
if __name__ == "__main__":
    creating_files()