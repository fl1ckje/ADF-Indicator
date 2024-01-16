from serial import Serial

arduino: Serial = None
serial_ports = []
rx_is_on = False
rx_data = ''
dir = 0.0


def init():
    global serial_ports
    global arduino
    global rx_is_on
    global rx_data
    global dir
