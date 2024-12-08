import os
import json
import sys
from modelos.estabelecimento import Estabelecimento
from modelos.restaurante import Restaurante
from modelos.avaliacao import Avaliacao

# Função para obter o caminho do diretório de dados
def get_data_dir():
    if getattr(sys, 'frozen', False):
        # Se estiver executando como um executável
        return os.path.dirname(sys.executable)
    else:
        # Se estiver executando como script
        return os.path.dirname(os.path.abspath(__file__))

# Nome do arquivo onde os dados dos estabelecimentos são armazenados
ARQUIVO_DADOS = os.path.join(get_data_dir(), 'dados_estabelecimentos.json')

# Função para carregar dados dos estabelecimentos a partir de um arquivo JSON
def carregar_dados(): 
    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            Estabelecimento.estabelecimentos.clear()  # Limpa a lista de estabelecimentos antes de carregar os novos dados
            for estabelecimento_dados in dados:
                if estabelecimento_dados['tipo'] == 'Restaurante':
                    estabelecimento = Restaurante(
                        estabelecimento_dados['nome'],
                        estabelecimento_dados['categoria']
                    )
                    estabelecimento._ativo = estabelecimento_dados['ativo']
                    estabelecimento._avaliacoes = [Avaliacao(**avaliacao) for avaliacao in estabelecimento_dados['avaliacoes']]
                else:
                    print(f"Tipo de estabelecimento não reconhecido: {estabelecimento_dados['tipo']}")
                    continue
    except FileNotFoundError:
        print(f"Arquivo de dados não encontrado. Criando um novo arquivo em {ARQUIVO_DADOS}")
        salvar_dados()  # Cria um arquivo vazio se não existir

# Função para salvar dados dos estabelecimentos em um arquivo JSON
def salvar_dados():
    dados = []
    for estabelecimento in Estabelecimento.estabelecimentos:
        dados.append({
            'tipo': estabelecimento.__class__.__name__,
            'nome': estabelecimento._nome,
            'categoria': estabelecimento._categoria,
            'ativo': estabelecimento._ativo,
            'avaliacoes': [avaliacao.__dict__() for avaliacao in estabelecimento._avaliacoes]
        })
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)  # Salva os dados no arquivo com indentação para melhor leitura

# Função principal do programa, que exibe o menu e executa as ações selecionadas pelo usuário
def main():
    carregar_dados()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpa a tela antes de exibir o menu
        print("=-=-=-=-= Estabelecimento Expresso (POO-Pilares)=-=-=-=-=")
        print("\n1. Cadastrar estabelecimento")
        print("2. Listar estabelecimentos")
        print("3. Habilitar/Desabilitar estabelecimento")
        print("4. Avaliar estabelecimento")
        print("5. Alterar estabelecimento")
        print("6. Excluir estabelecimento")
        print("7. Sair")
        
        opcao = input("\nEscolha uma opção: ")
        
        # Chama a função correspondente à opção escolhida
        if opcao == '1':
            cadastrar_estabelecimento()
        elif opcao == '2':
            listar_estabelecimentos()
        elif opcao == '3':
            habilitar_estabelecimento()
        elif opcao == '4':
            avaliar_estabelecimento()
        elif opcao == '5':
            alterar_estabelecimento()
        elif opcao == '6':
            excluir_estabelecimento()
        elif opcao == '7':
            salvar_dados()  # Salva os dados antes de sair
            print("\nDados salvos. Obrigado por usar o sistema. Até logo!")
            print("     =-=-= DEV's 2DE SENAI/SESI-2024 :) =-=-=\n")
            break
        else:
            print("Opção inválida. Tente novamente.")
        
        input("\nPressione Enter para continuar...")

