from cap_xml2 import cap_to_txt_xml
from frames_can2 import frames_can_exec
from second2 import services_occurrences
from CSV_third2 import make_csv

def main():
    cap_to_txt_xml()
    frames_can_exec()
    services_occurrences()
    make_csv()

def main2():
    cap_to_txt_xml()
    frames_can_exec()
    services_occurrences()
    make_csv()
    input("Finished, press enter to close window.")


if __name__ == "__main__":
    main2()