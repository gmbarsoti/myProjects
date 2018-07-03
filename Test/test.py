import shutil
from pathlib import Path
from os.path import isfile
from os import remove, rename, chdir, getcwd
from subprocess import  run, PIPE

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
    
    
file_name = "ApagaMemoria.txt"  
frames_can(file_name)



