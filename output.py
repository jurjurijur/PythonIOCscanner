"""
This script was written by Jasper van den Hoven for NFIR.
Its purpose is collecting the output from all the programs and put them into a single text file.
"""

import os.path as osp

# Function that checks if the scripts have made the needed output files import tabulate


def get_existence():
    # Scanner variable inputs
    reg_output = "Output\\registry-scan-results.txt"
    file_output = "Output\\file-scan-results.txt"
    process_output = "Output\\process-scan-results.txt"
    event_output = "Output\\eventOutput.json"

    # Call existence scanner
    reg_existence = check_existence(reg_output)
    file_existence = check_existence(file_output)
    process_existence = check_existence(process_output)
    event_existence = check_existence(event_output)

    return reg_existence, file_existence, process_existence, event_existence


def check_existence(scan_results):

    if osp.exists(scan_results):
        existence = True
    else:
        existence = False

    return existence


# Function that collects all the files
def collect_files(reg, file, process, event):
    final_output = open("Output\\Scan results.txt", "w")

    # Check if the files from the different scanners exist, if they do, write them to the new output file
    if reg:
        with open("Output\\registry-scan-results.txt", "r") as reg_output:
            final_output.write(reg_output.read())
            final_output.write("\n")
            reg_output.close()

    if file:
        with open("Output\\file-scan-results.txt", "r") as file_output:
            final_output.write(file_output.read())
            final_output.write("\n")
            file_output.close()

    if process:
        with open("Output\\process-scan-results.txt", "r") as process_output:
            final_output.write(process_output.read())
            final_output.write("\n")
            process_output.close()

    if event:
        with open("Output\\eventOutput.json", "r") as event_output:

            final_output.write("\n\n")
            final_output.write(120 * "-")
            final_output.write("\nEVENT LOG SCANNER RESULTS\n")
            final_output.write(120 * "-")
            final_output.write("\n")
            final_output.write(event_output.read())
            final_output.write("\n")
            final_output.write(120 * "-")
            event_output.close()

    final_output.close()


# Return the final document to the user
def print_results():
    final_document = open("Output\\Scan results.txt", "r")

    print(final_document.read())


# Function that controls what files get called when
def order_of_calling():
    reg, file, process, event = get_existence()
    collect_files(reg, file, process, event)


# Main function of script
def main():
    order_of_calling()


if __name__ == '__main__':
    main()