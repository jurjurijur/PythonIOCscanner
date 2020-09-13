import os
import logging

"""
This script was made by Maad Alhaj Saleh for NFIR, unless specified, all code in this document was written by the 
former name.

Refactoring and writing to output file by Jasper van den Hoven to comply with PEP8
Conversion of list item to string and int was done by Jasper van den Hoven.
"""

filesList = []


def input_check(p_1, p_2):
    logging.info("\n---FILE SCANNER---")

    output = open(r"Output\file-scan-results.txt", "w")
    output.write("\n\n")
    output.write(120 * "-")
    output.write("\nFILE SCANNING RESULTS\n")
    output.write(120 * "-")

    # convert list to list without , and []
    # convert list to str variable
    p1 = str(','.join(p_1))
    p2 = str(','.join(p_2))

    try:
        p2 = int(p2)
        if isinstance(p2, int):
            p2 = int(p2)

        else:
            p2 = str(p2)

    except:
        p2 = p2

    if isinstance(p1, str) and isinstance(p2, str):
        if p1.__contains__("\\"):
            for root, subdirs, files in os.walk(p1):
                for file in files:
                    if file.__contains__(p2):
                        output.write("\nPath: ")
                        output.write(root)
                        output.write("\nFile name: ")
                        output.write(str(file))
                        output.write("\n")

                        print('\nPath: ' + root + '\n' + 'File Name: ' + str(file))
                        logging.info("Path: " + root + " File Name: " + str(file))

            output.write("\n")
            output.write(120 * "-")
            output.write("\n\n")

        elif p2.__contains__("\\"):
            for root, subdirs, files in os.walk(p2):
                for file in files:
                    if file.__contains__(p1):
                        output.write("\nPath: ")
                        output.write(root)
                        output.write("\nFile name: ")
                        output.write(str(file))
                        output.write("\n")

                        print('\nPath: ' + root + '\n' + 'File Name: ' + str(file))
                        logging.info("Path: " + root + " File Name: " + str(file))

            output.write("\n")
            output.write(120 * "-")
            output.write("\n\n")

    elif isinstance(p2, int):  # TO DO write the logic when P2 is int
        for path, subdirs, files in os.walk(p1):
            for name in files:
                filesList.append(os.path.join(path, name))
            for i in filesList:
                file_size = os.path.getsize(str(i))
                if file_size >= p2 * 1024:
                    output.write("\nThe file name is: ")
                    output.write(str(i))
                    output.write("\nThe file size is: ")
                    output.write(str(file_size / 2014))
                    output.write(" kilobytes")
                    output.write("\n")

                    print("\nThe File: " + str(i) + " File Size is: " + str(file_size / 1024) + " kiloBytes")
                    logging.info("The File: " + str(i) + " File Size is: " + str(file_size / 1024) + " kiloBytes")

        output.write("\n")
        output.write(120 * "-")
        output.write("\n\n")

    elif isinstance(p1, int):
        for path, subdirs, files in os.walk(p2):
            for name in files:
                filesList.append(os.path.join(path, name))
            for i in filesList:
                file_size = os.path.getsize(str(i))
                if file_size >= p1 * 1024:
                    output.write("\nThe file name is: ")
                    output.write(str(i))
                    output.write("\nThe file size is: ")
                    output.write(str(file_size / 2014))
                    output.write(" kilobytes")
                    output.write("\n")

                    print("\nThe File: " + str(i) + " is: " + str(file_size / 1024) + " kiloBytes")
                    logging.info("The File: " + str(i) + " is: " + str(file_size / 1024) + " kiloBytes")

        output.write("\n")
        output.write(120 * "-")
        output.write("\n\n")

    else:
        print("input error")
        logging.info("input error")


if __name__ == "__main__":
    # InputCheck(P1, P2)
    print("if __name__" == "__main__")
