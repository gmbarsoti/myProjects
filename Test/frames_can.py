'''
Created on 4 de jul de 2018

@author: 155 X-MX
'''
from shutil import move, copy
from pathlib import Path
from os.path import isfile, isdir
from os import remove, chdir, getcwd, listdir, path, makedirs
from subprocess import  run, PIPE

def frames_can(file_name):
    ''' 1 - Receives name of a .txt captured file; 
        2 - Executes FramesCAN.exe at this file
        3 - Generates data.txt file with organized requests and responses'''
    
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
    copy(file_path, dest_path)
    print(".txt file copied!")
    
    # Renaming .txt file to captura.txt
    old_name = dest_path / file_name
    new_name = dest_path / "captura.txt"
    
    move(old_name, new_name)
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
    
if __name__ == "__main__":
    
    all_itens_names = listdir("D:/sand_box/cap_files/txt_files")
    
    if not isdir("D:/sand_box/FramesCAN/FramesCAN_processed/"):
        print("Missing FramesCAN_processed directory...")
        print("Creating directory FramesCAN_processed...")
        makedirs("D:/sand_box/FramesCAN/FramesCAN_processed/")
        
    
    for item_name in all_itens_names:
        path_to_check = "D:/sand_box/cap_files/txt_files/" + item_name
        if path.isfile(path_to_check):
            frames_can(item_name)
            move("D:/sand_box/FramesCAN/dados.txt", "D:/sand_box/FramesCAN/FramesCAN_processed/" + item_name)
    remove("D:/sand_box/FramesCAN/captura.txt")

