import serial, time

arduino = serial.Serial('COM10', 9600, timeout=.1)
time.sleep(1)  # give the connection a second to settle
arduino.write(b"H")
while True:
    data = arduino.readline()

    if data:
        print(data)
