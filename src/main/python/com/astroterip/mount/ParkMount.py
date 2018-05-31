import configparser
import subprocess

from com.astroterip.mount.Mount import Mount


class ParkMountAction():
    def __init__(self, configPath):
        self.configPath = configPath
        config = configparser.ConfigParser()
        config.read(self.configPath)
        self.ascomTelescopeName = config['mount']['ascomName']
    #end def

    def run(self):
        print("parking " + self.ascomTelescopeName)
        params = [r"ParkMountIronPython.bat", self.ascomTelescopeName]
        rc = subprocess.run(params, shell=True)
        if rc.returncode == 1:
            print("there was an error")
            return Mount.UNPARKED;
        else:
            return Mount.PARKED;

#end class

configPath = "E:/dev/projects/ObservatoryController/src/main/python/com/astroterip/observatory.ini"
action = ParkMountAction(configPath)
action.run()


