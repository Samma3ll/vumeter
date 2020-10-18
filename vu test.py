import serial
import time

ser = serial.Serial('COM10', 9600, timeout=10)


def checkport():
  try:
    ser = serial.Serial('COM10', 9600, timeout=10)
    while ser.read():
      print ('serial open')

      print ('serial closed')
      ser.close()

  except serial.serialutil.SerialException:
    print ('exception')

def setdail():
  while True:
    ser.write(b'950')
    print("950")
    time.sleep(1)
    ser.write(b'700')
    print("700")
    time.sleep(1)
    ser.write(b'400')
    print("400")
    time.sleep(1)




setdail()
