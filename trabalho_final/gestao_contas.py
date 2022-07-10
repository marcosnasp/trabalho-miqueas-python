from tkinter import *
from tkinter import ttk
from tokenize import Double
from tksheet import Sheet
import json
from cliente import Cliente
from collections import namedtuple
from json import JSONEncoder

import logging
logging.basicConfig(filename='registro.log', encoding='utf-8', level=logging.DEBUG)

# Abre os arquivos dos clientes e dos gerentes
clientes_file = open('clientes.json', "r")
gerentes_file = open('gerentes.json', "r")

# Parse JSON em um dicionario de cliente e gerentes
clientes = json.load(clientes_file)
gerentes = json.load(gerentes_file)

# Autentica o gerente, tendo sido fornecidos o login e a senha a partir da tela


def autenticar_gerente(login, senha):
    logging.info("Autenticando usuario com login: {0}, e senha: {1}".format(
        login.get(), senha.get()))
    estaAutenticado.set(False)
    for gerente in gerentes['gerentes']:
        if (gerente['nome'] == login.get() and gerente['senha'] == senha.get()):
            estaAutenticado.set(True)
            return estaAutenticado.get()
        else:
            estaAutenticado.set(False)
    return estaAutenticado.get()


root = Tk()
root.title('Gerenciamento de Contas')
root.geometry('650x650')

# Variavel para inserção dos dados do login do gerente no processo de autenticação
loginInput = StringVar()

# Variavel para inserção da senha do gerente no processo de autenticação
senhaInput = StringVar()

# Mensagem de status do usuario, se a autenticação foi bem sucedida ou não.
mensagemStatus = StringVar()

mensagemStatusSaque = StringVar()
mensagemStatusDeposito = StringVar()

# Mensagem geral, utilizada no processo de geração do relatório
mensagensGerais = StringVar()

# Mensagem de explicação, a ser apresentada para '*'
mensagemClienteQuinhentosMil = StringVar()

# Define se o gerente está autenticado
estaAutenticado = BooleanVar()

# Nome do cliente no processo do cadastro
nomeCliente = StringVar()

# Valor inicial do deposito do cliente no momento do cadastro
valorInicialDeposito = DoubleVar()
valorInicialDeposito.set(0.0)

valorSaldoAtual = DoubleVar()
valorSaldoAtual.set(0.0)

valorSaque = DoubleVar()
valorSaque.set(0.0)

valorDeposito = DoubleVar()
valorDeposito.set(0.0)

# Nome do cliente a ser buscado no arquivo clientes.json
nomeClienteBusca = StringVar()

# Resultado da Busca do cliente a ser exibido em tela.
resultadoBusca = StringVar()

# Autentica o Gerente junto aos registros do arquivo gerentes.json


def autenticar():
    if autenticar_gerente(loginInput, senhaInput):
        mensagemStatus.set("Autenticado com sucesso!")
        logging.info("Usuario: {0} Autenticado com sucesso!".format(loginInput.get()))
        carregar_botoes()
        estaAutenticado = True
        limpar_campos_autenticacao()
    else:
        mensagemStatus.set("Não foi possível autenticar!")
        logging.info(
            "Não foi possível autenticar para o Usuario: {0}!".format(loginInput.get()))
        estaAutenticado = False


# Define frame interno ao root (janela), com os componentes
# de label e botoes de login e senha
frm = ttk.Frame(root, padding=5, width=150, height=150)
frm.grid()

# Define frame interno para carregar a lista TKSheet com
# os dados obtidos do arquivo clientes.json (clientes_file)
lista_clientes = ttk.Frame(root, padding=5, height=150, width=450)
lista_clientes.grid()

ttk.Label(frm, text="Gestão de Contas").grid(column=0, row=0)

ttk.Label(frm, text="Login", padding=5).grid(column=0, row=1)
nome = ttk.Entry(frm, textvariable=loginInput).grid(column=1, row=1)

