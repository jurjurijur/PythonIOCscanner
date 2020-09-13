from Input import InputValidator
from Input import InputInterpeter

"""Maak De Objecten aan"""
validate = InputValidator.InputValidator()
interpert = InputInterpeter.InputInterpeter()

"""Validate de Input en krijg Raw String[] terug"""
registryList, fileList, eventList, processList, configList = validate.getInput("textfile.txt")

""" Parse de Registry Input """
registryList = interpert.transformRegistryInput(registryList)

""" Parse de File Input """
fileList = interpert.transformFileInput(fileList)

""" Parse de Event Input """
eventList = interpert.transformEventInput(eventList)

""" Parse de process Input """
processList = interpert.transformProcessInput(processList)

""" Parse de config Input """
configList = interpert.transformConfigInput(configList)

print("------------------- Zo Levert hij de Registry Input op: ----------------------")
print(registryList)
print("------------------- Zo Levert hij de File Input op: ----------------------")
print(fileList)
print("------------------- Zo Levert hij de Event Input op: ----------------------")
print(eventList)
print("------------------- Zo Levert hij de Process Input op: ----------------------")
print(processList)
print(configList)

