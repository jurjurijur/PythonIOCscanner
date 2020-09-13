"""
This script was made by Jasper van den Hoven for NFIR.
Its purpose is receiving the needed user input for the main program and saving this to a text file
that the main program can then read from.
"""

# Import needed modules
import os.path as osp
import logging


# Function that writes the config to IOC
def check_existence():
    # logging.info("Entered function to write config to file")

    file = None

    # Check if IOC list exists
    if osp.exists("IOC_lijst-test.txt"):
        # logging.info("FIle exists, writing to it in overwrite mode")

        file = open("IOC_lijst-test.txt", "w")
        file.close()

    elif not osp.exists("IOC_lijst.txt"):
        # logging.critical("No IOC list found, creating the file")

        file = open("IOC_lijst.txt", "x")
        file.close()


# Function that collects the user input
def get_config():
    output_config = get_write_location()
    registry_config = get_reg_data()
    process_config = get_process_data()
    file_scan_config = get_file_scan()
    event_config = get_event_log_data()

    return output_config, registry_config, process_config, file_scan_config, event_config


def get_event_log_data():
    amount = int(input("How many unique entries would you like to enter? "))
    i = 0

    event_type = []
    event_id = []
    sid = []
    source_name = []
    string_inserts = []
    event_category = []
    data = []
    computer_name = []
    log_type = []
    event_config = []

    while i < amount:
        event_type.append(input("Please enter a Event ID, for example 13 "))
        event_id.append(input("Please enter a event ID, for example 14 "))
        sid.append(input("Please enter a sid, for example 233434 "))
        source_name.append(input("Please enter a source name, for example \"lala\" "))
        string_inserts.append(input("Please enter a string insert, for example \"evil.exe\" "))
        event_category.append(input("Please enter a event category, for example 34 "))
        data.append(input("Please enter a value for the data field, for example \"lala\' "))
        computer_name.append(input("Please enter a host name , for example \"DESKTOP-V0TA2HL\" "))
        log_type.append(input("Please enter a log type, for example \"audit_success\" "))

        event_config.append(event_type)
        event_config.append(event_id)
        event_config.append(sid)
        event_config.append(source_name)
        event_config.append(string_inserts)
        event_config.append(event_category)
        event_config.append(data)
        event_config.append(computer_name)
        event_config.append(log_type)

    content = input("Are you satisfied with your entered information? (Y/n) ")

    if content.upper() == "Y":
        return event_config

    elif content.upper() == "N":
        get_event_log_data()


def get_process_data():
    # amount = input("How many unique entries would you like to enter? ")
    amount = 1
    i = 0

    process_name = []
    process_path = []
    process_config = []

    while i < amount:
        process_name.append(input("Please enter a process name, for example Skype: "))
        process_path.append(input("Please enter a process directory, for example "
                                  "C:\\Users\\Jasper\\AppData\\Local\\Microsoft\\OneDrive\\OneDrive.exe "))
        process_config.append(process_name)
        process_config.append(process_path)

    content = input("Are you satisfied with your entered information? (Y/n) ")

    if content.upper() == "Y":
        return process_config

    elif content.upper() == "N":
        get_process_data()


def get_file_scan():
    # amount = input("How many unique entries would you like to enter? ")
    amount = 1
    i = 0

    file_path = []
    file_size_name = []
    file_scan_config = []

    while i < amount:
        file_path.append(input("Please enter a file path, for example C:\\Users\\Jasper\\Downloads "))
        file_size_name.append(input("Please enter a process directory, for example \".exe\" or 10000 (10.000 KB) "))
        file_scan_config.append(file_path)
        file_scan_config.append(file_size_name)

    content = input("Are you satisfied with your entered information? (Y/n) ")

    if content.upper() == "Y":
        return file_scan_config

    elif content.upper() == "N":
        get_file_scan()