ttk.Label(frm, text="Senha", padding=5).grid(column=0, row=2)
senha = ttk.Entry(frm, show="*", textvariable=senhaInput,
                  width=20).grid(column=1, row=2)

ttk.Button(frm, text="Entrar", command=autenticar).grid(column=0, row=3)
ttk.Button(frm, text="Sair", command=root.destroy).grid(column=1, row=3)

ttk.Label(frm, text="\n", padding=5).grid(column=0, row=4)
ttk.Label(frm, text="Status do Usuario: ",
          textvariable=mensagemStatus, padding=5).grid(column=0, row=5)
ttk.Label(frm, text="Mensagens Gerais: ",
          textvariable=mensagensGerais, padding=5).grid(column=0, row=6)

# Carregamento dos Botoes em tela, para ações do usuario (gerente)


def carregar_botoes():
    ttk.Button(frm, text="Cadastrar Novo Cliente",
               command=abrirJanelaCadastroCliente).grid(column=0, row=7)
    ttk.Button(frm, text="Listar Clientes Cadastrados",
               command=carregar_grid).grid(column=1, row=7)
    ttk.Button(frm, text="Buscar Cliente",
               command=exibir_busca).grid(column=2, row=7)
    ttk.Button(frm, text="Emitir Relatório",
               command=emitirRelatorio).grid(column=3, row=7)

# Abre uma nova janela para o cadastro do cliente
# no arquivo clientes.json, definido em clientes_file


def abrirJanelaCadastroCliente():
    janela_cadastro_cliente = Toplevel(root)
    janela_cadastro_cliente.title("Cadastro de Clientes")
    janela_cadastro_cliente.geometry("300x400")

    Label(janela_cadastro_cliente,
          text="Nome do Cliente: ").grid(column=0, row=1)
    Entry(janela_cadastro_cliente, textvariable=nomeCliente).grid(column=1, row=1)

    Label(janela_cadastro_cliente, text="Valor Inicial: ").grid(column=0, row=2)
    Entry(janela_cadastro_cliente, textvariable=valorInicialDeposito).grid(
        column=1, row=2)

    Button(janela_cadastro_cliente, text="Cadastrar",
           command=cadastrarCliente).grid(column=0, row=3)
    Button(janela_cadastro_cliente, text="Cancelar",
           command=janela_cadastro_cliente.destroy).grid(column=1, row=3)
    janela_cadastro_cliente.grid()


def abrirTelaSaque():
    janela_saque = Toplevel(root)
    janela_saque.title("Saque em Conta do Cliente")
    janela_saque.geometry("300x400")

    Label(janela_saque,
          text="Nome do Cliente: ").grid(column=0, row=1)
    Entry(janela_saque, textvariable=nomeClienteBusca).grid(column=1, row=1)

    Label(janela_saque,
          text="Valor do Saldo Atual do Cliente: ").grid(column=0, row=2)
    Entry(janela_saque, textvariable=valorSaldoAtual).grid(column=1, row=2)

    Label(janela_saque, text="Valor do Saque: ").grid(column=0, row=3)
    Entry(janela_saque, textvariable=valorSaque).grid(
        column=1, row=3)

    Button(janela_saque, text="Sacar",
           command=sacar).grid(column=0, row=4)    
    Button(janela_saque, text="Cancelar Operação",
           command=janela_saque.destroy).grid(column=1, row=4) 
    Label(janela_saque, text="Novo Saldo Após Saque: ", textvariable=mensagemStatusSaque).grid(column=0, row=5)
    


