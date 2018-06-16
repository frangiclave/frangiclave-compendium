from io import BytesIO


class Reader(BytesIO):
    def read_string(self):
        string = bytearray()
        while True:
            b = self.read(1)
            if not b:
                break
            string += b
        return string.encode('utf-8')
