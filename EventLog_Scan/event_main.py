from EventLog_Scan import event_log_scanner
import win32evtlog
import traceback
import sys
from EventLog_Scan import EventRequest


def readEventLog(server, log_type):
    # Reads the log_type (e.g. "Application" or "System" from the Windows event viewer on the specified server

    try:
        # Open the log file and sort array on Event ID's
        log_handle = win32evtlog.OpenEventLog(server, log_type)
        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        total = win32evtlog.GetNumberOfEventLogRecords(log_handle)

        print("Scanning through {} events on {} in {}".format(total, server, log_type))

        # As long as there are events, keep reading
        readEvent_count = 1
        readEvents = 1
        events = []

        while readEvents:
            readEvents = win32evtlog.ReadEventLog(log_handle, flags, 1)

            for event in readEvents:
                events.append(event)
                readEvent_count += 1

        win32evtlog.CloseEventLog(log_handle)
        return events

    except:
        print("I can't read yar bastard")

        try:
            print(traceback.print_exc(sys.exc_info()))
        except:
            print("Exception whilst printing traceback")


def main():
    input_array = []
    event1 = EventRequest.EventRequest(13, 14, 233434, "lala", "evil.exe", 34, "lala", "mijnComputer", "information_type")
    event2 = EventRequest.EventRequest(13, 14, 233434, "lala", "evil.exe", 34, "lala", "mijnComputer", "audit_succes")
    event3 = EventRequest.EventRequest(13, 14, 233434, "lala", "evil.exe", 34, "lala", "mijnComputer", "audit_failure")
    event4 = EventRequest.EventRequest(13, 14, 233434, "lala", "evil.exe", 34, "lala", "mijnComputer", "error_type")
    event5 = EventRequest.EventRequest(13, 14, 233434, "lala", "evil.exe", 34, "lala", "mijnComputer", "warning_type")
    event6 = EventRequest.EventRequest(13, 14, 233434, "lala", "evil.exe", 34, "lala", "mijnComputer", " ")
    input_array.append(event1)
    input_array.append(event2)
    input_array.append(event3)
    input_array.append(event4)
    input_array.append(event5)
    input_array.append(event6)

    try:
        scan = event_log_scanner.EventLogScanner(input_array)
    except:
        try:
            print(traceback.print_exc(sys.exc_info()))
        except:
            print("Exception whilst printing traceback")


if __name__ == "__main__":
    main()
