from cap_xml import cap_to_txt_xml
from frames_can import frames_can_exec
from request_and_responses import services_occurrences
from CSV_third import generate_cvs_file
from join_files import join_files
from Cleanup import cleanup
from creating_directories import creating_dirs
import logging
import datetime
import traceback
import os



def option_framesCAN():
    """ Choose if framesCAN will be skipped or not """
    choice = ''
    valid_list = ['0','1']
    while not choice in valid_list:
        choice = input("Skip framesCAN?\n\n" +
                       "0 - NO\n"+
                       "1 - YES\n")
        if not choice in valid_list:
            print("\nChoose a valid option!\n")
    
    if choice == '0':
        choice = 0
    else:
        choice = 1
        
    return choice


def option_CAN_normal_extended():
    """ Choose between CAN normal or extended addressing """
    choice = ''
    valid_list = ['0','1']
    while not choice in valid_list:
        choice = input("CAN address type?\n\n" +
                       "0 - Normal\n"+
                       "1 - Extended\n")
        if not choice in valid_list:
            print("\nChoose a valid option!\n")
    
    if choice == '0':
        choice = 'Normal'
    else:
        choice = 'Extended'
        
    return choice




def main():
    
    print("Application started\n")
    do_log = True
    if do_log:
        if not os.path.isdir("./../logs"):
            print("Missing logs directory...")
            print("Creating directory logs...\n")
            os.makedirs("./../logs")
            
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file_name = "./../logs/log_" + time_stamp + ".log"
        logging.basicConfig(filename=log_file_name, level=logging.INFO)
        
        try:
            logging.info("Application started")
            
            logging.info("Creating directories...")
            creating_dirs()
            logging.info("Directories created!")
            
            logging.info("cleaning up...")
            cleanup()
            logging.info("cleaned up!")
            
            skip_framesCAN =  option_framesCAN()
            CAN_address_type = option_CAN_normal_extended()
            
            if not (skip_framesCAN):
            
                logging.info("Converting captured (.ctec) files to .txt and .xml...")
                cap_to_txt_xml()
                logging.info("Captured (.ctec) files were converted.")
                
                logging.info("Generating a file with all communications...")
                join_files()
                logging.info("File with all communications is generated!")
                
                logging.info("Using FramesCAN module...")
                frames_can_exec(CAN_address_type)
                logging.info("FramesCAN module executed!")
            
            logging.info("Creating list of requests and its responses...")
            request_responses_list = services_occurrences()
            logging.info("Requests and its responses list was created!")
            
            logging.info("Generating cvs file...")
            generate_cvs_file(request_responses_list)
            logging.info("CSV file was created!")
            
            logging.info("Application concluded without errors!")
            
            input("\nApplication is finished, press enter to close window.")
            
        except Exception:
            print(traceback.format_exc())
            logging.exception("\n---------Some exception occurred---------------\n")
            input("ERROR OCCURRED!!!\nPress enter to close this window")
            
            
    else:
        
        cap_to_txt_xml()
        
        frames_can_exec()
        
        request_responses_list = services_occurrences()
        
        generate_cvs_file(request_responses_list)
        
        join_files()
        
        input("\nFinished, press enter to close window.")
    

if __name__ == "__main__":
    main()