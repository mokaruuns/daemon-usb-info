#!/usr/bin/env python

import sys

import usb_daemon
from daemon3x import daemon3


class MyDaemon(daemon3):
    def run(self):
        usb_daemon.write_log(usb_daemon.listAvailableDevices())
        usb_daemon.start_updating()
        super(MyDaemon, self).run()


if __name__ == "__main__":
    daemon = MyDaemon('/tmp/usb-daemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print('start')
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
            print('stop')
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
