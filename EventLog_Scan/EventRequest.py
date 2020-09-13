class EventRequest:
    ID = 0

    def __init__(self,logType, eventType, eventID, sid, sourceName, stringInserts, eventCategory, data, computerName, found = False):
        self.EventID = eventID
        self.EventType = eventType
        self.EventCategory = eventCategory
        self.SourceName = sourceName
        self.StringInserts = stringInserts
        self.Sid = sid
        self.Data = data
        self.ComputerName = computerName
        self.LogType = self.logTypeTransform(logType)
        self.Found = found

    def logTypeTransform(self, logType):
        if logType == "audit_failure":
            logType = "EVENTLOG_AUDIT_FAILURE"
        elif logType == "audit_succes":
            logType = "EVENTLOG_AUDIT_SUCCESS"
        elif logType == "information_type":
            logType = "EVENTLOG_INFORMATION_TYPE"
        elif logType == "warning_type":
            logType = "EVENTLOG_WARNING_TYPE"
        elif logType == "error_type":
            logType = "EVENTLOG_ERROR_TYPE"
        elif logType == " " or logType == "ALL" or logType == "all":
            logType = "ALL"
        return logType
