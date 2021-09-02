import configparser
import os

import inotify.adapters
import usb1

config = configparser.ConfigParser()
path = os.path.abspath(os.curdir)
config.read(os.path.join(path, "config.ini"))
path_logfile = os.path.join(path, config["Daemon"]["path_log"])



def read_log():
    ports = {}
    try:
        with open(path_logfile, 'r') as f:
            for line in f.readlines():
                i = line.strip().split(', ')
                port_id = (i[4], i[5])
                ports[port_id] = {
                    'bus_id': i[0],
                    'device_address': i[1],
                    'product': i[2],
                    'manufacturer': i[3],
                    'vendor_id': i[4],
                    'product_id': i[5],
                    'current_state': i[6]
                }
    except FileNotFoundError:
        with open(path_logfile, 'w'):
            pass
    return ports


def write_log(ports):
    with open(path_logfile, 'w') as f:
        for i in ports.values():
            f.write(', '.join(i.values()))
            f.write('\n')


def merge_two_dicts(x, y):
    return {**x, **y}


def listAvailableDevices():
    ports = {}
    try:
        with usb1.USBContext() as context:
            for device in context.getDeviceIterator(skip_on_error=True):
                vid = str(device.getVendorID())
                pid = str(device.getProductID())
                port_id = (vid, pid)
                cs = 'connected'
                ports[port_id] = {
                    'bus_id': str(device.getBusNumber()),
                    'device_address': str(device.getDeviceAddress()),
                    'product': str(device.getProduct()),
                    'manufacturer': str(device.getManufacturer()),
                    'vendor_id': vid,
                    'product_id': pid,
                    'current_state': cs
                }
    except usb1.USBError:
        pass
    return ports


def get_update_dict():
    old_ports = read_log()
    new_ports = listAvailableDevices()
    diff_ports_keys = old_ports.keys() - new_ports.keys()
    union_ports = merge_two_dicts(old_ports, new_ports)
    for i in diff_ports_keys:
        union_ports[i]['current_state'] = 'disconnected'
    return union_ports


def start_updating():
    skip_name = {'null', 'kmsg', 'urandom'}
    event_type = {'IN_DELETE', 'IN_ATTRIB'}
    i = inotify.adapters.Inotify()
    i.add_watch('/dev/')
    for event in i.event_gen(yield_nones=False):
        (_, type_names, _, filename) = event
        if (filename not in skip_name) and (type_names[0] in event_type):
            updated_dict = get_update_dict()
            write_log(updated_dict)
