from winreg import *
import os.path as osp
import logging
import tabulate

"""
This Python sript was written by Jasper van den Hoven, Hogeschool Leiden for NFIR.
Its purpose is to read the Windows Registry with the keys/ paths you give it.
"""

# Global variables for ease of use in multiple functions
hkey_type = ""  # String variable that houses the HKEY type as a string
# Two lists that house the total HKEYs and Paths
hkey_list = []
path_list = []
hkey_filtered = []
path_list_backup = []
hkey_input = None
# Series of lists that collect the output of the program
index_number = []
item_name = []
field_name = []
reg_data = []
# Two lists that house the tabulate data
tabulate_reg = []
tabulate_filtered_reg = []


# Function that collects the input from a main and splits the input into local variables
# Afterwards it checks if the lists are equally long to prevent exceptions
def load_input_list(key, path):
    logging.info("\n---REGISTRY SCAN---")

    # import global variables to use them later on
    global hkey_list
    global path_list

    logging.info('Started loading the input list')

    # Fill key list with input values from main()
    for keys_amount in key:
        hkey_list.append(keys_amount)
        hkey_filtered.append(keys_amount)

    # Fill path list with input values from main()
    for path_amount in path:
        path_list.append(path_amount)
        path_list_backup.append(path_amount)

    # Checking to see if both lists are equally long to prevent errors later on
    if len(hkey_list) == len(path_list):

        # Call the next bit of the program that checks what register type needs to be read
        logging.info('Finished loading the input list')
        logging.info('Starting next function')
        hkey_switcher(hkey_list, False)  # feed the created list of keys into the switcher to call the correct key value

    else:
        # if the list aren't equally long, abort the program and return -1 to show errors happened
        logging.warning("Lists are not equally long!")
        # logging.warning('Length key list was:', len(hkey_list), "whilst path list was:", len(path_list))
        return -1


# Function that sets the current HKEY type for the function that reads the actual registry.
def hkey_switcher(hkey_feed, processed):
    # import global variables to use them later on
    global hkey_input

    logging.info('Started HKEY input processing')

    # Process the first item in the list to bind it to the correct key
    if not processed:

        # "Feed" it the first value in the array to fit it into the correct if/elif/else
        if hkey_feed[0] == "HKEY_CLASSES_ROOT":
            hkey_input = HKEY_CLASSES_ROOT
            logging.info('Processed input, HKEY type is: HKEY_CLASSES_ROOT, setting processed to True')
            hkey_switcher(hkey_feed, True)  # call the same function again but switch "Processed" to true

        elif hkey_feed[0] == "HKEY_CURRENT_USER":
            hkey_input = HKEY_CURRENT_USER
            logging.info('Processed input, HKEY type is: HKEY_CURRENT_USER, setting processed to True')
            hkey_switcher(hkey_feed, True)

        elif hkey_feed[0] == "HKEY_LOCAL_MACHINE":
            hkey_input = HKEY_LOCAL_MACHINE
            logging.info('Processed input, HKEY type is: HKEY_LOCAL_MACHINE, setting processed to True')
            hkey_switcher(hkey_feed, True)

        elif hkey_feed[0] == "HKEY_USERS":
            hkey_input = HKEY_USERS
            logging.info('Processed input, HKEY type is: HKEY_USERS, setting processed to True')
            hkey_switcher(hkey_feed, True)

        elif hkey_feed[0] == "HKEY_CURRENT_CONFIG":
            hkey_input = HKEY_CURRENT_CONFIG
            logging.info('Processed input, HKEY type is: HKEY_CHKEY_CURRENT_CONFIG, setting processed to True')
            hkey_switcher(hkey_feed, True)

        # If nothing fits, throw an error and return -1
        else:
            logging.critical('Invalid HKEY type as input')
            return -1

    # If the input is "Processed" call the next function with the variables created here
    else:
        logging.info('Input processed, starting next function')
        reg_key = OpenKey(hkey_input, path_list[0], 0)  # Open the key that matches the "Processed" input

        # read_registry(hkey_input, reg_key)  # Call the next function with newly opened registry key
        check_output_location(hkey_input, reg_key)


# Function that checks if the output file exists, and if not creates the file
def check_output_location(hkey, reg_key):
    # Check if the output file exists, if not, create the output file.
    if osp.isfile("Output\\registry-scan-results.txt"):
        logging.info('File existed, opening found file')
        file = open(r"Output\\registry-scan-results.txt", "w")

    # If the file doesn't exist, create the file
    else:
        logging.info('File did not exist, creating file')
        file = open(r"Output\\registry-scan-results.txt", "x")

    logging.info('Correct file exists, starting next function')
    file.close()
    read_registry(hkey, reg_key)


