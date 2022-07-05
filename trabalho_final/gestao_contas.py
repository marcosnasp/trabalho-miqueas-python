from tkinter import *
from tkinter import ttk
from tksheet import Sheet
import json
from cliente import Cliente
from collections import namedtuple
from json import JSONEncoder

# Opening JSON file
clientes_file = open('clientes.json', "r")
gerentes_file = open('gerentes.json', "r")


def customClienteDecoder(clientDict):
    return namedtuple('X', clientDict.keys())(*clientDict.values())


def customGerenteDecoder(gerenteDict):
    return namedtuple('X', gerenteDict.keys())(*gerenteDict.values())


# Parse JSON into an object with attributes corresponding to dict keys.
clientes = json.loads(clientes_file.read(), object_hook=customClienteDecoder)
gerentes = json.loads(gerentes_file.read(), object_hook=customGerenteDecoder)


def autenticar_gerente(login, senha):
    print("Autenticando usuario com login: {0}, e senha: {1}".format(
        login.get(), senha.get()))
    for gerente in gerentes[0]:
        if (gerente.nome == login.get() and gerente.senha == senha.get()):
            return True
        else:
            return False


root = Tk()
root.title('Gerenciamento de Contas')
root.geometry('800x400')


loginInput = StringVar()
senhaInput = StringVar()
mensagemStatus = StringVar()

nomeCliente = StringVar()
valorInicialDeposito = StringVar()


def printInput():
    if autenticar_gerente(loginInput, senhaInput):
        mensagemStatus.set("Autenticado com sucesso!")
        print("Usuario: {0} Autenticado com sucesso!".format(loginInput.get()))
        criar_botao_novo_cliente()
        carregar_grid()
    else:
        mensagemStatus.set("Não foi possível autenticar!")
        print(
            "Não foi possível autenticar para o Usuario: {0}!".format(loginInput.get()))


frm = ttk.Frame(root, padding=5, width=150, height=150)
frm.grid()

ttk.Label(frm, text="Gestão de Contas").grid(column=0, row=0)

ttk.Label(frm, text="Login", padding=5).grid(column=0, row=1)
nome = ttk.Entry(frm, textvariable=loginInput).grid(column=1, row=1)

ttk.Label(frm, text="Senha", padding=5).grid(column=0, row=2)
senha = ttk.Entry(frm, show="*", textvariable=senhaInput,
                  width=20).grid(column=1, row=2)

ttk.Button(frm, text="Entrar", command=printInput).grid(column=0, row=3)
ttk.Button(frm, text="Sair", command=root.destroy).grid(column=1, row=3)

ttk.Label(frm, text="\n", padding=5).grid(column=0, row=4)
ttk.Label(frm, text="Status do Usuario: ",
          textvariable=mensagemStatus, padding=5).grid(column=0, row=5)


def criar_botao_novo_cliente():
    ttk.Button(frm, text="Novo Cliente",
               command=abrirJanelaCadastroCliente).grid(column=0, row=6)


def abrirJanelaCadastroCliente():
    janela_cadastro_cliente = Toplevel(root)
    janela_cadastro_cliente.title("Cadastro de Clientes")
    janela_cadastro_cliente.geometry("400x600")

    Label(janela_cadastro_cliente,
          text="Nome do Cliente: ").grid(column=0, row=1)
    Entry(janela_cadastro_cliente, textvariable=nomeCliente).grid(column=1, row=1)

    Label(janela_cadastro_cliente, text="Valor Inicial: ").grid(column=0, row=2)
    Entry(janela_cadastro_cliente, textvariable=valorInicialDeposito).grid(
        column=1, row=2)

    Button(janela_cadastro_cliente, text="Cadastrar",
           command=cadastrarCliente).grid(column=0, row=3)
    Button(janela_cadastro_cliente, text="Cancelar",
           command=cancelarCadastroCliente).grid(column=1, row=3)
    janela_cadastro_cliente.grid()


def cadastrarCliente():
    id = getUltimoClienteId(clientes)
    novoId = int(id) + 1
    print("Cadastrando novo cliente com identificador: {0}, nome: {1}, depósito inicial: {2}.".format(
        novoId, nomeCliente.get(), valorInicialDeposito.get()))
    cli = Cliente(novoId, nomeCliente.get(), valorInicialDeposito.get(), 0)
    novo_cliente = json.dumps(cli.__dict__)
    clientes.append(novo_cliente)


def cancelarCadastroCliente():
    print("Cancelando cadastro")


def getUltimoClienteId(clientes):
    ultimoId = 0
    for c in clientes[0]:
        ultimoId = c.id
    return ultimoId


def carregar_grid():
    sheet = Sheet(frm, width=350,
                  height=250, column_width=120, set_all_heights_and_widths=True, expand_sheet_if_paste_too_big=True, data=[
                      [f"Id: {c.id}\n Nome: {c.nome}\n Saldo: {c.saldo} \n Rendimento: {c.valor_rendimento}" for c in clientes[0]]])
    sheet.enable_bindings()
    sheet.grid(column=0, row=7)


root.mainloop()
