import asyncore

class Cryptographer(asyncore.dispatcher):

    def __init__(self, host, port, name):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect((host, port))
        print('Cryptographer %s running' % name)
        self.send(str.encode('%s is here' % name))

    def handle_read(self):
        data = self.recv(8192)
        print(data)

if __name__ == '__main__':
    c = Cryptographer("127.0.0.1", 1338, "A")
    asyncore.loop();
