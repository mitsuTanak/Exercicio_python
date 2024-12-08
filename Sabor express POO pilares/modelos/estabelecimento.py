# modelos/estabelecimento.py
from modelos.avaliacao import Avaliacao
from abc import ABC, abstractmethod

class Estabelecimento(ABC):
    """
    Classe abstrata que representa um estabelecimento genérico.
    Possui os atributos e métodos comuns a qualquer tipo de estabelecimento.
    """
    estabelecimentos = []

    def __init__(self, nome, categoria):
        self._nome = nome.title()  # Nome do estabelecimento, formatado com a primeira letra maiúscula
        self._categoria = categoria.upper()  # Categoria do estabelecimento, formatada em letras maiúsculas
        self._ativo = False  # Estado inicial do estabelecimento, definido como inativo
        self._avaliacoes = []  # Lista que armazena as avaliações do estabelecimento
        Estabelecimento.estabelecimentos.append(self)  # Adiciona o estabelecimento à lista global de estabelecimentos

    def __str__(self):
        # Retorna uma representação textual do estabelecimento, mostrando nome e categoria
        return f'{self._nome} | {self._categoria}'

    @classmethod
    def listar_estabelecimentos(cls):
        """
        Exibe a lista de todos os estabelecimentos cadastrados.
        """
        print(" ")
        print(f"{'Nome do estabelecimento'.ljust(25)} | {'Categoria'.ljust(25)} | {'Avaliação'.ljust(25)} | {'Status'}")
        for estabelecimento in cls.estabelecimentos:
            print(f"{estabelecimento._nome.ljust(25)} | {estabelecimento._categoria.ljust(25)} | {str(estabelecimento.media_avaliacoes).ljust(25)} | {estabelecimento.ativo}")

    @property
    def ativo(self):
        """
        Retorna um símbolo visual representando se o estabelecimento está ativo ou inativo.
        """
        return '⌧' if self._ativo else '☐'

    def alternar_estado(self):
        """
        Alterna o estado do estabelecimento entre ativo e inativo.
        """
        self._ativo = not self._ativo

    @abstractmethod
    def receber_avaliacao(self, cliente, nota):
        """
        Método abstrato para receber uma nova avaliação do estabelecimento.
        As subclasses concretas devem implementar esse método.
        """
        pass

    @property
    def media_avaliacoes(self):
        """
        Calcula e retorna a média das avaliações do estabelecimento.
        """
        if not self._avaliacoes:
            return '-'
        soma_das_notas = sum(avaliacao._nota for avaliacao in self._avaliacoes)
        quantidade_de_notas = len(self._avaliacoes)
        media = round(soma_das_notas / quantidade_de_notas, 1)
        return media