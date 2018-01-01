import asyncore
import sys
import getopt
import time


class Cryptographer(asyncore.dispatcher):
    def __init__(self, host, port, name, participants=3):
        asyncore.dispatcher.__init__(self)
        self.preSharedKey = ''
        self.create_socket()
        self.connect((host, port))
        print('Cryptographer %s running ' % name)
        self.buffer = []
        self.name = name
        self.psk = []
        self.participants = participants
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

        print(bytes(decrypted))
        # print("As String: %s" % bytes(decrypted).decode())

    def handle_read(self):
        data = self.recv(8192)
        self.allowSending = True

        #print('%s received: %s bytes' % (self.name, len(data)))
        #print("%s / %s" % (len(self.recv_buffer), self.messageLength * self.participants))
        #print(data)
        for byte in data:
            self.recv_buffer.append(byte)

        if len(self.recv_buffer) == self.messageLength * self.participants:
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
        self.psk = [psk[0].to_bytes(keylen, byteorder="big"), psk[1].to_bytes(keylen, byteorder="big")]
        print(self.psk)
        self.psk_keylen = keylen


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
    return taskInput, optionalPar


def calcPSK(name, name2):
    return (42 * (ord(name[0]) + int(name[1:]) + ord(name2[0]) + int(name[1:]))) % 0xFFFF


if __name__ == "__main__":
    task, par = main(sys.argv[1:])

    if task == '1':
        c0 = Cryptographer("127.0.0.1", 1338, "A1")
        c1 = Cryptographer("127.0.0.1", 1338, "B2")
        c2 = Cryptographer("127.0.0.1", 1338, "C3")

        # create PSKs
        psk01 = calcPSK(c0.name, c1.name)
        psk02 = calcPSK(c0.name, c2.name)
        psk12 = calcPSK(c1.name, c2.name)
        c0.setPSK([psk01, psk02])
        c1.setPSK([psk01, psk12])
        c2.setPSK([psk02, psk12])

        print("[TASK1] For convenience all Cryptographers are created in the process.")
        text = input("[TASK1] Please enter message: ")

        l = len(str.encode(text))
        c0.setLength(l)
        c1.setLength(l)
        c2.setLength(l)

        empty = bytes([0] * l)
        c0.allowSending = True
        c0.sendEncrypted(str.encode(text))
        print(str.encode(text))
        c1.sendEncrypted(empty)
        c2.sendEncrypted(empty)

    elif task == '2':
        c0 = Cryptographer("127.0.0.1", 1338, "A1")
        c1 = Cryptographer("127.0.0.1", 1338, "B2")
        c2 = Cryptographer("127.0.0.1", 1338, "C3")

        # create PSKs
        psk01 = calcPSK(c0.name, c1.name)
        psk02 = calcPSK(c0.name, c2.name)
        psk12 = calcPSK(c1.name, c2.name)
        c0.setPSK([psk01, psk02])
        c1.setPSK([psk01, psk12])
        c2.setPSK([psk02, psk12])
        print("[TASK1] For convenience all Cryptographers are created in the process.")

        while True:
            # text = input("[TASK1] Please enter message: ")
            # l = len(str.encode(text))
            # c0.setLength(l)
            # c1.setLength(l)
            # c2.setLength(l)

            empty = bytes([0] * 6)

            c0.sendEncrypted(empty)
            c1.sendEncrypted(empty)
            c2.sendEncrypted(empty)
            print(empty)
            time.sleep(3)

    elif task == '3':
        print('Task3')

    elif task == '4':
        print('Task4')
        cList = []

        for i in range(int(par)):
            cList.append(Cryptographer("127.0.0.1", 1338, "C" + str(i), participants=int(par)))

        for c in cList:
            pskList = []
            for other in cList:
                if c.name != other.name:
                    pskList.append(calcPSK(c.name, other.name))
            c.setPSK(pskList)

        print("[TASK4] For convenience all Cryptographers are created in the process.")
        text = input("[TASK4] Please enter message: ")

        l = len(str.encode(text))
        for c in cList:
            c.setLength(l)

        empty = bytes([0] * l)
        cList[0].allowSending = True
        cList[0].sendEncrypted(str.encode(text))
        print(str.encode(text))
        for i in range(1, len(cList)):
            cList[i].sendEncrypted(empty)

    elif task == '5':
        print('Task5')
        cList = []
        for i in range(int(par)):
            cList.append(Cryptographer("127.0.0.1", 1338, "C" + str(i), participants=int(par)))

        for c in range(len(cList)):
            pskList = []
            prevName = ''
            nextName = ''

            prevName = cList[c-1].name
            if c == len(cList):
                nextName = cList[c+1].name
            else:
                nextName = cList[0].name

            pskList.append(calcPSK(cList[c].name, prevName))
            pskList.append(calcPSK(cList[c].name, nextName))
            cList[c].setPSK(pskList)

        print("[TASK5] For convenience all Cryptographers are created in the process.")
        text = 'test123'

        l = len(str.encode(text))
        for c in cList:
            c.setLength(l)

        empty = bytes([0] * l)
        cList[0].sendEncrypted(str.encode(text))
        print(str.encode(text))
        for i in range(1, len(cList)):
            time.sleep(1)
            cList[i].allowSending = True
            cList[i].sendEncrypted(empty)

    else:
        print('task-switch-case-default')
    asyncore.loop()