# Function that reads the Windows Registry based on the given input and stores the results in a list
def read_registry(hkey_input_value, key_input):
    # import global variables to use them later on
    global hkey_list
    global hkey_filtered
    global path_list
    global index_number
    global item_name
    global field_name
    global reg_data
    global tabulate_reg

    logging.info('Starting reading registry with current key and path')

    # For the amount of values in the key, do the following
    name = hkey_list[0]
    data = path_list[0]
    field_type = "Empty"

    tabulate_reg.append({
        'Name': name,
        'Data': data,
        'Field Type': field_type,
    })

    # Check if the key is empty to prevent output from showing the wrong key with the wrong results
    if range(QueryInfoKey(key_input)[1]) == range(0):
        logging.info('Current key is empty, filling in blanks')
        name = "Empty"
        data = "Empty"
        field_type = "Empty"

        tabulate_reg.append({
            'Name': name,
            'Data': data,
            'Field Type': field_type,
        })

    else:
        for i in range(QueryInfoKey(key_input)[1]):
            """This for loop was copied from Stack Overflow as this was the solution to my problem.
            It however has been altered to accommodate for writing to a Tabulate dictionary 
            instead of printing the results."""

            logging.info('Key is not empty, reading results')
            try:
                name, data, field_type = EnumValue(key_input, i)
                # Tabulate table appending
                name = str(name)
                data = str(data)
                field_type = str(field_type)

                tabulate_reg.append({
                    'Name': name,
                    'Data': data,
                    'Field Type': field_type,
                })

            # If try fails, print error
            except EnvironmentError:
                logging.critical('Environment Error')

    CloseKey(key_input)

    # With the first value in the list read, delete this value
    del hkey_list[0]
    del path_list[0]

    # With the first value removed, restart the process until the list is empty
    if len(hkey_list) and len(path_list) != 0:
        logging.info('List is not empty, restarting program')

        hkey_switcher(hkey_list, False)  # Call the switcher again with input being False

    # If the list isn't empty, print the results to the user
    else:
        logging.info('List is empty, starting next function')
        # result_input(tabulate_reg)


# Function that allows the user to filter the results based on their input
# The results of this function are stored in a Tabulate list
def result_input(registry_list):
    global tabulate_reg

    # 0 = hkey
    # 1 = path
    # 2 = filter_choice
    # 3 = filter_type
    # 4 = filter_name

    # input variable lists
    filter_choice = registry_list[2]
    filter_type = registry_list[3]
    filter_name = registry_list[4]

    # storage variables
    filtered_list = []
    filter_name_list = []
    filter_path_list = []
    input_list = tabulate_reg

    # counter variable
    a = 0

    while a < len(filter_choice):
        # Check if the user wanted to search or not
        if filter_choice[a] == "Y":

            # Check if the user wanted to search by name or by path
            if filter_type[a] == "1":
                for key in input_list:
                    if key in filtered_list:  # If the key has already been searched for, move on and don't add it again
                        continue
                    # Check if the given program name is in the total filter list
                    elif key["Name"] == filter_name[a]:
                        filtered_list.append(key)

            elif filter_type[a] == "2":
                for key in input_list:
                    if key in filtered_list:  # If the key has already been searched for, move on and don't add it again
                        continue
                    # Check if the given file path is in the total filter list
                    elif key["Data"].__contains__(filter_name[a]):
                        filtered_list.append(key)

        elif filter_choice[a] == "N":
            print("Won't be applying a filter for this search\n")

        a -=- 1
    return filtered_list


# Function that gets the Tabulate results and writes them to a text file
def write_results_tabulate(non_filtered, filtered, sought_after_name):
    # Non-filtered list
    tabulate_header = non_filtered[0].keys()
    tabulate_rows = [x.values() for x in non_filtered]
    reg_table = tabulate.tabulate(tabulate_rows, tabulate_header, tablefmt="rst")

    filtered_name = sought_after_name[0]

    # If the user opted for a filter of the registry, write the results of the search and the raw data
    if filtered:
        # Filtered list
        tabulate_header_filtered = filtered[0].keys()
        tabulate_rows_filtered = [x.values() for x in filtered]
        reg_table_filtered = tabulate.tabulate(tabulate_rows_filtered, tabulate_header_filtered, tablefmt="rst")

    if not filtered:
        logging.warning("No filter was applied, skipping these results!")
        print("\nRaw registry results")
        print(reg_table)

        # writing tables to file
        file = open("Output\\registry-scan-results.txt", "w")
        file.write(120 * "-")
        file.write("\nREGISTRY RESULTS\n")
        file.write(120 * "-")
        file.write("\nRaw registry results\n")
        file.write(reg_table)
        file.write("\n")

        file.write("\n")
        file.write("No results for given filter option\n")
        file.write("You searched for: ")
        file.write(filtered_name)
        file.write("\n\n")
        file.write(120 * "-")

    else:
        print("\nFiltered registry results")
        print(reg_table_filtered)

        # writing tables to file
        file = open("Output\\registry-scan-results.txt", "w")
        file.write(120 * "-")
        file.write("\nREGISTRY RESULTS\n")
        file.write(120 * "-")
        file.write("\nRaw registry results\n")
        file.write(reg_table)
        file.write("\n")

        file.write("\nFiltered registry results\n")
        file.write(reg_table_filtered)
        file.write("\n\n")
        file.write(120 * "-")
        file.close()


def main(registry_list):
    global tabulate_reg

    load_input_list(registry_list[0], registry_list[1])
    filtered_list = result_input(registry_list)
    write_results_tabulate(tabulate_reg, filtered_list, [""])


if __name__ == '__main__':
    main()
