'''
Created on 4 de jul de 2018

@author: 155 X-MX
'''
from shutil import move, copy
from pathlib import Path
from os.path import isfile, isdir
from os import remove, chdir, getcwd, listdir, makedirs, path
from subprocess import  run, PIPE
import shutil
from Frames_Can_extended_addr import framesCAN_extended_address

def frames_can(file_name, CAN_address_type):
    ''' 1 - Receives name of a .txt captured file; 
        2 - Executes FramesCAN.exe at this file
        3 - Generates data.txt file with organized requests and responses'''
    
    # remove file captura.txt
    framesCAN_dir = getcwd() + '\\FramesCAN'
    dest_path = Path(framesCAN_dir)
    cap_file = dest_path / "captura.txt"
    if isfile(cap_file):
        #print("Removing file: captura.txt")
        remove(cap_file)
    
    # Coping file to framesCAN directory
    
    parent_dir = path.dirname(getcwd()) 
    
    txt_files_dir = parent_dir + '\\cap_files\\txt_files'
    source_path = Path(txt_files_dir)
    
    file_path = source_path / file_name
    
    #dest_path = Path("./FramesCAN")

    copy(file_path, dest_path)
    #print(".txt file copied!")
    
    # Renaming .txt file to captura.txt
    old_name = dest_path / file_name
    new_name = dest_path / "captura.txt"
    
    move(old_name, new_name)
    #print(".txt file renamed!")
    
    
    # Changing directory to execute FramesCAN.exe
    
    main_dir = getcwd()
    
    chdir(framesCAN_dir)
    
    # Executing FramesCan.exe
    if(CAN_address_type == 'Normal'):
        run("FramesCAN.exe", shell=True, stdout=PIPE)
    if(CAN_address_type == 'Extended'):
        framesCAN_extended_address()
    
    #FramesCAN_return = run("FramesCAN.exe", shell=True, stdout=PIPE)
    #print("FramesCAN ran!")
    #print("\n\nFramesCAN output:\n\n", FramesCAN_return.stdout)
    
    # Changing directory to root
    
    chdir(main_dir)   

    
    

def frames_can_exec(CAN_address_type):
    #cleaning up
    
    FramesCAN_processed_dir = getcwd() + "\\FramesCAN\\FramesCAN_processed"
    
    if isdir(FramesCAN_processed_dir):
        data_directory = Path(FramesCAN_processed_dir)
        full_path = str(data_directory) 
        #shutil.rmtree('\\\\?\\'+ str(data_directory))
        shutil.rmtree(full_path)
    
    parent_dir = path.dirname(getcwd()) 
    
    txt_files_dir = parent_dir + '\\cap_files\\txt_files'
    
    all_itens_names = listdir(txt_files_dir)
    
    if not isdir(FramesCAN_processed_dir):
        print("Missing FramesCAN_processed directory...")
        print("Creating directory FramesCAN_processed...")
        makedirs(FramesCAN_processed_dir)
        
        
    cwd = getcwd()
    above_dir = path.dirname(cwd)
    
    data_directory = Path(txt_files_dir)
    check_path = above_dir + "\\cap_files\\txt_files\\"
    
    cwd = getcwd()
    
    FramesCAN = getcwd() + "\\FramesCAN"
    
    for item_name in all_itens_names:
        #path_to_check = "./../cap_files/txt_files/" + item_name
        path_to_check = check_path + item_name
        if isfile(str(path_to_check)):
            frames_can(item_name, CAN_address_type)
            
            data_directory = Path(FramesCAN)
            
            FC_dados_full_path = str(data_directory)  + "\\dados.txt"
            
            data_directory = Path(FramesCAN_processed_dir)
            
            FC_Proc_full_path = '\\\\?\\' + str(data_directory) 
            #print("dados\n " +FC_dados_full_path)
            #print("Proc\n " +FC_Proc_full_path + '\\' + item_name)
            #move("./FramesCAN/dados.txt", "./FramesCAN/FramesCAN_processed/" + item_name)
            move(FC_dados_full_path, FC_Proc_full_path + '\\' + item_name)
        else:
            print("not")
    remove(FramesCAN + "\\captura.txt")


 
if __name__ == "__main__":
     
    frames_can_exec()
