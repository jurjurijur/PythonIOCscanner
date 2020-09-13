from EventLog_Scan import EventRequest

class InputInterpeter:

    def transformEventInput(self, rawEventlist):
        EventRequestList = []
        if rawEventlist:
            for record in rawEventlist:
                for i in range(len(record)):
                    if record[i] == "" or record[i] == "None" or record[i] == "NONE":
                        record[i] = None
                try:
                    logtype = record[0].strip()
                    if record[1] is not None:
                        eventType = int(record[1])
                    else:
                        eventType = None
                    if record[2] is not None:
                        eventID = int(record[2])
                    else:
                        eventID = None
                    sid = record[3]
                    sourceName = record[4]
                    stringInserts = record[5]
                    if record[6] is not None:
                        eventCategory = int(record[6])
                    else:
                        eventCategory = None
                    data = record[7]
                    computerName = record[8]
                    event = EventRequest.EventRequest(logtype, eventType, eventID, sid, sourceName,
                                                      stringInserts, eventCategory, data, computerName)
                    EventRequestList.append(event)
                except TypeError:
                    """Record is not correct"""
                    print("Event Record is wrong")
            return EventRequestList
        else:
            """list is empty"""
            return False

    def transformRegistryInput(self, rawRegistryList):
        RegistryList = []
        Hkeylist = []
        Pathlist = []
        filter_choice = []
        filter_type = []
        filter_name = []

        if rawRegistryList:
            for record in rawRegistryList:
                Hkeylist.append(record[0])
                Pathlist.append(record[1])
                filter_choice.append(record[2])
                filter_type.append(record[3])
                filter_name.append(record[4])

            RegistryList.append(Hkeylist)
            RegistryList.append(Pathlist)
            RegistryList.append(filter_choice)
            RegistryList.append(filter_type)
            RegistryList.append(filter_name)

            return RegistryList
        else:
            """"list is empty"""
            return False

    def transformFileInput(self, rawFileList):
        FileList = []
        file_path_list = []
        file_size_name = []

        if rawFileList:
            for record in rawFileList:
                file_path_list.append(record[0])
                file_size_name.append(record[1])
            FileList.append(file_path_list)
            FileList.append(file_size_name)

            return FileList
        else:
            # List is empty
            return False

    def transformProcessInput(self, rawProcessList):
        ProcessList = []
        ProcessNameList = []
        SourcePathList = []

        if rawProcessList:
            for record in rawProcessList:
                ProcessNameList.append(record[0])
                SourcePathList.append(record[1])
            ProcessList.append(ProcessNameList)
            ProcessList.append(SourcePathList)

            return ProcessList

        else:
            """list is empty"""
            return False

    def transformConfigInput(self, rawConfigList):
        ConfigList = []
        if rawConfigList:
            for record in rawConfigList:
                ConfigList.append(record)
            return ConfigList
        else:
            """list is empty"""
            return False

