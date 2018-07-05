import shutil
from pathlib import Path
from os.path import isfile
from os import remove, rename, chdir, getcwd, makedirs, listdir, path
from subprocess import  run, PIPE
from second import line_adjust, adjust_list

def frames_can(file_name):
    ''' *** '''
    # remove file captura.txt
    dest_path = Path("D:/sand_box/FramesCAN")
    cap_file = dest_path / "captura.txt"
    if isfile(cap_file):
        print("Removing file: captura.txt")
        remove(cap_file)
    
    # Coping file to framesCAN directory
    source_path = Path("D:/sand_box/cap_files/txt_files")
    
    file_path = source_path / file_name
    
    dest_path = Path("D:/sand_box/FramesCAN")
    shutil.copy(file_path, dest_path)
    print(".txt file copied!")
    
    # Renaming .txt file to captura.txt
    old_name = dest_path / file_name
    new_name = dest_path / "captura.txt"
    
    rename(old_name, new_name)
    print(".txt file renamed!")
    
    
    # Changing directory to execute FramesCAN.exe
    
    main_dir = getcwd()
    
    chdir("D:/sand_box/FramesCAN")
    
    # Executing FramesCan.exe
    
    program_dir_path = Path("D:/sand_box/FramesCAN")
    program_path = program_dir_path / "FramesCAN.exe"
    
    FramesCAN_return = run([str(program_path)], shell=True, stdout=PIPE)
    print("FramesCAN ran!")
    print("\n\nFramesCAN output:\n\n", FramesCAN_return.stdout)
    
    # Changing directory to root
    
    chdir(main_dir)

def scanner_module_address(cap_file_txt):
    """Identify the address used by the scanner and the module
        Receives full path to a txt cap file after it be processed by FramesCAN.exe
        Return scanner and module addresses"""
    requester_address = ""
    responser_address = ""
    lines = open(cap_file_txt,"r").readlines()
    lines = adjust_list(lines)
    addresses_not_found = True
    iter_lines = iter(lines)
    ended_iteration = True
    
    while addresses_not_found and ended_iteration:
        try:
            line = next(iter_lines)            
        except StopIteration:
            ended_iteration = False
        else:
            line = line_adjust(line)
            address = line[0][:-1]
            # check if there is a service in this line address
            # list of responses 
            response_values = ['4','5','6','7','C','D','E','F'] # values with third bit enable Ex: 0101
            
            if not line[2][0] in response_values: # Check if line is a request
                requester_address = address
            else:
                responser_address = address
                
            if requester_address and responser_address:
                print("\nrequester/scanner address number: ",requester_address,
                      "\nresponse/module address number: ",responser_address,'\n')
                addresses_not_found = False
                
    return requester_address, responser_address
            
             
def mec():
    dir_files = listdir("D:/sand_box/FramesCAN/test")
    
    if not path.isdir("D:/sand_box/FramesCAN/test/fixed"):
        print("Missing fixed directory...")
        print("Missing fixed files...")
        print("Creating directory fixed...")
        makedirs("D:/sand_box/FramesCAN/test/fixed")
            
    for f in dir_files:
        print(f)
        f_lines = open("D:/sand_box/FramesCAN/test/" + f,"r").readlines()
        num_lines = len(f_lines)
        print("lines number from file: ",num_lines)
        i = 1
        while num_lines > i:
            if f_lines[i-1][0:3] == f_lines[i][0:3]:
                print(f_lines[i-1])
                print(f_lines[i])
            i+=1
            
    
    
if __name__ == "__main__":  
    #===========================================================================
    # file_name = "ApagaMemoria.txt"  
    # frames_can(file_name)
    #===========================================================================
    scanner_module_address("D:/sand_box/FramesCAN/test/LeiturasMotorLigado.txt")
    #scanner_module_address("D:/sand_box/FramesCAN/test/SpecialFunction_Calibration.txt")
    #mec()