# Função para cadastrar um novo estabelecimento
def cadastrar_estabelecimento():
    tipo = input("Digite o tipo de estabelecimento (Restaurante): ")
    nome = input("Digite o nome do estabelecimento: ")
    categoria = input("Digite a categoria do estabelecimento: ")
    
    if tipo.lower() == 'restaurante':
        novo_estabelecimento = Restaurante(nome, categoria)  # Cria um novo objeto Restaurante
    else:
        print("Tipo de estabelecimento não suportado.")
        return
    
    print(f"\n{tipo.capitalize()} '{nome}' cadastrado com sucesso!")
    salvar_dados()  # Salva os dados após o cadastro

# Função para listar todos os estabelecimentos cadastrados
def listar_estabelecimentos():
    print("Lista de Estabelecimentos:")
    Estabelecimento.listar_estabelecimentos()

# Função para habilitar ou desabilitar um estabelecimento
def habilitar_estabelecimento():
    nome = input("Digite o nome do estabelecimento que deseja habilitar/desabilitar: ")
    for estabelecimento in Estabelecimento.estabelecimentos:
        if estabelecimento._nome.lower() == nome.lower():
            estabelecimento.alternar_estado()  # Altera o estado do estabelecimento (ativo/inativo)
            print(f"Estado do estabelecimento {estabelecimento._nome} alterado para {estabelecimento.ativo}")
            salvar_dados()  # Salva os dados após a alteração
            return
    print("Estabelecimento não encontrado.")

# Função para adicionar uma avaliação a um estabelecimento
def avaliar_estabelecimento():
    nome = input("Digite o nome do estabelecimento que deseja avaliar: ")
    for estabelecimento in Estabelecimento.estabelecimentos:
        if estabelecimento._nome.lower() == nome.lower():
            cliente = input("Digite seu nome: ")
            while True:
                try:
                    nota = float(input("Digite a nota (de 0 a 10): "))
                    if 0 <= nota <= 10:
                        estabelecimento.receber_avaliacao(cliente, nota)  # Adiciona a avaliação ao estabelecimento
                        print("Avaliação registrada com sucesso!")
                        salvar_dados()  # Salva os dados após a avaliação
                        return
                    else:
                        print("A nota deve estar entre 0 e 10.")
                except ValueError:
                    print("Por favor, digite um número válido.")
    print("Estabelecimento não encontrado.")

# Função para alterar as informações de um estabelecimento
def alterar_estabelecimento():
    nome = input("Digite o nome do estabelecimento que deseja alterar: ")
    for estabelecimento in Estabelecimento.estabelecimentos:
        if estabelecimento._nome.lower() == nome.lower():
            novo_nome = input(f"Digite o novo nome do estabelecimento (atual: {estabelecimento._nome}): ")
            nova_categoria = input(f"Digite a nova categoria do estabelecimento (atual: {estabelecimento._categoria}): ")
            
            # Atualiza o nome e a categoria do estabelecimento se forem fornecidos novos valores
            if novo_nome:
                estabelecimento._nome = novo_nome.title()
            if nova_categoria:
                estabelecimento._categoria = nova_categoria.upper()
            
            print(f"Estabelecimento alterado com sucesso para: {estabelecimento}")
            salvar_dados()  # Salva os dados após a alteração
            return
    print("Estabelecimento não encontrado.")

# Função para excluir um estabelecimento da lista
def excluir_estabelecimento():
    nome = input("Digite o nome do estabelecimento que deseja excluir: ")
    for estabelecimento in Estabelecimento.estabelecimentos:
        if estabelecimento._nome.lower() == nome.lower():
            confirmacao = input(f"Tem certeza que deseja excluir o estabelecimento '{estabelecimento._nome}'? (S/N): ")
            if confirmacao.lower() == 's':
                Estabelecimento.estabelecimentos.remove(estabelecimento)  # Remove o estabelecimento da lista
                print(f"Estabelecimento '{estabelecimento._nome}' excluído com sucesso.")
                salvar_dados()  # Salva os dados após a exclusão
            else:
                print("Operação de exclusão cancelada.")
            return
    print("Estabelecimento não encontrado.")

# Verifica se o script está sendo executado diretamente e chama a função principal
if __name__ == '__main__':
    main()