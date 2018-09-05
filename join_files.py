from os import listdir
from os.path import isfile
#open files
#get lines
#record lines in captura.txt file

def copylines(path_to_source_file, target_file):
    
    source_file = open(path_to_source_file, 'r')
    all_lines = source_file.readlines()
    
    for line in all_lines: 
        target_file.write(line)
    
    source_file.close()


def join_files():
    
    target_file = open("./../output/captura.txt", 'w')

    all_cap_files = listdir("./../cap_files/txt_files")
    
    for file_name in all_cap_files:
        path_to_source_file = "./../cap_files/txt_files/" + file_name
        if isfile(path_to_source_file):
                    
            copylines(path_to_source_file, target_file)
    
    target_file.close()
            
            
            
            
if __name__ == '__main__':
    join_files()
            
            