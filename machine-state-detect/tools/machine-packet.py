import json
import yaml



class Machine:
    def __init__(self,_id):
        self._id = _id
        self._status = None
        self._event = None


    @property
    def id(self):
        return self._id
    
    @property
    def event(self):
        return self._event

    @event.setter
    def event(self, value):
        self._event = value

   
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value



if __name__ == "__main__":

    m = Machine("hello")
    m.event="world"
    m.status = "Idle"

    import time,sys
    sys.stdout.write("MachineID: {}".format(m.id))
    time.sleep(0.5)
    sys.stdout.write("\r")

    sys.stdout.write("MachineEvent: {}".format(m.event))
    time.sleep(0.5)
    sys.stdout.write("\r")

    sys.stdout.write("MachineStatus: {}".format(m.status))
    time.sleep(0.5)
    sys.stdout.write("\r")


    print("")

