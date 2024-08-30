from tkinter import *
from tkinter import messagebox
from modelos.restaurante import Restaurante

class Application(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Restaurante Expresso")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Cria os widgets para a interface gráfica
        self.label_title = Label(self, text="Restaurante Expresso", font=("Arial", 16))
        self.label_title.pack(pady=10)

        self.button_cadastrar = Button(self, text="Cadastrar Restaurante", command=self.cadastrar_restaurante)
        self.button_cadastrar.pack(fill="x")

        self.button_listar = Button(self, text="Listar Restaurantes", command=self.listar_restaurantes)
        self.button_listar.pack(fill="x")

        self.button_habilitar = Button(self, text="Habilitar Restaurante", command=self.habilitar_restaurante)
        self.button_habilitar.pack(fill="x")

        self.button_avaliar = Button(self, text="Avaliar Restaurante", command=self.avaliar_restaurante)
        self.button_avaliar.pack(fill="x")

        self.button_alterar = Button(self, text="Alterar Restaurante", command=self.alterar_restaurante)
        self.button_alterar.pack(fill="x")

        self.button_excluir = Button(self, text="Excluir Restaurante", command=self.excluir_restaurante)
        self.button_excluir.pack(fill="x")

        self.button_sair = Button(self, text="Sair", command=self.master.quit)
        self.button_sair.pack(fill="x", pady=5)

    def cadastrar_restaurante(self):
        # Lógica para cadastrar um novo restaurante
        def salvar_novo_restaurante():
            nome = entry_nome.get()
            categoria = entry_categoria.get()
            if nome and categoria:
                novo_restaurante = Restaurante(nome, categoria)
                messagebox.showinfo("Sucesso", f"Restaurante '{nome}' cadastrado com sucesso!")
                win.destroy()
            else:
                messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")

        win = Toplevel(self.master)
        win.title("Cadastrar Restaurante")
        Label(win, text="Nome do Restaurante:").pack(pady=5)
        entry_nome = Entry(win)
        entry_nome.pack(pady=5)
        Label(win, text="Categoria do Restaurante:").pack(pady=5)
        entry_categoria = Entry(win)
        entry_categoria.pack(pady=5)
        Button(win, text="Salvar", command=salvar_novo_restaurante).pack(pady=10)

    def listar_restaurantes(self):
        # Lógica para listar todos os restaurantes
        win = Toplevel(self.master)
        win.title("Listar Restaurantes")
        restaurantes = Restaurante.restaurantes
        text = Text(win)
        text.pack()

        if not restaurantes:
            text.insert(END, "Nenhum restaurante cadastrado.")
        else:
            text.insert(END, f"{'Nome'.ljust(25)} | {'Categoria'.ljust(25)} | {'Média Avaliações'.ljust(25)} | {'Status'}\n")
            text.insert(END, "-"*80 + "\n")
            for restaurante in restaurantes:
                text.insert(END, f"{restaurante._nome.ljust(25)} | {restaurante._categoria.ljust(25)} | {str(restaurante.media_avaliacoes).ljust(25)} | {restaurante.ativo}\n")

    def habilitar_restaurante(self):
        # Lógica para habilitar ou desabilitar um restaurante
        def alternar_estado():
            nome = entry_nome.get()
            for restaurante in Restaurante.restaurantes:
                if restaurante._nome.lower() == nome.lower():
                    restaurante.alternar_estado()
                    messagebox.showinfo("Sucesso", f"Estado do restaurante '{restaurante._nome}' alterado.")
                    win.destroy()
                    return
            messagebox.showerror("Erro", "Restaurante não encontrado.")

        win = Toplevel(self.master)
        win.title("Habilitar/Desabilitar Restaurante")
        Label(win, text="Nome do Restaurante:").pack(pady=5)
        entry_nome = Entry(win)
        entry_nome.pack(pady=5)
        Button(win, text="Alterar Estado", command=alternar_estado).pack(pady=10)

    def avaliar_restaurante(self):
        # Lógica para adicionar uma avaliação a um restaurante
        def salvar_avaliacao():
            nome = entry_nome.get()
            cliente = entry_cliente.get()
            try:
                nota = float(entry_nota.get())
                if 0 <= nota <= 10:
                    for restaurante in Restaurante.restaurantes:
                        if restaurante._nome.lower() == nome.lower():
                            restaurante.receber_avaliacao(cliente, nota)
                            messagebox.showinfo("Sucesso", "Avaliação registrada com sucesso!")
                            win.destroy()
                            return
                    messagebox.showerror("Erro", "Restaurante não encontrado.")
                else:
                    messagebox.showerror("Erro", "A nota deve estar entre 0 e 10.")
            except ValueError:
                messagebox.showerror("Erro", "Por favor, digite um número válido para a nota.")

        win = Toplevel(self.master)
        win.title("Avaliar Restaurante")
        Label(win, text="Nome do Restaurante:").pack(pady=5)
        entry_nome = Entry(win)
        entry_nome.pack(pady=5)
        Label(win, text="Nome do Cliente:").pack(pady=5)
        entry_cliente = Entry(win)
        entry_cliente.pack(pady=5)
        Label(win, text="Nota (0 a 10):").pack(pady=5)
        entry_nota = Entry(win)
        entry_nota.pack(pady=5)
        Button(win, text="Salvar Avaliação", command=salvar_avaliacao).pack(pady=10)

    def alterar_restaurante(self):
        # Lógica para alterar as informações de um restaurante
        def salvar_alteracao():
            nome = entry_nome.get()
            novo_nome = entry_novo_nome.get()
            nova_categoria = entry_nova_categoria.get()
            for restaurante in Restaurante.restaurantes:
                if restaurante._nome.lower() == nome.lower():
                    if novo_nome:
                        restaurante._nome = novo_nome.title()
                    if nova_categoria:
                        restaurante._categoria = nova_categoria.upper()
                    messagebox.showinfo("Sucesso", f"Restaurante '{restaurante}' alterado com sucesso!")
                    win.destroy()
                    return
            messagebox.showerror("Erro", "Restaurante não encontrado.")

        win = Toplevel(self.master)
        win.title("Alterar Restaurante")
        Label(win, text="Nome do Restaurante:").pack(pady=5)
        entry_nome = Entry(win)
        entry_nome.pack(pady=5)
        Label(win, text="Novo Nome:").pack(pady=5)
        entry_novo_nome = Entry(win)
        entry_novo_nome.pack(pady=5)
        Label(win, text="Nova Categoria:").pack(pady=5)
        entry_nova_categoria = Entry(win)
        entry_nova_categoria.pack(pady=5)
        Button(win, text="Salvar Alteração", command=salvar_alteracao).pack(pady=10)

    def excluir_restaurante(self):
        # Lógica para excluir um restaurante
        def confirmar_exclusao():
            nome = entry_nome.get()
            for restaurante in Restaurante.restaurantes:
                if restaurante._nome.lower() == nome.lower():
                    if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o restaurante '{restaurante._nome}'?"):
                        Restaurante.restaurantes.remove(restaurante)
                        messagebox.showinfo("Sucesso", f"Restaurante '{restaurante._nome}' excluído com sucesso.")
                        win.destroy()
                        return
            messagebox.showerror("Erro", "Restaurante não encontrado.")

        win = Toplevel(self.master)
        win.title("Excluir Restaurante")
        Label(win, text="Nome do Restaurante:").pack(pady=5)
        entry_nome = Entry(win)
        entry_nome.pack(pady=5)
        Button(win, text="Excluir", command=confirmar_exclusao).pack(pady=10)
