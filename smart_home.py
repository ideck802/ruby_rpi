import tinytuya

device = tinytuya.OutletDevice('ebb9985c9182dcafff8ucj', '192.168.1.15', 'dec9afdbcb8365a8')
device.set_version(3.3)
data = device.status()


def outlet_on():
    device.turn_on(switch=1)
    
def outlet_off():
    device.turn_off(switch=1)