import tkinter as tk


def validar_entrada(texto):
    """
    Valida a entrada do usuário permitindo apenas número e garantindo que o valor esteja entre 0 e 90
    """
    if texto.isdigit() or texto == "":
        if texto == "":
            return True
        valor = int(texto)
        return 0 <= valor <= 7 
    return False

janela = tk.Tk()
janela.title("Calculadora Trigonométrica")
janela.geometry("400x550")
janela.configure(bg="#f0f0f0")


janela = tk.Tk()
janela.title("-=-= RESTAURANTE EXPRESSO =-=-")
janela.geometry("400x550")
janela.configure(bg="#f0f0f0")


frame_titulo = tk.Frame(janela, bg="#000") 
frame_titulo.pack(pady=10)

label_angulo = tk.Label(frame_titulo, text="RESTAURANTE EXPRESSO", font=('Arial', 14), bg="#f0f0f0")
label_angulo.pack(pady=(0, 5))


frame_opcoes = tk.Frame(janela, bg="#f0f0f0") 
frame_opcoes.pack(pady=10)

label_opcao = tk.Label(frame_opcoes, text="1. Cadatrar Restaurante", font=('Arial', 12), bg="#f0f0f0")
label_opcao.grid(row=0, column=0, padx=10, pady=5, sticky='w') 

label_opcao = tk.Label(frame_opcoes, text="2. Listar Restaurantes", font=('Arial', 12), bg="#f0f0f0")
label_opcao.grid(row=1, column=0, padx=10, pady=5, sticky='w') 

label_opcao = tk.Label(frame_opcoes, text="3. Habilitar Restaurante", font=('Arial', 12), bg="#f0f0f0")
label_opcao.grid(row=2, column=0, padx=10, pady=5, sticky='w') 

label_opcao = tk.Label(frame_opcoes, text="4. Avaliar Restaurante", font=('Arial', 12), bg="#f0f0f0")
label_opcao.grid(row=3, column=0, padx=10, pady=5, sticky='w') 

label_opcao = tk.Label(frame_opcoes, text="5. Alterar Restaurante", font=('Arial', 12), bg="#f0f0f0")
label_opcao.grid(row=4, column=0, padx=10, pady=5, sticky='w') 

label_opcao = tk.Label(frame_opcoes, text="6. Excluir Restaurante", font=('Arial', 12), bg="#f0f0f0")
label_opcao.grid(row=5, column=0, padx=10, pady=5, sticky='w') 

label_opcao = tk.Label(frame_opcoes, text="7. Sair", font=('Arial', 12), bg="#f0f0f0")
label_opcao.grid(row=6, column=0, padx=10, pady=5, sticky='w') 

frame_entrada = tk.Frame(janela, bg="#f0f0f0") 
frame_entrada.pack(pady=10)

validacao = janela.register(validar_entrada) 

entrada_angulo = tk.Entry(frame_entrada, width=3, justify='center', font=('Arial', 16), 
                          bd=0, highlightthickness=0, relief='flat', bg="#f0f0f0", fg='red', 
                          validate="key", validatecommand=(validacao, '%P')) 

linha = tk.Frame (frame_entrada, bg="black", height=1, width=entrada_angulo.winfo_reqwidth()) 
linha.pack(pady=(0,5)) 

janela.mainloop()