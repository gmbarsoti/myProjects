'''
Created on 4 de jul de 2018

@author: 155 X-MX
'''
from shutil import move, copy
from pathlib import Path
from os.path import isfile, isdir
from os import remove, chdir, getcwd, listdir, path, makedirs
from subprocess import  run, PIPE
import shutil

def frames_can(file_name):
    ''' 1 - Receives name of a .txt captured file; 
        2 - Executes FramesCAN.exe at this file
        3 - Generates data.txt file with organized requests and responses'''
    
    # remove file captura.txt
    dest_path = Path("./FramesCAN")
    cap_file = dest_path / "captura.txt"
    if isfile(cap_file):
        #print("Removing file: captura.txt")
        remove(cap_file)
    
    # Coping file to framesCAN directory
    source_path = Path("./cap_files/txt_files")
    
    file_path = source_path / file_name
    
    dest_path = Path("./FramesCAN")
    copy(file_path, dest_path)
    #print(".txt file copied!")
    
    # Renaming .txt file to captura.txt
    old_name = dest_path / file_name
    new_name = dest_path / "captura.txt"
    
    move(old_name, new_name)
    #print(".txt file renamed!")
    
    
    # Changing directory to execute FramesCAN.exe
    
    main_dir = getcwd()
    
    chdir("./FramesCAN")
    
    # Executing FramesCan.exe
    run("FramesCAN.exe", shell=True, stdout=PIPE)
    
    #FramesCAN_return = run("FramesCAN.exe", shell=True, stdout=PIPE)
    #print("FramesCAN ran!")
    #print("\n\nFramesCAN output:\n\n", FramesCAN_return.stdout)
    
    # Changing directory to root
    
    chdir(main_dir)   

    
    

def frames_can_exec():
    #cleaning up
    shutil.rmtree('./FramesCAN/FramesCAN_processed/')
    
    all_itens_names = listdir("./cap_files/txt_files")
    
    if not isdir("./FramesCAN/FramesCAN_processed/"):
        print("Missing FramesCAN_processed directory...")
        print("Creating directory FramesCAN_processed...")
        makedirs("./FramesCAN/FramesCAN_processed/")
        
    
    for item_name in all_itens_names:
        path_to_check = "./cap_files/txt_files/" + item_name
        if path.isfile(path_to_check):
            frames_can(item_name)
            move("./FramesCAN/dados.txt", "./FramesCAN/FramesCAN_processed/" + item_name)
    remove("./FramesCAN/captura.txt")


 
if __name__ == "__main__":
     
    frames_can_exec()