def get_reg_data():
    amount = int(input("How many unique keys would you like to enter? "))
    i = 0

    hkey_list = []
    reg_path_list = []
    registry_config = []

    while i < amount:
        hkey_list.append(input("Enter a HKEY, for example HKEY_LOCAL_MACHINE: "))
        reg_path_list.append(input("Enter a registry path please, for example "
                                   "Software\\Microsoft\\Windows\\CurrentVersion\\Run "))
        registry_config.append(hkey_list)
        registry_config.append(reg_path_list)
        i -= - 1

    content = input("Are you satisfied with your entered information? (Y/n) ")

    if content.upper() == "Y":
        return registry_config

    elif content.upper() == "N":
        get_reg_data()


def get_write_location():
    # logging.info("Entered function to get user input")
    default_path = []
    backup_path = []
    output_config = []

    default_path.append(input("Where would you like to write the results to? (f.e. C:\\Users\\Public\\Desktop) "))
    # logging.info("User entered: " + str(default_path) + " as the default path")

    backup_path.append(input("What is the backup location in case the default can't be found? (default is current "
                             "directory) "))
    # logging.info("User entered: " + str(backup_path) + " as the backup path")

    # logging.info("Done getting results, returning inputs")

    content = input("Are you satisfied with your entered information? (Y/n) ")

    if content.upper() == "Y":
        output_config.append(default_path)
        output_config.append(backup_path)
        return output_config

    elif content.upper() == "N":
        get_write_location()


def write_to_file(output_config, registry_config, process_config, file_scan_config, event_config):
    file = open("IOC_lijst-test.txt", "w")

    # Write registry config to file
    file.write("\n---BEGIN_REGISTRY_SCAN---\n")
    file.write("# Registry scanner syntax\n")
    file.write("# hkey;;path\n")

    file.write(str(','.join(registry_config[0])))
    file.write(";;")
    file.write(str(','.join(registry_config[1])))

    file.write("\n---END---\n")

    # Write process config to file
    file.write("\n---BEGIN_PROCESS_SCAN---\n")
    file.write("# process name;;SourcePath\n")

    file.write(str(','.join(file_scan_config[0])))
    file.write(";;")
    file.write(str(','.join(file_scan_config[1])))

    file.write("\n---END---\n")

    # Write file scan config to file
    file.write("\n---BEGIN_FILE_SCAN---\n")
    file.write("# File Scanner syntax:\n")
    file.write("# path;;extension or size\n")
    file.write("# Allows for a maximum 1 item per search run\n")

    file.write(str(','.join(process_config[0])))
    file.write(";;")
    file.write(str(','.join(process_config[1])))

    file.write("\n---END---\n")

    # Write event log scanner to file
    file.write("\n---BEGIN_EVENTLOG_SCAN---\n")
    file.write("# Event log scanner syntax:\n")
    file.write("# eventType ;; eventID ;; sid ;; sourceName ;; stringInserts ;; eventCategory ;; data ;; computerName "
               ";; logType\n")
    file.write("# There are five logTypes: audit_failure, audit_success, information_type, warning_type, error_type\n")
    file.write("# To search all log types, choose ALL as your log type\n")

    file.write(str(','.join(event_config[0])))
    file.write(";;")
    file.write(str(','.join(event_config[1])))
    file.write(";;")
    file.write(str(','.join(event_config[2])))
    file.write(";;")
    file.write(str(','.join(event_config[3])))
    file.write(";;")
    file.write(str(','.join(event_config[4])))
    file.write(";;")
    file.write(str(','.join(event_config[5])))
    file.write(";;")
    file.write(str(','.join(event_config[6])))
    file.write(";;")
    file.write(str(','.join(event_config[7])))
    file.write(";;")
    file.write(str(','.join(event_config[8])))

    file.write("\n---END---\n")

    # write save config to file
    file.write("\n---BEGIN_CONFIG---\n")
    file.write(str(','.join(output_config[0])))
    file.write(";;")
    file.write(str(','.join(output_config[1])))
    file.write("\n---END---\n")


# Main function that controls the flow of functions that run
def main():
    check_existence()
    output_config, registry_config, process_config, file_scan_config, event_config = get_config()
    write_to_file(output_config, registry_config, process_config, file_scan_config, event_config)


if __name__ == '__main__':
    main()
