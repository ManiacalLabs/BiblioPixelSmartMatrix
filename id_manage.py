# {'COM9': 2, 'COM8': 3, 'COM3': 1}
if __name__ == "__main__":
    import sys
    from bibliopixel import log
    from bibliopixel.drivers.serial_driver import DriverSerial
    from time import sleep

    def getDevices():
        ports = DriverSerial.findSerialDevices(hardwareID="16C0:0483")
        devs = []
        print "Available Devices:"
        count = 0
        for port in ports:
            id = DriverSerial.getDeviceID(port)
            devs.append((id, port))
            print "{}: {} - ID {}".format(count, port, id)
            count += 1
        return devs

    try:
        if len(sys.argv) == 1:
            run = True
            print "Press Ctrl+C any time to exit."
            while run:
                devs = getDevices()
                if len(devs):
                    try:
                        choice = raw_input("Enter Device To Modify: ")
                        try:
                            choice = int(choice)
                            if choice < 0 or choice >= len(devs):
                                raise ValueError()
                        except:
                            print "Invalid choice!"
                            continue

                        dev = devs[choice]
                        print "{} - Current ID: {}".format(dev[1], dev[0])
                        newID = raw_input("Input new ID: ")
                        if newID != '':
                            try:
                                newID = int(newID)
                                if newID < 0 or newID > 255:
                                    raise ValueError()

                                try:
                                    DriverSerial.setDeviceID(dev[1], newID)
                                    print "Device ID set to: {}".format(DriverSerial.getDeviceID(dev[1]))
                                except:
                                    pass
                            except ValueError:
                                print "Please enter a valid number between 0 and 255."
                    except Exception, e:
                        print e
                else:
                    print "No serial devices found. Please connect one."
        else:
            args = sys.argv[1:]
            if len(args) % 2 != 0:
                print "Must provide device and ID for each device!"
                sys.exit(1)

            devs = getDevices()
            ports = [port for id, port in devs]
            args = [tuple(args[i:i + 2]) for i in range(0, len(args), 2)]
            args = [(port, int(id)) for port, id in args]
            for port, id in args:
                if port not in ports:
                    print "{} not available!".format(port)
                print "Setting {} to ID: {}".format(port, id)
                DriverSerial.setDeviceID(port, id)
                sleep(1)

            getDevices()
    except KeyboardInterrupt, err:
        pass
    else:
        pass
