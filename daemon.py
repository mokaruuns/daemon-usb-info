import configparser
import inotify.adapters
import usb1

config = configparser.ConfigParser()
config.read("config.ini")
path_logfile = config["Daemon"]["path_log"]


def read_log():
    ports = {}
    with open(path_logfile, 'r') as f:
        for i in f.readlines():
            i = i.split(', ')
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
    return ports


def write(ports):
    with open(path_logfile, 'w') as f:
        for i in ports.values():
            f.write(', '.join([str(j) for j in i.values()]))
            f.write('\n')


def merge_two_dicts(x, y):
    z = x.copy()  # start with x's keys and values
    z.update(y)  # modifies z with y's keys and values & returns None
    return z


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
                    'vendor_id': str(device.getVendorID()),
                    'product_id': str(device.getProductID()),
                    'current_state': cs
                }

    except usb1.USBError as e:
        return listAvailableDevices()
    return ports


def update():
    old_ports = read_log()
    old_ports_keys = old_ports.keys()
    new_ports = listAvailableDevices()
    new_ports_keys = new_ports.keys()
    all_ports = merge_two_dicts(old_ports, new_ports)
    intersection_ports_keys = old_ports_keys & new_ports_keys
    diff_ports_keys = old_ports_keys - intersection_ports_keys
    for i in diff_ports_keys:
        all_ports[i]['current_state'] = 'disconnected'
    write(all_ports)


def _main():
    skip_name = {'null', 'kmsg', 'urandom'}
    event_type = {'IN_DELETE', 'IN_ATTRIB'}
    i = inotify.adapters.Inotify()
    i.add_watch('/dev/')
    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        if (filename not in skip_name) and (type_names[0] in event_type):
            print(event)
            update()


if __name__ == '__main__':
    _main()
