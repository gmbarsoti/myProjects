'''
Created on 22 de jun de 2018

@author: 155 X-MX
'''
from subprocess import run, PIPE
from pathlib import Path

data_folder = Path("D:/sand_box/")
program_path = data_folder / "ProtocolAnalyzerSaveXml.exe"

data_folder = Path("D:/sand_box/")

cap_path = data_folder / "InitGscan.ctec"
print(program_path)
print (cap_path)
a = run([str(program_path),str(cap_path)], stdout=PIPE)

