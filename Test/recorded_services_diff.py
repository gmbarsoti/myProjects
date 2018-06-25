'''
Created on 25 de jun de 2018

@author: 155 X-MX
'''

from pathlib import Path
import os.path

# Getting requests that already occurred
# open file
data_folder = Path("C:/Users/155 X-MX/Desktop/services_diff")
file_to_open = data_folder / "req_res_painel.txt"
lines_first = []
#checking if the file already exists
if os.path.isfile(file_to_open): 
    f = open(file_to_open,"r")
    # Getting all lines    
    lines_first = f.readlines()
    f.close() 
    
    
file_to_open = data_folder / "req_res.txt"
lines_second = []
#checking if the file already exists
if os.path.isfile(file_to_open): 
    f = open(file_to_open,"r")
    # Getting all lines    
    lines_second = f.readlines()   
    f.close() 


file_to_open = data_folder / "equal_sevices.txt"
f_equal = open(file_to_open,"w")


file_to_open = data_folder / "diff_sevices.txt"
f_diff = open(file_to_open,"w")

for L1 in lines_first:
    if L1 in lines_second:
        f_equal.write(L1)
    else:
        f_diff.write(L1)
        
f_equal.close()
f_diff.close()