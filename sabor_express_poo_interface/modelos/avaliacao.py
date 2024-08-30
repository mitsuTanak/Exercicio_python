class Avaliacao:
    def __init__(self, nota):
        self._nota = nota

    def to_dict(self):
        return {'nota': self._nota}
