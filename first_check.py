import usb1


def listAvailableDevices():
    ports = []
    try:
        with usb1.USBContext() as context:
            for device in context.getDeviceIterator(skip_on_error=True):
                cs = 'connected'
                ports.append({
                    'bus_id': device.getBusNumber(),
                    'device_address': device.getDeviceAddress(),
                    'product': device.getProduct(),
                    'manufacturer': device.getManufacturer(),
                    'vendor_id': device.getVendorID(),
                    'product_id': device.getProductID(),
                    'current_state': cs
                }
                )
    except usb1.USBError as e:
        raise Exception("USB Error: %s", e)
    return ports