def abrirTelaDeposito():
    janela_deposito = Toplevel(root)
    janela_deposito.title("Deposito em Conta do Cliente")
    janela_deposito.geometry("300x400")

    Label(janela_deposito,
          text="Nome do Cliente: ").grid(column=0, row=1)
    Entry(janela_deposito, textvariable=nomeClienteBusca).grid(column=1, row=1)

    Label(janela_deposito,
          text="Valor do Saldo Atual do Cliente: ").grid(column=0, row=2)
    Entry(janela_deposito, textvariable=valorSaldoAtual).grid(column=1, row=2)

    Label(janela_deposito, text="Valor do Deposito: ").grid(column=0, row=3)
    Entry(janela_deposito, textvariable=valorDeposito).grid(
        column=1, row=3)

    Button(janela_deposito, text="Depositar",
           command=depositar).grid(column=0, row=4)    
    Button(janela_deposito, text="Cancelar Operação",
           command=janela_deposito.destroy).grid(column=1, row=4) 
    Label(janela_deposito, text="Novo Saldo Após Depósito: ", textvariable=mensagemStatusDeposito).grid(column=0, row=5)  


def sacar():
    saldoAposSaque = 0.0
    for cliente in clientes['clientes']:
        if nomeClienteBusca.get() in cliente['nome']:
            cliente['saldo'] = cliente['saldo'] - float(str(valorSaque.get()))
            saldoAposSaque = cliente['saldo']
    
    with open('clientes.json', 'w') as json_file:
        json.dump(clientes, json_file,
                  indent=4,
                  separators=(',', ': '))

    json_file.close()
    logging.info('Novo saldo do cliente: {0}'.format(saldoAposSaque))
    mensagemStatusSaque.set('Novo saldo do cliente: {0}'.format(saldoAposSaque))


def depositar():
    saldoAposDeposito = 0.0
    for cliente in clientes['clientes']:
        if nomeClienteBusca.get() in cliente['nome']:
            cliente['saldo'] = cliente['saldo'] + float(str(valorDeposito.get()))
            saldoAposDeposito = cliente['saldo']
    
    with open('clientes.json', 'w') as json_file:
        json.dump(clientes, json_file,
                  indent=4,
                  separators=(',', ': '))

    json_file.close()
    logging.info('Novo saldo do cliente: {0}'.format(saldoAposDeposito))
    mensagemStatusDeposito.set('Novo saldo do cliente: {0}'.format(saldoAposDeposito))


# Cadastra o cliente na base de clientes (cliente.json)
def cadastrarCliente():
    id = getUltimoClienteId(clientes)
    novoId = int(id) + 1  # incrementa por um, o id do cliente
    logging.info("Cadastrando novo cliente com identificador: {0}, nome: {1}, depósito inicial: {2}.".format(
        novoId, nomeCliente.get(), valorInicialDeposito.get()))

    clienteParaCadastro = Cliente(
        novoId, nomeCliente.get(), valorInicialDeposito.get(), 0.0)
    rendimento = calcularRendimento()
    clienteParaCadastro.valor_rendimento = rendimento
    clientes['clientes'].append(clienteParaCadastro.__dict__)

    with open('clientes.json', 'w') as json_file:
        json.dump(clientes, json_file,
                  indent=4,
                  separators=(',', ': '))

    json_file.close()
    limpar_campos_cadastro()


def exibir_busca():
    janela_busca_cliente = Toplevel(root)
    janela_busca_cliente.title("Busca de Clientes Por Nome")
    janela_busca_cliente.geometry("300x400")
    Label(janela_busca_cliente,
          text="Nome do Cliente: ",).grid(column=0, row=1)
    Entry(janela_busca_cliente,  textvariable=nomeClienteBusca).grid(
        column=1, row=1)
    Button(janela_busca_cliente, text="Buscar Cliente",
           command=buscarCliente).grid(column=0, row=3)
    Button(janela_busca_cliente, text="Cancelar",
           command=janela_busca_cliente.destroy).grid(column=1, row=3)

    Label(janela_busca_cliente, text="'*'",
          textvariable=mensagemClienteQuinhentosMil).grid(column=1, row=4)
    Label(janela_busca_cliente, text="resultados da Busca:",
          textvariable=resultadoBusca).grid(column=1, row=5)
    
    Button(janela_busca_cliente, text="Depositar",
           command=abrirTelaDeposito).grid(column=0, row=6) 
    Button(janela_busca_cliente, text="Realizar Saque",
           command=abrirTelaSaque).grid(column=1, row=6)

