from second import adjust_list, line_adjust


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