class Directory:
    def __init__(self):
        self.addresses = []
        self.handles = []

    def add_client(self, address, handle):
        self.addresses.append(address)
        self.handles.append(handle)

    def remove_client(self, address=None, handle=None):
        try:
            if address or handle:
                i = self.addresses.index(address) if address else self.handles.index(handle)

                self.addresses.pop(i)
                self.handles.pop(i)
        except:
            pass

    def get_handle(self, address):
        try:
            i = self.addresses.index(address)
            return self.handles[i]
        except:
            return None

    def get_address(self, handle):
        try:
            i = self.handles.index(handle)
            return self.addresses[i]
        except:
            return None