# Recupera o ultimo id do cliente registrado em clientes.json


def getUltimoClienteId(clientes):
    ultimoId = 0
    for cliente in clientes['clientes']:
        ultimoId = cliente['id']
    return ultimoId

# Carrega a Grid com a lista de clientes cadastrados no arquivo
# clientes.json


def carregar_grid():
    sheet = Sheet(lista_clientes, width=650,
                  height=250, column_width=120, set_all_heights_and_widths=True, expand_sheet_if_paste_too_big=True, data=[
                      [f"Id: {c['id']}\n Nome: {'*' if float(str(c['saldo'])) > 500000.0 else ''} \n {c['nome']}\n Saldo: {c['saldo']} \n Rendimento: {c['valor_rendimento']}" for c in clientes['clientes']]])
    sheet.enable_bindings()
    sheet.grid(column=0, row=0)

# Busca o cliente na base de arquivos definidos em clientes.json


def buscarCliente():
    mensagemClienteQuinhentosMil.set('')
    resultados = ''
    clientes_encontrados = []
    logging.info("Procure clientes com o seguinte nome: {0}".format(
        nomeClienteBusca.get()))
    for cliente in clientes['clientes']:
        if nomeClienteBusca.get() in cliente['nome']:
            clientes_encontrados.append(cliente)

    for cli in clientes_encontrados:
        if (cli['saldo'] > 500000):
            logging.info("Cliente com o seguinte nome: {0}, possui saldo com valor: {1}".format(
        cli['nome'], cli['saldo']))
            mensagemClienteQuinhentosMil.set('Cliente possui conta com saldo superior a R$ 500.000,00')
            resultados += "Cliente - Nome: {0} * e Saldo Atual: {1} \n".format(cli['nome'], cli['saldo'])
            valorSaldoAtual.set(cli['saldo'])
        else:
            logging.info("Cliente com o seguinte nome: {0}, possui saldo com valor: {1}".format(
        cli['nome'], cli['saldo']))
            resultados += "Cliente - Nome: {0} e Saldo Atual: {1}\n".format(cli['nome'], cli['saldo'])
            valorSaldoAtual.set(cli['saldo'])


    resultadoBusca.set(resultados)

    


# Emite o relatorio no formato txt, definido no diretorio raiz
# do projeto com o nome relatorio_clientes.txt
def emitirRelatorio():
    quantidade_total_clientes = len(clientes['clientes'])
    valor_total_depositado = calcular_valor_total_depositado(clientes)
    valor_media_ponderada_rendimento = calcula_media_ponderada_rendimento()
    valor_media_ponderada_saldo_contas = calcula_media_ponderada_saldo()

    with open('relatorio_clientes.txt', 'w') as f:
        f.write('Quantidade de clientes: {0}\n'.format(
            quantidade_total_clientes))
        f.write('Valor total depositado em todas as contas: {0}\n'.format(
            valor_total_depositado))
        f.write('Media Ponderada por Saldo e Rendimentos: {0}, {1}\n'.format(
            valor_media_ponderada_saldo_contas, valor_media_ponderada_rendimento))
    f.close()

    mensagensGerais.set(
        "Relatorio {0} Gerado com sucesso na saída".format('relatorio_clientes.txt'))

# Calcula o valor total depositado por todos os clientes cadastrados
# Esse valor será exibido no relatorio_clientes.txt
# Chamado pela função emitir_relatorio()


def calcular_valor_total_depositado(clientes):
    valor_total_depositado = 0.0
    for cliente in clientes['clientes']:
        valor_total_depositado = valor_total_depositado + \
            float(cliente['saldo'])
    return valor_total_depositado

# TODO - Implementar.


