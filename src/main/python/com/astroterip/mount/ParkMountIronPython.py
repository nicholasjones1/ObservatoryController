import clr
import time
import sys

# "key:AstroPhysicsV2.Telescope value:AstroPhysics GTO V2 Mount"
# info from
# http://www.ascom-standards.org/Help/Developer/html/T_ASCOM_DriverAccess_Telescope.htm
clr.AddReference("ASCOM.DriverAccess.dll")
clr.AddReference("ASCOM.Utilities.dll")
clr.AddReference("ASCOM.DeviceInterfaces.dll")

from ASCOM.DriverAccess import *
from ASCOM.Utilities import *
from ASCOM.DeviceInterface import *


print ("Running: ", sys.argv[0])

if len(sys.argv) != 2 :
    print("Usage: " + sys.argv + "<ASCOM name of Scope")
    #ASCOM.Simulator.Telescope
    exit(1)
#end if

mount= ""

try:
    mount = Telescope(sys.argv[1])
except:
    print("Cannot connect to " +sys.argv[1])
    exit(1)

#connect to the mount
mount.Connected = True
if (not mount.Connected):
    print("Cannot connect to " +sys.argv[1])
    exit(2)
#end if

print("Connected to " + sys.argv[1])

# unpark and go somewhere to test parking logic
mount.Unpark()
# stop traking so that a slew can be performed
# not all mount drivers support this, will have to test it on AP
mount.Tracking = False

# this is a blocking call - when it completes it has finished slewing

print("slewing to  az 0.5, 77 alt, near the meridian")
mount.SlewToAltAz(0.5, 77)

if (mount.Tracking):
    mount.Tracking = False

if (mount.AtPark == False):
    print(sys.argv[1] + " is currently unparked...")
    time.sleep(1)
    mount.Park()
else:
    print(sys.argv[1] + " is already parked")
#end if

if (mount.AtPark == True):
    print(sys.argv[1] + " has been parked")
    exit(0)
#end if

print("Cannot park " + sys.argv[1])
