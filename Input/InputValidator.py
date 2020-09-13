class InputValidator:
    def getInput(self, inputFileLocation):
        inputFile = open(inputFileLocation, "r")
        registryList = []
        fileList = []
        eventList = []
        processList = []
        configList = []

        for line in inputFile:
            if '---BEGIN_REGISTRY_SCAN---\n' in line.replace(" ", ""):
                for line in inputFile:
                    if line.replace(" ", "") == "---END---\n":
                        break
                    elif line[0] != "#":
                        """" Begin Parsing Records """
                        if line.strip():
                            if line.split(";;"):
                                 parsedLine = line.replace("\n", "")
                                 parsedLine = parsedLine.split(";;")
                                 registryList.append(parsedLine)
                            else:
                                 self.handleParseConflicts(line)

            if '---BEGIN_FILE_SCAN---\n' in line.replace(" ", ""):
                for line in inputFile:
                    if line.replace(" ", "") == "---END---\n":
                        break
                    elif line[0] != "#":
                        """" Begin Parsing Records """
                        if line.strip():
                            if line.split(";;"):
                                parsedLine = line.replace("\n", "")
                                parsedLine = parsedLine.split(";;")
                                fileList.append(parsedLine)
                            else:
                                self.handleParseConflicts(line)

            if '---BEGIN_EVENTLOG_SCAN---\n' in line.replace(" ", ""):
                for line in inputFile:
                    if line.replace(" ", "") == "---END---\n":
                        break
                    elif line[0] != "#":
                        """" Begin Parsing Records """
                        if line.strip():
                            if line.split(";;"):
                                parsedLine = line.replace("\n", "")
                                parsedLine = parsedLine.split(";;")
                                eventList.append(parsedLine)
                            else:
                                self.handleParseConflicts(line)

            if '---BEGIN_PROCESS_SCAN---\n' in line.replace(" ", ""):
                for line in inputFile:
                    if line.replace(" ", "") == "---END---\n":
                        break
                    elif line[0] != "#":
                        """" Begin Parsing Records """
                        if line.strip():
                            if line.split(";;"):
                                parsedLine = line.replace("\n", "")
                                parsedLine = parsedLine.split(";;")
                                processList.append(parsedLine)
                            else:
                                self.handleParseConflicts(line)

            if '---BEGIN_CONFIG---\n' in line.replace(" ", ""):
                for line in inputFile:
                    if line.replace(" ", "") == "---END---\n":
                        break
                    elif line[0] != "#":
                        """" Begin Parsing Records """
                        if line.strip():
                            if line.split(";;"):
                                parsedLine = line.replace("\n", "")
                                parsedLine = parsedLine.split(";;")
                                configList.append(parsedLine)
                            else:
                                self.handleParseConflicts(line)

        inputFile.close()
        return registryList, fileList, eventList, processList

    def handleParseConflicts(self, line):
        """Something is wrong with the record"""
        print(line)