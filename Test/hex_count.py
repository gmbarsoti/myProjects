'''
Created on 20 de jun de 2018

@author: 155 X-MX
'''
first_part = str.encode('Capture data for')
second_part = str.encode('Tecnomotor Eletronica do Brasil') 
mdkey = [3,1,2,0,0,1]
l_bytes = []
test = b''
for i in mdkey:
    b = i.to_bytes(1, byteorder='big', signed=True)
    l_bytes.append(b)
    test += b
print (test) 

full_key = first_part + test + second_part + test

print (full_key)
hex_str = input("hex_list: ")

hex_str_list = hex_str.split(",")
print(len(hex_str_list))