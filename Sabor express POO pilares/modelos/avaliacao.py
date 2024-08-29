# modelos/avaliacao.py
class Avaliacao:
    """
    Classe que representa uma avaliação feita por um cliente.
    """
    def __init__(self, cliente, nota):
        self._cliente = cliente  # Nome do cliente que fez a avaliação
        self._nota = nota  # Nota dada pelo cliente

    def __dict__(self):
        """
        Método para converter o objeto Avaliacao em um dicionário para salvar em JSON.
        """
        return {
            'cliente': self._cliente,
            'nota': self._nota
        }