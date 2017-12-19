import asyncore
import sys
import getopt


class Cryptographer(asyncore.dispatcher):

    def __init__(self, host, port, name):
        asyncore.dispatcher.__init__(self)
        self.preSharedKey = ''
        self.create_socket()
        self.connect((host, port))
        print('Cryptographer %s running' % name)
        self.send(str.encode('%s is here' % name))

    def handle_read(self):
        data = self.recv(8192)
        print(data)

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
        print 'test.py -t <task number> -o <optionalPar>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h','--help'):
            print 'test.py -t <task number> -o <optionalPar>'
            sys.exit()
        elif opt in ("-t", "--task"):
            taskInput = arg
        elif opt in ("-o", "--oPar"):
            optionalPar = arg
    print 'task number is: ', taskInput
    print 'Output file is: ', optionalPar


if __name__ == "__main__":
    main(sys.argv[1:])
    # c = Cryptographer("127.0.0.1", 1338, "A")
