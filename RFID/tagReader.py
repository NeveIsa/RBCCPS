import mercury
import sys

printnl=lambda x:sys.stdout.write(x)
defaultCB=lambda x:sys.stdout.write("DEFAULT CB: " + repr(x))

class isaRFID:
    def __init__(self,port):
        #reader = mercury.Reader("tmr:///dev/ttyUSB0")
        self.reader = mercury.Reader("tmr://{}".format(port))

    def test(self):
        print(self.reader.get_supported_regions())
        print(self.reader.get_read_powers())

    # Power is in centidBm, max power is 27dBm, so max value = 2700
    def setup(self,power=300):
        print("\nDEBUG: Setting power to %s centidBm.\n" % power)
        self.reader.set_region("IN")
        self.reader.set_read_plan([1], "GEN2",read_power=power)

        #setted_powers = self.eader.set_read_powers([1, 2], [500, 100])
        #print(setted_powers)

    def startReading(self,cb=defaultCB,_timeout=None,debug=True):
        if _timeout:
            readfn=lambda:self.reader.read(timeout=_timeout)
        else:
            readfn=self.reader.read

        while True:
            try:
                tags=readfn()
                if debug:
                    printnl("DEBUG: ")
                    print(tags)
                if len(tags):
                    printnl("Detected: ")
                    print(tags)
            except Exception as e:
                printnl("EXCEPTION: ")
                print(e)
                


if __name__=="__main__":
    
    import time
    RFIDreader=0

    def setupReader():
        global RFIDreader
        RFIDreader=isaRFID("/dev/ttyUSB0")
        RFIDreader.test()
        RFIDreader.setup(power=700)

    def destroyReader():
        global RFIDreader
        del RFIDreader

    setupReader()

    while True:
        try:
            RFIDreader.startReading()
        except Exception as e:
            printnl("FATAL: ")
            print(e)
            time.sleep(1)
