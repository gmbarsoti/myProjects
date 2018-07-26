from cap_xml import cap_to_txt_xml
from frames_can import frames_can_exec
from request_and_responses import services_occurrences
from CSV_third import generate_cvs_file
from join_files import join_files

def main():
   
    cap_to_txt_xml()
    
    frames_can_exec()
    
    request_responses_list = services_occurrences()
    
    generate_cvs_file(request_responses_list)
    
    join_files()
    
    input("\nFinished, press enter to close window.")


if __name__ == "__main__":
    main()