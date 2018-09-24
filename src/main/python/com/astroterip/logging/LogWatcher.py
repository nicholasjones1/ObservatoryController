#
#  Name: LogWatcher
#  Version: 1.0
#  Author: Nicholas Jones
#  com.astroterip.logging.LogWatcher
#  Description: Monitor log files in a particular file system folder for any new occurrences of a piece of text.
#               When a match if found, a user specified batch file is executed.
#               The application is strictly readonly.

import os
import argparse
import configparser
import time
import threading
from subprocess import Popen


class LogFile:
    def __init__(self, config, filename):
        self.config = config
        # self.path = config.g
        self.filename = filename
        self.logPosition = 0
        self.changed = False
        self.lastModified = ""
        self.size= -1

    def updateFromOs(self):
        filePath = os.path.join(self.config.logFolder, self.filename)
        size = os.path.getsize(filePath)
        if (size != self.size):
            self.changed = True
        # end if
        self.size = os.path.getsize(filePath)
        self.lastModified = time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getmtime(filePath)))
    # end def

    def printToStdio(self, text):
        datetimeStamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(datetimeStamp + " " + self.config.getName() + ": " + text)

    def getLastLineMatchingText(self, text, intialLoading):
        filePath = os.path.join(self.config.logFolder, self.filename)
        position = 0
        matchPosition = False

        with open(filePath, 'r') as f:
            for line in f:
                position = position + 1
                if position > self.logPosition or self.logPosition == 0:
                    # process_line(line)
                    # update the file line number position that has been processed to avoid reprocessing
                    # on subsequent scans

                    if text in line:
                        if not intialLoading:
                            self.printToStdio("found matching text in log " + self.filename + " at position " + str(position))
                        # end if
                        matchPosition = True
                    # end if
                # end if

            # end for loop
            self.logPosition = position
        # end with open file scope
        return matchPosition
    # end def
# end class LogFile


# class to list the log files that are present in the log folder.
class LogFileList:
    def __init__(self, config):
        self.config = config
        #self.path = path
        #self.fileExtension = fileExtension
        #self.text = text
        self.logFileList = []

    # this just cleans the in-memory references to log files
    # remove bookmarks of files that have been removed from the logging folder
    def cleanLogList(self):
        for logFile in self.logFileList:
            filePath = os.path.join(self.config.logFolder, logFile.filename)
            if not os.path.exists(filePath):
                self.printToStdio("log " + logFile.filename + " no longer exists, remove from the logWatch")
                self.logFileList.remove(logFile)
            # end if
        # end for
    # end def

    def printToStdio(self, text):
        datetimeStamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(datetimeStamp + " " + self.config.getName() + ": " + text)

    # scanLogs - check if there's any new text matches
    def scanLogsForMatch(self, initialLoad):
        self.cleanLogList()

        for filename in os.listdir(self.config.logFolder):
            filePath = os.path.join(self.config.logFolder, filename)
            if not os.path.isdir(filePath):
                if filePath.endswith(self.config.logFileExtension):
                    logFile = self.getFileInList(filename)
                    if not self.getFileInList(filename):
                        logFile = LogFile(self.config, filename)
                        self.logFileList.append(logFile)
                        self.printToStdio("add log file to scanning: " + filePath)
                    # end if not in list
                # end if
            # end if
        # end for loop

        newMatch = False

        for logFile in self.logFileList:
            currentFilePath = os.path.join(self.config.logFolder, logFile.filename)
            dateTimeStamp = time.strftime('%Y%m%d%H%M%S', time.gmtime(os.path.getmtime(currentFilePath)))
            # only bother scanning the file if it has been updated
            if (dateTimeStamp > logFile.lastModified):
                self.printToStdio("scan " + logFile.filename)
                if logFile.getLastLineMatchingText(self.config.logSeachText, initialLoad):
                    newMatch = True
                # end if
            # end if
            logFile.updateFromOs()
        # end if

        return newMatch
    # end def

    # retrieve the logFile object from the logFileList
    def getFileInList(self, filename):
        for logFile in self.logFileList:
           if logFile.filename == filename:
               return logFile
           # end if
        # end for
        return None
    # end def
# end class



class LogWatcherConfig:
    def __init__(self, name, logFolder, logFileExtension, searchText, executionFile, scanInterval):
        self.name = name
        self.logFolder = logFolder
        self.logFileExtension = logFileExtension
        self.logSeachText = searchText
        self.executionFile = executionFile
        self.scanInterval = scanInterval
    # end def

    def getName(self):
        return self.name

# end class


class LogWatcherConfigMgr:
    def __init__(self, configPath):
        self.configPath = configPath
        self.config = configparser.ConfigParser()
        self.config.read(self.configPath)
        self.logWatchLocations = []

        name = self.config['logwatch_1']['name']
        logFolder = self.config['logwatch_1']['folder']
        logFileExtension = self.config['logwatch_1']['fileExtension']
        logSearchText = self.config['logwatch_1']['searchText']
        executionFile = self.config['logwatch_1']['executionFile']
        scanInterval = self.config['logwatch_1']['scanInterval']

        logWatcherConfig = LogWatcherConfig(name, logFolder, logFileExtension, logSearchText, executionFile, scanInterval)
        self.logWatchLocations.append(logWatcherConfig)
    # end def

    def getConfig(self):
        return self.logWatchLocations[0];
    # end def

# end class



def eggTimer():
    global eggsAreReady
    eggsAreReady = True
# end def




def main(args):
    configMgr = LogWatcherConfigMgr("logWatcher.ini")
    config = configMgr.getConfig();

    logFileList = LogFileList(config)

    # initial load to by-pass any existing matches
    logFileList.scanLogsForMatch(True)

    global eggsAreReady
    eggsAreReady = False
    t = threading.Timer(int(config.scanInterval), eggTimer)
    t.start()

    while (True):
        if eggsAreReady:
            if logFileList.scanLogsForMatch(False):
                p = Popen(config.executionFile)
            # end if

            t.cancel()
            eggsAreReady = False

            # restart
            t = threading.Timer(int(config.scanInterval), eggTimer)
            t.start()
        # end if

        time.sleep(2)
    # end while
# end def main


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Log watch-dog to lookout for text and call a .bat file if it appears')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')

    args = parser.parse_args()

    main(args)
# end if

# main([])