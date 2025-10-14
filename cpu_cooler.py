import hid, pprint
from threading import Event, Thread
import psutil

def get_cpu_temp():
    #pprint.pprint(psutil.sensors_temperatures()['coretemp'])    
    temp = psutil.sensors_temperatures()['coretemp'][0].current    
    return temp

# GAMEMAX SIGMA 520 DEVICE
VENDOR_ID = 0x5131
PRODUCT_ID = 0x2007

device = hid.Device(VENDOR_ID, PRODUCT_ID)

def write_to_cpu_fan_display(dev):
    fCpuTemp = get_cpu_temp()

    # GAMEMAX SIGMA 520 CPU cooler requires the number 1 instead of 0 to be sent when writing to the display
    byte_comands = bytes([1, int(fCpuTemp)])
    
    print(f"Byte commands: {byte_comands}")
    try:        
        num_bytes_written = dev.write(byte_comands)
    except IOError as e:
        print ('Error writing command: {}'.format(e))
        return None 

    return num_bytes_written

def call_repeatedly(interval, func, *args):
    stopped = Event()
    def loop():
        while not stopped.wait(interval):
            func(*args)
    Thread(target=loop).start()    
    return stopped.set

print('Connected to {}\n'.format(PRODUCT_ID))

seconds = 1
cancel_future_calls = call_repeatedly(seconds, write_to_cpu_fan_display, device)
