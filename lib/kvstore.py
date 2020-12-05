
import msgpack

class kvstore():

    def __init__(self, name):

        self.name = name
        self.conf_file='data/' + name + 'msgpack'
        self.data={}

        # Load data at file creation
        self.read()

    def save(self):

        bin=msgpack.packb(self.data, use_bin_type=True)
        with open(self.conf_file, 'w') as file:
            file.write(bin)


    def read(self):
        with open(self.conf_file, 'r', encoding='utf-16') as file:
            bin = file.read()
        self.data = msgpack.unpackb(bin, raw=False)

