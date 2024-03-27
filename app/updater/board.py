class Board:
    def __init__(self, id, type, version, role):
        self.id = id
        self.type = type
        self.version = version
        self.role = role

    @classmethod
    def from_dict(cls, data):
        return cls(id=data['id'], type=data['type'], version=data['version'], role=data['role'])

def board_decoder(data):
    return Board.from_dict(data)


