import os
import json
import sys
from tkinter import *
from tkinter import messagebox, ttk
from modelos.restaurante import Restaurante
from modelos.avaliacao import Avaliacao
from modelos.prato import Prato

# Função para obter o caminho do diretório de dados
def get_data_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Nome do arquivo onde os dados dos restaurantes são armazenados
ARQUIVO_DADOS = os.path.join(get_data_dir(), 'dados_restaurantes.json')

# Função para carregar dados dos restaurantes a partir de um arquivo JSON
def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)
            Restaurante.restaurantes.clear()  # Limpa a lista de restaurantes antes de carregar os novos dados
            for restaurante_dados in dados:
                restaurante = Restaurante(
                    restaurante_dados['nome'],
                    restaurante_dados['categoria'],
                    restaurante_dados['telefone'],
                    restaurante_dados['endereco']
                )
                restaurante._ativo = restaurante_dados['ativo']
                restaurante._avaliacao = [Avaliacao(**avaliacao) for avaliacao in restaurante_dados['avaliacao']]
    except FileNotFoundError:
        print(f"Arquivo de dados não encontrado. Criando um novo arquivo em {ARQUIVO_DADOS}")
        salvar_dados()

# Função para salvar dados dos restaurantes em um arquivo JSON
def salvar_dados():
    dados = []
    for restaurante in Restaurante.restaurantes:
        dados.append({
            'nome': restaurante._nome,
            'categoria': restaurante._categoria,
            'telefone':restaurante._telefone,
            'endereco':restaurante._endereco,
            'ativo': restaurante._ativo,
            'avaliacao': [avaliacao.to_dict() for avaliacao in restaurante._avaliacao]
        })
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)

