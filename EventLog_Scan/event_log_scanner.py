import win32evtlog
import traceback
import sys
import logging
import json
import os


new_dir = "Output\\"
if not os.path.exists(new_dir):
    os.makedirs(new_dir)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(funcName)s:%(message)s')

file_handler = logging.FileHandler('Output\\eventScannerResults.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class EventLogScanner:
    run = True
    auditSuccesArray = []
    auditFailArray = []
    informationTypeArray = []
    warningTypeArray = []
    errorTypeArray = []
    machine = "localhost"

    def __init__(self, eventRequestArray):
        # eventRequestArray.sort(key=lambda x: x.LogType, reverse=True)
        self.divideInputInAppropriateList(eventRequestArray)
        self.runScanner(self.machine)

    ''''divide input into one of 5 lists that are required to open that specifik event log'''

    def divideInputInAppropriateList(self, eventRequestArray):
        for i, event in enumerate(eventRequestArray):
            if event.LogType == "EVENTLOG_AUDIT_FAILURE" or event.LogType == "ALL":
                event.ID = i
                self.auditFailArray.append(event)
            if event.LogType == "EVENTLOG_AUDIT_SUCCESS" or event.LogType == "ALL":
                event.ID = i
                self.auditSuccesArray.append(event)
            if event.LogType == "EVENTLOG_INFORMATION_TYPE" or event.LogType == "ALL":
                event.ID = i
                self.informationTypeArray.append(event)
            if event.LogType == "EVENTLOG_WARNING_TYPE" or event.LogType == "ALL":
                event.ID = i
                self.warningTypeArray.append(event)
            if event.LogType == "EVENTLOG_ERROR_TYPE" or event.LogType == "ALL":
                event.ID = i
                self.errorTypeArray.append(event)

    def compareLogRecordWithList(self, eventArray, readRecord):
        """"* this function is strongly dependant on a the list being sorted on all values with NONE at the bottom
              Very important that the array values are in the same order as that the list is sorted
        *"""
        seenValue = False
        parameterNameArray = ['EventType', 'EventID', 'Sid', 'SourceName', 'StringInserts', 'EventCategory',
                              'Data', 'ComputerName']
        indexOfParameters = 0
        givenParamToCheck = "event." + parameterNameArray[indexOfParameters]
        readParamToCheck = "readRecord." + parameterNameArray[indexOfParameters]
        try:
            for event in eventArray:
                if eval(givenParamToCheck) == eval(readParamToCheck):
                    self.compareIOCRecordWithLogRecord(event, readRecord)
                    seenValue = True
                elif eval(givenParamToCheck) != eval(readParamToCheck) and seenValue:
                    if eval(givenParamToCheck) is None:
                        indexOfParameters += 1
                        givenParamToCheck = "event." + parameterNameArray[indexOfParameters]
                        readParamToCheck = "readRecord." + parameterNameArray[indexOfParameters]
                        seenValue = False
                        if eval(givenParamToCheck) == eval(readParamToCheck):
                            self.compareIOCRecordWithLogRecord(event, readRecord)
                            seenValue = True
                elif eval(givenParamToCheck) is None and not seenValue:
                    indexOfParameters += 1
                    givenParamToCheck = "event." + parameterNameArray[indexOfParameters]
                    readParamToCheck = "readRecord." + parameterNameArray[indexOfParameters]
                    if eval(givenParamToCheck) == eval(readParamToCheck):
                        self.compareIOCRecordWithLogRecord(event, readRecord)
                        seenValue = True
        except:
            try:
                logger.info(traceback.print_exc(sys.exc_info()))
            except:
                logger.info("Exeption Cant compare record with Input List")

    def compareIOCRecordWithLogRecord(self, givenIOCRecord, readLogRecord):
        """Compare amount of parameters given with the amount of matches within the LOG record
               if all given values are equal it is a match
        """
        amountOfParametersGiven = 0
        amountOfMatchesFound = 0
        parameterNameArray = ['EventType', 'EventID', 'Sid', 'SourceName', 'StringInserts', 'EventCategory',
                              'Data', 'ComputerName']
        """For each Parameter defined in the parameterNameArray: 
                make a string for both objects with the parameter we want to check
                parse the string to an expression and check if the value is not None 
                    if the value is not None check if is equal to the read object
        """
        for parameterName in parameterNameArray:
            givenParamToCheck = "givenIOCRecord." + parameterName
            readParamToCheck = "readLogRecord." + parameterName
            if eval(givenParamToCheck) is not None:
                amountOfParametersGiven += 1
                if eval(givenParamToCheck) == eval(readParamToCheck):
                    amountOfMatchesFound += 1
        if amountOfParametersGiven == amountOfMatchesFound:
            givenIOCRecord.Found = True
            try:
                record = {"matchID": str(givenIOCRecord.ID),
                          "Reserved": str(readLogRecord.Reserved),
                          "RecordNumber": str(readLogRecord.RecordNumber),
                          "TimeGenerated": str(readLogRecord.TimeGenerated),
                          "TimeWritten": str(readLogRecord.TimeWritten),
                          "EventType": str(readLogRecord.EventType),
                          "EventID": str(readLogRecord.EventID),
                          "ReservedFlags": str(readLogRecord.ReservedFlags),
                          "ClosingRecordNumber": str(readLogRecord.ClosingRecordNumber),
                          "Sid": str(readLogRecord.Sid),
                          "SourceName": str(readLogRecord.SourceName),
                          "EventCategory": str(readLogRecord.EventCategory),
                          "StringInserts": str(readLogRecord.StringInserts),
                          "Data": str(readLogRecord.Data),
                          "ComputerName": str(readLogRecord.ComputerName)}

                self.writeOutput(record)
            except Exception as e:
                logger.info(e)
                try:
                    logger.info(traceback.print_exc(sys.exc_info()))
                except:
                    logger.info('Exception Log Record Cant be Constucted')

        else:
            return False

    def readEventLog(self, server, log_type, eventArray):
        '''
        Reads the log_type (e.g., "Application" or "System") Windows events from the
        specified server.
        '''
        try:
            """Open Log File and sort array on Event ID"""
            log_handle = win32evtlog.OpenEventLog(server, log_type)
            flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
            total = win32evtlog.GetNumberOfEventLogRecords(log_handle)
            try:
                eventArray.sort(key=lambda x: (x.EventType or 0, x.EventID or 0, x.Sid or 0, x.SourceName or '',
                                               x.StringInserts or '', x.EventCategory or 0, x.Data or '',
                                               x.ComputerName or ''), reverse=True)
            except Exception as e:
                print(e)
                try:
                    logger.info(traceback.print_exc(sys.exc_info()))
                except:
                    logger.info('Exception sort went wrong')
            logger.info("Scanning through {} events on {} in {}".format(total, server, log_type))

            """As long as there are events keep reading"""
            readEvent_count = 0
            readEvents = 1
            while readEvents:
                readEvents = win32evtlog.ReadEventLog(log_handle, flags, 0)
                for readEvent in readEvents:
                    self.compareLogRecordWithList(eventArray, readEvent)
                    readEvent_count += 1
            """"Close Log File"""
            logger.info("Scanned through {} events on {} in {}".format(readEvent_count, server, log_type))
            win32evtlog.CloseEventLog(log_handle)
        except:
            logger.info("I cant read yar bastard")
            try:
                logger.info(traceback.print_exc(sys.exc_info()))
            except:
                logger.info('Exception while printing traceback')

    def runScanner(self, machine):
        """While run is true
            1. read logtype from input
            2. read logtypes
        """
        if self.auditFailArray:
            self.readEventLog(machine, 'EVENTLOG_AUDIT_FAILURE', self.auditFailArray)
            self.writeInputRecords(self.auditFailArray)
        if self.auditSuccesArray:
            self.readEventLog(machine, 'EVENTLOG_AUDIT_SUCCESS', self.auditSuccesArray)
            self.writeInputRecords(self.auditSuccesArray)
        if self.informationTypeArray:
            self.readEventLog(machine, 'EVENTLOG_INFORMATION_TYPE', self.informationTypeArray)
            self.writeInputRecords(self.informationTypeArray)
        if self.warningTypeArray:
            self.readEventLog(machine, 'EVENTLOG_WARNING_TYPE', self.warningTypeArray)
            self.writeInputRecords(self.warningTypeArray)
        if self.errorTypeArray:
            self.readEventLog(machine, 'EVENTLOG_ERROR_TYPE', self.errorTypeArray)
            self.writeInputRecords(self.errorTypeArray)

    def writeInputRecords(self, inputArray):
        for event in inputArray:
            record = {'ID': str(event.ID),
                      'EventType': str(event.EventType),
                      'EventID': str(event.EventID),
                      'Sid': str(event.Sid),
                      'SourceName': str(event.SourceName),
                      'EventCategory': str(event.EventCategory),
                      'StringInsterts': str(event.StringInserts),
                      'Data': str(event.Data),
                      'ComputerName': str(event.ComputerName),
                      'logType': str(event.LogType),
                      'Found': str(event.Found)}
            self.writeOutput(record)

    def writeOutput(self, line):
        File = open("Output\\eventOutput.json", "a")
        File.write(json.dumps(line))
        File.write("\n")
        File.close()

# def stopScanner(self):
#    self.run = False
#   return
