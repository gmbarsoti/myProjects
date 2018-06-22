'''
Created on 21 de jun de 2018

@author: 155 X-MX
'''
from pathlib import Path
import zlib


path_to_directory = "C:/Users/155 X-MX/Desktop/sand_box"
#file_name = "Leituras.ctec"
file_name = "Init.ctec"

data_folder = Path(path_to_directory)
file_to_open = data_folder / file_name
     


compressed_data = open(file_to_open,"rb").read()
decompressed_data = zlib.decompress(compressed_data)




# open file
data_folder = Path("C:/Users/155 X-MX/Desktop/")
file_to_open = data_folder / "decompressed_cap.ctec"
f = open(file_to_open,"wb")
 
f.write(decompressed_data)
f.close() 

# Key: 'Capture data for' + ModuleKey + 'Tecnomotor Eletronica do Brasil' + ModuleKey
first_part = b'Capture data for'
second_part = b'Tecnomotor Eletronica do Brasil' 
#Capture data for312001Tecnomotor Eletronica do Brasil312001
# Tecnomotor Eletronica do BrasilCapture data for
# ModuleKey: 0x03 0x01 0x02 0x00 0x00 0x01
mdkey = [3,1,2,0,0,1]
l_bytes = []
test = b''
for i in mdkey:
    b = i.to_bytes(1, byteorder='big', signed=True)
    l_bytes.append(b)
    test += b
print (test) 

full_key = first_part + test + second_part + test
#full_key = 2E 88 D3 77 84 EE 12 00 90 C4 B2 00 28 EB 44 00
full_key = bytes.fromhex('2E77 D356 84EE 1200 90C4 B200 28EB 4400')    
#i.to_bytes(1, byteorder='big', signed=True) 
print(full_key)
#var = b'Capture data for'+'
print(decompressed_data)  





from Crypto.Cipher import Blowfish


bs = Blowfish.block_size
key = b'An arbitrarily long key'
#ciphertext = b'\xe2:\x141vp\x05\x92\xd7\xfa\xb5@\xda\x05w.\xaaRG+U+\xc5G\x08\xdf\xf4Xua\x88\x1b'
ciphertext = decompressed_data
iv = ciphertext[:bs]
ciphertext = ciphertext[bs:]

cipher = Blowfish.new(full_key, Blowfish.MODE_ECB)
msg = cipher.decrypt(decompressed_data)
last_byte = msg[-1]
msg = msg[:- (last_byte if type(last_byte) is int else ord(last_byte))]
print(repr(msg))



# open file
data_folder = Path("C:/Users/155 X-MX/Desktop/")
file_to_open = data_folder / "decompressed_cap.xml"
f = open(file_to_open,"wb")
 
f.write(msg)
f.close() 