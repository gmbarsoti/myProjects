from cap_xml import cap_to_txt_xml
from frames_can import frames_can_exec
from request_and_responses import services_occurrences
from CSV_third import generate_cvs_file
from join_files import join_files
import logging
import datetime

def main():
    
    do_log = False
    if do_log:
        time_stamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file_name = "./../logs/log_" + time_stamp + ".log"
        logging.basicConfig(filename=log_file_name, level=logging.INFO)
        
        try:
            logging.info("Application started")
            cap_to_txt_xml()
            
            frames_can_exec()
            
            request_responses_list = services_occurrences()
            
            generate_cvs_file(request_responses_list)
            
            join_files()
            
            input("\nFinished, press enter to close window.")
        except:
            logging.info("\n---------Some error occurred---------------\n")
            
    else:
        
        cap_to_txt_xml()
        
        frames_can_exec()
        
        request_responses_list = services_occurrences()
        
        generate_cvs_file(request_responses_list)
        
        join_files()
        
        input("\nFinished, press enter to close window.")
    

if __name__ == "__main__":
    main()