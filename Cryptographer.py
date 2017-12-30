import asyncore
import sys
import getopt


class Cryptographer(asyncore.dispatcher):
    def __init__(self, host, port, name):
        asyncore.dispatcher.__init__(self)
        self.preSharedKey = ''
        self.create_socket()
        self.connect((host, port))
        print('Cryptographer %s running ' % name)
        self.buffer = []
        self.name = name
        self.psk = (0, 0)
        self.participants = 3
        self.psk_keylen = 0
        self.messageLength = 0
        self.allowSending = False
        self.recv_buffer = []


    def x_or_with_psk(self, message):
        encoded = [] 
        for i in range(len(message)):
            currentByte = message[i]
            for p in range(0, len(self.psk)):
                currentByte = currentByte ^ self.psk[p][i % self.psk_keylen]

            encoded.append(currentByte)

        return bytes(encoded)


    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]

    def writable(self):
        return (len(self.buffer) > 0 and self.allowSending)

    def handle_close(self):
        pass

    def setLength(self, length):
        self.messageLength = length

    def sendEncrypted(self, message):
        encryped = self.x_or_with_psk(message)
        for byte in encryped:
            self.recv_buffer.append(byte)

        self.buffer = encryped

    def decrypt(self, b):
        # Split messages
        messages = [b[i:i + self.messageLength] for i in range(0, len(b), self.messageLength)]
        decrypted = []
        for i in range(0, self.messageLength):
            byte = messages[0][i]
            for j in range(1, self.participants):
                byte = byte ^ messages[j][i]
            decrypted.append(byte)

        print(bytes(decrypted).decode('utf8'))

    def handle_read(self):
        data = self.recv(8192)
        self.allowSending = True

        print('%s received: %s bytes' % (self.name, len(data)))
        for byte in data:
            self.recv_buffer.append(byte)

        if len(self.recv_buffer) == self.messageLength*self.participants:
            print('%s RECEIVED ALL MESSAGES / DECRYPTED:' % self.name)
            self.decrypt(self.recv_buffer)


        # print('PSK1: %i' % int.from_bytes(self.psk[0], byteorder='big'))
        # print('PSK2: %i' % int.from_bytes(self.psk[1], byteorder='big'))

        # testing xor
        # encoded1 = self.x_or_with_psk(data)
        # print('%s XOR: %s' % (self.name, encoded1))
        # print('%s XOR: %s' % (self.name, self.x_or_with_psk(encoded1)))


    def setPSK(self, psk):
        keylen = 2
        self.psk = (psk[0].to_bytes(keylen, byteorder="big"), psk[1].to_bytes(keylen, byteorder="big"))
        self.psk_keylen = keylen


# if __name__ == '__main__':
#     c = Cryptographer("127.0.0.1", 1338, "A")
#     asyncore.loop();


def main(argv):
    # parameter check for different tasks
    # -h, --help
    # -t, --task <task number>
    taskInput = '1'
    optionalPar = ''
    try:
        opts, args = getopt.getopt(argv, "ht:o:", ["task=", "oPar="])
    except getopt.GetoptError:
        print('test.py -t <task number> -o <optionalPar>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('test.py -t <task number> -o <optionalPar>')
            sys.exit()
        elif opt in ("-t", "--task"):
            taskInput = arg
        elif opt in ("-o", "--oPar"):
            optionalPar = arg
    print('task number is: ', taskInput)
    print('Output file is: ', optionalPar)


def calcPSK(name, name2):
    return (42 * ord(name) + 73 * ord(name2)) % 0xFFFF 


if __name__ == "__main__":
    main(sys.argv[1:])
    c0 = Cryptographer("127.0.0.1", 1338, "A")
    c1 = Cryptographer("127.0.0.1", 1338, "B")
    c2 = Cryptographer("127.0.0.1", 1338, "C")

    # create PSKs
    psk01 = calcPSK(c0.name, c1.name)
    psk02 = calcPSK(c0.name, c2.name)
    psk12 = calcPSK(c1.name, c2.name)
    c0.setPSK((psk01, psk02))
    c1.setPSK((psk01, psk12))
    c2.setPSK((psk02, psk12))


    print("[TASK1] For convenience all Cryptographers are created in the process.")
    text = input("[TASK1] Please enter message: ")

    c0.setLength(len(text))
    c1.setLength(len(text))
    c2.setLength(len(text))

    empty = bytes([0] * len(text))
    c0.allowSending = True
    c0.sendEncrypted(str.encode(text))
    c1.sendEncrypted(empty)
    c2.sendEncrypted(empty)


    asyncore.loop()
