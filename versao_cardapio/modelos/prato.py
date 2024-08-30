# Arquivo: prato.py
# Descrição: Este arquivo define a classe Prato, que representa um item no cardápio de um restaurante.

class Prato:
    """
    Classe que representa um prato no cardápio de um restaurante.
    
    Atributos:
        _nome (str): O nome do prato.
        _descricao (str): Uma breve descrição do prato.
        _preco (float): O preço do prato em reais.
    """

    def __init__(self, nome, descricao, preco):
        """
        Inicializa uma nova instância da classe Prato.

        Args:
            nome (str): O nome do prato.
            descricao (str): Uma breve descrição do prato.
            preco (float): O preço do prato em reais.
        """
        self._nome = nome
        self._descricao = descricao
        self._preco = preco

    @property
    def nome(self):
        """
        Getter para o nome do prato.

        Returns:
            str: O nome do prato.
        """
        return self._nome

    @property
    def descricao(self):
        """
        Getter para a descrição do prato.

        Returns:
            str: A descrição do prato.
        """
        return self._descricao

    @property
    def preco(self):
        """
        Getter para o preço do prato.

        Returns:
            float: O preço do prato.
        """
        return self._preco

    def to_dict(self):
        """
        Converte o objeto Prato em um dicionário.
        
        Este método é útil para serialização, por exemplo, ao salvar os dados em um arquivo JSON.

        Returns:
            dict: Um dicionário contendo os atributos do prato.
        """
        return {
            'nome': self._nome,
            'descricao': self._descricao,
            'preco': self._preco
        }