class Application(Tk):
    def __init__(self):
        super().__init__()
        self.title("Restaurante Expresso")
        self.geometry("500x350")  # Tamanho inicial da janela principal
        self.configure(bg="#f0f0f0")
        self.create_widgets()
        carregar_dados()

    def create_widgets(self):
        # Criação de botões
        button_cadastrar = Button(self, text="Cadastrar Restaurante", command=self.cadastrar_restaurante)
        button_listar = Button(self, text="Listar Restaurantes", command=self.listar_restaurantes)
        button_habilitar = Button(self, text="Habilitar/Desabilitar Restaurante", command=self.habilitar_restaurante)
        button_avaliar = Button(self, text="Avaliar Restaurante", command=self.avaliar_restaurante)
        button_alterar = Button(self, text="Alterar Restaurante", command=self.alterar_restaurante)
        button_excluir = Button(self, text="Excluir Restaurante", command=self.excluir_restaurante)
        button_sair = Button(self, text="Sair", command=self.quit, bg="#ea1d2c", fg="#fff")

        # Posicionamento dos botões na tela
        button_cadastrar.pack(pady=5)
        button_listar.pack(pady=5)
        button_habilitar.pack(pady=5)
        button_avaliar.pack(pady=5)
        button_alterar.pack(pady=5)
        button_excluir.pack(pady=5)
        button_sair.pack(pady=5)

    def cadastrar_restaurante(self):
        window = Toplevel(self)
        window.title("Cadastrar Restaurante")
        window.geometry("600x350")

        label_nome = Label(window, text="Nome do Restaurante:")
        label_nome.pack(pady=5)
        entry_nome = Entry(window)
        entry_nome.pack(pady=5)

        label_categoria = Label(window, text="Categoria do Restaurante:")
        label_categoria.pack(pady=5)
        entry_categoria = Entry(window)
        entry_categoria.pack(pady=5)

        label_telefone = Label(window, text="Telefone do Restaurante:")
        label_telefone.pack(pady=5)
        entry_telefone = Entry(window)
        entry_telefone.pack(pady=5)

        label_endereco = Label(window, text="Endereço do Restaurante:")
        label_endereco.pack(pady=5)
        entry_endereco = Entry(window)
        entry_endereco.pack(pady=5)

        def salvar():
            nome = entry_nome.get()
            categoria = entry_categoria.get()
            telefone = entry_telefone.get()
            endereco = entry_endereco.get()
            if nome and categoria and telefone and endereco :
                Restaurante(nome, categoria, telefone, endereco)
                salvar_dados()
                messagebox.showinfo("Sucesso", "Restaurante cadastrado com sucesso!")
                window.destroy()
            else:
                messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos.")

        button_salvar = Button(window, text="Salvar", command=salvar)
        button_salvar.pack(pady=10)

    def listar_restaurantes(self):
        window = Toplevel(self)
        window.title("Listar Restaurantes")
        window.geometry("1400x450")

        # Configuração da Treeview para exibição dos restaurantes
        tree = ttk.Treeview(window, columns=("nome", "categoria","telefone", "endereco", "media_avaliacoes", "status", "cardapio"), show='headings')
        tree.heading("nome", text="Nome")
        tree.heading("categoria", text="Categoria")
        tree.heading("telefone", text="Telefone")
        tree.heading("endereco", text="Endereço")
        tree.heading("media_avaliacoes", text="Média Avaliações")
        tree.heading("status", text="Status")

        # Centraliza o texto nas colunas
        tree.column("nome", anchor=CENTER)
        tree.column("categoria", anchor=CENTER)
        tree.column("telefone", anchor=CENTER)
        tree.column("endereco", anchor=CENTER)
        tree.column("media_avaliacoes", anchor=CENTER)
        tree.column("status", anchor=CENTER)

        # Inserção dos dados na Treeview
        for restaurante in Restaurante.restaurantes:
            tree.insert("", "end", values=(restaurante._nome, restaurante._categoria, restaurante._telefone, restaurante._endereco, restaurante.media_avaliacoes, restaurante.ativo))

        tree.pack(fill=BOTH, expand=True)

        # Botão para abrir o cardápio do restaurante selecionado
        def abrir_cardapio():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um restaurante para ver o cardápio.")
                return
            
            restaurante_index = tree.index(selected_item[0])
            restaurante = Restaurante.restaurantes[restaurante_index]
            self.mostrar_cardapio(restaurante)

        button_cardapio = Button(window, text="Ver Cardápio", command=abrir_cardapio)
        button_cardapio.pack(pady=10)

    def mostrar_cardapio(self, restaurante):
        window = Toplevel(self)
        window.title(f"Cardápio - {restaurante.nome}")
        window.geometry("600x400")

        # Botão para cadastrar novo prato
        button_cadastrar_prato = Button(window, text="Cadastrar Novo Prato", command=lambda: self.cadastrar_prato(restaurante, window))
        button_cadastrar_prato.pack(pady=10)

        # Treeview para listar os pratos
        tree = ttk.Treeview(window, columns=("nome", "descricao", "preco"), show='headings')
        tree.heading("nome", text="Nome")
        tree.heading("descricao", text="Descrição")
        tree.heading("preco", text="Preço (R$)")

        # Centraliza o texto nas colunas
        tree.column("nome", anchor=CENTER)
        tree.column("descricao", anchor=CENTER)
        tree.column("preco", anchor=CENTER)

        # Inserção dos dados na Treeview
        for prato in restaurante.cardapio:
            tree.insert("", "end", values=(prato.nome, prato.descricao, f"R$ {prato.preco:.2f}"))

        tree.pack(fill=BOTH, expand=True)

    def cadastrar_prato(self, restaurante, cardapio_window):
        window = Toplevel(self)
        window.title("Cadastrar Novo Prato")
        window.geometry("400x250")

        label_nome = Label(window, text="Nome do Prato:")
        label_nome.pack(pady=5)
        entry_nome = Entry(window)
        entry_nome.pack(pady=5)

        label_descricao = Label(window, text="Descrição do Prato:")
        label_descricao.pack(pady=5)
        entry_descricao = Entry(window)
        entry_descricao.pack(pady=5)

        label_preco = Label(window, text="Preço do Prato (R$):")
        label_preco.pack(pady=5)
        entry_preco = Entry(window)
        entry_preco.pack(pady=5)

        def salvar_prato():
            nome = entry_nome.get()
            descricao = entry_descricao.get()
            preco = entry_preco.get()

            if nome and descricao and preco:
                try:
                    preco = float(preco)
                    restaurante.adicionar_prato(nome, descricao, preco)
                    salvar_dados()
                    messagebox.showinfo("Sucesso", "Prato cadastrado com sucesso!")
                    window.destroy()
                    cardapio_window.destroy()  # Fecha a janela do cardápio
                    self.mostrar_cardapio(restaurante)  # Reabre a janela do cardápio atualizada
                except ValueError:
                    messagebox.showwarning("Aviso", "O preço deve ser um número válido.")
            else:
                messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos.")

        button_salvar = Button(window, text="Salvar Prato", command=salvar_prato)
        button_salvar.pack(pady=10)



    def habilitar_restaurante(self):
        window = Toplevel(self)
        window.title("Habilitar/Desabilitar Restaurante")
        window.geometry("600x400")

        label_selecao = Label(window, text="Selecione o restaurante para habilitar/desabilitar:")
        label_selecao.pack(pady=5)

        tree = ttk.Treeview(window, columns=("nome", "categoria", "status"), show='headings')
        tree.heading("nome", text="Nome")
        tree.heading("categoria", text="Categoria")
        tree.heading("status", text="Status")

        # Centraliza o texto nas colunas
        tree.column("nome", anchor=CENTER)
        tree.column("categoria", anchor=CENTER)
        tree.column("status", anchor=CENTER)

        for idx, restaurante in enumerate(Restaurante.restaurantes):
            tree.insert("", "end", iid=idx, values=(restaurante._nome, restaurante._categoria, restaurante.ativo))

        tree.pack(fill=BOTH, expand=True)

        def alternar_estado():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um restaurante para habilitar/desabilitar.")
                return
            
            for item in selected_item:
                restaurante_index = int(item)
                Restaurante.restaurantes[restaurante_index].alternar_estado()
            
            salvar_dados()
            messagebox.showinfo("Sucesso", "Estado do restaurante atualizado com sucesso!")
            window.destroy()

        button_alternar = Button(window, text="Habilitar/Desabilitar", command=alternar_estado)
        button_alternar.pack(pady=10)

    def avaliar_restaurante(self):
        window = Toplevel(self)
        window.title("Avaliar Restaurante")
        window.geometry("600x450")

        label_selecao = Label(window, text="Selecione o restaurante para avaliar:")
        label_selecao.pack(pady=5)

        tree = ttk.Treeview(window, columns=("nome", "categoria", "status"), show='headings')
        tree.heading("nome", text="Nome")
        tree.heading("categoria", text="Categoria")
        tree.heading("status", text="Status")

        # Centraliza o texto nas colunas
        tree.column("nome", anchor=CENTER)
        tree.column("categoria", anchor=CENTER)
        tree.column("status", anchor=CENTER)

        for idx, restaurante in enumerate(Restaurante.restaurantes):
            tree.insert("", "end", iid=idx, values=(restaurante._nome, restaurante._categoria, restaurante.ativo))

        tree.pack(fill=BOTH, expand=True)

        label_avaliacao = Label(window, text="Digite sua avaliação (0-10):")
        label_avaliacao.pack(pady=5)
        entry_avaliacao = Entry(window)
        entry_avaliacao.pack(pady=5)

        def salvar_avaliacao():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um restaurante para avaliar.")
                return
            
            nota = entry_avaliacao.get()
            if not nota.isdigit() or not (0 <= int(nota) <= 10):
                messagebox.showwarning("Aviso", "Digite uma nota válida entre 0 e 10.")
                return

            for item in selected_item:
                restaurante_index = int(item)
                Restaurante.restaurantes[restaurante_index].avaliar_restaurante(int(nota))
            
            salvar_dados()
            messagebox.showinfo("Sucesso", "Avaliação registrada com sucesso!")
            window.destroy()

        button_salvar_avaliacao = Button(window, text="Salvar Avaliação", command=salvar_avaliacao)
        button_salvar_avaliacao.pack(pady=10)

    def alterar_restaurante(self):
        window = Toplevel(self)
        window.title("Alterar Restaurante")
        window.geometry("1100x550")

        label_selecao = Label(window, text="Selecione o restaurante para alterar:")
        label_selecao.pack(pady=5)

        tree = ttk.Treeview(window, columns=("nome", "categoria", "telefone", "endereco", "status"), show='headings')
        tree.heading("nome", text="Nome")
        tree.heading("categoria", text="Categoria")
        tree.heading("telefone", text="Telefone")
        tree.heading("endereco", text="Endereço")
        tree.heading("status", text="Status")

        # Centraliza o texto nas colunas
        tree.column("nome", anchor=CENTER)
        tree.column("categoria", anchor=CENTER)
        tree.column("telefone", anchor=CENTER)
        tree.column("endereco", anchor=CENTER)
        tree.column("status", anchor=CENTER)

        for idx, restaurante in enumerate(Restaurante.restaurantes):
            tree.insert("", "end", iid=idx, values=(restaurante._nome, restaurante._categoria, restaurante._telefone, restaurante._endereco, restaurante.ativo))

        tree.pack(fill=BOTH, expand=True)

        label_nome = Label(window, text="Novo Nome do Restaurante:")
        label_nome.pack(pady=5)
        entry_nome = Entry(window)
        entry_nome.pack(pady=5)

        label_categoria = Label(window, text="Nova Categoria do Restaurante:")
        label_categoria.pack(pady=5)
        entry_categoria = Entry(window)
        entry_categoria.pack(pady=5)

        label_telefone = Label(window, text="Novo Telefone do Restaurante:")
        label_telefone.pack(pady=5)
        entry_telefone = Entry(window)
        entry_telefone.pack(pady=5)

        label_endereco = Label(window, text="Novo Endereço do Restaurante:")
        label_endereco.pack(pady=5)
        entry_endereco = Entry(window)
        entry_endereco.pack(pady=5)

        def salvar_alteracoes():
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um restaurante para alterar.")
                return
            
            novo_nome = entry_nome.get()
            nova_categoria = entry_categoria.get()
            novo_telefone = entry_telefone.get()
            novo_endereco = entry_endereco.get()

            for item in selected_item:
                restaurante_index = int(item)
                restaurante = Restaurante.restaurantes[restaurante_index]
                if novo_nome:
                    restaurante._nome = novo_nome
                if nova_categoria:
                    restaurante._categoria = nova_categoria
                if novo_telefone:
                    restaurante._telefone = novo_telefone
                if novo_endereco:
                    restaurante._endereco = novo_endereco
            
            salvar_dados()
            messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")
            window.destroy()

        button_salvar_alteracoes = Button(window, text="Salvar Alterações", command=salvar_alteracoes)
        button_salvar_alteracoes.pack(pady=10)

    def excluir_restaurante(self):
        window = Toplevel(self)
        window.title("Excluir Restaurante")
        window.geometry("600x450")

        label_selecao = Label(window, text="Selecione o restaurante para excluir:")
        label_selecao.pack(pady=5)

        tree = ttk.Treeview(window, columns=("nome", "categoria", "status"), show='headings')
        tree.heading("nome", text="Nome")
        tree.heading("categoria", text="Categoria")
        tree.heading("status", text="Status")

        # Centraliza o texto nas colunas
        tree.column("nome", anchor=CENTER)
        tree.column("categoria", anchor=CENTER)
        tree.column("status", anchor=CENTER)

        for idx, restaurante in enumerate(Restaurante.restaurantes):
            tree.insert("", "end", iid=idx, values=(restaurante._nome, restaurante._categoria, restaurante.ativo))

        tree.pack(fill=BOTH, expand=True)

        def confirmar_exclusao():
            # Obtém os itens selecionados na Treeview
            selected_item = tree.selection()
            if not selected_item:
                messagebox.showwarning("Aviso", "Selecione um restaurante para excluir.")
                return

            # Pergunta ao usuário se ele realmente deseja excluir os itens selecionados
            confirmacao = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir o restaurante selecionado?")
            
            if confirmacao:
                # Se o usuário confirmar a exclusão, remove o restaurante da lista
                for item in selected_item:
                    restaurante_index = int(item)
                    del Restaurante.restaurantes[restaurante_index]

                # Salva os dados atualizados
                salvar_dados()
                messagebox.showinfo("Sucesso", "Restaurante excluído com sucesso!")
                window.destroy()

        button_excluir = Button(window, text="Excluir", command=confirmar_exclusao)
        button_excluir.pack(pady=10)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
