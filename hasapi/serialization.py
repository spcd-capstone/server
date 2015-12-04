
class InvalidType(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class InvalidData(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def serialize(data):
    if (isinstance(data, int)):
        return "i" + str(int(data)) + "e"
    elif (isinstance(data, str)):
        return str(len(data)) + ":" + data
    raise InvalidType("Could not serialize type: {}".format(type(data).__name__))


def deserialize(data):
    if (data[0] == 'i') and (data[-1] == 'e') and len(data) > 2:
        return int(data[1:-1])
    elif ":" in data:
        [cnts, *body] = data.split(":")
        body = "".join(body)
        if not cnts.isdigit():
            raise InvalidData("Invalid character count in data: '{}'".format(data))
        cnt = int(cnts)
        if not cnt == len(body):
            raise InvalidData("Wrong length of string in value: '{}'".format(data))
        return body

    raise InvalidData("Not valid data: '{}'".format(data))


