import time, signal
import psutil
import GPUtil
from sender import Sender

s = Sender()

SLEEP_SECONDS = 0.8

BIT_VREF = (1 << 7)

# Network usage calc
NET_MBps = 400  # MegaBITS per second, use something like https://speedtest.net to find out
NET_MAX_BPS = NET_MBps * 125000  # bytes per second
g_networkBytes = 0

def ctrl_c_handler(signal, frame):
    print('Goodbye!')
    UpdateGauges(0, 0, 0, 0)
    exit()


def invalidRange(dialRange):
    if (dialRange < 0) or (dialRange > 100):
        print("Invalid dial range ! [ 0 <= dialRange <= 100 ]!")
        return True
    else:
        return False

def percentToDAC(percent):
    valuemin = int((percent) * 3600 / 100)
    value = int(valuemin + 400)
    upper = (((value >> 8) & 0xFF) | BIT_VREF)
    lower = (value & 0xFF)
    return (value)

# Update all four gauges
def UpdateGauges(dial1, dial2, dial3, dial4):
    if invalidRange(dial1):
        return
    elif invalidRange(dial2):
        return
    elif invalidRange(dial3):
        return
    elif invalidRange(dial4):
        return

    print("CPU=%3d MEM=%3d GPU_util=%3d network_usage=%3d" % (dial1, dial2, dial3, dial4))



    sendString = "%d,%d,%d,%d" % (percentToDAC(dial1), percentToDAC(dial2), percentToDAC(dial3), percentToDAC(dial4))
    show = "write_dials(" + sendString + ")"
    #print(sendString)
    print(show)
    s.send(show)



def CycleDial(step=1, delay=0.5):
    # Increment
    for i in range(0,101,step):
        UpdateGauges(i, i, i, i)
        time.sleep(delay)

    # Decrement
    for i in range(0,101,step):
        UpdateGauges(100-i, 100-i, 100-i, 100-i)
        time.sleep(delay)

def cpu_usage():
    return int(psutil.cpu_percent())

def memory_usage():
    return int(psutil.virtual_memory().percent)

def gpu_usage():
    GPUs = GPUtil.getGPUs()
    return int(GPUs[0].load*100)

def gpu_mem():
    GPUs = GPUtil.getGPUs()
    return int(GPUs[0].memoryUtil*100)

def network_usage():
    global g_networkBytes
    net_total = (psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv)

    # Edge case, on first start capture net status
    # so we can use it in the next iteration of the loop
    if g_networkBytes == 0:
        g_networkBytes = net_total
        percent = 0
    else:
        bytesPerSec = (net_total - g_networkBytes) / SLEEP_SECONDS
        percent = bytesPerSec / NET_MAX_BPS * 100
        if percent > 100:
            percent = 100

    g_networkBytes = net_total
    return int(percent)

def main():
    CycleDial(10, 0.2)
    while True:
        UpdateGauges(cpu_usage(), memory_usage(), gpu_usage(), network_usage())
        #UpdateGauges(100, 25, 50, 99)
        time.sleep(SLEEP_SECONDS)
    exit()


if __name__ == '__main__':
    signal.signal(signal.SIGINT, ctrl_c_handler)
    main()
