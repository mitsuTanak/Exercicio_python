from modelos.avaliacao import Avaliacao

class Restaurante:
    restaurantes = []

    def __init__(self, nome, categoria):
        self._nome = nome
        self._categoria = categoria
        self._ativo = True
        self._avaliacao = []
        Restaurante.restaurantes.append(self)

    @property
    def nome(self):
        return self._nome

    @property
    def categoria(self):
        return self._categoria

    @property
    def ativo(self):
        return "Ativo" if self._ativo else "Inativo"

    @property
    def media_avaliacoes(self):
        if not self._avaliacao:
            return "-"
        soma_das_notas = sum(avaliacao._nota for avaliacao in self._avaliacao)
        quantidade_de_notas = len(self._avaliacao)
        media = round(soma_das_notas / quantidade_de_notas, 1)
        return media

    def avaliar_restaurante(self, nota):
        avaliacao = Avaliacao(nota)
        self._avaliacao.append(avaliacao)

    def alternar_estado(self):
        self._ativo = not self._ativo
