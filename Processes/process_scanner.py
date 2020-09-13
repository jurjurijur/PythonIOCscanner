import psutil
import time
import tabulate
import os
import logging
import os.path as osp

# use tabulate
# use proceslist
# run pycharm in administrator

# Logging
tabulate_proc = []


# Function to check whether the output file already exists
def check_output_location():
    if osp.exists("Output\\process-scan-results.txt"):
        logging.info("Output file exists, writing to it in overwrite mode")
    else:
        file = open("Output\\process-scan-output.txt", "x")
        file.close()


# Use the process list to see if the sought after processes are running
def read_process_list(process_list):
    logging.info('Started reading the ProcessList to Check If process is running')
    for process in process_list:
        check_if_process_running(process)


# Use the process list to see processes are running with a specific name
def show_processes(process_list):
    logging.info('Started reading the ProcessList to find ProcessIdByName')
    for process in process_list:
        find_process_id_by_name(process)


# Find processes by absolute path
def find_procs_by_path(exe):
    file = open("Output\\process-scan-results.txt", "a")

    file.write(120 * "-")
    file.write("\nPROCESS SCAN RESULTS\n")
    file.write(120 * "-")

    file.write("\n*** found process by path ***\n")

    logging.info('Start function to find processes by Input Path')

    # Return a list of processes matching the given path
    ls = []

    logging.info('Started loop to compare exe with exe on device and add to list')

    for p in psutil.process_iter(attrs=["pid", "name", "exe"]):
        if exe == p.info['exe']:
            ls.append(p)
            file.write(str(ls))
            file.write("\n")
            print(ls)

    logging.info('End function Find_procs_by_Path')
    file.write("\n")
    file.close()

    return ls


# Check if name contains processlist is running
def check_if_process_running(process_name):
    """
    Check if there are any running process' that contain the given process names.
    """

    file = open("Output\\process-scan-results.txt", "a")
    file.write("*** Check if a process is running or not ***\n")

    logging.info('Start function to CheckIfProcessRunning')
    logging.info('Begin Loop to iterate over all the running processes')

    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                print('Yes, a ' + process_name + ' process was running')
                file.write("Yes, a ")
                file.write(process_name)
                file.write(" process was running\n")
                file.write("\n")

                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):

            print('No, a' + process_name + ' was not running')
            file.write("No, a ")
            file.write(process_name)
            file.write(" was not running\n")

            pass

    logging.info('End Function Check if processes are running')
    file.write("\n")
    file.close()

    return False


def find_process_id_by_name(process_name):
    """
    Get a list of all the PIDs of a all the running process whose name contains
    the given string processName
    """
    global tabulate_proc

    file = open("Output\\process-scan-results.txt", "a")
    file.write("*** Find PIDs of a running process by Name ***\n")

    logging.info('Start Function to get a list of processes by the given processName')

    list_of_process_objects = []

    logging.info('Begin loop to iterate over all the running processes')

    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            if process_name[0].lower() in proc.name().lower():
                pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
                print(pinfo)
                file.write(str(pinfo))
                file.write("\n")

            # Check if process name contains the given name string.
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    logging.info('End function to iterate over all the running processes')
    file.write("\n")
    file.close()

    return list_of_process_objects


def main(proc_lijst):
    exe = str(','.join(proc_lijst[1]))
    file = open("Output\\process-scan-results.txt", "a")

    logging.info("\n---PROCESS SCANNER---")
    logging.info('Start process main')

    # process by path (make exe a list or array []
    print("\n*** found process by path ***")
    find_procs_by_path(exe)

    # Check if any chrome process was running or not.
    print("\n*** Check if a process is running or not ***")
    read_process_list(proc_lijst[0])

    print("\n*** Find PIDs of a running process by Name ***")
    show_processes(proc_lijst)

    file.write(120 * "-")
    file.close()


if __name__ == '__main__':
    main()
