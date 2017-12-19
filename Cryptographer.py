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
        self.send(str.encode('%s is here' % name))
        self.name = name
        self.psk = (0, 0)

    def handle_read(self):
        data = self.recv(8192)
        print(data)

    def setPSK(self, psk):
        self.psk = psk


# if __name__ == '__main__':
#     c = Cryptographer("127.0.0.1", 1338, "A")
#     asyncore.loop();


def main(argv):
    # parameter check for different tasks
    # -h, --help
    # -t, --task <task number>
    taskInput = ''
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
    return (42 * ord(name) + 73 * ord(name2)) % 1337


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

    asyncore.loop()
