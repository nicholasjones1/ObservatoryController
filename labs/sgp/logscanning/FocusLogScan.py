import os
import sys
import re
import argparse
import logging
import threading
import time

# [04/22/18 01:46:06.176][DEBUG][CameraThread] New focus position is at 88386(@8.08C).  Moving focuser...

FilterPostionRegex = "Setting filter position ([1-9]{1})...";
FocusPostionRegex = " New focus position is at ([0-9]{1,5})...([0-9]{1,2}.[0-9]+)...  Moving focuser...";
FilterNameRegex = "Auto focus: setting filter"

class LogFile:
    def __init__(self):
        self.filename = ""
        self.lastModified = ""
        self.changed = False
        self.size = -1
        self.bookmark = 0
# end class

class FocusResult:
    def __init__(self):
        self.observatory = ""
        self.equipmentProfile = ""
        self.datetime = ""
        self.position = 0
        self.temp = 0
        self.name = ""
# end class

focusPositionList = []
currentFilter = ""

def process_line(line):

    global currentFilter

    if "Auto focus: setting filter" in line:
        currentFilter = line.split().pop()
    # end if

    if "Temperature compensation" in line:
        print(line)
    # end if

    if "Focuser moving to" in line:
        print(line)
    #end if

    if "New focus position is at" in line:
        #logging.info(line)
        valueList = re.split("(\[.+?\])", line)

        if valueList:
            datetime = valueList[1]
            datetime = datetime.replace("[", "").replace("]", "")
            matchObj = re.match(FocusPostionRegex, valueList[6], 0)
            if matchObj:
                focusResult = FocusResult()
                focusResult.name = currentFilter
                focusResult.datetime = datetime
                focusResult.position = matchObj.group(1)
                focusResult.temp = matchObj.group(2)
                focusPositionList.append(focusResult)
            # endif
        # end if
    # end if

  #  if "Exception" in line:
  #      logging.error(line)
    # end if

# def process_line


logBookmarks = {}


def scan_file(filename):
    canonicalFileName = filename.replace('\\', '').replace(':', '')

    if canonicalFileName in logBookmarks:
        logFile = logBookmarks[canonicalFileName]
    else:
        logFile = LogFile()
        logFile.filename = filename
        logBookmarks.update({canonicalFileName: logFile})
    # end if else

    if (os.path.getsize(filename) < logFile.size):
        logFile.bookmark = 0
    # end if

    if os.path.getsize(filename) != logFile.size:
        print("Size: {} Last modified: {}".format(os.path.getsize(filename), time.ctime(os.path.getmtime(filename))))
        logFile.size = os.path.getsize(filename)
        logFile.lastModified = time.ctime(os.path.getmtime(filename))
        logFile.changed = True

        with open(filename, 'r') as f:
            position = 0;
            for line in f:
                position = position + 1
                if position > logFile.bookmark:
                    process_line(line)
                    # update the file line number position that has been processed to avoid reprocessing
                    # on subsequent scans
                    logFile.bookmark = position
                # end if
            # end for loop
        # end with open file scope
    else:
        logFile.changed = False
    # end else
# end def

def scan_directory(path, recursive, fileExtension):
    for filename in os.listdir(path):
        sChildPath = os.path.join(path, filename)
        if os.path.isdir(sChildPath):
            if recursive:
                scan_directory(sChildPath, recursive, fileExtension)
            # end if
        else:
            if sChildPath.endswith(fileExtension):
                print("Scan file: ", sChildPath)
                scan_file(sChildPath)
            # end if
        # end if else
    # end for loop


# end print_directory


def isUpdated():
    for key, logFile in logBookmarks.items():
        if logFile.changed:
            return True
        # end if
    # end for loop

    return False


# end def


def timer():
    global keepRunning
    print("Timer ended")
    keepRunning = False


# end def

# \\\\Mdj-observatory\\c\\Users\\astroterip\\AppData\\Local\\SequenceGenerator

def main(args):
    global keepRunning

    keepRunning = True

    t = threading.Timer(120, timer)

    while (keepRunning):

        scan_directory(args.folder,
                       args.recursive,
                       ".txt")
        if isUpdated():
            t.cancel()
            # restart
            t = threading.Timer(120, timer)
            t.start()

            for focus in focusPositionList:
                print("--------------------------------------------------------")
                print("   filter name: ", focus.name)
                print("      datetime: ", focus.datetime)
                print("focus position: ", focus.position)
                print("    focus temp: ", focus.temp)
            # end for loop
        # end if

        if not keepRunning:
            print("No logging activity detected - end scanning")
            exit(0)
        # end if



        time.sleep(20)

    # end while


# end if


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process log files whist they are being update')
    parser.add_argument('folder', help='The folder to scan')
    parser.add_argument('-r', '--recursive', type=bool, default=True,
                        help='whether the folder scan should be recursive or not')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    main(args)
# endif