def calcula_media_ponderada_rendimento():
    quantidade_contas_rendimento_meio_porcento = 0
    quantidade_contas_rendimento_um_porcento = 0
    quantidade_contas_rendimento_um_porcento_meio = 0

    for cli in clientes['clientes']:
        if (float(str(cli['valor_rendimento'])) == 0.5):
            quantidade_contas_rendimento_meio_porcento = quantidade_contas_rendimento_meio_porcento + 1
        elif (float(str(cli['valor_rendimento'])) == 1):
            quantidade_contas_rendimento_um_porcento = quantidade_contas_rendimento_um_porcento + 1
        elif (float(str(cli['valor_rendimento'])) == 1.5):
            quantidade_contas_rendimento_um_porcento_meio = quantidade_contas_rendimento_um_porcento_meio + 1
    
    logging.info("Quantidade de contas por tipo: Rendimento de 0.5 %: {0}, 1%: {1} e 1.5%: {2}".format(quantidade_contas_rendimento_meio_porcento, quantidade_contas_rendimento_um_porcento, quantidade_contas_rendimento_um_porcento_meio))
    media = (quantidade_contas_rendimento_meio_porcento * 0.5 + quantidade_contas_rendimento_um_porcento * 1 + quantidade_contas_rendimento_um_porcento_meio * 1.5)/(0.5 + 1 + 1.5)
    logging.info("Media Ponderada das contas por rendimento: {0}".format(media))
    return media

# calcula a media ponderada do saldo por intervalo (menor que 10000), entre 10000 e 100000
# e maior que 100000
def calcula_media_ponderada_saldo():
    quantidade_contas_saldo_menor_dez_mil = 0
    quantidade_contas_rendimento_entre_dez_mil_cem_mil = 0
    quantidade_contas_rendimento_maior_cem_mil = 0

    for cli in clientes['clientes']:
        if (float(str(cli['saldo'])) < 10000.00):
            quantidade_contas_saldo_menor_dez_mil = quantidade_contas_saldo_menor_dez_mil + 1
        elif (float(str(cli['saldo'])) >= 10000.00 and float(str(cli['saldo'])) <= 100000.00):
            quantidade_contas_rendimento_entre_dez_mil_cem_mil = quantidade_contas_rendimento_entre_dez_mil_cem_mil + 1
        elif (float(str(cli['saldo'])) > 100000.00):
            quantidade_contas_rendimento_maior_cem_mil = quantidade_contas_rendimento_maior_cem_mil + 1
    
    
    logging.info("Quantidade de contas por tipo: Saldo Menor que R$ 10000: {0}, entre R$ 10000 e R$ 100000: {1} e Maior que R$ 100000: {2}".format(quantidade_contas_saldo_menor_dez_mil, quantidade_contas_rendimento_entre_dez_mil_cem_mil, quantidade_contas_rendimento_maior_cem_mil))
    media = (quantidade_contas_saldo_menor_dez_mil * 1 + quantidade_contas_rendimento_entre_dez_mil_cem_mil * 2 + quantidade_contas_rendimento_maior_cem_mil * 3)/(1 + 2 + 3)
    logging.info("Media Ponderada das contas por saldo: {0}".format(media))
    return media

# Calcula o Rendimento da conta de um cliente de acordo com
# o valor do depósito realizado em conta


def calcularRendimento():
    valor_rendimento = 0.0
    if (valorInicialDeposito.get() < 10000.00):
        valor_rendimento = 0.5
    elif (valorInicialDeposito.get() >= 10000.00 and valorInicialDeposito.get() <= 100000.00):
        valor_rendimento = 1.0
    elif (valorInicialDeposito.get() > 100000.00):
        valor_rendimento = 1.5
    return valor_rendimento

# Limpa os campos de Entry do nome do cliente e do valor inicial de deposito
# da tela de cadastro do cliente


def limpar_campos_cadastro():
    nomeCliente.set('')
    valorInicialDeposito.set(0.0)

# Limpa os campos de Entry do nome de usuario e senha do gerente


def limpar_campos_autenticacao():
    loginInput.set('')
    senhaInput.set('')


root.mainloop()
