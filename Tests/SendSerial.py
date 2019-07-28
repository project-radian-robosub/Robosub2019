from serial import Serial

ser = Serial("/dev/ttyACM0", 9600)  # change the serial port to whatever the arduino is connected to


while True:
    string = (input("values?" ))
    ser.write(string.encode())
