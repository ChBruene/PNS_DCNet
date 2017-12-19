import asyncore, sys


class Cryptographer(asyncore.dispatcher):

    def __init__(self, host, port, name):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect((host, port))
        self.name = name
        self.key = (0, 0)
        self.message = 0
        print('Cryptographer %s running' % name)
        self.send(str.encode('%s is here' % name))

    def handle_read(self):
        data = self.recv(8192)
        print(data)

    def dcEncrypt(self):
        return self.key[0] ^ self.key[1] ^ self.message


if __name__ == '__main__':

    param = sys.argv[1]

    cA = Cryptographer("127.0.0.1", 1338, "A")
    cB = Cryptographer("127.0.0.1", 1338, "B")
    cC = Cryptographer("127.0.0.1", 1338, "C")

    asyncore.loop()  # ???
    if param == 't1':  # Task 1
        ### create pre-shared-key
        kAB = (ord(cA.name) + ord(cB.name) * 42) % 1000
        kAC = (ord(cA.name) + ord(cC.name) * 42) % 1000
        kBC = (ord(cB.name) + ord(cC.name) * 42) % 1000
        cA.key = (kAB, kAC)
        cB.key = (kAB, kBC)
        cC.key = (kAC, kBC)
        ### Read/Set the message

        ### Send messages

        ### Receive public known message
    elif param == 't2':
        sendInterval = 3  # seconds
        # code here
    elif param == 't3':
        print(42)
        # code
    elif param == 't4':
        print(42)
        # code
    elif param == 't5':
        print(42)
        # code
    else:
        print('Cryptographer main switch-case-dafault')
