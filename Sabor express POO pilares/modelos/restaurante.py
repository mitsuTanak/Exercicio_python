from modelos.avaliacao import Avaliacao
from modelos.estabelecimento import Estabelecimento

class Restaurante(Estabelecimento):
    """
    Classe que representa um restaurante, herdando da classe abstrata Estabelecimento.
    Possui métodos específicos para restaurantes.
    """

    def receber_avaliacao(self, cliente, nota):
        """
        Adiciona uma nova avaliação ao restaurante, desde que a nota esteja entre 0 e 10.
        """
        if 0 <= nota <= 10:
            avaliacao = Avaliacao(cliente, nota)
            self._avaliacoes.append(avaliacao)
        else:
            print("A nota deve estar entre 0 e 10.")