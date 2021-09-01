import configparser

config = configparser.ConfigParser()
config.read("config.ini")
path_logfile = config["Daemon"]["path_log"]

with open(path_logfile, 'w') as f:
    import first_check

    for i in first_check.listAvailableDevices():
        f.write(', '.join([str(j) for j in i.values()]))
        f.write('\n')
