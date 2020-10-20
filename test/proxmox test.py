from proxmoxer import ProxmoxAPI
proxmox = ProxmoxAPI('192.168.0.7', user='root@pam', password='NickLQ!709**', verify_ssl=False)
import time, signal, serial
import psutil

SLEEP_SECONDS = 0.8

BIT_VREF = (1 << 7)

def ctrl_c_handler(signal, frame):
    print('Goodbye!')
    UpdateGauges(0, 0,)
    exit()


def invalidRange(dialRange):
    if (dialRange < 0) or (dialRange > 100):
        print("Invalid dial range ! [ 0 <= dialRange <= 100 ]!")
        return True
    else:
        return False

def percentToDAC(percent):
    valuemin = int((percent) * 1300 / 100)
    value = int(valuemin + 400)
    upper = (((value >> 8) & 0xFF) | BIT_VREF)
    lower = (value & 0xFF)
    return (value)

# Update all four gauges
def UpdateGauges(dial1, dial2):
    if invalidRange(dial1):
        return
    elif invalidRange(dial2):
        return

    print("CPU=%3d CPU=%3d" % (dial1, dial2))

    sendString = "[%d]\n" % (percentToDAC(dial1))
    print(sendString)
    print(sendString.encode())
    ser.write(sendString.encode())
    #print("\r\n")


def CycleDial(step=1, delay=0.5):
    # Increment
    for i in range(0,101,step):
        UpdateGauges(i, i,)
        time.sleep(delay)

    # Decrement
    for i in range(0,101,step):
        UpdateGauges(100-i, 100-i,)
        time.sleep(delay)

def cpu_usage():
    return int(psutil.cpu_percent())

def proxmox_cpu():
    node = proxmox.nodes('pve')
    data = node.status.get()
    cpu = data['cpu']
    cpu_p = int(cpu * 100)
    return(cpu_p)

def main():

    #global ser
    #ser = serial.Serial('COM10', 115200, timeout=10)

    #while True:
    #    CycleDial(5, 0.1)
    #exit()
    print(proxmox_cpu())
    #CycleDial(5, 0.1)
    #while True:
    #    UpdateGauges(cpu_usage(), cpu_usage())
    #    time.sleep(SLEEP_SECONDS)
    exit();


if __name__ == '__main__':
    signal.signal(signal.SIGINT, ctrl_c_handler)
    main()


node = proxmox.nodes('pve')
data = node.status.get()
print(data['cpu'])