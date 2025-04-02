from tkinter import ttk
import customtkinter as ctk
import sqlite3

items = ""


# todo---------------------------------------------------TODOS OS DEFS--------------------------------------------------

# Criando banco de dados
def criar_banco():
    conexao = sqlite3.connect("produtos.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute("CREATE TABLE IF NOT EXISTS produtos("
                         "nome TEXT ,"
                         "quantidade INTEGER,"
                         "preco REAL ,"
                         "descricao TEXT)")
    conexao.commit()
    conexao.close()


# Lendo os dados
def ler_dados():
    conexao = sqlite3.connect("produtos.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute("select * from produtos")
    receba_dados = terminal_sql.fetchall()

    for item in tabela_Restoque.get_children():
        tabela_Restoque.delete(item)

    for i in receba_dados:
        entrada_informar_nome = str(i[0])
        qtd = str(i[1])
        entrada_informar_preco = str(i[2])
        descricao_Tcadastro = str(i[3])
        tabela_Restoque.insert("", "end",
                               values=(entrada_informar_nome, qtd, entrada_informar_preco, descricao_Tcadastro))


# fazendo a lista de produtos da tela editar, saida e entrada
def lista_de_produtos():
    conexao = sqlite3.connect("produtos.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute("select nome from produtos")
    receber_nomes_produtos = terminal_sql.fetchall()

    for widget in lista_produtos_Teditar.winfo_children():
        widget.destroy()
    for widget in lista_Tsaida.winfo_children():
        widget.destroy()
    for widget in lista_Tentrada.winfo_children():
        widget.destroy()

    check_var = ctk.StringVar()
    for i in receber_nomes_produtos:
        entrada_informar_nome = str(i[0])
        produtos_Teditar = ctk.CTkCheckBox(lista_produtos_Teditar, text=entrada_informar_nome, border_color="#FFB046",
                                           border_width=2, onvalue=entrada_informar_nome, offvalue="",
                                           variable=check_var,
                                           command=lambda: selecionar_produto(
                                               check_var) if check_var.get() else apagar_entradas_Teditar())
        produtos_Teditar.pack(pady=5, anchor="w")

        produtos_Tsaida = ctk.CTkCheckBox(lista_Tsaida, text=entrada_informar_nome, border_color="#FFB046",
                                          border_width=2, onvalue=entrada_informar_nome, offvalue="",
                                          variable=check_var,
                                          command=lambda: lista_selecionados(
                                              check_var) if check_var.get() else apagar_entradas_Teditar())
        produtos_Tsaida.pack(pady=5, anchor="w")

        produtos_Tentrada = ctk.CTkCheckBox(lista_Tentrada, text=entrada_informar_nome, border_color="#FFB046",
                                            border_width=2, onvalue=entrada_informar_nome, offvalue="",
                                            variable=check_var,
                                            command=lambda: selecionar_produto(
                                                check_var) if check_var.get() else apagar_entradas_Teditar())
        produtos_Tentrada.pack(pady=5, anchor="w")


# deletar produtos na tela editar
def deletar_produtos(nome_produto):
    conexao = sqlite3.connect("produtos.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute(f"DELETE FROM produtos WHERE nome = '{nome_produto}'")
    conexao.commit()
    conexao.close()
    editar_nome_produto.delete(0, "end")
    editar_preco_produto.delete(0, "end")
    editar_descricao_produto.delete(0.0, "end")
    lista_de_produtos()


# salva a edição do produto
def salvar_edicao_produto(nome_produto, preco_produto, descricao_produto):
    conexao = sqlite3.connect("produtos.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute(
        f"UPDATE produtos SET nome = '{nome_produto}', preco = '{preco_produto}', descricao = '{descricao_produto}' WHERE nome = '{valor_checkbox}'")
    conexao.commit()
    conexao.close()
    editar_nome_produto.delete(0, "end")
    editar_preco_produto.delete(0, "end")
    editar_descricao_produto.delete(0.0, "end")
    lista_de_produtos()


# apagando as entry da tela editar
def apagar_entradas_Teditar():
    editar_nome_produto.delete(0, "end")
    editar_preco_produto.delete(0, "end")
    editar_descricao_produto.delete(0.0, "end")


# adiciona produto
def selecionar_produto(entrada_informar_nome):
    global valor_checkbox
    valor_checkbox = entrada_informar_nome.get().strip("(),'\"")

    conexao = sqlite3.connect("produtos.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute(f"SELECT * FROM produtos WHERE nome = '{valor_checkbox}'")
    receber_dados = terminal_sql.fetchall()
    print(receber_dados)

    editar_nome_produto.delete(0, "end")
    editar_nome_produto.insert(0, receber_dados[0][0])

    editar_preco_produto.delete(0, "end")
    editar_preco_produto.insert(0, receber_dados[0][2])

    editar_descricao_produto.delete(0.0, "end")
    editar_descricao_produto.insert(0.0, receber_dados[0][3])


# salva produto criado na tela cadastro
def salvar_dados_Tcadastro():
    conexao = sqlite3.connect("produtos.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute(f"insert into produtos (nome, preco, descricao) values(?,?,?)", (entrada_informar_nome.get(),
                                                                                          entrada_informar_preco.get(),
                                                                                          descricao_Tcadastro.get("1.0",
                                                                                                                  "end")
                                                                                          ,))
    conexao.commit()
    conexao.close()
    entrada_informar_nome.delete(0, "end")
    entrada_informar_preco.delete(0, "end")
    descricao_Tcadastro.delete("1.0", "end")
 

def lista_selecionados(entrada_informar_nome):
    global valor_checkbox_selecionados
    valor_checkbox_selecionados = entrada_informar_nome.get().strip("(),'\"")

    conexao = sqlite3.connect("produtos.db")
    terminal_sql = conexao.cursor()
    terminal_sql.execute(f"SELECT * FROM produtos WHERE nome = '{valor_checkbox_selecionados}'")
    receber_nome_listaSelecionadaos = terminal_sql.fetchall()
    print(receber_nome_listaSelecionadaos)
    adicionar_item_Ts_Tent

def adicionar_item_Ts_Tent(receber_nome_listaSelecionadaos):
    Label = ctk.CTkLabel(lista_selecionada_Tsaida, text=f"'{receber_nome_listaSelecionadaos[0][0]} {receber_nome_listaSelecionadaos[0][1]}'")
    Label.pack(pady=5)

        
def abrir_tela_cadastro():
    frame_editar.grid_forget()
    frame_tela_saida.grid_forget()
    frame_tela_entrada.grid_forget()
    frame_tela_relatorio.grid_forget()
    tela_cadastro.configure(fg_color="#290B2D")
    tela_editar.configure(fg_color="purple")
    tela_saida.configure(fg_color="purple")
    tela_entrada.configure(fg_color="purple")
    tela_relatorio.configure(fg_color="purple")
    frame_tela_cadastro.configure(height=380, width=590, fg_color="black", border_color="purple", border_width=2)
    frame_tela_cadastro.grid_propagate(False)
    frame_tela_cadastro.grid(row=0, column=1, padx=5, pady=10)


def abrir_tela_editar():
    lista_de_produtos()
    frame_tela_cadastro.grid_forget()
    frame_tela_saida.grid_forget()
    frame_tela_entrada.grid_forget()
    frame_tela_relatorio.grid_forget()
    tela_cadastro.configure(fg_color="purple")
    tela_editar.configure(fg_color="#290B2D")
    tela_saida.configure(fg_color="purple")
    tela_entrada.configure(fg_color="purple")
    tela_relatorio.configure(fg_color="purple")
    frame_editar.configure(height=380, width=590, fg_color="black", border_color="purple", border_width=2)
    frame_editar.grid_propagate(False)
    frame_editar.grid(row=0, column=1, padx=5, pady=10)


def abrir_tela_saida():
    lista_de_produtos()
    frame_tela_cadastro.grid_forget()
    frame_editar.grid_forget()
    frame_tela_entrada.grid_forget()
    frame_tela_relatorio.grid_forget()
    tela_cadastro.configure(fg_color="purple")
    tela_editar.configure(fg_color="purple")
    tela_saida.configure(fg_color="#290B2D")
    tela_entrada.configure(fg_color="purple")
    tela_relatorio.configure(fg_color="purple")
    frame_tela_saida.configure(height=380, width=590, fg_color="black", border_color="purple", border_width=2)
    frame_tela_saida.grid_propagate(False)
    frame_tela_saida.grid(row=0, column=1, padx=5, pady=10)


def abrir_tela_entrada():
    lista_de_produtos()
    frame_tela_cadastro.grid_forget()
    frame_editar.grid_forget()
    frame_tela_saida.grid_forget()
    frame_tela_relatorio.grid_forget()
    tela_cadastro.configure(fg_color="purple")
    tela_editar.configure(fg_color="purple")
    tela_saida.configure(fg_color="purple")
    tela_entrada.configure(fg_color="#290B2D")
    tela_relatorio.configure(fg_color="purple")
    frame_tela_entrada.configure(height=380, width=590, fg_color="black", border_color="purple", border_width=2)
    frame_tela_entrada.grid_propagate(False)
    frame_tela_entrada.grid(row=0, column=1, padx=5, pady=10)


def abrir_tela_Restoque():
    ler_dados()
    frame_tela_cadastro.grid_forget()
    frame_editar.grid_forget()
    frame_tela_saida.grid_forget()
    frame_tela_entrada.grid_forget()
    frame_Rsaida.grid_forget()
    frame_Rentrada.grid_forget()

    tela_cadastro.configure(fg_color="purple")
    tela_editar.configure(fg_color="purple")
    tela_saida.configure(fg_color="purple")
    tela_entrada.configure(fg_color="purple")
    tela_relatorio.configure(fg_color="#290B2D")

    frame_tela_relatorio.configure(height=380, width=590, fg_color="black", border_color="purple", border_width=2)
    frame_tela_relatorio.grid_propagate(False)
    frame_tela_relatorio.grid(row=0, column=1, padx=5, pady=10)


def relatorio_saida():
    frame_tela_cadastro.grid_forget()
    frame_editar.grid_forget()
    frame_tela_saida.grid_forget()
    frame_tela_entrada.grid_forget()
    frame_tela_relatorio.grid_forget()
    frame_Rentrada.grid_forget()
    frame_Rsaida.configure(height=380, width=590, fg_color="black", border_color="purple", border_width=2)
    frame_Rsaida.grid_propagate(False)
    frame_Rsaida.grid(row=0, column=1, padx=5, pady=10)


def relatorio_entrada():
    frame_tela_cadastro.grid_forget()
    frame_editar.grid_forget()
    frame_tela_saida.grid_forget()
    frame_tela_entrada.grid_forget()
    frame_Rsaida.grid_forget()
    frame_tela_relatorio.grid_forget()
    frame_Rsaida.grid_forget()
    frame_Rentrada.configure(height=380, width=590, fg_color="black", border_color="purple", border_width=2)
    frame_Rentrada.grid_propagate(False)
    frame_Rentrada.grid(row=0, column=1, padx=5, pady=10)


def exportar():
    janela01 = ctk.CTk()
    janela01.geometry("400x200")
    ctk.set_default_color_theme("blue")
    ctk.set_appearance_mode("dark")

    frame_mini_janela = ctk.CTkFrame(janela01, fg_color="#000000", width=400, height=200, border_color="#458A00",
                                     border_width=2)
    frame_mini_janela.grid_propagate(False)
    frame_mini_janela.grid(row=0, column=0, padx=0, pady=0)

    label_relatorio = ctk.CTkLabel(frame_mini_janela, text="Escolher relatório(s):", font=("", 15))
    label_relatorio.grid(row=0, column=0, padx=30, pady=10)

    check_estoque = ctk.CTkCheckBox(frame_mini_janela, text="Exportar estoque")
    check_estoque.grid(row=1, column=0, padx=30, pady=5, sticky="w")
    check_saida = ctk.CTkCheckBox(frame_mini_janela, text="Exportar saida")
    check_saida.grid(row=2, column=0, padx=30, pady=5, sticky="w")
    check_entrada = ctk.CTkCheckBox(frame_mini_janela, text="Exportar entrada")
    check_entrada.grid(row=3, column=0, padx=30, pady=5, sticky="w")

    label_extensao = ctk.CTkLabel(frame_mini_janela, text="Escolher extensão:", font=("", 15))
    label_extensao.grid(row=0, column=1, padx=30, pady=10, columnspan=2)

    check_word = ctk.CTkCheckBox(frame_mini_janela, text="Word")
    check_word.grid(row=1, column=1, padx=30, pady=5, sticky="w", columnspan=2)
    check_pdf = ctk.CTkCheckBox(frame_mini_janela, text="PDF")
    check_pdf.grid(row=2, column=1, padx=30, pady=5, sticky="w", columnspan=2)
    check_exel = ctk.CTkCheckBox(frame_mini_janela, text="Exel")
    check_exel.grid(row=3, column=1, padx=30, pady=5, sticky="w", columnspan=2)

    botao_salvar = ctk.CTkButton(frame_mini_janela, text="Salvar", width=80, fg_color="#458A00",
                                 hover_color="#193200", command=janela01.destroy)
    botao_salvar.grid(row=4, column=2, padx=5, pady=5, sticky="w")
    botao_cancelar = ctk.CTkButton(frame_mini_janela, text="Cancelar", width=80, fg_color="#FA0085",
                                   hover_color="#290B2D")
    botao_cancelar.grid(row=4, column=1, padx=5, pady=5, sticky="e")

    janela01.mainloop()


# todo>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# todo-------------------------------------------TELA DE MENU-----------------------------------------------------------
criar_banco()
janela = ctk.CTk()
janela.geometry("800x400")
ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("dark")

frame_fundo_tela = ctk.CTkFrame(janela, height=400, width=800, fg_color="black")
frame_fundo_tela.propagate(False)
frame_fundo_tela.grid(row=0, column=0, padx=0, pady=0)

frame_menu = ctk.CTkFrame(frame_fundo_tela, height=380, width=190, border_color="purple", border_width=2,
                          fg_color="black")
frame_menu.propagate(False)
frame_menu.grid(row=0, column=0, padx=5, pady=10)

titulo = ctk.CTkLabel(frame_menu, text="Nome do\nsistema", font=("Arial", 20, "bold"), )
titulo.pack(pady=20)

tela_cadastro = ctk.CTkButton(frame_menu, text="Cadastro", command=abrir_tela_cadastro, fg_color="purple",
                              hover_color="#290B2D")
tela_cadastro.pack(pady=5)

tela_editar = ctk.CTkButton(frame_menu, text="Editar", command=abrir_tela_editar, fg_color="purple",
                            hover_color="#290B2D")
tela_editar.pack(pady=5)

tela_saida = ctk.CTkButton(frame_menu, text="Saida", command=abrir_tela_saida, fg_color="purple", hover_color="#290B2D")
tela_saida.pack(pady=5)

tela_entrada = ctk.CTkButton(frame_menu, text="Entrada", command=abrir_tela_entrada, fg_color="purple",
                             hover_color="#290B2D")
tela_entrada.pack(pady=5)

tela_relatorio = ctk.CTkButton(frame_menu, text="Relatorio", command=abrir_tela_Restoque, fg_color="purple",
                               hover_color="#290B2D")
tela_relatorio.pack(pady=5)
# todo>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# todo----------------------------------------------TELA DE CADASTRO----------------------------------------------------
# Frame
frame_tela_cadastro = ctk.CTkFrame(frame_fundo_tela, height=380, width=590, fg_color="black", border_color="purple",
                                   border_width=2)
frame_tela_cadastro.grid_propagate(False)
frame_tela_cadastro.grid(row=0, column=1, padx=5, pady=10)

# Cod da Tela
# coluna 0
texto_nome_produto = ctk.CTkLabel(frame_tela_cadastro, text=f"Nome de Produto:")
texto_nome_produto.grid(row=1, column=0, padx=5, pady=5, sticky="e")
texto_preco = ctk.CTkLabel(frame_tela_cadastro, text=f"Preço(R$):")
texto_preco.grid(row=2, column=0, padx=5, pady=5, sticky="e")
texto_descricao = ctk.CTkLabel(frame_tela_cadastro, text=f"Descrição:")
texto_descricao.grid(row=3, column=0, padx=5, pady=5, sticky="en")

# coluna 1
titulo_Tcadastro = ctk.CTkLabel(frame_tela_cadastro, text="Cadastro de Produto", font=("", 20, "bold"))
titulo_Tcadastro.grid(row=0, column=1, padx=5, pady=20)

entrada_informar_nome = ctk.CTkEntry(frame_tela_cadastro, placeholder_text="Informe o nome do Produto:", width=300)
entrada_informar_nome.grid(row=1, column=1, padx=5, pady=5)

entrada_informar_preco = ctk.CTkEntry(frame_tela_cadastro, placeholder_text=f"0,00", width=80)
entrada_informar_preco.grid(row=2, column=1, padx=5, pady=5, sticky="w")

descricao_Tcadastro = ctk.CTkTextbox(frame_tela_cadastro, height=80, width=300)
descricao_Tcadastro.grid(row=3, column=1, padx=5, pady=5)

botao_salvar_Tcadastro = ctk.CTkButton(frame_tela_cadastro, text="Salvar", hover_color="#290B2D", width=80,
                                       fg_color="#FA0085", command=salvar_dados_Tcadastro)
botao_salvar_Tcadastro.grid(row=4, column=1, padx=5, pady=5, sticky="e")

# todo>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# todo--------------------------------------------TELA DE EDITAR--------------------------------------------------------
# Frame
frame_editar = ctk.CTkFrame(frame_fundo_tela, height=380, width=590, fg_color="black", border_color="purple",
                            border_width=2)
frame_editar.grid_propagate(False)

# Cod da Tela
# Coluna 0\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
Titulo_Teditar = ctk.CTkLabel(frame_editar, text="Editar Produto Cadastrado", font=("", 20, "bold"))
Titulo_Teditar.grid(row=0, column=0, padx=5, pady=20, columnspan=5)

busca_Teditar = ctk.CTkEntry(frame_editar, placeholder_text="Buscar Produto:", width=300)
busca_Teditar.grid(row=1, column=0, padx=5, pady=10, columnspan=2, sticky="w")

lista_produtos_Teditar = ctk.CTkScrollableFrame(frame_editar, height=200, width=160)
lista_produtos_Teditar.grid(row=2, column=0, pady=10, padx=20, rowspan=4, )

for item in items:
    box = ctk.CTkCheckBox(lista_produtos_Teditar, text=item, border_color="#FFB046", border_width=2)
    box.pack(pady=5, padx=0)

# Coluna 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
editar_descricao_produto = ctk.CTkTextbox(frame_editar, height=100, width=300)
editar_descricao_produto.grid(row=4, column=1, padx=5, pady=0, sticky="n", columnspan=3)

editar_nome_produto = ctk.CTkEntry(frame_editar, placeholder_text="Nome do Produto", width=300)
editar_nome_produto.grid(row=2, column=1, padx=5, pady=0, sticky="n", columnspan=3)

editar_preco_produto = ctk.CTkEntry(frame_editar, placeholder_text="0.00", width=80)
editar_preco_produto.grid(row=3, column=1, padx=5, pady=0, sticky="wn")

botao_excluir_Teditar = ctk.CTkButton(frame_editar, text="Excluir", fg_color="red", hover_color="#8A0500", width=80,
                                      command=lambda: deletar_produtos(editar_nome_produto.get()))
botao_excluir_Teditar.grid(row=5, column=1, padx=5, pady=0, sticky="w")

# Coluna 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
botao_cancelar_Teditar = ctk.CTkButton(frame_editar, text="Cancelar", width=80, fg_color="#FA0085",
                                       hover_color="#290B2D")
botao_cancelar_Teditar.grid(row=5, column=2, padx=5, pady=0)

# Coluna 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
botao_salvar_Teditar = ctk.CTkButton(frame_editar, text="Salvar", width=80, fg_color="#FA0085",
                                     hover_color="#290B2D",
                                     command=lambda: salvar_edicao_produto((editar_nome_produto.get()),
                                                                           (editar_preco_produto.get()),
                                                                           (editar_descricao_produto.get(0.0, "end"))))
botao_salvar_Teditar.grid(row=5, column=3, padx=5, pady=0, sticky="e")

# todo>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# todo---------------------------------------------TELA DE SAIDA--------------------------------------------------------
# Frame
frame_tela_saida = ctk.CTkFrame(frame_fundo_tela, height=380, width=590, fg_color="black", border_color="purple",
                                border_width=2)
frame_tela_saida.grid_propagate(False)

# Cod da tela
# Coluna 0\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
Titulo_Tsaida = ctk.CTkLabel(frame_tela_saida, text="Saida de Produto", font=("", 20, "bold"))
Titulo_Tsaida.grid(row=0, column=0, padx=0, pady=5, columnspan=4)

busca_Tsaida = ctk.CTkEntry(frame_tela_saida, placeholder_text="Digite para Buscar:", width=180)
busca_Tsaida.grid(row=1, column=0, padx=50, pady=0, rowspan=2, sticky="s")

lista_Tsaida = ctk.CTkScrollableFrame(frame_tela_saida, height=200, width=220)
lista_Tsaida.grid(row=2, column=0, pady=10, padx=5, rowspan=3, )

for item in items:
    box = ctk.CTkCheckBox(lista_Tsaida, text=item, border_color="#FFB046", border_width=2)
    box.pack(pady=5, padx=0, side="left")

# Coluna 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
qtd_estoque_Tsaida = ctk.CTkLabel(frame_tela_saida, text="Quantidade em Estoque: 18", font=("", 15, "bold"))
qtd_estoque_Tsaida.grid(row=1, column=1, padx=20, pady=0, columnspan=2, sticky="s")

qtd_retirada_Tsaida = ctk.CTkEntry(frame_tela_saida, placeholder_text="QTD.Retirada", width=90)
qtd_retirada_Tsaida.grid(row=2, column=1, padx=0, pady=0, sticky="nw")

botao_cancelar_Tsaida = ctk.CTkButton(frame_tela_saida, text="Cancelar", hover_color="#290B2D", fg_color="#FA0085",
                                      width=80)
botao_cancelar_Tsaida.grid(row=4, column=1, pady=0, padx=0, sticky="nw")

lista_selecionada_Tsaida = ctk.CTkScrollableFrame(frame_tela_saida, height=10, width=220)
lista_selecionada_Tsaida.grid(row=3, column=1, pady=5, padx=0, columnspan=2)


# Coluna 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
botao_add_Tsaida = ctk.CTkButton(frame_tela_saida, text="Adicionar Item", fg_color="#FA0085", hover_color="#290B2D",
                                 width=130)
botao_add_Tsaida.grid(row=2, column=2, padx=0, pady=0, sticky="n")

botao_salvar_Tsaida = ctk.CTkButton(frame_tela_saida, text="Salvar", fg_color="#FA0085", hover_color="#290B2D",
                                    width=80)
botao_salvar_Tsaida.grid(row=4, column=2, pady=0, padx=0, sticky="en")
# todo>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# todo---------------------------------------------TELA DE ENTRADA------------------------------------------------------
# Frame
frame_tela_entrada = ctk.CTkFrame(frame_fundo_tela, height=380, width=590, fg_color="black", border_color="purple",
                                  border_width=2)
frame_tela_entrada.grid_propagate(False)

# cod da tela
# Coluna 0\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
Titulo_Tentrada = ctk.CTkLabel(frame_tela_entrada, text="Tela de Entrada", font=("", 20, "bold"))
Titulo_Tentrada.grid(row=0, column=0, padx=5, pady=5, columnspan=4)

busca_Tentrada = ctk.CTkEntry(frame_tela_entrada, placeholder_text="Digite para Buscar:", width=180)
busca_Tentrada.grid(row=1, column=0, padx=50, pady=0, rowspan=2, sticky="s")

lista_Tentrada = ctk.CTkScrollableFrame(frame_tela_entrada, height=200, width=220)
lista_Tentrada.grid(row=2, column=0, pady=10, padx=5, rowspan=3, )

for item in items:
    box = ctk.CTkCheckBox(lista_Tentrada, text=item, border_color="#FFB046", border_width=2)
    box.pack(pady=5, padx=0, side="left")

# Coluna 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
qtd_estoque_Tentrada = ctk.CTkLabel(frame_tela_entrada, text="Quantidade em Estoque: 18", font=("", 15, "bold"))
qtd_estoque_Tentrada.grid(row=1, column=1, padx=20, pady=0, columnspan=2, sticky="s")

qtd_entrando_Tentrada = ctk.CTkEntry(frame_tela_entrada, placeholder_text="QTD.para Entrar", width=110)
qtd_entrando_Tentrada.grid(row=2, column=1, padx=0, pady=0, sticky="nw")

botao_cancelar_Tentrada = ctk.CTkButton(frame_tela_entrada, text="Cancelar", fg_color="#FA0085",
                                        hover_color="#290B2D", width=80)
botao_cancelar_Tentrada.grid(row=4, column=1, pady=0, padx=0, sticky="nw")

lista_selecionado_Tentrada = ctk.CTkScrollableFrame(frame_tela_entrada, height=10, width=220)
lista_selecionado_Tentrada.grid(row=3, column=1, pady=5, padx=0, columnspan=2)

for _ in items:
    botao_apagar_selecionado = ctk.CTkButton(lista_selecionado_Tentrada, text="X", fg_color="red",
                                             hover_color="#8A0500",
                                             width=20, height=20)
    botao_apagar_selecionado.grid(row=0, column=1, pady=5, padx=0, sticky="e")
    lista_selecionado_Tentrada.grid_columnconfigure(1, weight=2)
    box = ctk.CTkCheckBox(lista_selecionado_Tentrada, text=f"{items}", border_color="#FFB046", border_width=2)
    box.grid(row=0, column=0, pady=5, padx=0, sticky="w")

# Coluna 2\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
botao_add_Tentrada = ctk.CTkButton(frame_tela_entrada, text="Adicionar Item", fg_color="#FA0085",
                                   hover_color="#290B2D", width=115)
botao_add_Tentrada.grid(row=2, column=2, padx=0, pady=0, sticky="n")

botao_salvar_Tentrada = ctk.CTkButton(frame_tela_entrada, text="Salvar", fg_color="#FA0085",
                                      hover_color="#290B2D", width=80)
botao_salvar_Tentrada.grid(row=4, column=2, pady=0, padx=0, sticky="en")

# todo>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# todo--------------------------------------------TELA.Restoque---------------------------------------------------------

# Frame
frame_tela_relatorio = ctk.CTkFrame(frame_fundo_tela, height=380, width=590, fg_color="black", border_color="purple",
                                    border_width=2)
frame_tela_relatorio.grid_propagate(False)

# Cod da tela

# Coluna 0\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
Titulo_Restoque = ctk.CTkLabel(frame_tela_relatorio, text="Relatório de Estoque", font=("", 20, "bold"))
Titulo_Restoque.grid(row=0, column=0, padx=10, pady=5, columnspan=5)

frame_tabela_Restoque = ctk.CTkFrame(frame_tela_relatorio)
frame_tabela_Restoque.grid(row=2, column=0, padx=30, pady=5, columnspan=5)

colunas_Restoque = ("Nome", "Quantidade", "Preço", "Descrição")
tabela_Restoque = ttk.Treeview(frame_tabela_Restoque, columns=colunas_Restoque, show="headings", height=10)

for coluna_Restoque in colunas_Restoque:
    tabela_Restoque.heading(coluna_Restoque, text=coluna_Restoque)

tabela_Restoque.column("Nome", width=132)
tabela_Restoque.column("Quantidade", width=132)
tabela_Restoque.column("Preço", width=132)
tabela_Restoque.column("Descrição", width=132)

estilo_Restoque = ttk.Style()
estilo_Restoque.configure("Custom.Treeview",
                          background="#D3D3D3",
                          foreground="black",
                          fieldbackground="#D3D3D3",
                          font=("Arial", 10))

estilo_Restoque.configure("Custom.Treeview.Heading",
                          background="Blue",
                          foreground="Black",
                          font=("Arial", 12, "bold"))

tabela_Restoque.tag_configure("oddrow", background="#F0F0F0")
tabela_Restoque.tag_configure("evenrow", background="#FFFFFF")

tabela_Restoque.configure(style="Custom.Treeview")

tabela_Restoque.pack(pady=0)
tabela_Restoque.grid_propagate(False)

# Coluna 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
barra_pesquisa_Restoque = ctk.CTkEntry(frame_tela_relatorio, placeholder_text="Pesquisar:", width=210)
barra_pesquisa_Restoque.grid(row=1, column=1, padx=0, pady=5)

# Coluna 2 \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
botao_estoque_Restoque = ctk.CTkButton(frame_tela_relatorio, text="Estoque", width=80, fg_color="#FA0085",
                                       hover_color="#290B2D")
botao_estoque_Restoque.grid(row=3, column=2, padx=10, pady=5, sticky="e")
botao_estoque_Restoque.configure(fg_color="#290B2D")

# Coluna 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
botao_saida_Restoque = ctk.CTkButton(frame_tela_relatorio, text="Saida", width=80, fg_color="#FA0085",
                                     hover_color="#290B2D", command=relatorio_saida)
botao_saida_Restoque.grid(row=3, column=3, padx=0, pady=5)

# Coluna 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
botao_entrada_Restoque = ctk.CTkButton(frame_tela_relatorio, text="Entrada", width=80, fg_color="#FA0085",
                                       hover_color="#290B2D", command=relatorio_entrada)
botao_entrada_Restoque.grid(row=3, column=4, padx=10, pady=5, sticky="w")

botao_exportar_Restoque = ctk.CTkButton(frame_tela_relatorio, text="Exportar", width=80, fg_color="#458A00",
                                        hover_color="#193200", command=exportar)
botao_exportar_Restoque.grid(row=1, column=4, padx=10, pady=5, sticky="w")

# todo>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# todo-------------------------------------------RELATORIO DE SAIDA-----------------------------------------------------
# Frame
frame_Rsaida = ctk.CTkFrame(frame_fundo_tela, height=380, width=590, border_color="purple", border_width=2,
                            fg_color="black")
frame_Rsaida.grid_propagate(False)

# Cod da Tela
# Coluna 0\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
Titulo_Rsaida = ctk.CTkLabel(frame_Rsaida, text="Relatório de Saida", font=("", 20, "bold"))
Titulo_Rsaida.grid(row=0, column=0, padx=10, pady=5, columnspan=5)

frame_tabela_Rsaida = ctk.CTkFrame(frame_Rsaida)
frame_tabela_Rsaida.grid(row=2, column=0, padx=30, pady=5, columnspan=5)

columns_Rsaida = ("Nome", "Quantidade", "Data/Hora")
tabela_Rsaida = ttk.Treeview(frame_tabela_Rsaida, columns=columns_Rsaida, show="headings", height=10)

for colunas_saida in columns_Rsaida:
    tabela_Rsaida.heading(colunas_saida, text=colunas_saida)

tabela_Rsaida.column("Nome", width=176)
tabela_Rsaida.column("Quantidade", width=176)
tabela_Rsaida.column("Data/Hora", width=176)

dados_saida = [("Fone", 10,),
               ("Celular", 15,),
               ]

for itens_Rsaida in dados_saida:
    tabela_Rsaida.insert("", "end", values=itens_Rsaida)

estilo_Rsaida = ttk.Style()
estilo_Rsaida.configure("Custom.Treeview",
                        background="#D3D3D3",
                        foreground="black",
                        fieldbackground="#D3D3D3",
                        font=("Arial", 10))

estilo_Rsaida.configure("Custom.Treeview.Heading",
                        background="Blue",
                        foreground="Black",
                        font=("Arial", 12, "bold"))

tabela_Rsaida.tag_configure("oddrow", background="#F0F0F0")
tabela_Rsaida.tag_configure("evenrow", background="#FFFFFF")

tabela_Rsaida.configure(style="Custom.Treeview")

tabela_Rsaida.pack(pady=0)
tabela_Rsaida.grid_propagate(False)

# Coluna 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
barra_pesquisa_Rsaida = ctk.CTkEntry(frame_Rsaida, placeholder_text="Pesquisar:", width=210)
barra_pesquisa_Rsaida.grid(row=1, column=1, padx=0, pady=5)

# Coluna 2 \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

botao_estoque_Rsaida = ctk.CTkButton(frame_Rsaida, text="Estoque", width=80, fg_color="#FA0085",
                                     hover_color="#290B2D", command=abrir_tela_Restoque)
botao_estoque_Rsaida.grid(row=3, column=2, padx=10, pady=5, sticky="e")

# Coluna 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
botao_saida_Rsaida = ctk.CTkButton(frame_Rsaida, text="Saida", width=80, fg_color="#290B2D",
                                   hover_color="#290B2D")
botao_saida_Rsaida.grid(row=3, column=3, padx=0, pady=5)

# Coluna 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
botao_entrada_Rsaida = ctk.CTkButton(frame_Rsaida, text="Entrada", width=80, fg_color="#FA0085",
                                     hover_color="#290B2D", command=relatorio_entrada)
botao_entrada_Rsaida.grid(row=3, column=4, padx=10, pady=5, sticky="w")

botao_exportar_Rsaida = ctk.CTkButton(frame_Rsaida, text="Exportar", width=80, fg_color="#458A00",
                                      hover_color="#193200", command=exportar)
botao_exportar_Rsaida.grid(row=1, column=4, padx=10, pady=5, sticky="w")

# todo>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# todo--------------------------------------------RELATORIO DE ENTRADA--------------------------------------------------
# Frame
frame_Rentrada = ctk.CTkFrame(frame_fundo_tela, height=380, width=590, border_color="purple", border_width=2,
                              fg_color="black")
frame_Rentrada.grid_propagate(False)

# Cod da Tela
# Coluna 0\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
Titulo_Rentrada = ctk.CTkLabel(frame_Rentrada, text="Relatório de Entrada", font=("", 20, "bold"))
Titulo_Rentrada.grid(row=0, column=0, padx=10, pady=5, columnspan=5)

frame_tabela_Rentrada = ctk.CTkFrame(frame_Rentrada)
frame_tabela_Rentrada.grid(row=2, column=0, padx=30, pady=5, columnspan=5)

colunas_Rentrada = ("Nome", "Quantidade", "Data/Hora")
tabela_Rentrada = ttk.Treeview(frame_tabela_Rentrada, columns=colunas_Rentrada, show="headings", height=10)

for coluna_Rentrada in colunas_Rentrada:
    tabela_Rentrada.heading(coluna_Rentrada, text=coluna_Rentrada)

tabela_Rentrada.column("Nome", width=176)
tabela_Rentrada.column("Quantidade", width=176)
tabela_Rentrada.column("Data/Hora", width=176)

dados_Rentrada = [("Fone", 10,),
                  ("Celular", 15,)]

for item_Rentrada in dados_Rentrada:
    tabela_Rentrada.insert("", "end", values=item_Rentrada)

estilo_Rentrada = ttk.Style()
estilo_Rentrada.configure("Custom.Treeview",
                          background="#D3D3D3",
                          foreground="black",
                          fieldbackground="#D3D3D3",
                          font=("Arial", 10))

estilo_Rentrada.configure("Custom.Treeview.Heading",
                          background="Blue",
                          foreground="Black",
                          font=("Arial", 12, "bold"))

tabela_Rentrada.tag_configure("oddrow", background="#F0F0F0")
tabela_Rentrada.tag_configure("evenrow", background="#FFFFFF")

tabela_Rentrada.configure(style="Custom.Treeview")

tabela_Rentrada.pack(pady=0)
tabela_Rentrada.grid_propagate(False)

# Coluna 1\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
barra_pesquisa_Rentrada = ctk.CTkEntry(frame_Rentrada, placeholder_text="Pesquisar:", width=210)
barra_pesquisa_Rentrada.grid(row=1, column=1, padx=0, pady=5)

# Coluna 2 \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
botao_estoque_Rentrada = ctk.CTkButton(frame_Rentrada, text="Estoque", width=80, fg_color="#FA0085",
                                       hover_color="#290B2D", command=abrir_tela_Restoque)
botao_estoque_Rentrada.grid(row=3, column=2, padx=10, pady=5, sticky="e")

# Coluna 3\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
botao_saida_Rentrada = ctk.CTkButton(frame_Rentrada, text="Saida", width=80, fg_color="#FA0085",
                                     hover_color="#290B2D", command=relatorio_saida)
botao_saida_Rentrada.grid(row=3, column=3, padx=0, pady=5)

# Coluna 4\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
botao_entrada_Rentrada = ctk.CTkButton(frame_Rentrada, text="Entrada", width=80, fg_color="#290B2D",
                                       hover_color="#290B2D")
botao_entrada_Rentrada.grid(row=3, column=4, padx=10, pady=5, sticky="w")

botao_exportar_Rentrada = ctk.CTkButton(frame_Rentrada, text="Exportar", width=80, fg_color="#458A00",
                                        hover_color="#193200", command=exportar)
botao_exportar_Rentrada.grid(row=1, column=4, padx=10, pady=5, sticky="w")

# todo>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
janela.mainloop()
