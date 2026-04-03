from googlecalendar import theCalendar, extractPresent
from agent import returnJSON
from extraction import extract_text_from_image
import os
import json

from datetime import datetime

# files = []
# path = "C:/CS/Scheduler/testfiles/dbmsASSIGN.png"
# files.append(path)

#userInput = input()

def retriveFileNamefromFileObj(files):
    names = []
    for originName in files:
        if type(originName) == str:
            names.append(originName)
            continue
        else:
            tempName = f"C:/CS/Scheduler/testfiles/{originName.name}"
            with open(tempName, "wb") as f:
                f.write(originName.read())
            #print("XXX", tempName)
            names.append(tempName)
    return names

def processInput(userInput, files):
    fileNamesList = retriveFileNamefromFileObj(files)
    #print("HEHA", fileNamesList)
    #print("BUT", fileNamesList)
    result = returnJSON(fileNamesList, userInput)
    #print("TAHI", result)
    rawJSlist = json.loads(result)

    #print(rawJSlist)

    logResults = []

    print("DEBUG", rawJSlist)
    for rawJS in rawJSlist:
        if not theCalendar(rawJS):
            logResults.append(f"Failed to create event '{rawJS["title"]}'")
        else:
            logResults.append(f"Succesfully created event '{rawJS["title"]}'")

    return logResults

# if __name__ == __main__: 
# processInput("", files=files)
    
 