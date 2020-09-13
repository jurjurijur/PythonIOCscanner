"""
This Python sript was written by Jasper van den Hoven, Hogeschool Leiden for NFIR.
Its purpose is to start and control what parts of our IOC scanner get called when and with what input.
"""

from Input import InputValidator as ir
from Input import InputInterpeter as ii
from EventLog_Scan import event_log_scanner as els
from File_scan import file_scanner as fs
from Registry import read_registry as rreg
from Processes import process_scanner as pss
import sys
import output
import os

import logging

# Set logging settings and create newline, upon starting this function
logging.basicConfig(filename="Output\\logging.log", level=logging.INFO, format='%(asctime)s, %(levelname)s, '
                                                                               '%(funcName)s, ''%(message)s')


def make_output_dir():
    output_dir = "Output\\"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


# Function that gets the input from the IOC List input file
def get_input():
    logging.info("\n---GET INPUT---")
    logging.info("Started getting config from the config file")

    # Make objects
    logging.info("Creating input objects")
    validate = ir.InputValidator()
    interpret = ii.InputInterpeter()

    # Validate the config file and return the raw_string[]
    logging.info("Getting lists from config file")
    registry_list, file_list, event_list, process_list = validate.getInput(r"IOC_lijst.txt")

    # Parse hkey_list and add it to a variable
    logging.info("Binding registry lists to variables: hkey_list")
    registry_list = interpret.transformRegistryInput(registry_list)

    # Parse file_list and add it to a variable
    logging.info("Binding file list to variable: file_list")
    file_list = interpret.transformFileInput(file_list)

    # Parse event_list and add it to a variable
    logging.info("Binding event list to variable: event_list")
    event_list = interpret.transformEventInput(event_list)

    # Parse process_list and add it to a variable
    logging.info("Binding event list to variable: process_list")
    process_list = interpret.transformProcessInput(process_list)

    # Parse config_list and add it to a variable
    logging.info("Binding event list to variable: config_list")
    # config_list = interpret.transformConfigInput(config_list)

    # Returning newly created variables
    logging.info("Returning made variables: hkey_list, path_list, file_list, event_list, process_list, config_list")

    return registry_list, file_list, event_list, process_list


# Function that controls what scanner gets called when
def order_of_calling(registry_list, file_list, event_list, process_list):
    logging.info("\n---SCANNER CONTROL---")
    logging.info("Started calling scanners with given input")

    logging.info("Starting registry scan")
    rreg.main(registry_list)

    logging.info("Starting process scanner")
    pss.main(process_list)

    logging.info("Starting event log scanner")
    els.EventLogScanner(event_list)

    logging.info("Starting file scanner")
    fs.input_check(file_list[0], file_list[1])

    output.main()

    print("")
    input("Press ENTER to quit")
    logging.info("Exiting program")
    sys.exit(0)


# Main function of the script
def main():
    logging.info("\n---MAIN OF PROGRAM---")

    logging.info("Checking if output directory exists")
    make_output_dir()

    logging.info("Retrieving input from config file")
    registry_list, file_list, event_list, process_list = get_input()

    logging.info("Starting scanner calling function with config file input")
    order_of_calling(registry_list, file_list, event_list, process_list)


if __name__ == '__main__':
    main()
