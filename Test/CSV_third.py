from pathlib import Path


def fileLines(directory_path,file_name):
    # Return lines of a txt file in a list
    
    data_folder = Path(directory_path) # format ex: "C:/Users/155 X-MX/Desktop/Preenche Servicos"
    path_to_file = data_folder / file_name # Ex: 'file_name.txt'
    # Checking if file exists     
    if path_to_file.exists():
        print("Yay, the file exists!")
        f = open(path_to_file,"r")
        # Getting all lines    
        all_lines = f.readlines()
        f.close()
        print('Number of lines: ', str(len(all_lines)))
        return all_lines
    
    print("Oops, file doesn't exist!")
    return -1

def generate_csv(directory_path):
    
    
    file_name = 'req_res.txt'
    
    all_lines = fileLines(directory_path, file_name)
    if all_lines == -1:
        print("In path: ", directory_path, "\nDidn't find req_res.txt file!!!")
        return -1
    
    else:
    # change to list
    # get requests and responses
    # Create string to csv file   
    # writing to csv file
    
        directory_path = 'D:/sand_box/output'
        file_name = 'req_res_table.csv'
        
        data_folder = Path(directory_path) # format ex: "C:/Users/155 X-MX/Desktop/Preenche Servicos"
        path_to_file = data_folder / file_name # Ex: 'file_name.txt'
        
        csv_file = open(path_to_file,'w')
        csv_file.write('000 REQUESTS,000 RESPONSES\n')
        
        
        for line in all_lines:
            # change to list
            line_list = line.split(' ')
            
            # get requests and responses
            request = line_list[1]
            response = line_list[3]#[:-1] # response without \n
            
            # Create string to csv file
            line_to_csv = request + ',' + response 
            
            # writing to csv file
            csv_file.write(line_to_csv)
            
            print(line_list)
            print(line_to_csv)
            
        
        
        csv_file.close()  
        

if __name__ == "__main__":
    directory_path = 'C:/Users/155 X-MX/Desktop/sand_box'
    generate_csv(directory_path)
    
