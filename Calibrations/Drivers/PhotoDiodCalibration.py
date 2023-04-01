import serial


class SerialPortManager:
    def __init__(self, com_port, baud_rate, timeout):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.__initialization_handshake__()

    def __initialization_handshake__(self):
        self.serial_port = serial.Serial(self.com_port, self.baud_rate, timeout=self.timeout)
        read_line = self.serial_port.readline().decode().strip()
        assert read_line == "Device is ready ...", f"What is {read_line}"
        print(read_line)
        # self.serial_port.write('0'.encode())
        # read_line = self.serial_port.readline().decode().strip()
        # assert read_line == "Operational Mode"

    def restart(self):
        del self.serial_port
        self.__initialization_handshake__()

    def send_command(self, command):
        self.serial_port.write(command.encode())
        read_line = self.serial_port.readline()
        if int(command) % 10 == 0:
            voltage = int(read_line.decode().strip())/1024 * 5.12
            print(voltage)
        else:
            print(read_line)

    def read_delay(self):
        try:
            arduino_delay = int(self.serial_port.readline().decode().strip().split(' ')[-1]) // 1000
        except:
            arduino_delay = None

        return arduino_delay


serial_port = SerialPortManager("COM6", 115200, 2)

while 1:
    command = input('>>')

    if command == "exit":
        break
    else:
        serial_port.send_command(command)
