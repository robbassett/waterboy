import serial
import glob

# THIS MAY NEED TO BE CHANGED DEPENDING ON THE 
# NAME OF THE SERIAL PORT OF THE PICO
ttyport = glob.glob('/dev/tty.u*')[0]

class Talker:
    TERMINATOR = '\r'.encode('UTF8')

    def __init__(self, timeout=1):
        self.serial = serial.Serial(ttyport, 115200, timeout=timeout)

    def send(self, text: str):
        line = '%s\r\f' % text
        self.serial.write(line.encode('utf-8'))
        reply = self.receive()
        reply = reply.replace('>>> ','') # lines after first will be prefixed by a propmt
        if reply != text: # the line should be echoed, so the result should match
            raise ValueError('expected %s got %s' % (text, reply))

    def receive(self) -> str:
        line = self.serial.read_until(self.TERMINATOR)
        return line.decode('UTF8').strip()

    def close(self):
        self.serial.close()