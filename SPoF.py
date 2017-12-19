import asyncore

cryptographers = []

class SPoFHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            print('Message %s' % data)
            for c in cryptographers:
                if c != self:
                    c.send(data)

    def handle_close(self):
        if self in cryptographers:
            cryptographers.remove(self)

class SPoFServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)
        print('SPoF running')

    def handle_accepted(self, sock, addr):
        print('Cryptographer connected from %s' % repr(addr))
        c = SPoFHandler(sock)
        cryptographers.append(c)



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

    # server = SPoFServer('localhost', 1338)
    # asyncore.loop()












    